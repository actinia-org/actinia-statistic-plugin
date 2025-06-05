# -*- coding: utf-8 -*-
"""
Perform raster map sampling on a raster map layer based on input points.
"""

import pickle
import tempfile
from flask import jsonify, make_response
from copy import deepcopy
from flask_restful_swagger_2 import swagger
from flask_restful_swagger_2 import Schema
from actinia_core.models.response_models import ProcessingErrorResponseModel
from actinia_processing_lib.ephemeral_processing import EphemeralProcessing
from actinia_processing_lib.exceptions import AsyncProcessError
from actinia_rest_lib.resource_base import ResourceBase
from actinia_core.core.common.kvdb_interface import enqueue_job
from actinia_core.core.common.app import auth
from actinia_core.core.common.api_logger import log_api_call
from .response_models import RasterSamplingResponseModel


__license__ = "GPLv3"
__author__ = "Markus Neteler"
__copyright__ = (
    "Copyright 2022-2022, Markus Neteler and mundialis GmbH & Co. KG"
)


class PointListModel(Schema):
    """This schema defines the JSON input of the raster sampling resource"""

    type = "object"
    properties = {
        "points": {
            "type": "array",
            "items": {
                "type": "array",
                "items": {"type": "string", "maxItems": 3, "minItems": 3},
            },
            "description": "A list of coordinate points with unique ids "
            "[(id, x, y), (id, x, y), (id, x, y)]",
        }
    }
    example = {"points": [["a", "1", "1"], ["b", "2", "2"], ["c", "3", "3"]]}
    required = ["points"]


SCHEMA_DOC = {
    "tags": ["Raster Sampling"],
    "description": "Spatial sampling of a raster dataset with vector points. "
    "The vector points must be in the same coordinate reference system as the "
    "project that contains the raster dataset. The result of the sampling "
    "is located in the resource response"
    "JSON document after the processing was finished, "
    "as a list of values for each vector point. "
    "Minimum required user role: user.",
    "consumes": ["application/json"],
    "parameters": [
        {
            "name": "project_name",
            "description": "The project name",
            "required": True,
            "in": "path",
            "type": "string",
        },
        {
            "name": "mapset_name",
            "description": "The name of the mapset that contains the required "
            "raster map layer",
            "required": True,
            "in": "path",
            "type": "string",
        },
        {
            "name": "raster_name",
            "description": "The name of the raster map layer to perform the "
            "raster map sampling from",
            "required": True,
            "in": "path",
            "type": "string",
        },
        {
            "name": "points",
            "description": "The sampling point array [[id, x, y],[id, x, y]]. "
            "The coordinates of the sampling points must be in the same "
            "coordinate reference system as the project "
            "that contains the vector dataset.",
            "required": True,
            "in": "body",
            "schema": PointListModel,
        },
    ],
    "responses": {
        "200": {
            "description": "The result of the raster map sampling",
            "schema": RasterSamplingResponseModel,
        },
        "400": {
            "description": "The error message and a detailed log why raster "
            "sampling did not succeed",
            "schema": ProcessingErrorResponseModel,
        },
    },
}


class AsyncEphemeralRasterSamplingResource(ResourceBase):
    """
    Perform raster map sampling on a raster map layer based on input points,
    asynchronous call
    """

    decorators = [log_api_call, auth.login_required]

    def _execute(self, project_name, mapset_name, raster_name):

        rdc = self.preprocess(
            has_json=True,
            has_xml=False,
            project_name=project_name,
            mapset_name=mapset_name,
            map_name=raster_name,
        )
        if rdc:
            enqueue_job(self.job_timeout, start_job, rdc)

        return rdc

    @swagger.doc(deepcopy(SCHEMA_DOC))
    def post(self, project_name, mapset_name, raster_name):
        """
        Perform raster map sampling on a raster map layer based on input
        points asynchronously
        """
        self._execute(project_name, mapset_name, raster_name)
        html_code, response_model = pickle.loads(self.response_data)
        return make_response(jsonify(response_model), html_code)


class SyncEphemeralRasterSamplingResource(
    AsyncEphemeralRasterSamplingResource
):
    """
    Perform raster map sampling on a raster map layer based on input points,
    synchronous call
    """

    decorators = [log_api_call, auth.login_required]

    @swagger.doc(deepcopy(SCHEMA_DOC))
    def post(self, project_name, mapset_name, raster_name):
        """
        Perform raster map sampling on a raster map layer based on input
        points synchronously
        """
        check = self._execute(project_name, mapset_name, raster_name)
        if check is not None:
            http_code, response_model = self.wait_until_finish()
        else:
            http_code, response_model = pickle.loads(self.response_data)
        return make_response(jsonify(response_model), http_code)


def start_job(*args):
    processing = AsyncEphemeralRasterSampling(*args)
    processing.run()


class AsyncEphemeralRasterSampling(EphemeralProcessing):
    """Sample a raster map at vector points"""

    def __init__(self, *args):
        EphemeralProcessing.__init__(self, *args)
        self.response_model_class = RasterSamplingResponseModel

    def _execute(self):

        self._setup()

        # Points are stored in self.request_data
        raster_name = self.map_name
        points = self.request_data["points"]

        if not points or len(points) == 0:
            raise AsyncProcessError("Empty coordinate list")

        point_file = tempfile.NamedTemporaryFile(
            dir=self.temp_file_path, delete=True
        )
        result_file = tempfile.NamedTemporaryFile(
            dir=self.temp_file_path, delete=True
        )

        for tuple in points:
            if len(tuple) != 3:
                raise AsyncProcessError("Wrong number of coordinate entries")

            id, x, y = tuple
            row = "%s|%s|%s\n" % (id, x, y)
            point_file.write(row.encode())

        point_file.flush()

        pc = {
            "list": [
                {
                    "id": "v_in_ascii_1",
                    "module": "v.in.ascii",
                    "inputs": [
                        {"param": "input", "value": point_file.name},
                        {"param": "format", "value": "point"},
                        {
                            "param": "column",
                            "value": "id text, x double precision, y double "
                                     "precision",
                        },
                        {"param": "x", "value": "2"},
                        {"param": "y", "value": "3"},
                    ],
                    "outputs": [{"param": "output", "value": "input_points"}],
                    "superquiet": True
                },
                {
                    "id": "g_region_2",
                    "module": "g.region",
                    "inputs": [
                        {"param": "vector", "value": "input_points"},
                        {
                            "param": "align",
                            "value": "%s@%s" % (raster_name, self.mapset_name),
                        },
                    ],
                    "flags": "p",
                    "superquiet": True
                },
                {
                    "id": "r_what_3",
                    "module": "r.what",
                    "inputs": [
                        {
                            "param": "map",
                            "value": "%s@%s" % (raster_name, self.mapset_name),
                        },
                        {"param": "points", "value": "input_points"},
                    ],
                    "outputs": [
                        {"param": "output", "value": result_file.name}
                    ],
                    "flags": "nrf",
                    "overwrite": True,
                    "superquiet": True,
                },
            ],
            "version": "1",
        }

        self.request_data = pc

        # Run the process chain
        EphemeralProcessing._execute(self, skip_permission_check=True)

        result = open(result_file.name, "r").readlines()

        output_list = []
        raster_name_qualified = "%s@%s" % (raster_name, self.mapset_name)
        # remove map name from columns
        colum_name = [
            col
            if raster_name_qualified not in col
            else col.replace(f"{raster_name_qualified}_", "").replace(
                raster_name_qualified, "value"
            )
            for col in result[0].strip().split("|")
        ]
        for line, point in zip(result[1:], points):
            entry = dict()
            entry[point[0]] = {
                key: value
                for key, value in zip(colum_name, line.strip().split("|"))
            }
            # remove site_name (always empty)
            del entry[point[0]]["site_name"]
            # add "map_name": raster_name
            entry[point[0]]["map_name"] = raster_name

            output_list.append(entry)

        self.module_results = output_list

        point_file.close()
        result_file.close()

# -*- coding: utf-8 -*-
"""
Perform vector map sampling on a vector map layer based on input points.
"""

import pickle
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
from .response_models import VectorSamplingResponseModel


__license__ = "GPLv3"
__author__ = "Markus Neteler"
__copyright__ = (
    "Copyright 2022-2022, Markus Neteler and mundialis GmbH & Co. KG"
)


class PointListModel(Schema):
    """This schema defines the JSON input of the vector sampling resource"""

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
    "tags": ["Vector Sampling"],
    "description": "Spatial sampling of a vector dataset with vector points. "
    "The vector points must be in the same coordinate reference system as the "
    "project that contains the vector dataset. The result of the sampling is "
    "located in the resource response JSON document after the processing was "
    "finished, as a list of values for each vector point. "
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
            "vector map layer",
            "required": True,
            "in": "path",
            "type": "string",
        },
        {
            "name": "vector_name",
            "description": "The name of the vector map layer to perform the "
            "vector map sampling from",
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
            "description": "The result of the vector map sampling",
            "schema": VectorSamplingResponseModel,
        },
        "400": {
            "description": "The error message and a detailed log why vector "
            "sampling did not succeed",
            "schema": ProcessingErrorResponseModel,
        },
    },
}


class AsyncEphemeralVectorSamplingResource(ResourceBase):
    """
    Perform vector map sampling on a vector map layer based on input points,
    asynchronous call"""

    decorators = [log_api_call, auth.login_required]

    def _execute(self, project_name, mapset_name, vector_name):

        rdc = self.preprocess(
            has_json=True,
            has_xml=False,
            project_name=project_name,
            mapset_name=mapset_name,
            map_name=vector_name,
        )
        if rdc:
            enqueue_job(self.job_timeout, start_job, rdc)

        return rdc

    @swagger.doc(deepcopy(SCHEMA_DOC))
    def post(self, project_name, mapset_name, vector_name):
        """
        Perform vector map sampling on a vector map layer based on input
        points asynchronously
        """
        self._execute(project_name, mapset_name, vector_name)
        html_code, response_model = pickle.loads(self.response_data)
        return make_response(jsonify(response_model), html_code)


class SyncEphemeralVectorSamplingResource(
    AsyncEphemeralVectorSamplingResource
):
    """
    Perform vector map sampling on a vector map layer based on input points,
    synchronous call
    """

    decorators = [log_api_call, auth.login_required]

    @swagger.doc(deepcopy(SCHEMA_DOC))
    def post(self, project_name, mapset_name, vector_name):
        """
        Perform vector map sampling on a vector map layer based on input
        points synchronously
        """
        check = self._execute(project_name, mapset_name, vector_name)
        if check is not None:
            http_code, response_model = self.wait_until_finish()
        else:
            http_code, response_model = pickle.loads(self.response_data)
        return make_response(jsonify(response_model), http_code)


def start_job(*args):
    processing = AsyncEphemeralVectorSampling(*args)
    processing.run()


class AsyncEphemeralVectorSampling(EphemeralProcessing):
    """Sample a vector map at vector points"""

    def __init__(self, *args):
        EphemeralProcessing.__init__(self, *args)
        self.response_model_class = VectorSamplingResponseModel

    def _execute(self):

        self._setup()

        # Points are stored in self.request_data
        vector_name = self.map_name
        points = self.request_data["points"]

        if not points or len(points) == 0:
            raise AsyncProcessError("Empty coordinate list")

        coordinates_string = ""
        for tuple in points:
            if len(tuple) != 3:
                raise AsyncProcessError("Wrong number of coordinate entries")

            id, x, y = tuple
            coordinates_string += "%s,%s," % (x, y)

        pc = {
            "list": [
                {
                    "id": "v_what",
                    "module": "v.what",
                    "inputs": [
                        {
                            "param": "map",
                            "value": "%s@%s" % (vector_name, self.mapset_name),
                        },
                        {
                            "param": "coordinates",
                            "value": coordinates_string[:-1],
                        },
                    ],
                    "stdout": {
                        "id": "info",
                        "format": "list",
                        "delimiter": "|",
                    },
                    "flags": "ag",
                    "superquiet": True
                },
            ],
            "version": "1",
        }

        self.request_data = pc

        # Run the process chain
        EphemeralProcessing._execute(self, skip_permission_check=True)

        count = -1
        output_list = []
        # Convert the result of v.what into actinia response format (list of
        # points with point ID, coordinate pair and vector map attributes)
        for entry in self.module_results["info"]:
            if "=" in entry:
                key, val = entry.split("=")
                if key == "East":
                    count += 1
                    if "point" in locals():
                        output_list.append(point)
                    point = {points[count][0]: {key: val}}
                else:
                    point[points[count][0]][key] = val

        output_list.append(point)

        self.module_results = output_list

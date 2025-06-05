# -*- coding: utf-8 -*-
"""
Sample a space-time raster dataset at specific vector points
"""

import pickle
import tempfile
from flask import jsonify, make_response
from copy import deepcopy
from flask_restful_swagger_2 import swagger, Schema
from actinia_core.models.response_models import (
    ProcessingResponseModel,
    ProcessingErrorResponseModel,
)
from actinia_processing_lib.ephemeral_processing import EphemeralProcessing
from actinia_rest_lib.resource_base import ResourceBase
from actinia_core.core.common.kvdb_interface import enqueue_job
from actinia_processing_lib.exceptions import AsyncProcessError

__license__ = "GPLv3"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2016, Sören Gebbert"
__maintainer__ = "Sören Gebbert"
__email__ = "soerengebbert@googlemail.com"


class STRDSSampleResponseModel(ProcessingResponseModel):
    """Response schema for a STRDS sampling result.

    This schema is a derivative of the ProcessingResponseModel that defines
    a different *process_results* schema.
    """

    type = "object"
    properties = deepcopy(ProcessingResponseModel.properties)
    properties["process_results"] = {}
    properties["process_results"]["type"] = "array"
    properties["process_results"]["items"] = {
        "type": "array",
        "items": {"type": "string", "minItems": 3},
    }
    required = deepcopy(ProcessingResponseModel.required)
    example = {
        "accept_datetime": "2017-05-11 10:09:47.237997",
        "accept_timestamp": 1494490187.237996,
        "api_info": {
            "endpoint": "syncephemeralstrdssamplingresource",
            "method": "POST",
            "path": "/projects/ECAD/mapsets/PERMANENT/strds/temperature_mean_"
            "1950_2013_yearly_celsius/sampling_sync",
            "request_url": "http://localhost/projects/ECAD/mapsets/PERMANENT/"
            "strds/temperature_mean_1950_2013_yearly_celsius/sampling_sync",
        },
        "datetime": "2017-05-11 10:09:48.376521",
        "http_code": 200,
        "message": "Processing successfully finished",
        "process_log": [
            {
                "executable": "v.in.ascii",
                "parameter": [
                    "column=id text, x double precision, y double precision",
                    "input=/tmp/tmpOlouNV",
                    "y=3",
                    "x=2",
                    "format=point",
                    "output=input_points",
                ],
                "return_code": 0,
                "stderr": [
                    "Scanning input for column types...",
                    "Number of columns: 3",
                    "Number of rows: 3",
                    "Importing points...",
                    "0..33..66..100",
                    "Populating table...",
                    "Building topology for vector map <input_points@mapset_"
                    "ffb3520846104a42878271a83117a93f>...",
                    "Registering primitives...",
                    "",
                    "3 primitives registered",
                    "3 vertices registered",
                    "Building areas...",
                    "0..33..66..100",
                    "0 areas built",
                    "0 isles built",
                    "Attaching islands...",
                    "Attaching centroids...",
                    "33..66..100",
                    "Number of nodes: 0",
                    "Number of primitives: 3",
                    "Number of points: 3",
                    "Number of lines: 0",
                    "Number of boundaries: 0",
                    "Number of centroids: 0",
                    "Number of areas: 0",
                    "Number of isles: 0",
                    "",
                ],
                "stdout": "",
            },
            {
                "executable": "t.rast.sample",
                "parameter": [
                    "column=id",
                    "points=input_points",
                    "where=start_time >'2010-01-01'",
                    "strds=temperature_mean_1950_2013_yearly_celsius@"
                    "PERMANENT",
                    "output=/tmp/tmpgU9ITw",
                    "-rn",
                    "--o",
                    "--v",
                ],
                "return_code": 0,
                "stderr": [
                    "Sample map <temperature_mean_yearly_celsius_60> number  "
                    "1 out of 3",
                    "Sample map <temperature_mean_yearly_celsius_61> number "
                    " 2 out of 3",
                    "Sample map <temperature_mean_yearly_celsius_62> number "
                    " 3 out of 3",
                    "",
                ],
                "stdout": "",
            },
        ],
        "process_results": [
            ["start_time", "end_time", "a", "b", "c"],
            [
                "2010-01-01 00:00:00",
                "2011-01-01 00:00:00",
                "16.5293979135",
                "7.50153213006",
                "7.67950249616",
            ],
            [
                "2011-01-01 00:00:00",
                "2012-01-01 00:00:00",
                "17.3258000667",
                "9.35620500512",
                "8.37665885817",
            ],
            [
                "2012-01-01 00:00:00",
                "2013-01-01 00:00:00",
                "16.5512179273",
                "8.8377879125",
                "7.87268863552",
            ],
        ],
        "progress": {"num_of_steps": 2, "step": 2},
        "resource_id": "resource_id-96554e63-3dad-4a16-8652-e7c6be734057",
        "status": "finished",
        "timestamp": 1494490188.376519,
        "urls": {
            "resources": [],
            "status": "http://localhost/status/admin/resource_id-96554e63-"
            "3dad-4a16-8652-e7c6be734057",
        },
        "user_id": "admin",
    }


class PointListModel(Schema):
    """This schema defines the JSON input of the strds sampling resource"""

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
        },
        "where": {
            "type": "string",
            "description": "The where statement to select specific subsets "
            "of the strds, for example: start_time > '2001-01-01'",
        },
    }
    example = {
        "where": "start_time > '2001-01-01'",
        "points": [["a", "1", "1"], ["b", "2", "2"], ["c", "3", "3"]],
    }
    required = ["points"]


SCHEMA_DOC = {
    "tags": ["STRDS Sampling"],
    "description": "Spatial sampling of a space-time raster dataset with "
    "vector points. The vector points must be in the same coordinate reference"
    " system as the project that contains the space-time raster dataset. "
    "The result of the sampling is located in the resource response"
    "JSON docuement after the processing was finished, "
    "as a list of timestamped values for each vector point. "
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
            "name": "strds_name",
            "description": "The name of the space-time raster dataset that "
            "should be sampled",
            "required": True,
            "in": "path",
            "type": "string",
        },
        {
            "name": "points",
            "description": "The sampling point array [[id, x, y],[id, x, y]] "
            "and an optional where statement. "
            "The coordinates of the sampling points must be the same as of "
            "the project "
            "that contains the space-time raster dataset.",
            "required": True,
            "in": "body",
            "schema": PointListModel,
        },
    ],
    "responses": {
        "200": {
            "description": "The result of the strds sampling",
            "schema": STRDSSampleResponseModel,
        },
        "400": {
            "description": "The error message and a detailed log why strds "
            "sampling did not succeeded",
            "schema": ProcessingErrorResponseModel,
        },
    },
}


class AsyncEphemeralSTRDSSamplingResource(ResourceBase):
    """Sample a STRDS at vector point projects, asynchronous call"""

    def _execute(self, project_name, mapset_name, strds_name):

        rdc = self.preprocess(
            has_json=True,
            has_xml=False,
            project_name=project_name,
            mapset_name=mapset_name,
            map_name=strds_name,
        )
        if rdc:
            enqueue_job(self.job_timeout, start_job, rdc)

        return rdc

    @swagger.doc(deepcopy(SCHEMA_DOC))
    def post(self, project_name, mapset_name, strds_name):
        """Sample a strds by point coordinates, asynchronous call"""
        self._execute(project_name, mapset_name, strds_name)
        html_code, response_model = pickle.loads(self.response_data)
        return make_response(jsonify(response_model), html_code)


class SyncEphemeralSTRDSSamplingResource(AsyncEphemeralSTRDSSamplingResource):
    """Sample a STRDS at vector point projects, synchronous call"""

    @swagger.doc(deepcopy(SCHEMA_DOC))
    def post(self, project_name, mapset_name, strds_name):
        """Sample a strds by point coordinates, synchronous call"""
        check = self._execute(project_name, mapset_name, strds_name)
        if check is not None:
            http_code, response_model = self.wait_until_finish()
        else:
            http_code, response_model = pickle.loads(self.response_data)
        return make_response(jsonify(response_model), http_code)


def start_job(*args):
    processing = AsyncEphemeralSTRDSSampling(*args)
    processing.run()


class AsyncEphemeralSTRDSSampling(EphemeralProcessing):
    """Sample a STRDS at vector points"""

    def __init__(self, *args):
        EphemeralProcessing.__init__(self, *args)
        self.response_model_class = STRDSSampleResponseModel

    def _execute(self):

        self._setup()
        where = None

        # Points and where statement are stored in self.request_data
        strds_name = self.map_name
        points = self.request_data["points"]
        if "where" in self.request_data:
            where = self.request_data["where"]

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
                        {
                            "param": "input",
                            "value": point_file.name,
                        },
                        {
                            "param": "format",
                            "value": "point",
                        },
                        {
                            "param": "column",
                            "value": "id text, x double precision, y double "
                                     "precision",
                        },
                        {
                            "param": "x",
                            "value": "2",
                        },
                        {
                            "param": "y",
                            "value": "3",
                        }
                    ],
                    "outputs": [
                        {
                            "param": "output",
                            "value": "input_points",
                        }
                    ],
                    "superquiet": True
                },
                {
                    "id": "t_rast_sample_2",
                    "module": "t.rast.sample",
                    "inputs": [
                        {
                            "param": "strds",
                            "value": "%s@%s" % (strds_name, self.mapset_name),
                        },
                        {
                            "param": "points",
                            "value": "input_points",
                        },
                        {
                            "param": "column",
                            "value": "id",
                        }
                    ],
                    "outputs": [
                        {
                            "param": "output",
                            "value": result_file.name,
                        }
                    ],
                    "flags": "rn",
                    "superquiet": True
                },
            ],
            "version": "1",
        }

        if where is not None:
            pc["list"][1]["inputs"].append({"param": "where", "value": where})

        self.request_data = pc

        # Run the process chain
        EphemeralProcessing._execute(self, skip_permission_check=True)

        result = open(result_file.name, "r").readlines()

        output_list = []
        for line in result:
            output_list.append(line.strip().split("|"))

        self.module_results = output_list

        point_file.close()
        result_file.close()

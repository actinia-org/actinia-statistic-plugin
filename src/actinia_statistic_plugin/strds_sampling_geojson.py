# -*- coding: utf-8 -*-
"""
Sample a space-time raster dataset at specific vector points
"""

import pickle
import tempfile
from flask import jsonify, make_response
from flask.json import dumps as json_dumps
from copy import deepcopy
from flask_restful_swagger_2 import swagger
from actinia_core.models.response_models import (
    ProcessingResponseModel,
    ProcessingErrorResponseModel,
)
from actinia_processing_lib.ephemeral_processing import EphemeralProcessing
from actinia_rest_lib.resource_base import ResourceBase
from actinia_core.core.common.kvdb_interface import enqueue_job
from actinia_api import URL_PREFIX

__license__ = "GPLv3"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2016, Sören Gebbert"
__maintainer__ = "Sören Gebbert"
__email__ = "soerengebbert@googlemail.com"


class STRDSSampleGeoJSONResponseModel(ProcessingResponseModel):
    """The response content that is returned by the POST request"""

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
        "accept_datetime": "2017-09-04 19:41:41.456341",
        "accept_timestamp": 1504546901.456339,
        "api_info": {
            "endpoint": "syncephemeralstrdssamplinggeojsonresource",
            "method": "POST",
            "path": f"{URL_PREFIX}/projects/ECAD/mapsets/PERMANENT/strds/"
            "temperature_mean_1950_2013_yearly_celsius/sampling_sync_geojson",
            "request_url": f"http://localhost{URL_PREFIX}/projects/ECAD"
            "/mapsets/PERMANENT/strds/temperature_mean_1950_2013_yearly_"
            "celsius/sampling_sync_geojson",
        },
        "datetime": "2017-09-04 19:41:42.622865",
        "http_code": 200,
        "message": "Processing successfully finished",
        "process_log": [
            {
                "executable": "v.import",
                "parameter": [
                    "input=/tmp/gisdbase_3e090bec1a744be78743668a573cbf5b/"
                    ".tmp/tmpk6Le10",
                    "output=input_points",
                ],
                "return_code": 0,
                "run_time": 0.25067806243896484,
                "stderr": [
                    "Check if OGR layer <OGRGeoJSON> contains polygons...",
                    "0..33..66..100",
                    "Column name <cat> renamed to <cat_>",
                    "Importing 3 features (OGR layer <OGRGeoJSON>)...",
                    "0..33..66..100",
                    "-----------------------------------------------------",
                    "Building topology for vector map <input_points@mapset_"
                    "3e090bec1a744be78743668a573cbf5b>...",
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
                    "Input </tmp/gisdbase_3e090bec1a744be78743668a573cbf5b/"
                    ".tmp/tmpk6Le10> successfully imported without "
                    "reprojection",
                    "",
                ],
                "stdout": "",
            },
            {
                "executable": "t.rast.sample",
                "parameter": [
                    "points=input_points",
                    "strds=temperature_mean_1950_2013_yearly_celsius@"
                    "PERMANENT",
                    "output=/tmp/gisdbase_3e090bec1a744be78743668a573cbf5b/"
                    ".tmp/tmp3ilr28",
                    "-rn",
                    "--o",
                    "--v",
                ],
                "return_code": 0,
                "run_time": 0.5513670444488525,
                "stderr": [
                    "Default TGIS driver / database set to:",
                    "driver: sqlite",
                    "database: $GISDBASE/$LOCATION_NAME/$MAPSET/tgis/sqlite."
                    "db",
                    "WARNING: Temporal database connection defined as:",
                    "/tmp/gisdbase_3e090bec1a744be78743668a573cbf5b/ECAD"
                    "/mapset_3e090bec1a744be78743668a573cbf5b/tgis/sqlite.db",
                    "But database file does not exist.",
                    "Creating temporal database: /tmp/gisdbase_3e090bec1a744b"
                    "e78743668a573cbf5b/ECAD/mapset_3e090bec1a744be78743668a57"
                    "3cbf5b/tgis/sqlite.db",
                    "Sample map <temperature_mean_yearly_celsius_0> number  "
                    "1 out of 63",
                    "Sample map <temperature_mean_yearly_celsius_62> number "
                    " 63 out of 63",
                    "",
                ],
                "stdout": "",
            },
        ],
        "process_results": [
            ["start_time", "end_time", "1", "2", "3"],
            [
                "1950-01-01 00:00:00",
                "1951-01-01 00:00:00",
                "16.4121888761",
                "8.17818215566",
                "7.17657693292",
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
        "resource_id": "resource_id-6ee74d8c-1ef6-4b01-a098-2bc04bcb75c8",
        "status": "finished",
        "time_delta": 1.1665611267089844,
        "timestamp": 1504546902.622857,
        "urls": {
            "resources": [],
            "status": f"http://localhost{URL_PREFIX}/status/admin/resource_id"
            "-6ee74d8c-1ef6-4b01-a098-2bc04bcb75c8",
        },
        "user_id": "admin",
    }


SCHEMA_DOC = {
    "tags": ["STRDS Sampling"],
    "description": "Spatial sampling of a space-time raster dataset (STRDS) "
    "with vector points. The vector points must be provided as GeoJSON vector"
    " point format that includes correct coordinate system specification. "
    "The result of the sampling is located in the resource response"
    "JSON document after the processing was finished, "
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
            "default": "ECAD",
        },
        {
            "name": "mapset_name",
            "description": "The name of the mapset that contains the required "
            "raster map layer",
            "required": True,
            "in": "path",
            "type": "string",
            "default": "PERMANENT",
        },
        {
            "name": "strds_name",
            "description": "The name of the space-time raster dataset that"
            " should be sampled",
            "required": True,
            "in": "path",
            "type": "string",
            "default": "temperature_mean_1950_2013_yearly_celsius",
        },
        {
            "name": "points",
            "description": "GeoJSON vector input that contains the vector "
            "points for sampling",
            "required": True,
            "in": "body",
            "schema": "string",
            "default": """
{
"type": "FeatureCollection",
"crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:"
"CRS84"}},
"features": [
    {"type": "Feature", "properties": {"cat": 1},
     "geometry": {"type": "Point", "coordinates": [-5.095406, 38.840583]}},
    {"type": "Feature", "properties": {"cat": 2},
     "geometry": {"type": "Point", "coordinates": [9.9681980, 51.666166]}},
    {"type": "Feature", "properties": {"cat": 3},
     "geometry": {"type": "Point", "coordinates": [24.859647, 52.699099]}}
]
}
                        """,
        },
    ],
    "responses": {
        "200": {
            "description": "The result of the strds sampling",
            "schema": STRDSSampleGeoJSONResponseModel,
        },
        "400": {
            "description": "The error message and a detailed log why strds "
            "sampling did not succeeded",
            "schema": ProcessingErrorResponseModel,
        },
    },
}


class AsyncEphemeralSTRDSSamplingGeoJSONResource(ResourceBase):
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
            # # for debugging
            # processing = AsyncEphemeralSTRDSSamplingGeoJSON(rdc)
            # processing.run()
            enqueue_job(self.job_timeout, start_job, rdc)

        return rdc

    @swagger.doc(deepcopy(SCHEMA_DOC))
    def post(self, project_name, mapset_name, strds_name):
        """Sample a strds by point coordinates, asynchronous call"""
        self._execute(project_name, mapset_name, strds_name)
        html_code, response_model = pickle.loads(self.response_data)
        return make_response(jsonify(response_model), html_code)


class SyncEphemeralSTRDSSamplingGeoJSONResource(
    AsyncEphemeralSTRDSSamplingGeoJSONResource
):
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
    processing = AsyncEphemeralSTRDSSamplingGeoJSON(*args)
    processing.run()


class AsyncEphemeralSTRDSSamplingGeoJSON(EphemeralProcessing):
    """Sample a STRDS at vector points using GeoJSON as input"""

    def __init__(self, *args):
        EphemeralProcessing.__init__(self, *args)
        self.response_model_class = STRDSSampleGeoJSONResponseModel

    def _execute(self):
        self._setup()

        # Points and where statement are stored in self.request_data
        strds_name = self.map_name
        geojson = self.request_data

        point_file = tempfile.NamedTemporaryFile(
            dir=self.temp_file_path, delete=True
        )
        result_file = tempfile.NamedTemporaryFile(
            dir=self.temp_file_path, delete=True
        )

        point_file.write(json_dumps(geojson).encode())
        point_file.flush()

        pc = {
            "list": [
                {
                    "id": "v_import_1",
                    "module": "v.import",
                    "inputs": [
                        {
                            "param": "input",
                            "value": point_file.name,
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

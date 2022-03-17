# -*- coding: utf-8 -*-
"""
Perform vector map sampling on a vector map layer based on input points.
"""

import pickle
import tempfile
from flask import jsonify, make_response
from copy import deepcopy
from flask_restful_swagger_2 import swagger
from flask_restful_swagger_2 import Schema
from actinia_core.models.response_models import ProcessingErrorResponseModel
from actinia_core.rest.ephemeral_processing import EphemeralProcessing
from actinia_core.rest.resource_base import ResourceBase
from actinia_core.core.common.redis_interface import enqueue_job
from flask.json import dumps
from actinia_core.core.common.app import auth
from actinia_core.core.common.api_logger import log_api_call
from .response_models import VectorSamplingResponseModel


__license__ = "GPLv3"
__author__ = "Sören Gebbert, Markus Neteler"
__copyright__ = "Copyright 2016-present, Sören Gebbert and mundialis GmbH & Co. KG"


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
            "description": "A list of coordinate points with unique ids [(id, x, y), (id, x, y), (id, x, y)]",
        }
    }
    example = {"points": [["a", "1", "1"], ["b", "2", "2"], ["c", "3", "3"]]}
    required = ["points"]


SCHEMA_DOC = {
    "tags": ["Vector Sampling"],
    "description": "Spatial sampling of a vector dataset with vector points. The vector points must "
    "be in the same coordinate reference system as the location that contains the "
    "vector dataset. The result of the sampling is located in the resource response"
    "JSON document after the processing was finished, "
    "as a list of values for each vector point. "
    "Minimum required user role: user.",
    "consumes": ["application/json"],
    "parameters": [
        {
            "name": "location_name",
            "description": "The location name",
            "required": True,
            "in": "path",
            "type": "string",
        },
        {
            "name": "mapset_name",
            "description": "The name of the mapset that contains the required vector map layer",
            "required": True,
            "in": "path",
            "type": "string",
        },
        {
            "name": "vector_name",
            "description": "The name of the vector map layer to perform the vector map sampling from",
            "required": True,
            "in": "path",
            "type": "string",
        },
        {
            "name": "points",
            "description": "The sampling point array [[id, x, y],[id, x, y]]. "
            "The coordinates of the sampling points must be the same as of the location "
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
            "description": "The error message and a detailed log why vector sampling did not succeed",
            "schema": ProcessingErrorResponseModel,
        },
    },
}


class AsyncEphemeralVectorSamplingResource(ResourceBase):
    """Perform vector map sampling on a vector map layer based on input points, asynchronous call"""

    decorators = [log_api_call, auth.login_required]

    def _execute(self, location_name, mapset_name, vector_name):

        rdc = self.preprocess(
            has_json=True,
            has_xml=False,
            location_name=location_name,
            mapset_name=mapset_name,
            map_name=vector_name,
        )
        if rdc:
            enqueue_job(self.job_timeout, start_job, rdc)

        return rdc

    @swagger.doc(deepcopy(SCHEMA_DOC))
    def post(self, location_name, mapset_name, vector_name):
        """Perform vector map sampling on a vector map layer based on input points asynchronously"""
        self._execute(location_name, mapset_name, vector_name)
        html_code, response_model = pickle.loads(self.response_data)
        return make_response(jsonify(response_model), html_code)


class SyncEphemeralVectorSamplingResource(AsyncEphemeralVectorSamplingResource):
    """Perform vector map sampling on a vector map layer based on input points, synchronous call"""

    decorators = [log_api_call, auth.login_required]

    @swagger.doc(deepcopy(SCHEMA_DOC))
    def post(self, location_name, mapset_name, vector_name):
        """Perform vector map sampling on a vector map layer based on input points synchronously"""
        check = self._execute(location_name, mapset_name, vector_name)
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

        # g.region probably not needed
        pc = {
            "list": [
                {
                    "id": "g_region",
                    "module": "g.region",
                    "inputs": [
                        {
                            "param": "vector",
                            "value": "%s@%s" % (vector_name, self.mapset_name)
                        }
                    ],
                    "flags": "p",
                },
                {
                    "id": "v_what",
                    "module": "v.what",
                    "inputs": [
                        {
                            "param": "map",
                            "value": "%s@%s" % (vector_name, self.mapset_name)
                        },
                        {
                            "param": "coordinates",
                            "value": coordinates_string[:-1]
                        }
                    ],
                    "stdout":
                        {
                            "id": "info",
                            "format": "list",
                            "delimiter": "|"
                        },
                    "flags": "aj",
                },
            ],
            "version": "1",
        }

        self.request_data = pc

        # {'info': [
        # 'East=638684'
        # 'North=220210'
        # ''
        # 'Map=zipcodes_wake'
        # 'Mapset=PERMANENT'
        # 'Type=Area'
        # 'Sq_Meters=130875884.223'
        # 'Hectares=13087.588'
        # 'Acres=32340.135'
        # 'Sq_Miles=50.5315'
        # ...

        # GRASS nc_spm_08_grass7/user1:~ > v.what map=zipcodes_wake coordinates=638684.0,220210.0,635676.0,226371.0  -ja | jq
        # {
        # "Coordinates": {
        # "East": "638684",
        # "North": "220210"
        # },
        # "Maps": [
        # {
        # "Map": "zipcodes_wake",
        # "Mapset": "PERMANENT",
        # "Type": "Area",
        # "Sq_Meters": 130875884.223,
        # "Hectares": 13087.588,
        # "Acres": 32340.135,
        # "Sq_Miles": 50.5315,
        # "Categories": [
        # {
        # "Layer": 1,
        # "Category": 40,
        # "Driver": "sqlite",
        # "Database": "/home/mneteler/grassdata/nc_spm_08_grass7/PERMANENT/sqlite/sqlite.db",
        # "Table": "zipcodes_wake",
        # "Key_column": "cat",
        # "Attributes": {
        # "cat": "40",
        # "OBJECTID": "286",
        # "WAKE_ZIPCO": "1285870010.66",
        # "PERIMETER": "282815.79339",
        # "ZIPCODE_": "37",
        # "ZIPCODE_ID": "66",
        # "ZIPNAME": "RALEIGH",
        # "ZIPNUM": "27603",
        # "ZIPCODE": "RALEIGH 27603",
        # "NAME": "RALEIGH",
        # "SHAPE_Leng": "285693.495599",
        # "SHAPE_Area": "1408742751.36"
        # }
        # }
        # ]
        # }
        # ]
        # }
        # {
        # "Coordinates": {
        # "East": "635676",
        # "North": "226371"
        # },
        # "Maps": [
        # {
        # "Map": "zipcodes_wake",
        # "Mapset": "PERMANENT",
        # "Type": "Area",
        # "Sq_Meters": 63169356.527,
        # "Hectares": 6316.936,
        # "Acres": 15609.488,
        # "Sq_Miles": 24.3898,
        # "Categories": [
        # {
        # "Layer": 1,
        # "Category": 42,
        # "Driver": "sqlite",
        # "Database": "/home/mneteler/grassdata/nc_spm_08_grass7/PERMANENT/sqlite/sqlite.db",
        # "Table": "zipcodes_wake",
        # "Key_column": "cat",
        # "Attributes": {
        # "cat": "42",
        # "OBJECTID": "298",
        # "WAKE_ZIPCO": "829874917.625",
        # "PERIMETER": "230773.26059",
        # "ZIPCODE_": "39",
        # "ZIPCODE_ID": "2",
        # "ZIPNAME": "RALEIGH",
        # "ZIPNUM": "27606",
        # "ZIPCODE": "RALEIGH 27606",
        # "NAME": "RALEIGH",
        # "SHAPE_Leng": "212707.32257",
        # "SHAPE_Area": "679989401.948"
        # }
        # }
        # ]
        # }
        # ]
        # }

        # curl --no-progress-meter ${AUTH} -X POST -H "content-type: application/json" "${actinia}/api/v3/locations/nc_spm_08/mapsets/PERMANENT/vector_layers/zipcodes_wake/sampling_sync" -d @test_raster_sample_data.json | jq .process_results
        # {
        # "info": [
        # "{\"Coordinates\": {\"East\": \"638684\", \"North\": \"220210\"},",
        # "\"Maps\": [",
        # "{\"Map\": \"zipcodes_wake\",",
        # "\"Mapset\": \"PERMANENT\",",
        # "\"Type\": \"Area\",",
        # ...
        # "\"WAKE_ZIPCO\": \"1285870010.66\",",
        # "\"PERIMETER\": \"282815.79339\",",
        # "\"ZIPCODE_\": \"37\",",
        # ...
        # "\"SHAPE_Area\": \"1408742751.36\"}}]}]}",
        # "{\"Coordinates\": {\"East\": \"635676\", \"North\": \"226371\"},",
        # "\"Maps\": [",
        # "{\"Map\": \"zipcodes_wake\",",
        # ...

        # [
        # {
        # "p1": {
        # "color": "229:229:204",
        # "easting": "638684",
        # "label": "Managed Herbaceous Cover",
        # "map_name": "landuse96_28m",
        # "northing": "220210",
        # "value": "4"
        # }
        # },
        # {
        # "p2": {
        # "color": "255:051:076",
        # "easting": "635676",
        # "label": "Low Intensity Developed",
        # "map_name": "landuse96_28m",
        # "northing": "226371",
        # "value": "2"
        # }
        # }
        # ]

        # Run the process chain
        EphemeralProcessing._execute(self, skip_permission_check=True)
        print("")
        print(self.module_results)
        print("")

        # self.module_results = output_list

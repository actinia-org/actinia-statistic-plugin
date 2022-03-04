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
from actinia_core.rest.ephemeral_processing import EphemeralProcessing
from actinia_core.rest.resource_base import ResourceBase
from actinia_core.core.common.redis_interface import enqueue_job
from flask.json import dumps
from actinia_core.core.common.app import auth
from actinia_core.core.common.api_logger import log_api_call
from .response_models import RasterSamplingResponseModel


__license__ = "GPLv3"
__author__ = "Sören Gebbert, Markus Neteler"
__copyright__ = "Copyright 2016-present, Sören Gebbert and mundialis GmbH & Co. KG"


class PointListModel(Schema):
    """This schema defines the JSON input of the raster sampling resource
    """
    type = 'object'
    properties = {
        'points': {
            'type': 'array',
            'items': {'type': 'array', 'items': {'type': 'string', 'maxItems': 3, 'minItems': 3}},
            'description': 'A list of coordinate points with unique ids [(id, x, y), (id, x, y), (id, x, y)]'
        }
    }
    example = {"points": [["a", "1", "1"],
                          ["b", "2", "2"],
                          ["c", "3", "3"]]}
    required = ['points']


SCHEMA_DOC = {
    'tags': ['Raster Sampling'],
    'description': 'Spatial sampling of a raster dataset with vector points. The vector points must '
                   'be in the same coordinate reference system as the location that contains the '
                   'raster dataset. The result of the sampling is located in the resource response'
                   'JSON document after the processing was finished, '
                   'as a list of values for each vector point. '
                   'Minimum required user role: user.',
    'consumes': ['application/json'],
    'parameters': [
        {
            'name': 'location_name',
            'description': 'The location name',
            'required': True,
            'in': 'path',
            'type': 'string'
        },
        {
            'name': 'mapset_name',
            'description': 'The name of the mapset that contains the required raster map layer',
            'required': True,
            'in': 'path',
            'type': 'string'
        },
        {
            'name': 'raster_name',
            'description': 'The name of the raster map layer to perform the raster map sampling from',
            'required': True,
            'in': 'path',
            'type': 'string'
        },
        {
            'name': 'points',
            'description': 'The sampling point array [[id, x, y],[id, x, y]]. '
                           'The coordinates of the sampling points must be the same as of the location '
                           'that contains the raster dataset.',
            'required': True,
            'in': 'body',
            'schema': PointListModel
        }
    ],
    'responses': {
        '200': {
            'description': 'The result of the raster map sampling',
            'schema':RasterSamplingResponseModel
        },
        '400': {
            'description':'The error message and a detailed log why raster sampling did not succeed',
            'schema':ProcessingErrorResponseModel
        }
    }
 }


class AsyncEphemeralRasterSamplingResource(ResourceBase):
    """Perform raster map sampling on a raster map layer based on input points, asynchronous call
    """
    decorators = [log_api_call, auth.login_required]

    def _execute(self, location_name, mapset_name, raster_name):

        rdc = self.preprocess(has_json=True, has_xml=False,
                              location_name=location_name,
                              mapset_name=mapset_name,
                              map_name=raster_name)
        if rdc:
            enqueue_job(self.job_timeout, start_job, rdc)

        return rdc

    @swagger.doc(deepcopy(SCHEMA_DOC))
    def post(self, location_name, mapset_name, raster_name):
        """Perform raster map sampling on a raster map layer based on input points asynchronously
        """
        self._execute(location_name, mapset_name, raster_name)
        html_code, response_model = pickle.loads(self.response_data)
        return make_response(jsonify(response_model), html_code)


class SyncEphemeralRasterSamplingResource(AsyncEphemeralRasterSamplingResource):
    """Perform raster map sampling on a raster map layer based on input points, synchronous call
    """
    decorators = [log_api_call, auth.login_required]

    @swagger.doc(deepcopy(SCHEMA_DOC))
    def post(self, location_name, mapset_name, raster_name):
        """Perform raster map sampling on a raster map layer based on input points synchronously
        """
        check = self._execute(location_name, mapset_name, raster_name)
        if check is not None:
            http_code, response_model = self.wait_until_finish()
        else:
            http_code, response_model = pickle.loads(self.response_data)
        return make_response(jsonify(response_model), http_code)


def start_job(*args):
    processing = AsyncEphemeralRasterSampling(*args)
    processing.run()


class AsyncEphemeralRasterSampling(EphemeralProcessing):
    """Sample a raster map at vector points
    """

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

        point_file = tempfile.NamedTemporaryFile(dir=self.temp_file_path, delete=True)
        result_file = tempfile.NamedTemporaryFile(dir=self.temp_file_path, delete=True)

        for tuple in points:
            if len(tuple) != 3:
                raise AsyncProcessError("Wrong number of coordinate entries")

            id, x, y = tuple
            row = "%s|%s|%s\n" % (id, x, y)
            point_file.write(row.encode())

        point_file.flush()

        pc = dict()
        pc["1"] = {"module": "v.in.ascii",
                   "inputs": {"input": point_file.name,
                              "format": "point",
                              "column": "id text, x double precision, y double precision",
                              "x": 2,
                              "y": 3},
                   "outputs": {"output": {"name": "input_points"}}}
        pc["2"]= {"module": "g.region",
                  "inputs": {"points": "input_points",
                             "align": "%s@%s" % (raster_name, self.mapset_name)},
                  "flags": "p"},
        pc["3"]= {"module": "r.what",
                  "inputs": {"map": "%s@%s" % (raster_name, self.mapset_name),
                             "points": "input_points"},
                  "outputs": {"output": {"name":result_file.name}},
                  "flags": "nrf",
                  "overwrite": True,
                  "superquiet": True}

        self.request_data = pc

        # Run the process chain
        EphemeralProcessing._execute(self, skip_permission_check=True)

        result = open(result_file.name, "r").readlines()

        output_list = []
        for line in result:
            output_list.append(line.replace("@" + self.mapset_name, "").strip().split("|"))

        self.module_results = output_list

        point_file.close()
        result_file.close()

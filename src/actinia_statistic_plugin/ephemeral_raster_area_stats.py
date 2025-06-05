# -*- coding: utf-8 -*-
"""
Compute areal categorical statistics on a raster map layer based on an input
polygon.
"""

from flask import jsonify, make_response
from actinia_processing_lib.ephemeral_processing import EphemeralProcessing
from actinia_rest_lib.resource_base import ResourceBase
from actinia_core.core.common.kvdb_interface import enqueue_job
from flask.json import dumps
import pickle
import tempfile
from copy import deepcopy
from flask_restful_swagger_2 import swagger
from actinia_core.core.common.app import auth
from actinia_core.core.common.api_logger import log_api_call
from .response_models import (
    CategoricalStatisticsResultModel,
    RasterAreaStatsResponseModel,
)
from actinia_core.models.response_models import ProcessingErrorResponseModel

__license__ = "GPLv3"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2016, Sören Gebbert"
__maintainer__ = "Sören Gebbert"
__email__ = "soerengebbert@googlemail.com"


SCHEMA_DOC = {
    "tags": ["Raster Statistics"],
    "description": "Compute areal categorical statistics on a raster map layer"
    " based on an input polygon. The input polygon must be provided as GeoJSON"
    " content in the request body. A correct coordinate reference system must "
    "be present in the GeoJSON definition. For each category the size of the "
    "occupied area, the number of pixel of the area and the percentage of the "
    "area size in relation to all other categories inclusive NULL data are "
    "computed. Minimum required user role: user.",
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
            "description": "The name of the raster map layer to compute the "
                           "statistics from",
            "required": True,
            "in": "path",
            "type": "string",
        },
        {
            "name": "shape",
            "description": "GeoJSON definition of the polygon to compute the "
                           "statistics for.",
            "required": True,
            "in": "body",
            "schema": {"type": "string"},
        },
    ],
    "responses": {
        "200": {
            "description": "The result of the areal raster statistical "
                           "computation",
            "schema": RasterAreaStatsResponseModel,
        },
        "400": {
            "description": "The error message and a detailed log why raster"
                           " statistic did not succeeded",
            "schema": ProcessingErrorResponseModel,
        },
    },
}


class AsyncEphemeralRasterAreaStatsResource(ResourceBase):
    """
    Compute areal categorical statistics on a raster map layer based on an
    input polygon, asynchronous call
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
        Compute areal categorical statistics on a raster map layer based on
        an input polygon asynchronously
        """
        self._execute(project_name, mapset_name, raster_name)
        html_code, response_model = pickle.loads(self.response_data)
        return make_response(jsonify(response_model), html_code)


class SyncEphemeralRasterAreaStatsResource(
    AsyncEphemeralRasterAreaStatsResource
):
    """
    Compute areal categorical statistics on a raster map layer based on an
    input polygon, synchronous call
    """

    decorators = [log_api_call, auth.login_required]

    @swagger.doc(deepcopy(SCHEMA_DOC))
    def post(self, project_name, mapset_name, raster_name):
        """
        Compute areal categorical statistics on a raster map layer based on an
        input polygon synchronously
        """
        check = self._execute(project_name, mapset_name, raster_name)
        if check is not None:
            http_code, response_model = self.wait_until_finish()
        else:
            http_code, response_model = pickle.loads(self.response_data)
        return make_response(jsonify(response_model), http_code)


def start_job(*args):
    processing = AsyncEphemeralRasterAreaStats(*args)
    processing.run()


class AsyncEphemeralRasterAreaStats(EphemeralProcessing):
    def __init__(self, *args):
        EphemeralProcessing.__init__(self, *args)
        self.response_model_class = RasterAreaStatsResponseModel

    def _execute(self):

        self._setup()

        raster_name = self.map_name
        self.required_mapsets.append(self.mapset_name)
        gml_file = tempfile.NamedTemporaryFile(
            dir=self.temp_file_path, delete=False
        )

        tmp_file = open(gml_file.name, "w")

        data = dumps(self.request_data)
        tmp_file.write(data)
        tmp_file.close()

        result_file = tempfile.NamedTemporaryFile(
            dir=self.temp_file_path, delete=False
        )

        pc = {
            "list": [
                {
                    "id": "v_import_1",
                    "module": "v.import",
                    "inputs": [{"param": "input", "value": gml_file.name}],
                    "outputs": [{"param": "output", "value": "polygon"}],
                    "superquiet": True
                },
            ],
            "version": "1",
        }

        # Run the import, ignore region settings
        self.skip_region_check = True
        process_list = (
            self._create_temporary_grass_environment_and_process_list(
                process_chain=pc, skip_permission_check=True
            )
        )
        self._execute_process_list(process_list)

        pc = {
            "list": [
                {
                    "id": "g_region_2",
                    "module": "g.region",
                    "inputs": [
                        {
                            "param": "vector",
                            "value": "polygon"
                        },
                        {
                            "param": "align",
                            "value": raster_name + "@" + self.mapset_name
                        }
                    ],
                    "flags": "p",
                    "superquiet": True
                },
                {
                    "id": "r_mask_3",
                    "module": "r.mask",
                    "inputs": [
                        {
                            "param": "vector",
                            "value": "polygon"
                        }
                    ],
                    "superquiet": True
                },
                {
                    "id": "r_stats_4",
                    "module": "r.stats",
                    "inputs": [
                        {
                            "param": "input",
                            "value": raster_name + "@" + self.mapset_name
                        },
                        {
                            "param": "separator",
                            "value": "|"
                        }
                    ],
                    "outputs": [
                        {
                            "param": "output",
                            "value": result_file.name
                        }
                    ],
                    "flags": "acpl",
                    "superquiet": True
                },
            ],
            "version": "1",
        }

        # Run the area statistics and check for correct region settings
        self.skip_region_check = False
        process_list = self._validate_process_chain(
            process_chain=pc, skip_permission_check=True
        )
        self._execute_process_list(process_list)

        result = open(result_file.name, "r").readlines()

        output_list = []
        for line in result:
            stat_list = line.strip().split("|")

            output_list.append(
                CategoricalStatisticsResultModel(
                    cat=stat_list[0],
                    name=stat_list[1],
                    area=float(stat_list[2]),
                    cell_count=int(stat_list[3]),
                    percent=float(stat_list[4].split("%")[0]),
                )
            )

        self.module_results = output_list

        gml_file.close()
        result_file.close()

# -*- coding: utf-8 -*-
"""
Compute areal categorical statistics on a space-time raster dataset based on
an input polygon.
"""

import pickle
import tempfile
from datetime import datetime
from copy import deepcopy
from flask import jsonify, make_response
from flask.json import dumps
from actinia_processing_lib.ephemeral_processing import EphemeralProcessing
from actinia_rest_lib.resource_base import ResourceBase
from actinia_core.core.common.kvdb_interface import enqueue_job
from actinia_processing_lib.exceptions import AsyncProcessError
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
    "tags": ["STRDS Statistics"],
    "description": "Compute areal categorical statistics on a raster map "
    "layer contained in a "
    "space-time raster dataset based on an input polygon. "
    "The input polygon must be provided as GeoJSON content"
    " in the request body. A correct "
    "coordinate reference system must be present in the GeoJSON definition. "
    "For each category the "
    "size of the occupied area, the number of pixel of the area and the "
    "percentage of the area size "
    "in relation to all other categories inclusive NULL data are computed. "
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
            "space-time raster dataset",
            "required": True,
            "in": "path",
            "type": "string",
        },
        {
            "name": "strds_name",
            "description": "The name of the space-time raster dataset to "
            "select the raster map layer from",
            "required": True,
            "in": "path",
            "type": "string",
        },
        {
            "name": "timestamp",
            "description": "The time stamp that should be used for raster map "
            "layer selection. "
            "Required format is: YYYY-MM-DDTHH:MM:SS for example "
            "2001-03-16T12:30:15.",
            "required": True,
            "in": "path",
            "type": "string",
            "format": "dateTime",
        },
        {
            "name": "shape",
            "description": "GeoJSON definition of the polygon to compute the "
            "statistics for. The .",
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
            "description": "The error message and a detailed log why raster "
            "statistic did not succeeded",
            "schema": ProcessingErrorResponseModel,
        },
    },
}


class AsyncEphemeralSTRDSAreaStatsResource(ResourceBase):
    """
    Compute area statistics based on a vector map for a single raster layer
    that is temporally sampled from a STRDS by a timestamp.
    """

    decorators = [log_api_call, auth.login_required]

    def _execute(self, project_name, mapset_name, strds_name, timestamp):
        """Prepare and enqueue the raster area statistics

        Raises:
            InvalidUsage: In case the timestamp is wrong or the XML content
                          is missing
        """
        # Check the time stamp
        try:
            datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            msg = (
                "Wrong timestamp format. Required format is: "
                "YYYY-MM-DDTHH:MM:SS for example 2001-03-16T12:30:15"
            )
            return self.get_error_response(message=msg)

        rdc = self.preprocess(
            has_json=True,
            has_xml=False,
            project_name=project_name,
            mapset_name=mapset_name,
            map_name=strds_name,
        )
        if rdc:
            rdc.set_user_data(timestamp)
            enqueue_job(self.job_timeout, start_job, rdc)

        return rdc

    @swagger.doc(deepcopy(SCHEMA_DOC))
    def post(self, project_name, mapset_name, strds_name, timestamp):
        """
        Compute area statistics based on a vector map for a single raster
        layer that is temporally sampled from a STRDS by a timestamp.

        Raises:
            InvalidUsage: In case the timestamp is wrong or the XML content
                          is missing
        """
        self._execute(project_name, mapset_name, strds_name, timestamp)
        html_code, response_model = pickle.loads(self.response_data)
        return make_response(jsonify(response_model), html_code)


class SyncEphemeralSTRDSAreaStatsResource(
    AsyncEphemeralSTRDSAreaStatsResource
):
    """Compute area statistics based on a vector map for a single raster layer
    that is temporally sampled from a STRDS by a timestamp.
    """

    decorators = [log_api_call, auth.login_required]

    @swagger.doc(deepcopy(SCHEMA_DOC))
    def post(self, project_name, mapset_name, strds_name, timestamp):
        """Compute area statistics based on a vector map for a single raster
        layer that is temporally sampled from a STRDS by a timestamp.

        Raises:
            InvalidUsage: In case the timestamp is wrong or the XML content
                          is missing

        """
        check = self._execute(
            project_name, mapset_name, strds_name, timestamp
        )
        if check is not None:
            http_code, response_model = self.wait_until_finish()
        else:
            http_code, response_model = pickle.loads(self.response_data)
        return make_response(jsonify(response_model), http_code)


def start_job(*args):
    processing = AsyncEphemeralSTRDSAreaStats(*args)
    processing.run()


class AsyncEphemeralSTRDSAreaStats(EphemeralProcessing):
    """
    Compute area statistics based on a vector map for a single raster layer
    that is temporally sampled from a STRDS by a timestamp.
    """

    def __init__(self, *args):
        EphemeralProcessing.__init__(self, *args)
        self.response_model_class = RasterAreaStatsResponseModel

    def _execute(self):

        self._setup()

        strds_name = self.map_name
        timestamp = self.rdc.user_data

        self.required_mapsets.append(self.mapset_name)
        gml_file = tempfile.NamedTemporaryFile(
            dir=self.temp_file_path, delete=True
        )

        tmp_file = open(gml_file.name, "w")
        tmp_file.write(dumps(self.request_data))
        tmp_file.close()

        pc = {
            "list": [
                {
                    "id": "v_import_1",
                    "module": "v.import",
                    "inputs": [
                        {
                            "param": "input",
                            "value": gml_file.name,
                        }
                    ],
                    "outputs": [
                        {
                            "param": "output",
                            "value": "polygon",
                        }
                    ],
                    "superquiet": True
                },
                {
                    "id": "t_create_2",
                    "module": "t.create",
                    "inputs": [
                        {
                            "param": "type",
                            "value": "stvds",
                        },
                        {
                            "param": "temporaltype",
                            "value": "absolute",
                        },
                        {
                            "param": "semantictype",
                            "value": "mean",
                        },
                        {
                            "param": "title",
                            "value": "Polygon",
                        },
                        {
                            "param": "description",
                            "value": "Polygon",
                        },
                    ],
                    "outputs": [
                        {
                            "param": "output",
                            "value": "polygon_stvds",
                        }
                    ],
                    "superquiet": True
                },
                {
                    "id": "t_register_3",
                    "module": "t.register",
                    "inputs": [
                        {
                            "param": "type",
                            "value": "vector",
                        },
                        {
                            "param": "input",
                            "value": "polygon_stvds",
                        },
                        {
                            "param": "maps",
                            "value": "polygon",
                        },
                        {
                            "param": "start",
                            "value": timestamp,
                        },
                        {
                            "param": "increment",
                            "value": "1 second",
                        },
                    ],
                    "flags": "i",
                    "superquiet": True
                },
                {
                    "id": "t_sample_4",
                    "module": "t.sample",
                    "inputs": [
                        {
                            "param": "sample",
                            "value": "polygon_stvds",
                        },
                        {
                            "param": "inputs",
                            "value": strds_name + "@" + self.mapset_name,
                        },
                        {
                            "param": "samtype",
                            "value": "stvds",
                        },
                        {
                            "param": "intype",
                            "value": "strds",
                        },
                    ],
                    "superquiet": True
                },
            ],
            "version": "1",
        }

        # Setup the grass environment, check the process chain and run the
        # modules
        self.skip_region_check = True
        process_list = (
            self._create_temporary_grass_environment_and_process_list(
                process_chain=pc, skip_permission_check=True
            )
        )
        self._execute_process_list(process_list)

        gml_file.close()

        # Extract raster name
        map_list = self.module_output_log[3]["stdout"]

        self.message_logger.debug("Maplist: " + str(map_list))
        # Check if a map was found
        try:
            raster_name = map_list.split("|")[1]
            # Select the first raster name from a list of names
            if "," in raster_name:
                raster_name = raster_name.split(",")[0]
        except Exception:
            raise AsyncProcessError(
                "No raster maps found for timestamp: " + timestamp
            )

        if raster_name == "None":
            raise AsyncProcessError(
                "No raster maps found for timestamp: " + timestamp
            )

        result_file = tempfile.NamedTemporaryFile(
            dir=self.temp_file_path, delete=True
        )

        pc = {
            "list": [
                {
                    "id": "g_region_5",
                    "module": "g.region",
                    "inputs": [
                        {
                            "param": "vector",
                            "value": "polygon",
                        },
                        {
                            "param": "align",
                            "value": raster_name,
                        },
                    ],
                    "superquiet": True
                },
                {
                    "id": "r_mask_6",
                    "module": "r.mask",
                    "inputs": [
                        {
                            "param": "vector",
                            "value": "polygon",
                        }
                    ],
                    "superquiet": True
                },
                {
                    "id": "r_stats_7",
                    "module": "r.stats",
                    "inputs": [
                        {
                            "param": "input",
                            "value": raster_name,
                        },
                        {
                            "param": "separator",
                            "value": "|",
                        },
                    ],
                    "outputs": [
                        {
                            "param": "output",
                            "value": result_file.name,
                        }
                    ],
                    "flags": "acpl",
                    "superquiet": True
                },
            ],
            "version": "1",
        }

        # Check the process chain and run the modules
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

        result_file.close()

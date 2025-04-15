# -*- coding: utf-8 -*-
from flask_restful_swagger_2 import Schema
from copy import deepcopy
from actinia_core.models.response_models import ProcessingResponseModel
from actinia_api import URL_PREFIX

__license__ = "GPLv3"
__author__ = "Sören Gebbert, Markus Neteler"
__copyright__ = "Copyright 2016-2022, Sören Gebbert, Markus Neteler and "
"mundialis GmbH & Co. KG"


class UnivarResultModel(Schema):
    """
    Response schema for the result of univariate computations of raster layers.

    It is used as schema to define the *process_result* in a
    ProcessingResponseModel derivative.
    """

    type = "object"
    properties = {
        "name": {
            "type": "string",
            "description": "The name of the raster resource",
        },
        "cells": {
            "type": "number",
            "format": "double",
        },
        "coeff_var": {
            "type": "number",
            "format": "double",
        },
        "max": {
            "type": "number",
            "format": "double",
        },
        "mean": {
            "type": "number",
            "format": "double",
        },
        "mean_of_abs": {
            "type": "number",
            "format": "double",
        },
        "min": {
            "type": "number",
            "format": "double",
        },
        "n": {
            "type": "number",
            "format": "double",
        },
        "null_cells": {
            "type": "number",
            "format": "double",
        },
        "range": {
            "type": "number",
            "format": "double",
        },
        "stddev": {
            "type": "number",
            "format": "double",
        },
        "sum": {
            "type": "number",
            "format": "double",
        },
        "variance": {
            "type": "number",
            "format": "double",
        },
    }
    # If a map is empty, r.univar will return nothing, hence no required
    # variables
    # required = ['name', 'cells', 'coeff_var', 'max', 'mean', 'mean_of_abs',
    #           'min', 'n', 'null_cells', 'range', 'stddev', 'sum', 'variance']


class CategoricalStatisticsResultModel(Schema):
    """
    Response schema for the result of r.stats computations of raster layers.

    It is used as schema to define the *process_result* in a
    ProcessingResponseModel derivative.
    """

    type = "object"
    required = ["cat", "name", "area", "cell_count", "percent"]
    properties = {
        "cat": {"type": "string", "description": "The raster category"},
        "name": {
            "type": "string",
            "description": "The name of raster category",
        },
        "area": {
            "type": "number",
            "format": "double",
            "description": "The size of the area in square meters",
        },
        "cell_count": {
            "type": "number",
            "format": "double",
            "description": "The number of cells that have the raster category",
        },
        "percent": {
            "type": "number",
            "format": "double",
            "description": "The percentage of the area",
        },
    }
    example = {
        "area": 812.25,
        "cat": "0",
        "cell_count": 1,
        "name": "not classified",
        "percent": 0.0,
    }


class RasterAreaStatsResponseModel(ProcessingResponseModel):
    """Response schema for a list of categorical statistics.

    This schema is a derivative of the ProcessingResponseModel that defines a
    different *process_results* schema.
    """

    type = "object"
    properties = deepcopy(ProcessingResponseModel.properties)
    properties["process_results"] = {}
    properties["process_results"]["type"] = "array"
    properties["process_results"]["items"] = CategoricalStatisticsResultModel
    required = deepcopy(ProcessingResponseModel.required)
    example = {
      "accept_datetime": "2022-07-31 16:57:18.978035",
      "accept_timestamp": 1659286638.9780345,
      "api_info": {
        "endpoint": "syncephemeralrasterareastatsresource",
        "method": "POST",
        "path": f"{URL_PREFIX}/projects/nc_spm_08/mapsets/PERMANENT/"
                "raster_layers/landuse96_28m/area_stats_sync",
        "request_url": f"http://localhost:8088{URL_PREFIX}/projects/"
                       "nc_spm_08/mapsets/PERMANENT/raster_layers/"
                       "landuse96_28m/area_stats_sync"
      },
      "datetime": "2022-07-31 16:57:21.441611",
      "http_code": 200,
      "message": "Processing successfully finished",
      "process_chain_list": [
        {
          "list": [
            {
              "id": "v_import_1",
              "inputs": [
                {
                  "param": "input",
                  "value": "/tmp/gisdbase_f74f788c0834401d990582fbafc3eb1f/"
                           ".tmp/tmpjh3rr_ra"
                }
              ],
              "module": "v.import",
              "outputs": [
                {
                  "param": "output",
                  "value": "polygon"
                }
              ],
              "superquiet": True
            }
          ],
          "version": "1"
        },
        {
          "list": [
            {
              "flags": "p",
              "id": "g_region_2",
              "inputs": [
                {
                  "param": "vector",
                  "value": "polygon"
                },
                {
                  "param": "align",
                  "value": "landuse96_28m@PERMANENT"
                }
              ],
              "module": "g.region",
              "superquiet": True
            },
            {
              "id": "r_mask_3",
              "inputs": [
                {
                  "param": "vector",
                  "value": "polygon"
                }
              ],
              "module": "r.mask",
              "superquiet": True
            },
            {
              "flags": "acpl",
              "id": "r_stats_4",
              "inputs": [
                {
                  "param": "input",
                  "value": "landuse96_28m@PERMANENT"
                },
                {
                  "param": "separator",
                  "value": "|"
                }
              ],
              "module": "r.stats",
              "outputs": [
                {
                  "param": "output",
                  "value": "/tmp/gisdbase_f74f788c0834401d990582fbafc3eb1f/"
                           ".tmp/tmp8wtkfuox"
                }
              ],
              "superquiet": True
            }
          ],
          "version": "1"
        }
      ],
      "process_log": [
        {
          "executable": "v.import",
          "id": "v_import_1",
          "mapset_size": 15979,
          "parameter": [
            "input=/tmp/gisdbase_f74f788c0834401d990582fbafc3eb1f/.tmp/"
            "tmpjh3rr_ra",
            "output=polygon",
            "--qq"
          ],
          "return_code": 0,
          "run_time": 0.3008110523223877,
          "stderr": [
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "g.region",
          "id": "g_region_2",
          "mapset_size": 16025,
          "parameter": [
            "vector=polygon",
            "align=landuse96_28m@PERMANENT",
            "-p",
            "--qq"
          ],
          "return_code": 0,
          "run_time": 0.10030579566955566,
          "stderr": [
            ""
          ],
          "stdout": "projection: 99 (NAD83(HARN) / North Carolina)\nzone:    "
          "   0\ndatum:      nad83harn\nellipsoid:  grs80\nnorth:      "
          "647021.25\nsouth:      64994.25\nwest:       329989\neast:       "
          "337000\nnsres:      28.5\newres:      28.5\nrows:       20422\n"
          "cols:       246\ncells:      5023812\n"
        },
        {
          "executable": "r.mask",
          "id": "r_mask_3",
          "mapset_size": 956099,
          "parameter": [
            "vector=polygon",
            "--qq"
          ],
          "return_code": 0,
          "run_time": 0.952303409576416,
          "stderr": [
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "r.stats",
          "id": "r_stats_4",
          "mapset_size": 956099,
          "parameter": [
            "input=landuse96_28m@PERMANENT",
            "separator=|",
            "output=/tmp/gisdbase_f74f788c0834401d990582fbafc3eb1f/.tmp/"
            "tmp8wtkfuox",
            "-acpl",
            "--qq"
          ],
          "return_code": 0,
          "run_time": 0.501760721206665,
          "stderr": [
            ""
          ],
          "stdout": ""
        }
      ],
      "process_results": [
        {
          "area": 4080591297.0,
          "cat": "*",
          "cell_count": 5023812,
          "name": "no data",
          "percent": 100.0
        }
      ],
      "progress": {
        "num_of_steps": 4,
        "step": 4
      },
      "resource_id": "resource_id-67fab95f-2782-41c8-9b89-b767f67a9df9",
      "status": "finished",
      "time_delta": 2.4635958671569824,
      "timestamp": 1659286641.4415936,
      "urls": {
        "resources": [],
        "status": f"http://localhost:8088{URL_PREFIX}/resources/actinia-gdi/"
                  "resource_id-67fab95f-2782-41c8-9b89-b767f67a9df9"
      },
      "user_id": "actinia-gdi"
    }


class AreaUnivarResultModel(Schema):
    """
    Response schema for the result of univariate computations of raster layers
    based on a vector area.

    It is used as schema to define the *process_result* in a
    ProcessingResponseModel derivative.
    """

    type = "object"
    properties = {
        "fid": {
            "type": "string",
            "description": "Field id from the polygon of the vector map layer"
            " used for area stats computation",
        },
        "cat": {
            "type": "string",
            "description": "The category id from the polygon of the vector"
            " map layer used for area stats computation",
        },
        "raster_number": {
            "type": "number",
            "format": "double",
        },
        "raster_minimum": {
            "type": "number",
            "format": "double",
        },
        "raster_maximum": {
            "type": "number",
            "format": "double",
        },
        "raster_range": {
            "type": "number",
            "format": "double",
        },
        "raster_average": {
            "type": "number",
            "format": "double",
        },
        "raster_median": {
            "type": "number",
            "format": "double",
        },
        "raster_stddev": {
            "type": "number",
            "format": "double",
        },
        "raster_sum": {
            "type": "number",
            "format": "double",
        },
        "raster_variance": {
            "type": "number",
            "format": "double",
        },
        "raster_coeff_var": {
            "type": "number",
            "format": "double",
        },
    }
    example = {
        "cat": "1",
        "fid": "swwake_10m.0",
        "raster_average": 4.27381481481481,
        "raster_coeff_var": 36.2154244540989,
        "raster_maximum": 6.0,
        "raster_median": 5.0,
        "raster_minimum": 1.0,
        "raster_number": 2025000.0,
        "raster_range": 5.0,
        "raster_stddev": 1.54778017556735,
        "raster_sum": 8654475.0,
        "raster_variance": 2.39562347187929,
    }


class RasterAreaUnivarStatsResponseModel(ProcessingResponseModel):
    """
    Response schema for resources that generate area univariate result lists
     as processing results.

    This schema is a derivative of the ProcessingResponseModel that defines a
    different *process_results* schema.
    """

    type = "object"
    properties = deepcopy(ProcessingResponseModel.properties)
    properties["process_results"] = {}
    properties["process_results"]["type"] = "array"
    properties["process_results"]["items"] = AreaUnivarResultModel
    required = deepcopy(ProcessingResponseModel.required)
    # required.append("process_results")
    example = {
      "accept_datetime": "2022-07-31 17:08:36.534924",
      "accept_timestamp": 1659287316.5349228,
      "api_info": {
        "endpoint": "syncephemeralstrdsareastatsunivarresource",
        "method": "POST",
        "path": f"{URL_PREFIX}/projects/nc_spm_08/mapsets/modis_lst/strds/"
                "LST_Day_monthly/timestamp/2016-01-01T00:00:00/"
                "area_stats_univar_sync",
        "request_url": f"http://localhost:8088{URL_PREFIX}/projects/nc_spm_08"
                       "/mapsets/modis_lst/strds/LST_Day_monthly/timestamp/"
                       "2016-01-01T00:00:00/area_stats_univar_sync"
      },
      "datetime": "2022-07-31 17:08:42.056326",
      "http_code": 200,
      "message": "Processing successfully finished",
      "process_chain_list": [
        {
          "list": [
            {
              "id": "v_import_1",
              "inputs": [
                {
                  "param": "input",
                  "value": "/tmp/gisdbase_a9254feb879d4381bbcffb2a1f08a67c/"
                           ".tmp/tmptsev20y3"
                }
              ],
              "module": "v.import",
              "outputs": [
                {
                  "param": "output",
                  "value": "polygon"
                }
              ],
              "superquiet": True
            },
            {
              "id": "t_create_2",
              "inputs": [
                {
                  "param": "type",
                  "value": "stvds"
                },
                {
                  "param": "temporaltype",
                  "value": "absolute"
                },
                {
                  "param": "semantictype",
                  "value": "mean"
                },
                {
                  "param": "title",
                  "value": "Polygon"
                },
                {
                  "param": "description",
                  "value": "Polygon"
                }
              ],
              "module": "t.create",
              "outputs": [
                {
                  "param": "output",
                  "value": "polygon_stvds"
                }
              ],
              "superquiet": True
            },
            {
              "flags": "i",
              "id": "t_register_3",
              "inputs": [
                {
                  "param": "type",
                  "value": "vector"
                },
                {
                  "param": "input",
                  "value": "polygon_stvds"
                },
                {
                  "param": "maps",
                  "value": "polygon"
                },
                {
                  "param": "start",
                  "value": "2016-01-01T00:00:00"
                },
                {
                  "param": "increment",
                  "value": "1 second"
                }
              ],
              "module": "t.register",
              "superquiet": True
            },
            {
              "id": "t_sample_4",
              "inputs": [
                {
                  "param": "sample",
                  "value": "polygon_stvds"
                },
                {
                  "param": "samtype",
                  "value": "stvds"
                },
                {
                  "param": "intype",
                  "value": "strds"
                },
                {
                  "param": "inputs",
                  "value": "LST_Day_monthly@modis_lst"
                }
              ],
              "module": "t.sample",
              "superquiet": True
            }
          ],
          "version": "1"
        },
        {
          "list": [
            {
              "id": "g_region_5",
              "inputs": [
                {
                  "param": "vector",
                  "value": "polygon"
                }
              ],
              "module": "g.region",
              "superquiet": True
            },
            {
              "id": "v_rast_stats_6",
              "inputs": [
                {
                  "param": "map",
                  "value": "polygon"
                },
                {
                  "param": "method",
                  "value": "number,minimum,maximum,range,average,median,stddev"
                           ",sum,variance,coeff_var"
                },
                {
                  "param": "raster",
                  "value": "MOD11B3.A2016001.h11v05.single_LST_Day_6km@"
                           "modis_lst"
                },
                {
                  "param": "column_prefix",
                  "value": "raster"
                }
              ],
              "module": "v.rast.stats",
              "superquiet": True
            },
            {
              "id": "v_db_select_7",
              "inputs": [
                {
                  "param": "map",
                  "value": "polygon"
                }
              ],
              "module": "v.db.select",
              "outputs": [
                {
                  "param": "file",
                  "value": "/tmp/gisdbase_a9254feb879d4381bbcffb2a1f08a67c/"
                           ".tmp/tmp19gkkrii"
                }
              ],
              "superquiet": True
            }
          ],
          "version": "1"
        }
      ],
      "process_log": [
        {
          "executable": "v.import",
          "id": "v_import_1",
          "mapset_size": 16040,
          "parameter": [
            "input=/tmp/gisdbase_a9254feb879d4381bbcffb2a1f08a67c/.tmp/"
            "tmptsev20y3",
            "output=polygon",
            "--qq"
          ],
          "return_code": 0,
          "run_time": 0.3008089065551758,
          "stderr": [
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "t.create",
          "id": "t_create_2",
          "mapset_size": 495359,
          "parameter": [
            "type=stvds",
            "temporaltype=absolute",
            "semantictype=mean",
            "title=Polygon",
            "description=Polygon",
            "output=polygon_stvds",
            "--qq"
          ],
          "return_code": 0,
          "run_time": 0.6529664993286133,
          "stderr": [
            "WARNING: Temporal database connection defined as:",
            "/tmp/gisdbase_a9254feb879d4381bbcffb2a1f08a67c/nc_spm_08/"
            "mapset_a9254feb879d4381bbcffb2a1f08a67c/tgis/sqlite.db",
            "But database file does not exist.",
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "t.register",
          "id": "t_register_3",
          "mapset_size": 495401,
          "parameter": [
            "type=vector",
            "input=polygon_stvds",
            "maps=polygon",
            "start=2016-01-01T00:00:00",
            "increment=1 second",
            "-i",
            "--qq"
          ],
          "return_code": 0,
          "run_time": 0.6026990413665771,
          "stderr": [
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "t.sample",
          "id": "t_sample_4",
          "mapset_size": 495401,
          "parameter": [
            "sample=polygon_stvds",
            "samtype=stvds",
            "intype=strds",
            "inputs=LST_Day_monthly@modis_lst",
            "--qq"
          ],
          "return_code": 0,
          "run_time": 0.652012825012207,
          "stderr": [
            ""
          ],
          "stdout": "polygon@mapset_a9254feb879d4381bbcffb2a1f08a67c|"
          "MOD11B3.A2016001.h11v05.single_LST_Day_6km@modis_lst|2016-01-01 "
          "00:00:00|2016-01-01 00:00:01|1.1574074074074073e-05|0.0\n"
        },
        {
          "executable": "g.region",
          "id": "g_region_5",
          "mapset_size": 495437,
          "parameter": [
            "vector=polygon",
            "--qq"
          ],
          "return_code": 0,
          "run_time": 0.10033965110778809,
          "stderr": [
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "v.rast.stats",
          "id": "v_rast_stats_6",
          "mapset_size": 496399,
          "parameter": [
            "map=polygon",
            "method=number,minimum,maximum,range,average,median,stddev,sum,"
            "variance,coeff_var",
            "raster=MOD11B3.A2016001.h11v05.single_LST_Day_6km@modis_lst",
            "column_prefix=raster",
            "--qq"
          ],
          "return_code": 0,
          "run_time": 1.9554402828216553,
          "stderr": [
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "v.db.select",
          "id": "v_db_select_7",
          "mapset_size": 496399,
          "parameter": [
            "map=polygon",
            "file=/tmp/gisdbase_a9254feb879d4381bbcffb2a1f08a67c/.tmp/"
            "tmp19gkkrii",
            "--qq"
          ],
          "return_code": 0,
          "run_time": 0.1003561019897461,
          "stderr": [
            ""
          ],
          "stdout": ""
        }
      ],
      "process_results": [
        {
          "cat": "1",
          "fid": "test",
          "raster_average": 13868.2019230769,
          "raster_coeff_var": 1.04355110326768,
          "raster_maximum": 14170.0,
          "raster_median": 13824.0,
          "raster_minimum": 13649.0,
          "raster_number": 104.0,
          "raster_range": 521.0,
          "raster_stddev": 144.721774171659,
          "raster_sum": 1442293.0,
          "raster_variance": 20944.3919193928
        }
      ],
      "progress": {
        "num_of_steps": 7,
        "step": 7
      },
      "resource_id": "resource_id-a314816e-bc38-4c58-8601-78fe20c9aea6",
      "status": "finished",
      "time_delta": 5.521468162536621,
      "timestamp": 1659287322.056266,
      "urls": {
        "resources": [],
        "status": f"http://localhost:8088{URL_PREFIX}/resources/actinia-gdi/"
        "resource_id-a314816e-bc38-4c58-8601-78fe20c9aea6"
      },
      "user_id": "actinia-gdi"
    }


class RasterSamplingResponseModel(ProcessingResponseModel):
    """
    Response schema for a raster map sampling result.

    This schema is a derivative of the ProcessingResponseModel that defines a
     different *process_results* schema.
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
        "accept_datetime": "2022-03-17 12:29:27.718749",
        "accept_timestamp": 1647520167.718739,
        "api_info": {
            "endpoint": "syncephemeralrastersamplingresource",
            "method": "POST",
            "path": f"{URL_PREFIX}/projects/nc_spm_08/mapsets/PERMANENT/"
            "raster_layers/landuse96_28m/sampling_sync",
            "request_url": f"http://localhost{URL_PREFIX}/projects/nc_spm_08"
            "/mapsets/PERMANENT/raster_layers/landuse96_28m/sampling_sync",
        },
        "datetime": "2022-03-17 12:29:28.431388",
        "http_code": 200,
        "message": "Processing successfully finished",
        "process_chain_list": [
            {
                "list": [
                    {
                        "id": "v_in_ascii",
                        "inputs": [
                            {
                                "param": "input",
                                "value": "/tmp/"
                                "gisdbase_3ef25f3f447844f2aaea07b4a34a2107/"
                                ".tmp/tmpnk7lt8rx",
                            },
                            {"param": "format", "value": "point"},
                            {
                                "param": "column",
                                "value": "id text, x double precision, y"
                                " double precision",
                            },
                            {"param": "x", "value": "2"},
                            {"param": "y", "value": "3"},
                        ],
                        "module": "v.in.ascii",
                        "outputs": [
                            {"param": "output", "value": "input_points"}
                        ],
                    },
                    {
                        "flags": "p",
                        "id": "g_region",
                        "inputs": [
                            {"param": "vector", "value": "input_points"},
                            {
                                "param": "align",
                                "value": "landuse96_28m@PERMANENT",
                            },
                        ],
                        "module": "g.region",
                    },
                    {
                        "flags": "nrf",
                        "id": "r_what",
                        "inputs": [
                            {
                                "param": "map",
                                "value": "landuse96_28m@PERMANENT",
                            },
                            {"param": "points", "value": "input_points"},
                        ],
                        "module": "r.what",
                        "outputs": [
                            {
                                "param": "output",
                                "value": "/tmp/"
                                "gisdbase_3ef25f3f447844f2aaea07b4a34a2107/"
                                ".tmp/tmp0ktsyzl6",
                            }
                        ],
                        "overwrite": True,
                        "superquiet": True,
                    },
                ],
                "version": "1",
            }
        ],
        "process_log": [
            {
                "executable": "v.in.ascii",
                "id": "v_in_ascii",
                "mapset_size": 15753,
                "parameter": [
                    "input=/tmp/gisdbase_3ef25f3f4"
                    "47844f2aaea07b4a34a2107/.tmp/tmpnk7lt8rx",
                    "format=point",
                    "column=id text, x double precision, y double precision",
                    "x=2",
                    "y=3",
                    "output=input_points",
                ],
                "return_code": 0,
                "run_time": 0.10030794143676758,
                "stderr": [
                    "Scanning input for column types...",
                    "Number of columns: 3",
                    "Number of data rows: 2",
                    "Importing points...",
                    "0..50..100",
                    "Populating table...",
                    "Building topology for vector map <input_points@mapset_3e"
                    "f25f3f447844f2aaea07b4a34a2107>...",
                    "Registering primitives...",
                    "",
                    "",
                ],
                "stdout": "",
            },
            {
                "executable": "g.region",
                "id": "g_region",
                "mapset_size": 15761,
                "parameter": [
                    "vector=input_points",
                    "align=landuse96_28m@PERMANENT",
                    "-p",
                ],
                "return_code": 0,
                "run_time": 0.10032916069030762,
                "stderr": [""],
                "stdout": "projection: 99 (Lambert Conformal Conic)\nzone:  "
                "     0\ndatum:      nad83\nellipsoid:  a=6378137 es=0.006694"
                "380022900787\nnorth:      226389.75\nsouth:      220205.25\n"
                "west:       635651.5\neast:       638701\nnsres:      28.5\n"
                "ewres:      28.5\nrows:       217\ncols:       107\ncells:   "
                "   23219\n",
            },
            {
                "executable": "r.what",
                "id": "r_what",
                "mapset_size": 15761,
                "parameter": [
                    "map=landuse96_28m@PERMANENT",
                    "points=input_points",
                    "output=/tmp/gisdbase_3ef25f3f4"
                    "47844f2aaea07b4a34a2107/.tmp/tmp0ktsyzl6",
                    "-nrf",
                    "--o",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.1003561019897461,
                "stderr": [""],
                "stdout": "",
            },
        ],
        "process_results": [
            {
                "p1": {
                    "color": "229:229:204",
                    "easting": "638684",
                    "label": "Managed Herbaceous Cover",
                    "map_name": "landuse96_28m",
                    "northing": "220210",
                    "value": "4",
                }
            },
            {
                "p2": {
                    "color": "255:000:000",
                    "easting": "635676",
                    "label": "High Intensity Developed",
                    "map_name": "landuse96_28m",
                    "northing": "226371",
                    "value": "1",
                }
            },
        ],
        "progress": {"num_of_steps": 3, "step": 3},
        "resource_id": "resource_id-14d1b433-f875-4ffd-a42a-27449d76341a",
        "status": "finished",
        "time_delta": 0.7126758098602295,
        "timestamp": 1647520168.431363,
        "urls": {
            "resources": [],
            "status": f"http://localhost{URL_PREFIX}/resources/actinia-gdi/"
            "resource_id-14d1b433-f875-4ffd-a42a-27449d76341a",
        },
        "user_id": "actinia-gdi",
    }


class VectorSamplingResponseModel(ProcessingResponseModel):
    """
    Response schema for a vector map sampling result.

    This schema is a derivative of the ProcessingResponseModel that defines a
    different *process_results* schema.
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
        "accept_datetime": "2022-03-17 13:41:43.981103",
        "accept_timestamp": 1647524503.9810963,
        "api_info": {
            "endpoint": "syncephemeralvectorsamplingresource",
            "method": "POST",
            "path": f"{URL_PREFIX}/projects/nc_spm_08/mapsets/PERMANENT/"
            "vector_layers/zipcodes_wake/sampling_sync",
            "request_url": f"http://localhost{URL_PREFIX}//projects/nc_spm_08"
            "/mapsets/PERMANENT/vector_layers/zipcodes_wake/sampling_sync",
        },
        "datetime": "2022-03-17 13:41:44.467395",
        "http_code": 200,
        "message": "Processing successfully finished",
        "process_chain_list": [
            {
                "list": [
                    {
                        "flags": "p",
                        "id": "g_region",
                        "inputs": [
                            {
                                "param": "vector",
                                "value": "zipcodes_wake@PERMANENT",
                            }
                        ],
                        "module": "g.region",
                    },
                    {
                        "flags": "ag",
                        "id": "v_what",
                        "inputs": [
                            {
                                "param": "map",
                                "value": "zipcodes_wake@PERMANENT",
                            },
                            {
                                "param": "coordinates",
                                "value": "638684.0,220210.0,635676.0,226371.0",
                            },
                        ],
                        "module": "v.what",
                        "stdout": {
                            "delimiter": "|",
                            "format": "list",
                            "id": "info",
                        },
                    },
                ],
                "version": "1",
            }
        ],
        "process_log": [
            {
                "executable": "g.region",
                "id": "g_region",
                "mapset_size": 485,
                "parameter": ["vector=zipcodes_wake@PERMANENT", "-p"],
                "return_code": 0,
                "run_time": 0.10039043426513672,
                "stderr": [""],
                "stdout": "projection: 99 (Lambert Conformal Conic)\nzone:  "
                "     0\ndatum:      nad83\nellipsoid:  a=6378137 es=0.006694"
                "380022900787\nnorth:      258102.57214598\nsouth:      "
                "196327.52090104\nwest:       610047.86645109\neast:       "
                "677060.680666\nnsres:      498.18589714\newres:      "
                "500.09562847\nrows:       124\ncols:       134\ncells:    "
                "  16616\n",
            },
            {
                "executable": "v.what",
                "id": "v_what",
                "mapset_size": 485,
                "parameter": [
                    "map=zipcodes_wake@PERMANENT",
                    "coordinates=638684.0,220210.0,635676.0,226371.0",
                    "-ag",
                ],
                "return_code": 0,
                "run_time": 0.10032153129577637,
                "stderr": [""],
                "stdout": "East=638684\nNorth=220210\n\nMap=zipcodes_wake\n"
                "Mapset=PERMANENT\nType=Area\nSq_Meters=130875884.223\n"
                "Hectares=13087.588\nAcres=32340.135\nSq_Miles=50.5315\n"
                "Layer=1\nCategory=40\nDriver=sqlite\nDatabase=/actinia_core/"
                "workspace/temp_db/gisdbase_5ce6c4cf9b8f47628f816e89b7767819/"
                "nc_spm_08/PERMANENT/sqlite/sqlite.db\nTable=zipcodes_wake\n"
                "Key_column=cat\ncat=40\nOBJECTID=286\nWAKE_ZIPCO=12858700"
                "10.66\nPERIMETER=282815.79339\nZIPCODE_=37\nZIPCODE_ID=66\n"
                "ZIPNAME=RALEIGH\nZIPNUM=27603\nZIPCODE=RALEIGH_27603\nNAME="
                "RALEIGH\nSHAPE_Leng=285693.495599\nSHAPE_Area=1408742751.36"
                "\nEast=635676\nNorth=226371\n\nMap=zipcodes_wake\nMapset="
                "PERMANENT\nType=Area\nSq_Meters=63169356.527\nHectares="
                "6316.936\nAcres=15609.488\nSq_Miles=24.3898\nLayer=1\n"
                "Category=42\nDriver=sqlite\nDatabase=/actinia_core/workspace"
                "/temp_db/gisdbase_5ce6c4cf9b8f47628f816e89b7767819/nc_spm_08"
                "/PERMANENT/sqlite/sqlite.db\nTable=zipcodes_wake\nKey_column"
                "=cat\ncat=42\nOBJECTID=298\nWAKE_ZIPCO=829874917.625\n"
                "PERIMETER=230773.26059\nZIPCODE_=39\nZIPCODE_ID=2\nZIPNAME="
                "RALEIGH\nZIPNUM=27606\nZIPCODE=RALEIGH_27606\nNAME=RALEIGH\n"
                "SHAPE_Leng=212707.32257\nSHAPE_Area=679989401.948\n",
            },
        ],
        "process_results": [
            {
                "p1": {
                    "Acres": "32340.135",
                    "Category": "40",
                    "Database": "/tmp/gisdbase_5ce"
                    "6c4cf9b8f47628f816e89b7767819/nc_spm_08/PERMANENT/sqlite"
                    "/sqlite.db",
                    "Driver": "sqlite",
                    "East": "638684",
                    "Hectares": "13087.588",
                    "Key_column": "cat",
                    "Layer": "1",
                    "Map": "zipcodes_wake",
                    "Mapset": "PERMANENT",
                    "NAME": "RALEIGH",
                    "North": "220210",
                    "OBJECTID": "286",
                    "PERIMETER": "282815.79339",
                    "SHAPE_Area": "1408742751.36",
                    "SHAPE_Leng": "285693.495599",
                    "Sq_Meters": "130875884.223",
                    "Sq_Miles": "50.5315",
                    "Table": "zipcodes_wake",
                    "Type": "Area",
                    "WAKE_ZIPCO": "1285870010.66",
                    "ZIPCODE": "RALEIGH_27603",
                    "ZIPCODE_": "37",
                    "ZIPCODE_ID": "66",
                    "ZIPNAME": "RALEIGH",
                    "ZIPNUM": "27603",
                    "cat": "40",
                }
            },
            {
                "p2": {
                    "Acres": "15609.488",
                    "Category": "42",
                    "Database": "/tmp/gisdbase_5c"
                    "e6c4cf9b8f47628f816e89b7767819/nc_spm_08/PERMANENT/sqlite"
                    "/sqlite.db",
                    "Driver": "sqlite",
                    "East": "635676",
                    "Hectares": "6316.936",
                    "Key_column": "cat",
                    "Layer": "1",
                    "Map": "zipcodes_wake",
                    "Mapset": "PERMANENT",
                    "NAME": "RALEIGH",
                    "North": "226371",
                    "OBJECTID": "298",
                    "PERIMETER": "230773.26059",
                    "SHAPE_Area": "679989401.948",
                    "SHAPE_Leng": "212707.32257",
                    "Sq_Meters": "63169356.527",
                    "Sq_Miles": "24.3898",
                    "Table": "zipcodes_wake",
                    "Type": "Area",
                    "WAKE_ZIPCO": "829874917.625",
                    "ZIPCODE": "RALEIGH_27606",
                    "ZIPCODE_": "39",
                    "ZIPCODE_ID": "2",
                    "ZIPNAME": "RALEIGH",
                    "ZIPNUM": "27606",
                    "cat": "42",
                }
            },
        ],
        "progress": {"num_of_steps": 2, "step": 2},
        "resource_id": "resource_id-6527a077-a74d-4195-a44c-90a75692bd22",
        "status": "finished",
        "time_delta": 0.4863121509552002,
        "timestamp": 1647524504.4673853,
        "urls": {
            "resources": [],
            "status": f"http://localhost{URL_PREFIX}//resources/actinia-gdi/"
            "resource_id-6527a077-a74d-4195-a44c-90a75692bd22",
        },
        "user_id": "actinia-gdi",
    }

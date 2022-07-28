# -*- coding: utf-8 -*-
from flask_restful_swagger_2 import Schema
from copy import deepcopy
from actinia_core.models.response_models import ProcessingResponseModel
from actinia_api import URL_PREFIX

__license__ = "GPLv3"
__author__ = "Sören Gebbert, Markus Neteler"
__copyright__ = "Copyright 2016-present, Sören Gebbert, Markus Neteler and "
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
        "accept_datetime": "2018-05-04 22:02:42.503999",
        "accept_timestamp": 1525464162.5039973,
        "api_info": {
            "endpoint": "syncephemeralrasterareastatsresource",
            "method": "POST",
            "path": f"{URL_PREFIX}/locations/nc_spm_08/mapsets/PERMANENT/"
                    "raster_layers/landuse96_28m/area_stats_sync",
            "request_url": f"http://localhost{URL_PREFIX}/locations/nc_spm_08/"
            "mapsets/PERMANENT/raster_layers/landuse96_28m/area_stats_sync",
        },
        "datetime": "2018-05-04 22:02:43.014544",
        "http_code": 200,
        "message": "Processing successfully finished",
        "process_chain_list": [
            {
                "1": {
                    "inputs": {
                        "input": "/tmp/gisdbase_c9071ae8c7844743a40fc2f8649"
                        "11a69/.tmp/tmpfgs_4jur"
                    },
                    "module": "v.import",
                    "outputs": {"output": {"name": "polygon"}},
                    "superquiet": True,
                }
            },
            {
                "2": {
                    "flags": "p",
                    "inputs": {
                        "align": "landuse96_28m@PERMANENT",
                        "vector": "polygon",
                    },
                    "module": "g.region",
                },
                "3": {
                    "inputs": {"vector": "polygon"},
                    "module": "r.mask",
                    "superquiet": True,
                },
                "4": {
                    "flags": "acpl",
                    "inputs": {
                        "input": "landuse96_28m@PERMANENT",
                        "separator": "|",
                    },
                    "module": "r.stats",
                    "outputs": {
                        "output": {
                            "name": "/tmp/gisdbase_c9071ae8c7844743a40fc2f86"
                            "4911a69/.tmp/tmp00trsfwh"
                        }
                    },
                    "superquiet": True,
                },
            },
        ],
        "process_log": [
            {
                "executable": "v.import",
                "parameter": [
                    "input=/tmp/gisdbase_c9071ae8c7844743a40fc2f864911a69/"
                    ".tmp/tmpfgs_4jur",
                    "output=polygon",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.15042471885681152,
                "stderr": [
                    "WARNING: Width for column fid set to 255 (was "
                    "not specified by OGR), some strings may be "
                    "truncated!",
                    "",
                ],
                "stdout": "",
            },
            {
                "executable": "g.region",
                "parameter": [
                    "vector=polygon",
                    "align=landuse96_28m@PERMANENT",
                    "-p",
                ],
                "return_code": 0,
                "run_time": 0.050189971923828125,
                "stderr": [""],
                "stdout": "projection: 99 (Lambert Conformal Conic)\n"
                "zone:       0\n"
                "datum:      nad83\n"
                "ellipsoid:  a=6378137 es=0.006694380022900787\n"
                "north:      228527.25\n"
                "south:      214989.75\n"
                "west:       629980\n"
                "east:       645028\n"
                "nsres:      28.5\n"
                "ewres:      28.5\n"
                "rows:       475\n"
                "cols:       528\n"
                "cells:      250800\n",
            },
            {
                "executable": "r.mask",
                "parameter": ["vector=polygon", "--qq"],
                "return_code": 0,
                "run_time": 0.1504218578338623,
                "stderr": [""],
                "stdout": "",
            },
            {
                "executable": "r.stats",
                "parameter": [
                    "separator=|",
                    "input=landuse96_28m@PERMANENT",
                    "output=/tmp/gisdbase_c9071ae8c7844743a40fc2f864911a69/"
                    ".tmp/tmp00trsfwh",
                    "-acpl",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.050148725509643555,
                "stderr": [""],
                "stdout": "",
            },
        ],
        "process_results": [
            {
                "area": 812.25,
                "cat": "0",
                "cell_count": 1,
                "name": "not classified",
                "percent": 0.0,
            },
            {
                "area": 28297165.5,
                "cat": "1",
                "cell_count": 34838,
                "name": "High Intensity Developed",
                "percent": 13.89,
            },
            {
                "area": 30871185.75,
                "cat": "2",
                "cell_count": 38007,
                "name": "Low Intensity Developed",
                "percent": 15.16,
            },
            {
                "area": 1727655.75,
                "cat": "3",
                "cell_count": 2127,
                "name": "Cultivated",
                "percent": 0.85,
            },
            {
                "area": 20610843.75,
                "cat": "4",
                "cell_count": 25375,
                "name": "Managed Herbaceous Cover",
                "percent": 10.12,
            },
            {
                "area": 24367.5,
                "cat": "6",
                "cell_count": 30,
                "name": "Riverine/Estuarine Herbaceous",
                "percent": 0.01,
            },
            {
                "area": 13308716.25,
                "cat": "7",
                "cell_count": 16385,
                "name": "Evergreen Shrubland",
                "percent": 6.53,
            },
            {
                "area": 256671.0,
                "cat": "8",
                "cell_count": 316,
                "name": "Deciduous Shrubland",
                "percent": 0.13,
            },
            {
                "area": 36551.25,
                "cat": "9",
                "cell_count": 45,
                "name": "Mixed Shrubland",
                "percent": 0.02,
            },
            {
                "area": 6394032.0,
                "cat": "10",
                "cell_count": 7872,
                "name": "Mixed Hardwoods",
                "percent": 3.14,
            },
            {
                "area": 15972896.25,
                "cat": "11",
                "cell_count": 19665,
                "name": "Bottomland Hardwoods/Hardwood Swamps",
                "percent": 7.84,
            },
            {
                "area": 52401496.5,
                "cat": "15",
                "cell_count": 64514,
                "name": "Southern Yellow Pine",
                "percent": 25.72,
            },
            {
                "area": 27352518.75,
                "cat": "18",
                "cell_count": 33675,
                "name": "Mixed Hardwoods/Conifers",
                "percent": 13.43,
            },
            {
                "area": 4289492.25,
                "cat": "20",
                "cell_count": 5281,
                "name": "Water Bodies",
                "percent": 2.11,
            },
            {
                "area": 157576.5,
                "cat": "21",
                "cell_count": 194,
                "name": "Unconsolidated Sediment",
                "percent": 0.08,
            },
            {
                "area": 2010318.75,
                "cat": "*",
                "cell_count": 2475,
                "name": "no data",
                "percent": 0.99,
            },
        ],
        "progress": {"num_of_steps": 4, "step": 4},
        "resource_id": "resource_id-9757d66b-4986-4bc7-9b7d-7f985900fb20",
        "status": "finished",
        "time_delta": 0.5105781555175781,
        "timestamp": 1525464163.0145323,
        "urls": {
            "resources": [],
            "status": f"http://localhost{URL_PREFIX}/resources/admin/resource"
            "_id-9757d66b-4986-4bc7-9b7d-7f985900fb20",
        },
        "user_id": "admin",
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
        "accept_datetime": "2018-05-04 22:07:14.108967",
        "accept_timestamp": 1525464434.1089664,
        "api_info": {
            "endpoint": "syncephemeralrasterareastatsunivarresource",
            "method": "POST",
            "path": f"{URL_PREFIX}/locations/nc_spm_08/mapsets/PERMANENT/"
            "raster_layers/towns/area_stats_univar_sync",
            "request_url": f"http://localhost{URL_PREFIX}/locations/nc_spm_08/"
            "mapsets/PERMANENT/raster_layers/towns/area_stats_univar_sync",
        },
        "datetime": "2018-05-04 22:07:15.793146",
        "http_code": 200,
        "message": "Processing successfully finished",
        "process_chain_list": [
            {
                "1": {
                    "inputs": {
                        "input": "/tmp/gisdbase_d36dd6841e7446f3b8d3b1bf5adc"
                        "f527/.tmp/tmpdqtuzub4"
                    },
                    "module": "v.import",
                    "outputs": {"output": {"name": "polygon"}},
                    "superquiet": True,
                }
            },
            {
                "2": {
                    "flags": "p",
                    "inputs": {"vector": "polygon"},
                    "module": "g.region",
                },
                "3": {
                    "inputs": {
                        "column_prefix": "raster",
                        "map": "polygon",
                        "method": "number,minimum,maximum,range,average,"
                        "median,stddev,sum,variance,coeff_var",
                        "raster": "towns@PERMANENT",
                    },
                    "module": "v.rast.stats",
                    "superquiet": True,
                },
                "4": {
                    "inputs": {"map": "polygon"},
                    "module": "v.db.select",
                    "outputs": {
                        "file": {
                            "name": "/tmp/gisdbase_d36dd6841e7446f3b8d3b1bf5"
                            "adcf527/.tmp/tmpztw47z19"
                        }
                    },
                },
            },
        ],
        "process_log": [
            {
                "executable": "v.import",
                "parameter": [
                    "input=/tmp/gisdbase_d36dd6841e7446f3b8d3b1bf5adcf527/"
                    ".tmp/tmpdqtuzub4",
                    "output=polygon",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.1504511833190918,
                "stderr": [
                    "WARNING: Width for column fid set to 255 (was "
                    "not specified by OGR), some strings may be "
                    "truncated!",
                    "",
                ],
                "stdout": "",
            },
            {
                "executable": "g.region",
                "parameter": ["vector=polygon", "-p"],
                "return_code": 0,
                "run_time": 0.050218820571899414,
                "stderr": [""],
                "stdout": "projection: 99 (Lambert Conformal Conic)\n"
                "zone:       0\n"
                "datum:      nad83\n"
                "ellipsoid:  a=6378137 es=0.006694380022900787\n"
                "north:      228500\n"
                "south:      215000\n"
                "west:       630000\n"
                "east:       645000\n"
                "nsres:      500\n"
                "ewres:      500\n"
                "rows:       27\n"
                "cols:       30\n"
                "cells:      810\n",
            },
            {
                "executable": "v.rast.stats",
                "parameter": [
                    "raster=towns@PERMANENT",
                    "map=polygon",
                    "column_prefix=raster",
                    "method=number,minimum,maximum,range,average,median,stddev"
                    ",sum,variance,coeff_var",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 1.354858636856079,
                "stderr": [""],
                "stdout": "",
            },
            {
                "executable": "v.db.select",
                "parameter": [
                    "map=polygon",
                    "file=/tmp/gisdbase_d36dd6841e7446f3b8d3b1bf5adcf527/"
                    ".tmp/tmpztw47z19",
                ],
                "return_code": 0,
                "run_time": 0.05019712448120117,
                "stderr": [""],
                "stdout": "",
            },
        ],
        "process_results": [
            {
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
        ],
        "progress": {"num_of_steps": 4, "step": 4},
        "resource_id": "resource_id-ed2c2fdb-9963-4f71-acd0-1fbdff93f590",
        "status": "finished",
        "time_delta": 1.6842188835144043,
        "timestamp": 1525464435.7931283,
        "urls": {
            "resources": [],
            "status": f"http://localhost{URL_PREFIX}/resources/admin/resource"
            "_id-ed2c2fdb-9963-4f71-acd0-1fbdff93f590",
        },
        "user_id": "admin",
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
            "path": f"{URL_PREFIX}/locations/nc_spm_08/mapsets/PERMANENT/"
            "raster_layers/landuse96_28m/sampling_sync",
            "request_url": f"http://localhost{URL_PREFIX}/locations/nc_spm_08"
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
                                "value": "/actinia_core/workspace/temp_db/"
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
                                "value": "/actinia_core/workspace/temp_db/"
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
                    "input=/actinia_core/workspace/temp_db/gisdbase_3ef25f3f4"
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
                    "output=/actinia_core/workspace/temp_db/gisdbase_3ef25f3f4"
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
            "path": f"{URL_PREFIX}/locations/nc_spm_08/mapsets/PERMANENT/"
            "vector_layers/zipcodes_wake/sampling_sync",
            "request_url": f"http://localhost{URL_PREFIX}//locations/nc_spm_08"
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
                    "Database": "/actinia_core/workspace/temp_db/gisdbase_5ce"
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
                    "Database": "/actinia_core/workspace/temp_db/gisdbase_5c"
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

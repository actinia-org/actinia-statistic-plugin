# -*- coding: utf-8 -*-
from flask_restful_swagger_2 import Schema
from copy import deepcopy
from actinia_core.resources.common.response_models import ProcessingResponseModel

__license__ = "GPLv3"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2016, Sören Gebbert"
__maintainer__ = "Sören Gebbert"
__email__ = "soerengebbert@googlemail.com"


class UnivarResultModel(Schema):
    """Response schema for the result of univariate computations of raster layers.

    It is used as schema to define the process_result in a  ProcessingResponseModel.
    """
    type = 'object'
    properties = {
        'name': {
            'type': 'string',
            'description': 'The name of the raster resource'
        },
        'cells': {
            'type': 'number',
            'format': 'double',
        },
        'coeff_var': {
            'type': 'number',
            'format': 'double',
        },
        'max': {
            'type': 'number',
            'format': 'double',
        },
        'mean': {
            'type': 'number',
            'format': 'double',
        },
        'mean_of_abs': {
            'type': 'number',
            'format': 'double',
        },
        'min': {
            'type': 'number',
            'format': 'double',
        },
        'n': {
            'type': 'number',
            'format': 'double',
        },
        'null_cells': {
            'type': 'number',
            'format': 'double',
        },
        'range': {
            'type': 'number',
            'format': 'double',
        },
        'stddev': {
            'type': 'number',
            'format': 'double',
        },
        'sum': {
            'type': 'number',
            'format': 'double',
        },
        'variance': {
            'type': 'number',
            'format': 'double',
        }
    }
    # If a map is empty, r.univar will return nothing, hence no required variables
    # required = ['name', 'cells', 'coeff_var', 'max', 'mean', 'mean_of_abs',
    #            'min', 'n', 'null_cells', 'range', 'stddev', 'sum', 'variance']


class CategoricalStatisticsResultModel(Schema):
    """Response schema for the result of r.stats computations of raster layers.

    It is used as schema to define the process_result in a  ProcessingResponseModel.
    """
    type = 'object'
    required = ['cat', 'name', 'area', 'cell_count', 'percent']
    properties = {
        'cat': {
            'type': 'string',
            'description': 'The raster category'
        },
        'name': {
            'type': 'string',
            'description': 'The name of raster category'
        },
        'area': {
            'type': 'number',
            'format': 'double',
            'description': 'The size of the area in square meters'
        },
        'cell_count': {
            'type': 'number',
            'format': 'double',
            'description': 'The number of cells that have the raster category'
        },
        'percent': {
            'type': 'number',
            'format': 'double',
            'description': 'The percentage of the area'
        }
    }
    example = {
        "area": 812.25,
        "cat": "0",
        "cell_count": 1,
        "name": "not classified",
        "percent": 0.0
    }


class RasterAreaStatsResponseModel(ProcessingResponseModel):
    """Response schema for a list of categorical statistics
    """
    type = 'object'
    properties = deepcopy(ProcessingResponseModel.properties)
    properties["process_results"] = {}
    properties["process_results"]["type"] = "array"
    properties["process_results"]["items"] = CategoricalStatisticsResultModel
    required = deepcopy(ProcessingResponseModel.required)
    example = {
        'accept_datetime': '2018-05-04 22:02:42.503999',
        'accept_timestamp': 1525464162.5039973,
        'api_info': {'endpoint': 'syncephemeralrasterareastatsresource',
                     'method': 'POST',
                     'path': '/locations/nc_spm_08/mapsets/PERMANENT/raster_layers/landuse96_28m/area_stats_sync',
                     'request_url': 'http://localhost/locations/nc_spm_08/mapsets/PERMANENT/raster_layers/landuse96_28m/area_stats_sync'},
        'datetime': '2018-05-04 22:02:43.014544',
        'http_code': 200,
        'message': 'Processing successfully finished',
        'process_chain_list': [
            {'1': {'inputs': {'input': '/tmp/gisdbase_c9071ae8c7844743a40fc2f864911a69/.tmp/tmpfgs_4jur'},
                   'module': 'v.import',
                   'outputs': {'output': {'name': 'polygon'}},
                   'superquiet': True}},
            {'2': {'flags': 'p',
                   'inputs': {'align': 'landuse96_28m@PERMANENT',
                              'vector': 'polygon'},
                   'module': 'g.region'},
             '3': {'inputs': {'vector': 'polygon'},
                   'module': 'r.mask',
                   'superquiet': True},
             '4': {'flags': 'acpl',
                   'inputs': {'input': 'landuse96_28m@PERMANENT',
                              'separator': '|'},
                   'module': 'r.stats',
                   'outputs': {
                       'output': {'name': '/tmp/gisdbase_c9071ae8c7844743a40fc2f864911a69/.tmp/tmp00trsfwh'}},
                   'superquiet': True}}],
        'process_log': [{'executable': 'v.import',
                         'parameter': ['input=/tmp/gisdbase_c9071ae8c7844743a40fc2f864911a69/.tmp/tmpfgs_4jur',
                                       'output=polygon',
                                       '--qq'],
                         'return_code': 0,
                         'run_time': 0.15042471885681152,
                         'stderr': ['WARNING: Width for column fid set to 255 (was '
                                    'not specified by OGR), some strings may be '
                                    'truncated!',
                                    ''],
                         'stdout': ''},
                        {'executable': 'g.region',
                         'parameter': ['vector=polygon',
                                       'align=landuse96_28m@PERMANENT',
                                       '-p'],
                         'return_code': 0,
                         'run_time': 0.050189971923828125,
                         'stderr': [''],
                         'stdout': 'projection: 99 (Lambert Conformal Conic)\n'
                                   'zone:       0\n'
                                   'datum:      nad83\n'
                                   'ellipsoid:  a=6378137 es=0.006694380022900787\n'
                                   'north:      228527.25\n'
                                   'south:      214989.75\n'
                                   'west:       629980\n'
                                   'east:       645028\n'
                                   'nsres:      28.5\n'
                                   'ewres:      28.5\n'
                                   'rows:       475\n'
                                   'cols:       528\n'
                                   'cells:      250800\n'},
                        {'executable': 'r.mask',
                         'parameter': ['vector=polygon', '--qq'],
                         'return_code': 0,
                         'run_time': 0.1504218578338623,
                         'stderr': [''],
                         'stdout': ''},
                        {'executable': 'r.stats',
                         'parameter': ['separator=|',
                                       'input=landuse96_28m@PERMANENT',
                                       'output=/tmp/gisdbase_c9071ae8c7844743a40fc2f864911a69/.tmp/tmp00trsfwh',
                                       '-acpl',
                                       '--qq'],
                         'return_code': 0,
                         'run_time': 0.050148725509643555,
                         'stderr': [''],
                         'stdout': ''}],
        'process_results': [{'area': 812.25,
                             'cat': '0',
                             'cell_count': 1,
                             'name': 'not classified',
                             'percent': 0.0},
                            {'area': 28297165.5,
                             'cat': '1',
                             'cell_count': 34838,
                             'name': 'High Intensity Developed',
                             'percent': 13.89},
                            {'area': 30871185.75,
                             'cat': '2',
                             'cell_count': 38007,
                             'name': 'Low Intensity Developed',
                             'percent': 15.16},
                            {'area': 1727655.75,
                             'cat': '3',
                             'cell_count': 2127,
                             'name': 'Cultivated',
                             'percent': 0.85},
                            {'area': 20610843.75,
                             'cat': '4',
                             'cell_count': 25375,
                             'name': 'Managed Herbaceous Cover',
                             'percent': 10.12},
                            {'area': 24367.5,
                             'cat': '6',
                             'cell_count': 30,
                             'name': 'Riverine/Estuarine Herbaceous',
                             'percent': 0.01},
                            {'area': 13308716.25,
                             'cat': '7',
                             'cell_count': 16385,
                             'name': 'Evergreen Shrubland',
                             'percent': 6.53},
                            {'area': 256671.0,
                             'cat': '8',
                             'cell_count': 316,
                             'name': 'Deciduous Shrubland',
                             'percent': 0.13},
                            {'area': 36551.25,
                             'cat': '9',
                             'cell_count': 45,
                             'name': 'Mixed Shrubland',
                             'percent': 0.02},
                            {'area': 6394032.0,
                             'cat': '10',
                             'cell_count': 7872,
                             'name': 'Mixed Hardwoods',
                             'percent': 3.14},
                            {'area': 15972896.25,
                             'cat': '11',
                             'cell_count': 19665,
                             'name': 'Bottomland Hardwoods/Hardwood Swamps',
                             'percent': 7.84},
                            {'area': 52401496.5,
                             'cat': '15',
                             'cell_count': 64514,
                             'name': 'Southern Yellow Pine',
                             'percent': 25.72},
                            {'area': 27352518.75,
                             'cat': '18',
                             'cell_count': 33675,
                             'name': 'Mixed Hardwoods/Conifers',
                             'percent': 13.43},
                            {'area': 4289492.25,
                             'cat': '20',
                             'cell_count': 5281,
                             'name': 'Water Bodies',
                             'percent': 2.11},
                            {'area': 157576.5,
                             'cat': '21',
                             'cell_count': 194,
                             'name': 'Unconsolidated Sediment',
                             'percent': 0.08},
                            {'area': 2010318.75,
                             'cat': '*',
                             'cell_count': 2475,
                             'name': 'no data',
                             'percent': 0.99}],
        'progress': {'num_of_steps': 4, 'step': 4},
        'resource_id': 'resource_id-9757d66b-4986-4bc7-9b7d-7f985900fb20',
        'status': 'finished',
        'time_delta': 0.5105781555175781,
        'timestamp': 1525464163.0145323,
        'urls': {'resources': [],
                 'status': 'http://localhost/resources/admin/resource_id-9757d66b-4986-4bc7-9b7d-7f985900fb20'},
        'user_id': 'admin'
    }


class AreaUnivarResultModel(Schema):
    """Response schema for the result of univariate computations of raster layers
    based on a vector area.

    It is used as schema to define the process_result in a  ProcessingResponseModel.

    cat
    fid
    raster_number
    raster_minimum
    raster_maximum
    raster_range
    raster_average
    raster_median
    raster_stddev
    raster_sum
    raster_variance
    raster_coeff_var

    """
    type = 'object'
    properties = {
        'fid': {
            'type': 'string',
            'description': 'Field id from the polygon of the vector map layer used for area stats computation'
        },
        'cat': {
            'type': 'string',
            'description': 'The category id from the polygon of the vector map layer used for area stats computation'
        },
        'raster_number': {
            'type': 'number',
            'format': 'double',
        },
        'raster_minimum': {
            'type': 'number',
            'format': 'double',
        },
        'raster_maximum': {
            'type': 'number',
            'format': 'double',
        },
        'raster_range': {
            'type': 'number',
            'format': 'double',
        },
        'raster_average': {
            'type': 'number',
            'format': 'double',
        },
        'raster_median': {
            'type': 'number',
            'format': 'double',
        },
        'raster_stddev': {
            'type': 'number',
            'format': 'double',
        },
        'raster_sum': {
            'type': 'number',
            'format': 'double',
        },
        'raster_variance': {
            'type': 'number',
            'format': 'double',
        },
        'raster_coeff_var': {
            'type': 'number',
            'format': 'double',
        }
    }
    example = {'cat': '1',
               'fid': 'swwake_10m.0',
               'raster_average': 4.27381481481481,
               'raster_coeff_var': 36.2154244540989,
               'raster_maximum': 6.0,
               'raster_median': 5.0,
               'raster_minimum': 1.0,
               'raster_number': 2025000.0,
               'raster_range': 5.0,
               'raster_stddev': 1.54778017556735,
               'raster_sum': 8654475.0,
               'raster_variance': 2.39562347187929}


class RasterAreaUnivarStatsResponseModel(ProcessingResponseModel):
    """Response schema for resources that generate area univariate result lists
     as processing results.
    """
    type = 'object'
    properties = deepcopy(ProcessingResponseModel.properties)
    properties["process_results"] = {}
    properties["process_results"]["type"] = "array"
    properties["process_results"]["items"] = AreaUnivarResultModel
    required = deepcopy(ProcessingResponseModel.required)
    # required.append("process_results")
    example = {
        'accept_datetime': '2018-05-04 22:07:14.108967',
        'accept_timestamp': 1525464434.1089664,
        'api_info': {'endpoint': 'syncephemeralrasterareastatsunivarresource',
                     'method': 'POST',
                     'path': '/locations/nc_spm_08/mapsets/PERMANENT/raster_layers/towns/area_stats_univar_sync',
                     'request_url': 'http://localhost/locations/nc_spm_08/mapsets/PERMANENT/raster_layers/towns/area_stats_univar_sync'},
        'datetime': '2018-05-04 22:07:15.793146',
        'http_code': 200,
        'message': 'Processing successfully finished',
        'process_chain_list': [
            {'1': {'inputs': {'input': '/tmp/gisdbase_d36dd6841e7446f3b8d3b1bf5adcf527/.tmp/tmpdqtuzub4'},
                   'module': 'v.import',
                   'outputs': {'output': {'name': 'polygon'}},
                   'superquiet': True}},
            {'2': {'flags': 'p',
                   'inputs': {'vector': 'polygon'},
                   'module': 'g.region'},
             '3': {'inputs': {'column_prefix': 'raster',
                              'map': 'polygon',
                              'method': 'number,minimum,maximum,range,average,median,stddev,sum,variance,coeff_var',
                              'raster': 'towns@PERMANENT'},
                   'module': 'v.rast.stats',
                   'superquiet': True},
             '4': {'inputs': {'map': 'polygon'},
                   'module': 'v.db.select',
                   'outputs': {'file': {'name': '/tmp/gisdbase_d36dd6841e7446f3b8d3b1bf5adcf527/.tmp/tmpztw47z19'}}}}],
        'process_log': [{'executable': 'v.import',
                         'parameter': ['input=/tmp/gisdbase_d36dd6841e7446f3b8d3b1bf5adcf527/.tmp/tmpdqtuzub4',
                                       'output=polygon',
                                       '--qq'],
                         'return_code': 0,
                         'run_time': 0.1504511833190918,
                         'stderr': ['WARNING: Width for column fid set to 255 (was '
                                    'not specified by OGR), some strings may be '
                                    'truncated!',
                                    ''],
                         'stdout': ''},
                        {'executable': 'g.region',
                         'parameter': ['vector=polygon', '-p'],
                         'return_code': 0,
                         'run_time': 0.050218820571899414,
                         'stderr': [''],
                         'stdout': 'projection: 99 (Lambert Conformal Conic)\n'
                                   'zone:       0\n'
                                   'datum:      nad83\n'
                                   'ellipsoid:  a=6378137 es=0.006694380022900787\n'
                                   'north:      228500\n'
                                   'south:      215000\n'
                                   'west:       630000\n'
                                   'east:       645000\n'
                                   'nsres:      500\n'
                                   'ewres:      500\n'
                                   'rows:       27\n'
                                   'cols:       30\n'
                                   'cells:      810\n'},
                        {'executable': 'v.rast.stats',
                         'parameter': ['raster=towns@PERMANENT',
                                       'map=polygon',
                                       'column_prefix=raster',
                                       'method=number,minimum,maximum,range,average,median,stddev,sum,variance,coeff_var',
                                       '--qq'],
                         'return_code': 0,
                         'run_time': 1.354858636856079,
                         'stderr': [''],
                         'stdout': ''},
                        {'executable': 'v.db.select',
                         'parameter': ['map=polygon',
                                       'file=/tmp/gisdbase_d36dd6841e7446f3b8d3b1bf5adcf527/.tmp/tmpztw47z19'],
                         'return_code': 0,
                         'run_time': 0.05019712448120117,
                         'stderr': [''],
                         'stdout': ''}],
        'process_results': [{'cat': '1',
                             'fid': 'swwake_10m.0',
                             'raster_average': 4.27381481481481,
                             'raster_coeff_var': 36.2154244540989,
                             'raster_maximum': 6.0,
                             'raster_median': 5.0,
                             'raster_minimum': 1.0,
                             'raster_number': 2025000.0,
                             'raster_range': 5.0,
                             'raster_stddev': 1.54778017556735,
                             'raster_sum': 8654475.0,
                             'raster_variance': 2.39562347187929}],
        'progress': {'num_of_steps': 4, 'step': 4},
        'resource_id': 'resource_id-ed2c2fdb-9963-4f71-acd0-1fbdff93f590',
        'status': 'finished',
        'time_delta': 1.6842188835144043,
        'timestamp': 1525464435.7931283,
        'urls': {'resources': [],
                 'status': 'http://localhost/resources/admin/resource_id-ed2c2fdb-9963-4f71-acd0-1fbdff93f590'},
        'user_id': 'admin'
    }

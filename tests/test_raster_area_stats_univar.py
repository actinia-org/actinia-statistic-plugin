# -*- coding: utf-8 -*-
import unittest
import time
from pprint import pprint
from flask.json import loads as json_load
from flask.json import dumps as json_dump
try:
    from .test_resource_base import ActiniaResourceTestCaseBase, URL_PREFIX
except:
    from test_resource_base import ActiniaResourceTestCaseBase, URL_PREFIX


__license__ = "GPLv3"
__author__     = "Sören Gebbert"
__copyright__  = "Copyright 2016, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__      = "soerengebbert@googlemail.com"


JSON = {
"type": "FeatureCollection",
"crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:EPSG::3358" } },
"features": [
{ "type": "Feature", "properties": { "fid": "swwake_10m.0" }, "geometry": { "type": "Polygon", "coordinates": [ [ [ 630000.0, 215000.0 ], [ 630000.0, 228500.0 ], [ 645000.0, 228500.0 ], [ 645000.0, 215000.0 ], [ 630000.0, 215000.0 ] ] ] } }
]
}


class RasterAreaStatsTestCase(ActiniaResourceTestCaseBase):

    # def test_async_raster_area_stats_json(self):
    #     rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/mapsets/PERMANENT/raster_layers/elevation/'
    #                           'area_stats_univar_async',
    #                           headers=self.admin_auth_header,
    #                           data=json_dump(JSON),
    #                           content_type="application/json")
    #
    #     import pdb; pdb.set_trace()
    #     rv = self.waitAsyncStatusAssertHTTP(rv, headers=self.admin_auth_header)
    #
    #     value_list = rv["process_results"]
    #     import pdb; pdb.set_trace()
    #     self.assertEqual(value_list[0]["cat"], "1")
    #     self.assertEqual(value_list[0]["raster_number"], 2025000)

    def test_sync_raster_area_stats_1(self):

        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/mapsets/PERMANENT/raster_layers/elevation/'
                              'area_stats_univar_sync',
                              headers=self.admin_auth_header,
                              data=json_dump(JSON),
                              content_type="application/json")

        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 200, "HTML status code is wrong %i"%rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s"%rv.mimetype)

        value_list = json_load(rv.data)["process_results"]
        self.assertEqual(value_list[0]["cat"], "1")
        self.assertEqual(value_list[0]["raster_number"], 2025000)

    def test_sync_raster_area_stats_2(self):

        import pdb; pdb.set_trace()
        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/mapsets/PERMANENT/raster_layers/towns/'
                              'area_stats_univar_sync',
                              headers=self.admin_auth_header,
                              data=json_dump(JSON),
                              content_type="application/json")

        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 200, "HTML status code is wrong %i"%rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s"%rv.mimetype)

        value_list = json_load(rv.data)["process_results"]
        self.assertEqual(value_list[0]["cat"], "1")
        self.assertEqual(value_list[0]["raster_number"], 2025000)

    #################### ERRORS ###############################################

    def test_sync_raster_area_stats_error_wrong_content_type(self):
        import pdb; pdb.set_trace()

        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/mapsets/PERMANENT/raster_layers/towns/'
                              'area_stats_univar_sync',
                              headers=self.admin_auth_header,
                              data=" This is no data",
                              content_type="application/XML")

        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 400, "HTML status code is wrong %i"%rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s"%rv.mimetype)

    def test_sync_raster_area_stats_module_error(self):
        import pdb; pdb.set_trace()
        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/mapsets/PERMANENT/raster_layers/towns/'
                              'area_stats_univar_sync',
                              headers=self.admin_auth_header,
                              data=json_dump({}),
                              content_type="application/json")

        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 400, "HTML status code is wrong %i"%rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s"%rv.mimetype)

    def test_sync_raster_area_stats_nodata_error(self):
        import pdb; pdb.set_trace()
        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/mapsets/PERMANENT/raster_layers/towns/'
                              'area_stats_univar_sync',
                              headers=self.admin_auth_header,
                              data=None,
                              content_type="application/json")

        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 400, "HTML status code is wrong %i"%rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s"%rv.mimetype)


if __name__ == '__main__':
    unittest.main()

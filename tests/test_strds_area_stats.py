# -*- coding: utf-8 -*-
import unittest
import time
from pprint import pprint
from flask.json import loads as json_load
from flask.json import dumps as json_dump

try:
    from .test_resource_base import ActiniaResourceTestCaseBase
except:
    from test_resource_base import ActiniaResourceTestCaseBase

__license__ = "GPLv3"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2016, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

JSON = {
    "type": "FeatureCollection",
    "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
    "features": [
        {"type": "Feature", "properties": {"fid": "ecad_area.0"}, "geometry": {"type": "Polygon", "coordinates": [
            [[7.756, 52.298157894736846], [11.986947368421044, 51.657105263157924],
             [9.550947368421047, 48.580052631578958], [6.345684210526304, 48.836473684210539],
             [7.756, 52.298157894736846]]]}}
    ]
}


class STRDSAreaStatsTestCase(ActiniaResourceTestCaseBase):

    def test_async_raster_area_stats_json(self):
        rv = self.server.post('/locations/ECAD/mapsets/PERMANENT/strds/'
                              'temperature_mean_1950_2013_yearly_celsius/'
                              'timestamp/2001-01-01T00:00:00/'
                              'area_stats_async',
                              headers=self.admin_auth_header,
                              data=json_dump(JSON),
                              content_type="application/json")

        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 200, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)

        data = self.waitAsyncStatusAssertHTTP(rv, headers=self.admin_auth_header)

        self.assertEqual(len(data["process_results"]), 29)

    def test_sync_raster_area_stats_1(self):
        rv = self.server.post('/locations/ECAD/mapsets/PERMANENT/strds/'
                              'temperature_mean_1950_2013_yearly_celsius/'
                              'timestamp/2001-01-01T00:00:00/'
                              'area_stats_sync',
                              headers=self.admin_auth_header,
                              data=json_dump(JSON),
                              content_type="application/json")

        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 200, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)

        value_list = json_load(rv.data)["process_results"]
        self.assertEqual(len(value_list), 29)

    def test_sync_raster_area_stats_2(self):
        rv = self.server.post('/locations/ECAD/mapsets/PERMANENT/strds/'
                              'temperature_mean_1950_2013_yearly_celsius/'
                              'timestamp/2001-01-01T00:00:00/'
                              'area_stats_sync',
                              headers=self.admin_auth_header,
                              data=json_dump(JSON),
                              content_type="application/json")

        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 200, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)

        value_list = json_load(rv.data)["process_results"]
        self.assertEqual(len(value_list), 29)

    #################### ERRORS ###############################################

    def test_sync_raster_area_stats_error_no_map_found(self):
        rv = self.server.post('/locations/ECAD/mapsets/PERMANENT/strds/'
                              'temperature_mean_1950_2013_yearly_celsius/'
                              'timestamp/2021-01-01T00:00:00/'
                              'area_stats_sync',
                              headers=self.admin_auth_header,
                              data=json_dump(JSON),
                              content_type="application/json")

        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 400, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)

    def test_sync_raster_area_stats_wrong_content_type(self):
        rv = self.server.post('/locations/ECAD/mapsets/PERMANENT/strds/'
                              'temperature_mean_1950_2013_yearly_celsius/'
                              'timestamp/2001-01-01T00:00:00/'
                              'area_stats_sync',
                              headers=self.admin_auth_header,
                              data=" This is no data",
                              content_type="application/XML")

        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 400, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)

    def test_sync_raster_area_stats_error_nodata(self):
        rv = self.server.post('/locations/ECAD/mapsets/PERMANENT/strds/'
                              'temperature_mean_1950_2013_yearly_celsius/'
                              'timestamp/2001-01-01T00:00:00/'
                              'area_stats_sync',
                              headers=self.admin_auth_header,
                              data=json_dump({}),
                              content_type="application/json")

        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 400, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)

    def test_sync_raster_area_stats_error(self):
        rv = self.server.post('/locations/ECAD/mapsets/PERMANENT/strds/'
                              'temperature_mean_1950_2013_yearly_celsius/'
                              'timestamp/2001-01-01T00:00:00/'
                              'area_stats_sync',
                              headers=self.admin_auth_header,
                              data=None,
                              content_type="application/json")

        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 400, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)

    def test_sync_raster_area_stats_error_wrong_timestamp(self):
        rv = self.server.post('/locations/ECAD/mapsets/PERMANENT/strds/'
                              'temperature_mean_1950_2013_yearly_celsius/'
                              'timestamp/2001-01-01T00.00.00/'
                              'area_stats_sync',
                              headers=self.admin_auth_header,
                              data=json_dump(JSON),
                              content_type="application/json")

        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 400, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)


if __name__ == '__main__':
    unittest.main()

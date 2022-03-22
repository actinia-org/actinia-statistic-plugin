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
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2016, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

# TODO use modis data
LOCATION = "nc_spm_08"
MAPSET = "modis_lst"
STRDS = "LST_Day_monthly"

JSON = {
    "type": "FeatureCollection",
    "crs": {"type": "name", "properties": {
        "name": "urn:ogc:def:crs:EPSG::3358"}},
    "features": [
        {"type": "Feature", "properties": {"fid": "test"}, "geometry": {
            "type": "Polygon", "coordinates": [
                [[349852.196963928756304, 252507.816825738176703],
                 [349852.196963928756304, 244101.739720351994038],
                 [361635.941179184708744, 244101.739720351994038],
                 [361635.941179184708744, 252507.816825738176703],
                 [349852.196963928756304, 252507.816825738176703]]]}}
    ]
}


# class STRDSAreaStatsTestCase(ActiniaResourceTestCaseBase):

    # def test_async_raster_area_stats_json(self):
    #     rv = self.server.post(
    #         f"{URL_PREFIX}/locations/{LOCATION}/mapsets/{MAPSET}/strds/"
    #         f"{STRDS}/timestamp/2016-01-01T00:00:00/area_stats_async",
    #         headers=self.admin_auth_header,
    #         data=json_dump(JSON),
    #         content_type="application/json")
    #
    #     pprint(json_load(rv.data))
    #     self.assertEqual(rv.status_code, 200, "HTML status code is wrong %i" % rv.status_code)
    #     self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)
    #
    #     data = self.waitAsyncStatusAssertHTTP(rv, headers=self.admin_auth_header)
    #
    #     self.assertEqual(len(data["process_results"]), 29)

    # def test_sync_raster_area_stats_1(self):
    #     rv = self.server.post(
    #         f"{URL_PREFIX}/locations/{LOCATION}/mapsets/{MAPSET}/strds/"
    #         f"{STRDS}/timestamp/2016-01-01T00:00:00/area_stats_sync",
    #         headers=self.admin_auth_header,
    #         data=json_dump(JSON),
    #         content_type="application/json")
    #
    #     pprint(json_load(rv.data))
    #     self.assertEqual(rv.status_code, 200, "HTML status code is wrong %i" % rv.status_code)
    #     self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)
    #
    #     value_list = json_load(rv.data)["process_results"]
    #     self.assertEqual(len(value_list), 29)

    # def test_sync_raster_area_stats_2(self):
    #     rv = self.server.post(
    #         f"{URL_PREFIX}/locations/{LOCATION}/mapsets/{MAPSET}/strds/"
    #         f"{STRDS}/timestamp/2016-01-01T00:00:00/area_stats_sync",
    #     # URL_PREFIX + '/locations/ECAD/mapsets/PERMANENT/strds/'
    #     #                       'temperature_mean_1950_2013_yearly_celsius/'
    #     #                       'timestamp/2001-01-01T00:00:00/'
    #     #                       'area_stats_sync',
    #         headers=self.admin_auth_header,
    #         data=json_dump(JSON),
    #         content_type="application/json")
    #
    #     pprint(json_load(rv.data))
    #     self.assertEqual(rv.status_code, 200, "HTML status code is wrong %i" % rv.status_code)
    #     self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)
    #
    #     value_list = json_load(rv.data)["process_results"]
    #     self.assertEqual(len(value_list), 29)

    #################### ERRORS ###############################################

    # def test_sync_raster_area_stats_error_no_map_found(self):
    #     rv = self.server.post(URL_PREFIX + '/locations/ECAD/mapsets/PERMANENT/strds/'
    #                           'temperature_mean_1950_2013_yearly_celsius/'
    #                           'timestamp/2021-01-01T00:00:00/'
    #                           'area_stats_sync',
    #                           headers=self.admin_auth_header,
    #                           data=json_dump(JSON),
    #                           content_type="application/json")
    #
    #     pprint(json_load(rv.data))
    #     self.assertEqual(rv.status_code, 400, "HTML status code is wrong %i" % rv.status_code)
    #     self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)
    #
    # def test_sync_raster_area_stats_wrong_content_type(self):
    #     rv = self.server.post(URL_PREFIX + '/locations/ECAD/mapsets/PERMANENT/strds/'
    #                           'temperature_mean_1950_2013_yearly_celsius/'
    #                           'timestamp/2001-01-01T00:00:00/'
    #                           'area_stats_sync',
    #                           headers=self.admin_auth_header,
    #                           data=" This is no data",
    #                           content_type="application/XML")
    #
    #     pprint(json_load(rv.data))
    #     self.assertEqual(rv.status_code, 400, "HTML status code is wrong %i" % rv.status_code)
    #     self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)
    #
    # def test_sync_raster_area_stats_error_nodata(self):
    #     rv = self.server.post(URL_PREFIX + '/locations/ECAD/mapsets/PERMANENT/strds/'
    #                           'temperature_mean_1950_2013_yearly_celsius/'
    #                           'timestamp/2001-01-01T00:00:00/'
    #                           'area_stats_sync',
    #                           headers=self.admin_auth_header,
    #                           data=json_dump({}),
    #                           content_type="application/json")
    #
    #     pprint(json_load(rv.data))
    #     self.assertEqual(rv.status_code, 400, "HTML status code is wrong %i" % rv.status_code)
    #     self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)
    #
    # def test_sync_raster_area_stats_error(self):
    #     rv = self.server.post(URL_PREFIX + '/locations/ECAD/mapsets/PERMANENT/strds/'
    #                           'temperature_mean_1950_2013_yearly_celsius/'
    #                           'timestamp/2001-01-01T00:00:00/'
    #                           'area_stats_sync',
    #                           headers=self.admin_auth_header,
    #                           data=None,
    #                           content_type="application/json")
    #
    #     pprint(json_load(rv.data))
    #     self.assertEqual(rv.status_code, 400, "HTML status code is wrong %i" % rv.status_code)
    #     self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)
    #
    # def test_sync_raster_area_stats_error_wrong_timestamp(self):
    #     rv = self.server.post(URL_PREFIX + '/locations/ECAD/mapsets/PERMANENT/strds/'
    #                           'temperature_mean_1950_2013_yearly_celsius/'
    #                           'timestamp/2001-01-01T00.00.00/'
    #                           'area_stats_sync',
    #                           headers=self.admin_auth_header,
    #                           data=json_dump(JSON),
    #                           content_type="application/json")
    #
    #     pprint(json_load(rv.data))
    #     self.assertEqual(rv.status_code, 400, "HTML status code is wrong %i" % rv.status_code)
    #     self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)


if __name__ == '__main__':
    unittest.main()

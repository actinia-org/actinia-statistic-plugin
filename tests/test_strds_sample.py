# -*- coding: utf-8 -*-
import unittest
# import time
# from pprint import pprint
# from flask.json import loads as json_load
# from flask.json import dumps as json_dump
#
# try:
#     from .test_resource_base import ActiniaResourceTestCaseBase, URL_PREFIX
# except Exception:
#     from test_resource_base import ActiniaResourceTestCaseBase, URL_PREFIX


__license__ = "GPLv3"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2016, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

# TODO use modis data
LOCATION = "nc_spm_08"
MAPSET = "modis_lst"
STRDS = "LST_Day_monthly"

# TODO change coordinates
JSON = {
    "type": "FeatureCollection",
    "crs": {
        "type": "name",
        "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"},
    },
    "features": [
        {
            "type": "Feature",
            "properties": {"cat": 1},
            "geometry": {
                "type": "Point",
                "coordinates": [-5.095406, 38.840583],
            },
        },
        {
            "type": "Feature",
            "properties": {"cat": 2},
            "geometry": {
                "type": "Point",
                "coordinates": [9.9681980, 51.666166],
            },
        },
        {
            "type": "Feature",
            "properties": {"cat": 3},
            "geometry": {
                "type": "Point",
                "coordinates": [24.859647, 52.699099],
            },
        },
    ],
}


"""
class STRDSTestCase(ActiniaResourceTestCaseBase):
    def test_async_sampling(self):

        rv = self.server.post(
            f"{URL_PREFIX}/locations/ECAD/mapsets/PERMANENT/strds/"
            "temperature_mean_1950_2013_yearly_celsius/sampling_async",
            headers=self.user_auth_header,
            data=json_dump(
                {
                    "points": [
                        ["a", "-5.095406", "38.840583"],
                        ["b", "9.9681980", "51.666166"],
                        ["c", "24.859647", "52.699099"],
                    ]
                }
            ),
            content_type="application/json",
        )

        pprint(json_load(rv.data))
        self.assertEqual(
            rv.status_code,
            200,
            "HTML status code is wrong %i" % rv.status_code,
        )
        self.assertEqual(
            rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype
        )

        resp = json_load(rv.data)

        rv_user_id = resp["user_id"]
        rv_resource_id = resp["resource_id"]

        while True:
            rv = self.server.get(
                URL_PREFIX + "/resources/%s/%s" % (rv_user_id, rv_resource_id),
                headers=self.user_auth_header,
            )
            resp = json_load(rv.data)
            if resp["status"] == "finished" or resp["status"] == "error":
                break
            time.sleep(0.2)

        self.assertEquals(resp["status"], "finished")
        self.assertEqual(
            rv.status_code,
            200,
            "HTML status code is wrong %i" % rv.status_code,
        )

        value_list = json_load(rv.data)["process_results"]

        self.assertEqual(value_list[0][0], "start_time")
        self.assertEqual(value_list[0][1], "end_time")
        self.assertEqual(value_list[0][2], "a")
        self.assertEqual(value_list[0][3], "b")
        self.assertEqual(value_list[0][4], "c")

        time.sleep(1)

    def test_sync_sampling(self):

        rv = self.server.post(
            f"{URL_PREFIX}/locations/ECAD/mapsets/PERMANENT/strds/"
            "temperature_mean_1950_2013_yearly_celsius/sampling_sync",
            headers=self.user_auth_header,
            data=json_dump(
                {
                    "points": [
                        ["a", "-5.095406", "38.840583"],
                        ["b", "9.9681980", "51.666166"],
                        ["c", "24.859647", "52.699099"],
                    ]
                }
            ),
            content_type="application/json",
        )

        pprint(json_load(rv.data))
        self.assertEqual(
            rv.status_code,
            200,
            "HTML status code is wrong %i" % rv.status_code,
        )
        self.assertEqual(
            rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype
        )

        value_list = json_load(rv.data)["process_results"]

        self.assertEqual(value_list[0][0], "start_time")
        self.assertEqual(value_list[0][1], "end_time")
        self.assertEqual(value_list[0][2], "a")
        self.assertEqual(value_list[0][3], "b")
        self.assertEqual(value_list[0][4], "c")

        time.sleep(1)

    def test_sync_sampling_geojson(self):

        rv = self.server.post(
            f"{URL_PREFIX}/locations/ECAD/mapsets/PERMANENT/strds/"
            "temperature_mean_1950_2013_yearly_celsius/sampling_sync_geojson",
            headers=self.user_auth_header,
            data=json_dump(JSON),
            content_type="application/json",
        )

        pprint(json_load(rv.data))
        self.assertEqual(
            rv.status_code,
            200,
            "HTML status code is wrong %i" % rv.status_code,
        )
        self.assertEqual(
            rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype
        )

        value_list = json_load(rv.data)["process_results"]

        self.assertEqual(value_list[0][0], "start_time")
        self.assertEqual(value_list[0][1], "end_time")
        self.assertEqual(value_list[0][2], "1")
        self.assertEqual(value_list[0][3], "2")
        self.assertEqual(value_list[0][4], "3")

    def test_sync_sampling_where(self):

        rv = self.server.post(
            f"{URL_PREFIX}/locations/ECAD/mapsets/PERMANENT/strds/"
            "temperature_mean_1950_2013_yearly_celsius/sampling_sync",
            headers=self.user_auth_header,
            data=json_dump(
                {
                    "points": [
                        ["a", "-5.095406", "38.840583"],
                        ["b", "9.9681980", "51.666166"],
                        ["c", "24.859647", "52.699099"],
                    ],
                    "where": "start_time >'2010-01-01'",
                }
            ),
            content_type="application/json",
        )

        pprint(json_load(rv.data))
        self.assertEqual(
            rv.status_code,
            200,
            "HTML status code is wrong %i" % rv.status_code,
        )
        self.assertEqual(
            rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype
        )

        value_list = json_load(rv.data)["process_results"]

        self.assertEqual(value_list[0][0], "start_time")
        self.assertEqual(value_list[0][1], "end_time")
        self.assertEqual(value_list[0][2], "a")
        self.assertEqual(value_list[0][3], "b")
        self.assertEqual(value_list[0][4], "c")
"""


if __name__ == "__main__":
    unittest.main()

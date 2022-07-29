# -*- coding: utf-8 -*-
import unittest
import time
from flask.json import loads as json_load
from flask.json import dumps as json_dump

try:
    from .test_resource_base import ActiniaResourceTestCaseBase, URL_PREFIX
except Exception:
    from test_resource_base import ActiniaResourceTestCaseBase, URL_PREFIX


__license__ = "GPLv3"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2016, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

LOCATION = "nc_spm_08"
MAPSET = "modis_lst"
STRDS = "LST_Day_monthly"

JSON = {
    "type": "FeatureCollection",
    "crs": {
        "type": "name",
        "properties": {"name": "urn:x-ogc:def:crs:EPSG:3358"}
    },
    "features": [
        {
            "type": "Feature",
            "properties": {"cat": 1},
            "geometry": {"type": "Point", "coordinates": [330000.0, 65000.0]}
        },
        {
            "type": "Feature",
            "properties": {"cat": 2},
            "geometry": {"type": "Point", "coordinates": [500000.0, 500000.0]}
        }
    ]
}
POINT_LIST = [
    ["a", "330000.0", "65000.0"],
    ["b", "300000.0", "60000.0"],
    ["c", "500000.0", "500000.0"],
]
WHERE = "start_time >'2016-01-01'"


class STRDSTestCase(ActiniaResourceTestCaseBase):
    def test_async_sampling(self):

        url = f"{URL_PREFIX}/locations/{LOCATION}/mapsets/{MAPSET}/strds/" \
            f"{STRDS}/sampling_async"

        rv = self.server.post(
            url,
            headers=self.user_auth_header,
            data=json_dump({"points": POINT_LIST}),
            content_type="application/json",
        )

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

        url = f"{URL_PREFIX}/locations/{LOCATION}/mapsets/{MAPSET}/strds/" \
            f"{STRDS}/sampling_sync"
        rv = self.server.post(
            url,
            headers=self.user_auth_header,
            data=json_dump({"points": POINT_LIST}),
            content_type="application/json",
        )

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

    def test_sync_sampling_where(self):

        url = f"{URL_PREFIX}/locations/{LOCATION}/mapsets/{MAPSET}/strds/" \
            f"{STRDS}/sampling_sync"
        rv = self.server.post(
            url,
            headers=self.user_auth_header,
            data=json_dump(
                {
                    "points": POINT_LIST,
                    "where": WHERE,
                }
            ),
            content_type="application/json",
        )

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

    def test_sync_sampling_geojson(self):

        url = f"{URL_PREFIX}/locations/{LOCATION}/mapsets/{MAPSET}/strds/" \
            f"{STRDS}/sampling_sync_geojson"
        rv = self.server.post(
            url,
            headers=self.user_auth_header,
            data=json_dump(JSON),
            content_type="application/json",
        )

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


if __name__ == "__main__":
    unittest.main()

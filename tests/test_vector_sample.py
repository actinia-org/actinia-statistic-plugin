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
__author__ = "Sören Gebbert, Markus Neteler"
__copyright__ = "Copyright 2016-present, Sören Gebbert and mundialis GmbH & Co. KG"

JSON = {
    "type": "FeatureCollection",
    "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
    "features": [
        {
            "type": "Feature",
            "properties": {"cat": 1},
            "geometry": {"type": "Point", "coordinates": [638684.0, 220210.0]},
        },
        {
            "type": "Feature",
            "properties": {"cat": 2},
            "geometry": {"type": "Point", "coordinates": [635676.0, 226371.0]},
        },
    ],
}


class RasterTestCase(ActiniaResourceTestCaseBase):

    # ################### Raster SAMPLING ###################################

    def test_async_sampling(self):

        rv = self.server.post(
            URL_PREFIX
            + "/locations/nc_spm_08/mapsets/PERMANENT/vector_layers/zipcodes_wake/"
            "sampling_async",
            headers=self.user_auth_header,
            data=json_dump(
                {
                    "points": [
                        ["a", "638684.0", "220210.0"],
                        ["b", "635676.0", "226371.0"],
                    ]
                }
            ),
            content_type="application/json",
        )

        pprint(json_load(rv.data))
        self.assertEqual(
            rv.status_code, 200, "HTML status code is wrong %i" % rv.status_code
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
            print(rv.data)
            resp = json_load(rv.data)
            if resp["status"] == "finished" or resp["status"] == "error":
                break
            time.sleep(0.2)

        self.assertEquals(resp["status"], "finished")
        self.assertEqual(
            rv.status_code, 200, "HTML status code is wrong %i" % rv.status_code
        )

        value_list = json_load(rv.data)["process_results"]

        self.assertEqual(value_list[0][0], "easting")
        self.assertEqual(value_list[0][1], "northing")
        self.assertEqual(value_list[0][2], "site_name")
        self.assertEqual(value_list[0][3], "zipcodes_wake")
        self.assertEqual(value_list[0][4], "zipcodes_wake_label")
        self.assertEqual(value_list[0][5], "zipcodes_wake_color")

        time.sleep(1)

    def test_sync_sampling(self):

        rv = self.server.post(
            URL_PREFIX
            + "/locations/nc_spm_08/mapsets/PERMANENT/vector_layers/zipcodes_wake/"
            "sampling_sync",
            headers=self.user_auth_header,
            data=json_dump(
                {
                    "points": [
                        ["p1", "638684.0", "220210.0"],
                        ["p2", "635676.0", "226371.0"],
                    ]
                }
            ),
            content_type="application/json",
        )

        pprint(json_load(rv.data))
        self.assertEqual(
            rv.status_code, 200, "HTML status code is wrong %i" % rv.status_code
        )
        self.assertEqual(
            rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype
        )

        value_list = json_load(rv.data)["process_results"]

        self.assertIn("East", value_list["p1"])
        self.assertIn("North", value_list["p2"])
        self.assertIn("ZIPCODE", value_list["p2"])
        self.assertEqual(value_list["p2"]["ZIPCODE"], "RALEIGH_27606")

        time.sleep(1)


#    def test_sync_sampling_geojson(self):
#
#        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/mapsets/PERMANENT/vector_layers/zipcodes_wake/'
#                              'sampling_sync_geojson',
#                              headers=self.user_auth_header,
#                              data=json_dump(JSON),
#                              content_type="application/json")
#
#        pprint(json_load(rv.data))
#        self.assertEqual(rv.status_code, 200, "HTML status code is wrong %i"%rv.status_code)
#        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s"%rv.mimetype)
#
#        value_list = json_load(rv.data)["process_results"]
#
#        self.assertEqual(value_list[0][0], "easting")
#        self.assertEqual(value_list[0][1], "northing")
#        self.assertEqual(value_list[0][2], "site_name")
#        self.assertEqual(value_list[0][3], "zipcodes_wake")
#        self.assertEqual(value_list[0][4], "zipcodes_wake_label")
#        self.assertEqual(value_list[0][5], "zipcodes_wake_color")


if __name__ == "__main__":
    unittest.main()

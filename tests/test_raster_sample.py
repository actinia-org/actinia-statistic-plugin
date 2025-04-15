# -*- coding: utf-8 -*-
import unittest
import time
from flask.json import loads as json_load
from flask.json import dumps as json_dump

try:
    from .test_resource_base import ActiniaResourceTestCaseBase, URL_PREFIX
except Exception:
    from test_resource_base import ActiniaResourceTestCaseBase, URL_PREFIX

from actinia_core.version import init_versions, G_VERSION

__license__ = "GPLv3"
__author__ = "Markus Neteler"
__copyright__ = (
    "Copyright 2022-2022, Markus Neteler and mundialis GmbH & Co. KG"
)

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

    project_url_part = "projects"
    # set project_url_part to "locations" if GRASS GIS version < 8.4
    init_versions()
    grass_version_s = G_VERSION["version"]
    grass_version = [int(item) for item in grass_version_s.split(".")[:2]]
    if grass_version < [8, 4]:
        project_url_part = "locations"

    def test_async_sampling(self):

        rv = self.server.post(
            f"{URL_PREFIX}/{self.project_url_part}/nc_spm_08/mapsets/PERMANENT"
            "/raster_layers/landuse96_28m/sampling_async",
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

        self.assertEqual(resp["status"], "finished", "Process not finished.")
        self.assertEqual(
            rv.status_code,
            200,
            "HTML status code is wrong %i" % rv.status_code,
        )

        value_list = json_load(rv.data)["process_results"]

        self.assertIn("p1", value_list[0], "'p1' not in process_results")
        self.assertIn("p2", value_list[1], "'p2' not in process_results")
        self.assertIn("easting", value_list[0]["p1"])
        self.assertIn("northing", value_list[0]["p1"])
        self.assertIn("map_name", value_list[0]["p1"])
        self.assertIn("label", value_list[0]["p1"])
        self.assertIn("value", value_list[0]["p1"])
        self.assertIn("color", value_list[0]["p1"])
        self.assertEqual(value_list[0]["p1"]["map_name"], "landuse96_28m")

        time.sleep(1)

    def test_sync_sampling(self):
        # PROBLEM: Not yet returned!

        rv = self.server.post(
            f"{URL_PREFIX}/{self.project_url_part}/nc_spm_08/mapsets/PERMANENT"
            "/raster_layers/landuse96_28m/sampling_sync",
            headers=self.user_auth_header,
            data=json_dump({"points": [["p1", "638684.0", "220210.0"],
                                       ["p2", "635676.0", "226371.0"]]}),
            content_type="application/json")

        self.assertEqual(
            rv.status_code, 200, "HTML status code is wrong %i"
            % rv.status_code)
        self.assertEqual(
            rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)

        value_list = json_load(rv.data)["process_results"]

        self.assertIn("p1", value_list[0], "'p1' not in process_results")
        self.assertIn("p2", value_list[1], "'p2' not in process_results")
        self.assertIn("easting", value_list[0]["p1"])
        self.assertIn("northing", value_list[0]["p1"])
        self.assertIn("map_name", value_list[0]["p1"])
        self.assertIn("label", value_list[0]["p1"])
        self.assertIn("value", value_list[0]["p1"])
        self.assertIn("color", value_list[0]["p1"])
        self.assertEqual(value_list[0]["p1"]["map_name"], "landuse96_28m")

        time.sleep(1)


if __name__ == "__main__":
    unittest.main()

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
__author__ = "Sören Gebbert, Anika Weinmann"
__copyright__ = "Copyright 2016-2022, Sören Gebbert and mundialis GmbH & Co.KG"
__maintainer__ = "mundialis GmbH & Co. KG"

PROJECT = "nc_spm_08"
MAPSET = "PERMANENT"
RASTER = "landuse96_28m"
RASTER2 = "basin_50K"
JSON = {
    "type": "FeatureCollection",
    "crs": {
        "type": "name",
        "properties": {"name": "urn:ogc:def:crs:EPSG::3358"},
    },
    "features": [
        {
            "type": "Feature",
            "properties": {"fid": "swwake_10m.0"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [630000.0, 215000.0],
                        [630000.0, 228500.0],
                        [645000.0, 228500.0],
                        [645000.0, 215000.0],
                        [630000.0, 215000.0],
                    ]
                ],
            },
        }
    ],
}


class RasterAreaStatsTestCase(ActiniaResourceTestCaseBase):

    project_url_part = "projects"
    # set project_url_part to "locations" if GRASS GIS version < 8.4
    init_versions()
    grass_version_s = G_VERSION["version"]
    grass_version = [int(item) for item in grass_version_s.split(".")[:2]]
    if grass_version < [8, 4]:
        project_url_part = "locations"

    def test_async_raster_area_stats_json(self):
        rv = self.server.post(
            f"{URL_PREFIX}/{self.project_url_part}/{PROJECT}/mapsets/{MAPSET}"
            f"/raster_layers/{RASTER}/area_stats_async",
            headers=self.admin_auth_header,
            data=json_dump(JSON),
            content_type="application/json",
        )

        rv = self.waitAsyncStatusAssertHTTP(rv, headers=self.admin_auth_header)

        self.assertEqual(len(rv["process_results"]), 16)

        time.sleep(1)

    def test_sync_raster_area_stats_1(self):
        rv = self.server.post(
            f"{URL_PREFIX}/{self.project_url_part}/{PROJECT}/mapsets/{MAPSET}"
            f"/raster_layers/{RASTER}/area_stats_sync",
            headers=self.admin_auth_header,
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
        self.assertEqual(len(value_list), 16)

    def test_sync_raster_area_stats_2(self):

        rv = self.server.post(
            f"{URL_PREFIX}/{self.project_url_part}/{PROJECT}/mapsets/{MAPSET}"
            f"/raster_layers/{RASTER2}/area_stats_sync",
            headers=self.admin_auth_header,
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
        self.assertEqual(len(value_list), 16)

    def test_sync_raster_area_stats_error_wrong_content_type(self):
        rv = self.server.post(
            f"{URL_PREFIX}/{self.project_url_part}/{PROJECT}/mapsets/{MAPSET}"
            f"/raster_layers/{RASTER}/area_stats_sync",
            headers=self.admin_auth_header,
            data="{}",
            content_type="application/json",
        )

        self.assertEqual(
            rv.status_code,
            400,
            "HTML status code is wrong %i" % rv.status_code,
        )
        self.assertEqual(
            rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype
        )

    def test_sync_raster_area_stats_error_wrong_request_missing_json(self):
        rv = self.server.post(
            f"{URL_PREFIX}/{self.project_url_part}/{PROJECT}/mapsets/{MAPSET}"
            f"/raster_layers/{RASTER}/area_stats_sync",
            headers=self.admin_auth_header,
            data=None,
            content_type="application/json",
        )

        self.assertEqual(
            rv.status_code,
            400,
            "HTML status code is wrong %i" % rv.status_code,
        )
        self.assertEqual(
            rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype
        )


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
import unittest
# import time
from flask.json import loads as json_load
from flask.json import dumps as json_dump

try:
    from .test_resource_base import ActiniaResourceTestCaseBase, URL_PREFIX
except Exception:
    from test_resource_base import ActiniaResourceTestCaseBase, URL_PREFIX

from actinia_core.version import init_versions, G_VERSION

__license__ = "GPLv3"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2016, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

# TODO use modis data
PROJECT = "nc_spm_08"
MAPSET = "modis_lst"
STRDS = "LST_Day_monthly"
TIMESTAMP = "2016-01-01T00:00:00"

# TODO change coordinates
JSON = {
    "type": "FeatureCollection",
    "crs": {
        "type": "name",
        "properties": {"name": "urn:x-ogc:def:crs:EPSG:3358"},
    },
    "features": [
        {
            "type": "Feature",
            "properties": {"fid": "ecad_area.0"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [330000.0, 65000.0],
                        [331000.0, 65000.0],
                        [331000.0, 649000.0],
                        [330000.0, 649000.0],
                        [330000.0, 65000.0],
                    ]
                ],
            },
        }
    ],
}


class STRDSAreaStatsUnivarTestCase(ActiniaResourceTestCaseBase):

    project_url_part = "projects"
    # set project_url_part to "locations" if GRASS GIS version < 8.4
    init_versions()
    grass_version_s = G_VERSION["version"]
    grass_version = [int(item) for item in grass_version_s.split(".")[:2]]
    if grass_version < [8, 4]:
        project_url_part = "locations"

    def test_async_raster_area_stats_json(self):
        rv = self.server.post(
            URL_PREFIX + f"/{self.project_url_part}/{PROJECT}/mapsets/{MAPSET}"
            f"/strds/{STRDS}/timestamp/{TIMESTAMP}/"
            "area_stats_univar_async",
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

        value_list = self.waitAsyncStatusAssertHTTP(
            rv, headers=self.admin_auth_header
        )["process_results"]
        self.assertEqual(value_list[0]["cat"], "1")
        self.assertEqual(value_list[0]["raster_maximum"], 13781.)
        self.assertEqual(value_list[0]["raster_number"], 1.0)

    def test_sync_raster_area_stats_1(self):
        rv = self.server.post(
            URL_PREFIX + f"/{self.project_url_part}/{PROJECT}/mapsets/{MAPSET}"
            f"/strds/{STRDS}/timestamp/{TIMESTAMP}/"
            "area_stats_univar_sync",
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
        self.assertEqual(value_list[0]["cat"], "1")
        self.assertEqual(value_list[0]["raster_maximum"], 13781.)
        self.assertEqual(value_list[0]["raster_number"], 1.0)

    def test_sync_raster_area_stats_2(self):
        rv = self.server.post(
            URL_PREFIX + f"/{self.project_url_part}/{PROJECT}/mapsets/{MAPSET}"
            f"/strds/{STRDS}/timestamp/{TIMESTAMP}/"
            "area_stats_univar_sync",
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
        self.assertEqual(value_list[0]["cat"], "1")
        self.assertEqual(value_list[0]["raster_maximum"], 13781.)
        self.assertEqual(value_list[0]["raster_number"], 1.0)

    def test_sync_raster_area_stats_error_no_map_found(self):
        rv = self.server.post(
            URL_PREFIX + f"/{self.project_url_part}/{PROJECT}/mapsets/{MAPSET}"
            f"/strds/{STRDS}/timestamp/{TIMESTAMP}/"
            "area_stats_univar_sync",
            headers=self.admin_auth_header,
            data=None,
            content_type="text/XML",
        )

        self.assertEqual(
            rv.status_code,
            400,
            "HTML status code is wrong %i" % rv.status_code,
        )
        self.assertEqual(
            rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype
        )

    def test_sync_raster_area_stats_module_error(self):
        rv = self.server.post(
            URL_PREFIX + f"/{self.project_url_part}/{PROJECT}/mapsets/{MAPSET}"
            f"/strds/{STRDS}/timestamp/{TIMESTAMP}/"
            "area_stats_univar_sync",
            headers=self.admin_auth_header,
            data=json_dump({}),
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

    def test_sync_raster_area_stats_error_nodata(self):
        rv = self.server.post(
            URL_PREFIX + f"/{self.project_url_part}/{PROJECT}/mapsets/{MAPSET}"
            f"/strds/{STRDS}/timestamp/{TIMESTAMP}/"
            "area_stats_univar_sync",
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

    def test_sync_raster_area_stats_error_wrong_timestamp(self):
        rv = self.server.post(
            URL_PREFIX + f"/{self.project_url_part}/{PROJECT}/mapsets/{MAPSET}"
            f"/strds/{STRDS}/timestamp/2001-01-01T00.00.00/"
            "area_stats_univar_sync",
            headers=self.admin_auth_header,
            data=json_dump(JSON),
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

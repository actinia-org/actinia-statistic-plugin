# -*- coding: utf-8 -*-
import unittest
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
RASTER = "elevation"
RASTER2 = "aspect"
JSON = {
    "type": "FeatureCollection",
    "crs": {
        "type": "name",
        "properties": {"name": "urn:x-ogc:def:crs:EPSG:3358"}
    },
    "features": [
        {
            "type": "Feature",
            "properties": {"fid": "test"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [635000.0, 220000.0],
                        [637000.0, 220000.0],
                        [637000.0, 221000.0],
                        [635000.0, 221000.0],
                        [635000.0, 220000.0]
                    ]
                ]
            }
        }
    ]
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
            f"{URL_PREFIX}/{self.project_url_part}/{PROJECT}/mapsets/{MAPSET}/"
            f"raster_layers/{RASTER}/area_stats_univar_async",
            headers=self.admin_auth_header,
            data=json_dump(JSON),
            content_type="application/json",
        )

        rv = self.waitAsyncStatusAssertHTTP(rv, headers=self.admin_auth_header)

        value_list = rv["process_results"]

        self.assertEqual(value_list[0]["cat"], "1")
        self.assertEqual(value_list[0]["raster_number"], 20000.0)
        self.assertEqual(value_list[0]["raster_maximum"], 138.268508911133)

    def test_sync_raster_area_stats_1(self):

        rv = self.server.post(
            f"{URL_PREFIX}/{self.project_url_part}/{PROJECT}/mapsets/{MAPSET}/"
            f"raster_layers/{RASTER}/area_stats_univar_sync",
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
        self.assertEqual(value_list[0]["raster_number"], 20000.0)
        self.assertEqual(value_list[0]["raster_maximum"], 138.268508911133)

    def test_sync_raster_area_stats_2(self):

        rv = self.server.post(
            f"{URL_PREFIX}/{self.project_url_part}/{PROJECT}/mapsets/{MAPSET}/"
            f"raster_layers/{RASTER2}/area_stats_univar_sync",
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
        self.assertEqual(value_list[0]["raster_number"], 20000.0)
        self.assertEqual(value_list[0]["raster_maximum"], 359.995971679688)

    def test_sync_raster_area_stats_error_wrong_content_type(self):

        rv = self.server.post(
            f"{URL_PREFIX}/{self.project_url_part}/{PROJECT}/mapsets/{MAPSET}/"
            f"raster_layers/{RASTER}/area_stats_univar_sync",
            headers=self.admin_auth_header,
            data=" This is no data",
            content_type="application/XML",
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
            f"{URL_PREFIX}/{self.project_url_part}/{PROJECT}/mapsets/{MAPSET}/"
            f"raster_layers/{RASTER}/area_stats_univar_sync",
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

    def test_sync_raster_area_stats_nodata_error(self):
        rv = self.server.post(
            f"{URL_PREFIX}/{self.project_url_part}/{PROJECT}/mapsets/{MAPSET}/"
            f"raster_layers/{RASTER}/area_stats_univar_sync",
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

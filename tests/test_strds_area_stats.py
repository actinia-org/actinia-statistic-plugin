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
            "properties": {"fid": "test"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [330000.0, 65000.0],
                        [337000.0, 65000.0],
                        [337000.0, 647000.0],
                        [330000.0, 647000.0],
                        [330000.0, 65000.0],
                    ]
                ],
            },
        }
    ],
}

PROJECT_URL_PART = "projects"
# set project_url_part to "locations" if GRASS GIS version < 8.4
init_versions()
GRASS_VERSION_S = G_VERSION["version"]
GRASS_VERSION = [int(item) for item in GRASS_VERSION_S.split(".")[:2]]
if GRASS_VERSION < [8, 4]:
    PROJECT_URL_PART = "locations"

TIMESTAMP = "2016-01-01T00:00:00"
BASE_URL = f"{URL_PREFIX}/{PROJECT_URL_PART}/{PROJECT}/mapsets/{MAPSET}" \
    f"/strds/{STRDS}/timestamp/{TIMESTAMP}"
ASYNC_URL = f"{BASE_URL}/area_stats_async"
SYNC_URL = f"{BASE_URL}/area_stats_sync"


class STRDSAreaStatsTestCase(ActiniaResourceTestCaseBase):

    def test_async_raster_area_stats_json(self):

        rv = self.server.post(
            ASYNC_URL,
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

        data = self.waitAsyncStatusAssertHTTP(
            rv, headers=self.admin_auth_header
        )

        self.assertEqual(len(data["process_results"]), 93)

    def test_sync_raster_area_stats_1(self):

        rv = self.server.post(
            SYNC_URL,
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
        self.assertEqual(len(value_list), 93)

    def test_sync_raster_area_stats_2(self):

        rv = self.server.post(
            SYNC_URL,
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
        self.assertEqual(len(value_list), 93)

    def test_sync_raster_area_stats_error_no_map_found(self):

        newer_timestamp = "2021-01-01T00:00:00"
        rv = self.server.post(
            SYNC_URL.replace(TIMESTAMP, newer_timestamp),
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

    def test_sync_raster_area_stats_wrong_content_type(self):

        rv = self.server.post(
            SYNC_URL,
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

    def test_sync_raster_area_stats_error_nodata(self):
        rv = self.server.post(
            SYNC_URL,
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

    def test_sync_raster_area_stats_error(self):
        rv = self.server.post(
            SYNC_URL,
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

        wrong_timestamp = "2016-01-01T00.00.00"
        rv = self.server.post(
            SYNC_URL.replace(TIMESTAMP, wrong_timestamp),
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

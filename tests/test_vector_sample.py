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
__author__ = "Markus Neteler, Anika Weinmann"
__copyright__ = (
    "Copyright 2016-present, Markus Neteler and mundialis GmbH & Co. KG"
)

LOCATION = "nc_spm_08"
MAPSET = "PERMANENT"
VECTOR = "nc_state"

POINTS_LIST = [
    ["p1", "638684.0", "220210.0"],
    ["p2", "635676.0", "226371.0"],
]


class VectorTestCase(ActiniaResourceTestCaseBase):
    def test_async_sampling(self):

        url = f"{URL_PREFIX}/locations/{LOCATION}/mapsets/{MAPSET}/" \
            f"vector_layers/{VECTOR}/sampling_async"
        rv = self.server.post(
            url,
            headers=self.user_auth_header,
            data=json_dump({"points": POINTS_LIST}),
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

        self.assertEqual(resp["status"], "finished", resp)
        self.assertEqual(
            rv.status_code,
            200,
            "HTML status code is wrong %i" % rv.status_code,
        )

        value_list = json_load(rv.data)["process_results"]

        self.assertIn("East", value_list[0]["p1"])
        self.assertIn("North", value_list[1]["p2"])
        self.assertIn("STATE", value_list[1]["p2"])
        self.assertEqual(value_list[1]["p2"]["STATE"], "NORTH_CAROLINA")

        time.sleep(1)

    def test_sync_sampling(self):

        url = f"{URL_PREFIX}/locations/{LOCATION}/mapsets/{MAPSET}/" \
            f"vector_layers/{VECTOR}/sampling_sync"
        rv = self.server.post(
            url,
            headers=self.user_auth_header,
            data=json_dump({"points": POINTS_LIST}),
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

        self.assertIn("East", value_list[0]["p1"])
        self.assertIn("North", value_list[1]["p2"])
        self.assertIn("STATE", value_list[1]["p2"])
        self.assertEqual(value_list[1]["p2"]["STATE"], "NORTH_CAROLINA")

        time.sleep(1)


if __name__ == "__main__":
    unittest.main()

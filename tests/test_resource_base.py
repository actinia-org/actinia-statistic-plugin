# -*- coding: utf-8 -*-

"""
Tests: Actinia statistic plugin resource test case base
"""
import atexit
import os
import signal
import time
from flask_restful import Api
from actinia_core.testsuite import ActiniaTestCaseBase, URL_PREFIX
from actinia_core.core.common.config import global_config
from actinia_core.core.common.app import flask_api
from actinia_statistic_plugin.endpoints import create_endpoints
from actinia_core.endpoints import create_endpoints as create_actinia_endpoints

__license__ = "GPLv3"
__author__ = "Sören Gebbert"
__copyright__ = (
    "Copyright 2016-2022, Sören Gebbert and mundialis GmbH & Co. KG"
)
__maintainer__ = "mundialis GmbH & Co. KG"

kvdb_pid = None
server_test = False
custom_actinia_cfg = False

# Create endpoints
create_actinia_endpoints()
create_endpoints(flask_api)

# If this environmental variable is set, then a real http request will be send
# instead of using the flask test_client.
if "ACTINIA_SERVER_TEST" in os.environ:
    server_test = bool(os.environ["ACTINIA_SERVER_TEST"])
# Set this variable to use a actinia config file in a docker container
if "ACTINIA_CUSTOM_TEST_CFG" in os.environ:
    custom_actinia_cfg = str(os.environ["ACTINIA_CUSTOM_TEST_CFG"])


def setup_environment():
    global kvdb_pid
    # Set the port to the test kvdb server
    global_config.KVDB_SERVER_SERVER = "localhost"
    global_config.KVDB_SERVER_PORT = 7000
    # Set the path to kvdb WORKER_LOGFILE
    # global_config.WORKER_LOGFILE = "/var/log/valkey/valkey"

    # home = os.getenv("HOME")

    # GRASS GIS
    # Setup the test environment
    global_config.GRASS_GIS_BASE = "/usr/local/grass/"
    global_config.GRASS_GIS_START_SCRIPT = "/usr/local/bin/grass"
    # global_config.GRASS_DATABASE= "/usr/local/grass_test_db"
    # global_config.GRASS_DATABASE = "%s/actinia/grass_test_db" % home
    global_config.GRASS_TMP_DATABASE = "/tmp"

    if server_test is False and custom_actinia_cfg is False:
        # Start the kvdb server for user and logging management
        kvdb_pid = os.spawnl(
            os.P_NOWAIT,
            "/usr/bin/valkey-server",
            "common/valkey.conf",
            "--port %i" % global_config.KVDB_SERVER_PORT,
        )
        time.sleep(1)

    if server_test is False and custom_actinia_cfg is not False:
        global_config.read(custom_actinia_cfg)


def stop_kvdb():
    if server_test is False:
        global kvdb_pid
        # Kill th kvdb server
        if kvdb_pid is not None:
            os.kill(kvdb_pid, signal.SIGTERM)


# Register the kvdb stop function
atexit.register(stop_kvdb)
# Setup the environment
setup_environment()


class ActiniaResourceTestCaseBase(ActiniaTestCaseBase):
    pass

#!flask/bin/python
# -*- coding: utf-8 -*-
"""SPDX-FileCopyrightText: (c) 2016-2025 mundialis GmbH & Co. KG

SPDX-License-Identifier: GPL-3.0-or-later

Actinia statistic plugin endpoint definitions.
"""

from flask_restful_swagger_2 import Resource

from .ephemeral_strds_area_stats_univar import (
    AsyncEphemeralSTRDSAreaStatsUnivarResource,
    SyncEphemeralSTRDSAreaStatsUnivarResource,
)
from .ephemeral_strds_area_stats import (
    AsyncEphemeralSTRDSAreaStatsResource,
    SyncEphemeralSTRDSAreaStatsResource,
)
from .ephemeral_raster_area_stats import (
    AsyncEphemeralRasterAreaStatsResource,
    SyncEphemeralRasterAreaStatsResource,
)
from .ephemeral_raster_area_stats_univar import (
    AsyncEphemeralRasterAreaStatsUnivarResource,
    SyncEphemeralRasterAreaStatsUnivarResource,
)
from .strds_sampling import (
    AsyncEphemeralSTRDSSamplingResource,
    SyncEphemeralSTRDSSamplingResource,
)
from .strds_sampling_geojson import (
    AsyncEphemeralSTRDSSamplingGeoJSONResource,
    SyncEphemeralSTRDSSamplingGeoJSONResource,
)
from .raster_sampling import (
    AsyncEphemeralRasterSamplingResource,
    SyncEphemeralRasterSamplingResource,
)
from .vector_sampling import (
    AsyncEphemeralVectorSamplingResource,
    SyncEphemeralVectorSamplingResource,
)

__license__ = "GPL-3.0-or-later"
__author__ = "Sören Gebbert, Markus Neteler"
__copyright__ = (
    "Copyright 2016-2025, Sören Gebbert and mundialis GmbH & Co. KG"
)


def get_endpoint_class_name(endpoint_class: Resource) -> str:
    """Create the name for the given endpoint class."""
    return endpoint_class.__name__.lower()


def project_and_location_routes(path: str):
    """Return project and deprecated location routes for the same endpoint."""
    return (
        f"/projects{path}",
        f"/locations{path}",
    )


def create_project_endpoints(flask_api):
    """
    Function to add resources with "projects" inside the endpoint url.
    Args:
        flask_api (flask_restful_swagger_2.Api): Flask api.
    """
    flask_api.add_resource(
        AsyncEphemeralSTRDSAreaStatsUnivarResource,
        *project_and_location_routes(
            "/<string:project_name>/mapsets/"
            "<string:mapset_name>/strds/"
            "<string:strds_name>/timestamp/"
            "<string:timestamp>/area_stats_univar_async"
        ),
        endpoint=get_endpoint_class_name(
            AsyncEphemeralSTRDSAreaStatsUnivarResource
        ),
    )
    flask_api.add_resource(
        SyncEphemeralSTRDSAreaStatsUnivarResource,
        *project_and_location_routes(
            "/<string:project_name>/mapsets/"
            "<string:mapset_name>/strds/"
            "<string:strds_name>/timestamp/"
            "<string:timestamp>/area_stats_univar_sync"
        ),
        endpoint=get_endpoint_class_name(
            SyncEphemeralSTRDSAreaStatsUnivarResource
        ),
    )
    flask_api.add_resource(
        AsyncEphemeralSTRDSAreaStatsResource,
        *project_and_location_routes(
            "/<string:project_name>/mapsets/"
            "<string:mapset_name>/strds/<string:strds_name>"
            "/timestamp/<string:timestamp>/area_stats_async"
        ),
        endpoint=get_endpoint_class_name(AsyncEphemeralSTRDSAreaStatsResource),
    )
    flask_api.add_resource(
        SyncEphemeralSTRDSAreaStatsResource,
        *project_and_location_routes(
            "/<string:project_name>/mapsets/"
            "<string:mapset_name>/strds/<string:strds_name>"
            "/timestamp/<string:timestamp>/area_stats_sync"
        ),
        endpoint=get_endpoint_class_name(SyncEphemeralSTRDSAreaStatsResource),
    )
    flask_api.add_resource(
        AsyncEphemeralRasterAreaStatsResource,
        *project_and_location_routes(
            "/<string:project_name>/mapsets/"
            "<string:mapset_name>/raster_layers/"
            "<string:raster_name>/area_stats_async"
        ),
        endpoint=get_endpoint_class_name(
            AsyncEphemeralRasterAreaStatsResource
        ),
    )
    flask_api.add_resource(
        SyncEphemeralRasterAreaStatsResource,
        *project_and_location_routes(
            "/<string:project_name>/mapsets/"
            "<string:mapset_name>/raster_layers/"
            "<string:raster_name>/area_stats_sync"
        ),
        endpoint=get_endpoint_class_name(SyncEphemeralRasterAreaStatsResource),
    )
    flask_api.add_resource(
        AsyncEphemeralRasterAreaStatsUnivarResource,
        *project_and_location_routes(
            "/<string:project_name>/mapsets/"
            "<string:mapset_name>/raster_layers/"
            "<string:raster_name>"
            "/area_stats_univar_async"
        ),
        endpoint=get_endpoint_class_name(
            AsyncEphemeralRasterAreaStatsUnivarResource
        ),
    )
    flask_api.add_resource(
        SyncEphemeralRasterAreaStatsUnivarResource,
        *project_and_location_routes(
            "/<string:project_name>/mapsets/"
            "<string:mapset_name>/raster_layers/"
            "<string:raster_name>"
            "/area_stats_univar_sync"
        ),
        endpoint=get_endpoint_class_name(
            SyncEphemeralRasterAreaStatsUnivarResource
        ),
    )
    flask_api.add_resource(
        AsyncEphemeralSTRDSSamplingResource,
        *project_and_location_routes(
            "/<string:project_name>/mapsets/"
            "<string:mapset_name>/strds/<string:strds_name>"
            "/sampling_async"
        ),
        endpoint=get_endpoint_class_name(AsyncEphemeralSTRDSSamplingResource),
    )
    flask_api.add_resource(
        SyncEphemeralSTRDSSamplingResource,
        *project_and_location_routes(
            "/<string:project_name>/mapsets/"
            "<string:mapset_name>/strds/<string:strds_name>"
            "/sampling_sync"
        ),
        endpoint=get_endpoint_class_name(SyncEphemeralSTRDSSamplingResource),
    )
    flask_api.add_resource(
        AsyncEphemeralSTRDSSamplingGeoJSONResource,
        *project_and_location_routes(
            "/<string:project_name>/mapsets/"
            "<string:mapset_name>/strds/<string:strds_name>"
            "/sampling_async_geojson"
        ),
        endpoint=get_endpoint_class_name(
            AsyncEphemeralSTRDSSamplingGeoJSONResource
        ),
    )
    flask_api.add_resource(
        SyncEphemeralSTRDSSamplingGeoJSONResource,
        *project_and_location_routes(
            "/<string:project_name>/mapsets/"
            "<string:mapset_name>/strds/<string:strds_name>"
            "/sampling_sync_geojson"
        ),
        endpoint=get_endpoint_class_name(
            SyncEphemeralSTRDSSamplingGeoJSONResource
        ),
    )
    flask_api.add_resource(
        AsyncEphemeralRasterSamplingResource,
        *project_and_location_routes(
            "/<string:project_name>/mapsets/"
            "<string:mapset_name>/raster_layers/<string:raster_name>"
            "/sampling_async"
        ),
        endpoint=get_endpoint_class_name(AsyncEphemeralRasterSamplingResource),
    )
    flask_api.add_resource(
        SyncEphemeralRasterSamplingResource,
        *project_and_location_routes(
            "/<string:project_name>/mapsets/"
            "<string:mapset_name>/raster_layers/<string:raster_name>"
            "/sampling_sync"
        ),
        endpoint=get_endpoint_class_name(SyncEphemeralRasterSamplingResource),
    )
    flask_api.add_resource(
        AsyncEphemeralVectorSamplingResource,
        *project_and_location_routes(
            "/<string:project_name>/mapsets/"
            "<string:mapset_name>/vector_layers/<string:vector_name>"
            "/sampling_async"
        ),
        endpoint=get_endpoint_class_name(AsyncEphemeralVectorSamplingResource),
    )
    flask_api.add_resource(
        SyncEphemeralVectorSamplingResource,
        *project_and_location_routes(
            "/<string:project_name>/mapsets/"
            "<string:mapset_name>/vector_layers/<string:vector_name>"
            "/sampling_sync"
        ),
        endpoint=get_endpoint_class_name(SyncEphemeralVectorSamplingResource),
    )


def create_endpoints(flask_api):

    # add deprecated location and project endpoints
    create_project_endpoints(flask_api)

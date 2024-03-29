#!flask/bin/python
# -*- coding: utf-8 -*-
"""
Actinia statistic plugin endpoint definitions
"""
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


__license__ = "GPLv3"
__author__ = "Sören Gebbert, Markus Neteler"
__copyright__ = (
    "Copyright 2016-2022, Sören Gebbert and mundialis GmbH & Co. KG"
)


def create_endpoints(flask_api):
    flask_api.add_resource(
        AsyncEphemeralSTRDSAreaStatsUnivarResource,
        "/locations/<string:location_name>/mapsets/"
        "<string:mapset_name>/strds/"
        "<string:strds_name>/timestamp/"
        "<string:timestamp>/area_stats_univar_async",
    )
    flask_api.add_resource(
        SyncEphemeralSTRDSAreaStatsUnivarResource,
        "/locations/<string:location_name>/mapsets/"
        "<string:mapset_name>/strds/"
        "<string:strds_name>/timestamp/"
        "<string:timestamp>/area_stats_univar_sync",
    )

    flask_api.add_resource(
        AsyncEphemeralSTRDSAreaStatsResource,
        "/locations/<string:location_name>/mapsets/"
        "<string:mapset_name>/strds/<string:strds_name>"
        "/timestamp/<string:timestamp>/area_stats_async",
    )
    flask_api.add_resource(
        SyncEphemeralSTRDSAreaStatsResource,
        "/locations/<string:location_name>/mapsets/"
        "<string:mapset_name>/strds/<string:strds_name>"
        "/timestamp/<string:timestamp>/area_stats_sync",
    )

    flask_api.add_resource(
        AsyncEphemeralRasterAreaStatsResource,
        "/locations/<string:location_name>/mapsets/"
        "<string:mapset_name>/raster_layers/"
        "<string:raster_name>/area_stats_async",
    )
    flask_api.add_resource(
        SyncEphemeralRasterAreaStatsResource,
        "/locations/<string:location_name>/mapsets/"
        "<string:mapset_name>/raster_layers/"
        "<string:raster_name>/area_stats_sync",
    )

    flask_api.add_resource(
        AsyncEphemeralRasterAreaStatsUnivarResource,
        "/locations/<string:location_name>/mapsets/"
        "<string:mapset_name>/raster_layers/"
        "<string:raster_name>"
        "/area_stats_univar_async",
    )
    flask_api.add_resource(
        SyncEphemeralRasterAreaStatsUnivarResource,
        "/locations/<string:location_name>/mapsets/"
        "<string:mapset_name>/raster_layers/"
        "<string:raster_name>"
        "/area_stats_univar_sync",
    )

    flask_api.add_resource(
        AsyncEphemeralSTRDSSamplingResource,
        "/locations/<string:location_name>/mapsets/"
        "<string:mapset_name>/strds/<string:strds_name>"
        "/sampling_async",
    )
    flask_api.add_resource(
        SyncEphemeralSTRDSSamplingResource,
        "/locations/<string:location_name>/mapsets/"
        "<string:mapset_name>/strds/<string:strds_name>"
        "/sampling_sync",
    )

    flask_api.add_resource(
        AsyncEphemeralSTRDSSamplingGeoJSONResource,
        "/locations/<string:location_name>/mapsets/"
        "<string:mapset_name>/strds/<string:strds_name>"
        "/sampling_async_geojson",
    )
    flask_api.add_resource(
        SyncEphemeralSTRDSSamplingGeoJSONResource,
        "/locations/<string:location_name>/mapsets/"
        "<string:mapset_name>/strds/<string:strds_name>"
        "/sampling_sync_geojson",
    )

    flask_api.add_resource(
        AsyncEphemeralRasterSamplingResource,
        "/locations/<string:location_name>/mapsets/"
        "<string:mapset_name>/raster_layers/<string:raster_name>"
        "/sampling_async",
    )
    flask_api.add_resource(
        SyncEphemeralRasterSamplingResource,
        "/locations/<string:location_name>/mapsets/"
        "<string:mapset_name>/raster_layers/<string:raster_name>"
        "/sampling_sync",
    )

    flask_api.add_resource(
        AsyncEphemeralVectorSamplingResource,
        "/locations/<string:location_name>/mapsets/"
        "<string:mapset_name>/vector_layers/<string:vector_name>"
        "/sampling_async",
    )
    flask_api.add_resource(
        SyncEphemeralVectorSamplingResource,
        "/locations/<string:location_name>/mapsets/"
        "<string:mapset_name>/vector_layers/<string:vector_name>"
        "/sampling_sync",
    )

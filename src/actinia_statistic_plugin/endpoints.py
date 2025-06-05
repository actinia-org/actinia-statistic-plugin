#!flask/bin/python
# -*- coding: utf-8 -*-
"""
Actinia statistic plugin endpoint definitions
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

__license__ = "GPLv3"
__author__ = "Sören Gebbert, Markus Neteler"
__copyright__ = (
    "Copyright 2016-2022, Sören Gebbert and mundialis GmbH & Co. KG"
)


def get_endpoint_class_name(
    endpoint_class: Resource,
    projects_url_part: str = "projects",
) -> str:
    """Create the name for the given endpoint class."""
    endpoint_class_name = endpoint_class.__name__.lower()
    if projects_url_part != "projects":
        name = f"{endpoint_class_name}_{projects_url_part}"
    else:
        name = endpoint_class_name
    return name


def create_project_endpoints(flask_api, projects_url_part="projects"):
    """
    Function to add resources with "projects" inside the endpoint url.
    Args:
        apidoc (flask_restful_swagger_2.Api): Flask api
        projects_url_part (str): The name of the projects inside the endpoint
                                 URL; to add deprecated location endpoints set
                                 it to "locations"
    """
    flask_api.add_resource(
        AsyncEphemeralSTRDSAreaStatsUnivarResource,
        f"/{projects_url_part}/<string:project_name>/mapsets/"
        "<string:mapset_name>/strds/"
        "<string:strds_name>/timestamp/"
        "<string:timestamp>/area_stats_univar_async",
        endpoint=get_endpoint_class_name(
            AsyncEphemeralSTRDSAreaStatsUnivarResource, projects_url_part
        ),
    )
    flask_api.add_resource(
        SyncEphemeralSTRDSAreaStatsUnivarResource,
        f"/{projects_url_part}/<string:project_name>/mapsets/"
        "<string:mapset_name>/strds/"
        "<string:strds_name>/timestamp/"
        "<string:timestamp>/area_stats_univar_sync",
        endpoint=get_endpoint_class_name(
            SyncEphemeralSTRDSAreaStatsUnivarResource, projects_url_part
        ),
    )
    flask_api.add_resource(
        AsyncEphemeralSTRDSAreaStatsResource,
        f"/{projects_url_part}/<string:project_name>/mapsets/"
        "<string:mapset_name>/strds/<string:strds_name>"
        "/timestamp/<string:timestamp>/area_stats_async",
        endpoint=get_endpoint_class_name(
            AsyncEphemeralSTRDSAreaStatsResource, projects_url_part
        ),
    )
    flask_api.add_resource(
        SyncEphemeralSTRDSAreaStatsResource,
        f"/{projects_url_part}/<string:project_name>/mapsets/"
        "<string:mapset_name>/strds/<string:strds_name>"
        "/timestamp/<string:timestamp>/area_stats_sync",
        endpoint=get_endpoint_class_name(
            SyncEphemeralSTRDSAreaStatsResource, projects_url_part
        ),
    )
    flask_api.add_resource(
        AsyncEphemeralRasterAreaStatsResource,
        f"/{projects_url_part}/<string:project_name>/mapsets/"
        "<string:mapset_name>/raster_layers/"
        "<string:raster_name>/area_stats_async",
        endpoint=get_endpoint_class_name(
            AsyncEphemeralRasterAreaStatsResource, projects_url_part
        ),
    )
    flask_api.add_resource(
        SyncEphemeralRasterAreaStatsResource,
        f"/{projects_url_part}/<string:project_name>/mapsets/"
        "<string:mapset_name>/raster_layers/"
        "<string:raster_name>/area_stats_sync",
        endpoint=get_endpoint_class_name(
            SyncEphemeralRasterAreaStatsResource, projects_url_part
        ),
    )
    flask_api.add_resource(
        AsyncEphemeralRasterAreaStatsUnivarResource,
        f"/{projects_url_part}/<string:project_name>/mapsets/"
        "<string:mapset_name>/raster_layers/"
        "<string:raster_name>"
        "/area_stats_univar_async",
        endpoint=get_endpoint_class_name(
            AsyncEphemeralRasterAreaStatsUnivarResource, projects_url_part
        ),
    )
    flask_api.add_resource(
        SyncEphemeralRasterAreaStatsUnivarResource,
        f"/{projects_url_part}/<string:project_name>/mapsets/"
        "<string:mapset_name>/raster_layers/"
        "<string:raster_name>"
        "/area_stats_univar_sync",
        endpoint=get_endpoint_class_name(
            SyncEphemeralRasterAreaStatsUnivarResource, projects_url_part
        ),
    )
    flask_api.add_resource(
        AsyncEphemeralSTRDSSamplingResource,
        f"/{projects_url_part}/<string:project_name>/mapsets/"
        "<string:mapset_name>/strds/<string:strds_name>"
        "/sampling_async",
        endpoint=get_endpoint_class_name(
            AsyncEphemeralSTRDSSamplingResource, projects_url_part
        ),
    )
    flask_api.add_resource(
        SyncEphemeralSTRDSSamplingResource,
        f"/{projects_url_part}/<string:project_name>/mapsets/"
        "<string:mapset_name>/strds/<string:strds_name>"
        "/sampling_sync",
        endpoint=get_endpoint_class_name(
            SyncEphemeralSTRDSSamplingResource, projects_url_part
        ),
    )
    flask_api.add_resource(
        AsyncEphemeralSTRDSSamplingGeoJSONResource,
        f"/{projects_url_part}/<string:project_name>/mapsets/"
        "<string:mapset_name>/strds/<string:strds_name>"
        "/sampling_async_geojson",
        endpoint=get_endpoint_class_name(
            AsyncEphemeralSTRDSSamplingGeoJSONResource, projects_url_part
        ),
    )
    flask_api.add_resource(
        SyncEphemeralSTRDSSamplingGeoJSONResource,
        f"/{projects_url_part}/<string:project_name>/mapsets/"
        "<string:mapset_name>/strds/<string:strds_name>"
        "/sampling_sync_geojson",
        endpoint=get_endpoint_class_name(
            SyncEphemeralSTRDSSamplingGeoJSONResource, projects_url_part
        ),
    )
    flask_api.add_resource(
        AsyncEphemeralRasterSamplingResource,
        f"/{projects_url_part}/<string:project_name>/mapsets/"
        "<string:mapset_name>/raster_layers/<string:raster_name>"
        "/sampling_async",
        endpoint=get_endpoint_class_name(
            AsyncEphemeralRasterSamplingResource, projects_url_part
        ),
    )
    flask_api.add_resource(
        SyncEphemeralRasterSamplingResource,
        f"/{projects_url_part}/<string:project_name>/mapsets/"
        "<string:mapset_name>/raster_layers/<string:raster_name>"
        "/sampling_sync",
        endpoint=get_endpoint_class_name(
            SyncEphemeralRasterSamplingResource, projects_url_part
        ),
    )
    flask_api.add_resource(
        AsyncEphemeralVectorSamplingResource,
        f"/{projects_url_part}/<string:project_name>/mapsets/"
        "<string:mapset_name>/vector_layers/<string:vector_name>"
        "/sampling_async",
        endpoint=get_endpoint_class_name(
            AsyncEphemeralVectorSamplingResource, projects_url_part
        ),
    )
    flask_api.add_resource(
        SyncEphemeralVectorSamplingResource,
        f"/{projects_url_part}/<string:project_name>/mapsets/"
        "<string:mapset_name>/vector_layers/<string:vector_name>"
        "/sampling_sync",
        endpoint=get_endpoint_class_name(
            SyncEphemeralVectorSamplingResource, projects_url_part
        ),
    )


def create_endpoints(flask_api):

    # add deprecated location and project endpoints
    create_project_endpoints(flask_api)
    create_project_endpoints(flask_api, projects_url_part="locations")

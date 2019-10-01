========================
Actinia Statistic Plugin
========================

This actinia plugin is deigned for to compute raster map layer and raster-time-series statistics
for categorical and continuous data. It provides endpoints to sample raster
time series data.

Note:

    Actinia[1] is an open source REST API for scalable, distributed, high performance
    processing of geographical data that uses GRASS GIS for computational tasks.

    The Actinia service consists of the *Actinia Core* that provides the basic but sophisticated processing service
    and *Actinia plugins* that provide problem specific services like Sentinel-2 and Landsat NDVI computation,
    spatio-temporal statistical analysis and many more.

    [1] https://github.com/mundialis/actinia_core


Installation
============

The actinia plugin must be installed in the same environment as actinia core.
Actinia core must be configured to load the installed plugin. When the plugin is
loaded and all plugin endpoints are available in actinia.
The interface description of actinia will be extended with the endpoints of the plugins.

    .. code-block:: bash

        git clone https://github.com/mundialis/actinia_statistic_plugin.git

        cd actinia_statistic_plugin
        pip3 install -r requirements.txt
        python3 setup.py install

    ..

After installation set the plugin name in the actinia core configuration
and restart the actinia core server.

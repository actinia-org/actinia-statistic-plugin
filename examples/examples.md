# Examples
```
BASE_URL="http://localhost:8088/api/v3"
AUTH='actinia-gdi:actinia-gdi'
```

## STRDS sampling

Sampling STRDS at point coordinates
```
# async
curl -u ${AUTH} -H 'Content-Type: application/json' -X POST ${BASE_URL}/locations/nc_spm_08/mapsets/modis_lst/strds/LST_Day_monthly/sampling_async -d @points.json

# sync
curl -u ${AUTH} -H 'Content-Type: application/json' -X POST ${BASE_URL}/locations/nc_spm_08/mapsets/modis_lst/strds/LST_Day_monthly/sampling_sync -d @points.json
```

Sampling STRDS at point coordinates by filtering the time of the STRDS
```
# async
curl -u ${AUTH} -H 'Content-Type: application/json' -X POST ${BASE_URL}/locations/nc_spm_08/mapsets/modis_lst/strds/LST_Day_monthly/sampling_async -d @points_where.json

# sync
curl -u ${AUTH} -H 'Content-Type: application/json' -X POST ${BASE_URL}/locations/nc_spm_08/mapsets/modis_lst/strds/LST_Day_monthly/sampling_sync -d @points_where.json
```

Sampling STRDS at Points in a GeoJson
```
curl -u ${AUTH} -H 'Content-Type: application/json' -X POST ${BASE_URL}/locations/nc_spm_08/mapsets/modis_lst/strds/LST_Day_monthly/sampling_sync_geojson -d @points.geojson
```

Sampling STRDS by area
```
curl -u ${AUTH} -H 'Content-Type: application/json' -X POST ${BASE_URL}/locations/nc_spm_08/mapsets/modis_lst/strds/LST_Day_monthly/timestamp/2016-01-01T00:00:00/area_stats_sync -d @area.geojson
```

area_stats_univar for STRDS
```
# async
curl -u ${AUTH} -H 'Content-Type: application/json' -X POST ${BASE_URL}/locations/nc_spm_08/mapsets/modis_lst/strds/LST_Day_monthly/timestamp/2016-01-01T00:00:00/area_stats_univar_async -d @area.geojson

# sync
curl -u ${AUTH} -H 'Content-Type: application/json' -X POST ${BASE_URL}/locations/nc_spm_08/mapsets/modis_lst/strds/LST_Day_monthly/timestamp/2016-01-01T00:00:00/area_stats_univar_sync -d @area.geojson
```


## Raster sampling
Raster statistics of area
```
curl -u ${AUTH} -H 'Content-Type: application/json' -X POST ${BASE_URL}/locations/nc_spm_08/mapsets/PERMANENT/raster_layers/landuse96_28m/area_stats_sync -d @area2.geojson
```

Univar raster statistics of area
```
curl -u ${AUTH} -H 'Content-Type: application/json' -X POST ${BASE_URL}/locations/nc_spm_08/mapsets/PERMANENT/raster_layers/elevation/area_stats_univar_sync -d @area2.geojson
```
```
# async
curl -u ${AUTH} -H 'Content-Type: application/json' -X POST ${BASE_URL}/locations/nc_spm_08/mapsets/PERMANENT/raster_layers/landuse96_28m/sampling_async -d @points2.json
# sync
curl -u ${AUTH} -H 'Content-Type: application/json' -X POST ${BASE_URL}/locations/nc_spm_08/mapsets/PERMANENT/raster_layers/landuse96_28m/sampling_sync -d @points2.json
# note: sync doesn't run successfully (even though test_raste_sample.py passed all tests)
```


## Vector sampling
```
curl -u ${AUTH} -H 'Content-Type: application/json' -X POST ${BASE_URL}/locations/nc_spm_08/mapsets/PERMANENT/vector_layers/nc_state/sampling_async -d @points2.json
```


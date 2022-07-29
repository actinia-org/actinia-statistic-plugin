# Examples
```
BASE_URL="http://localhost:8088/api/v3"
AUTH='actinia-gdi:actinia-gdi'
```

## STRDS sampeling

Sampeling STRDS at point coordinates
```
# async
curl -u ${AUTH} -H 'Content-Type: application/json' -X POST ${BASE_URL}/locations/nc_spm_08/mapsets/modis_lst/strds/LST_Day_monthly/sampling_async -d @points.json

# sync
curl -u ${AUTH} -H 'Content-Type: application/json' -X POST ${BASE_URL}/locations/nc_spm_08/mapsets/modis_lst/strds/LST_Day_monthly/sampling_sync -d @points.json
```

Sampeling STRDS at point coordinates by filtering the time of the STRDS
```
# async
curl -u ${AUTH} -H 'Content-Type: application/json' -X POST ${BASE_URL}/locations/nc_spm_08/mapsets/modis_lst/strds/LST_Day_monthly/sampling_async -d @points_where.json

# sync
curl -u ${AUTH} -H 'Content-Type: application/json' -X POST ${BASE_URL}/locations/nc_spm_08/mapsets/modis_lst/strds/LST_Day_monthly/sampling_sync -d @points_where.json
```

Sampeling STRDS at Points in a GeoJson
```
curl -u ${AUTH} -H 'Content-Type: application/json' -X POST ${BASE_URL}/locations/nc_spm_08/mapsets/modis_lst/strds/LST_Day_monthly/sampling_sync_geojson -d @points.geojson
```


## Vector sampling
```
curl -u ${AUTH} -H 'Content-Type: application/json' -X POST ${BASE_URL}/locations/nc_spm_08/mapsets/PERMANENT/vector_layers/nc_state/sampling_async -d @points2.json
```

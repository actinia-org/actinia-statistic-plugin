# Examples

## STRDS sampeling

Sampeling STRDS at point coordinates
```
# async
curl -u actinia-gdi:actinia-gdi -H 'Content-Type: application/json' -X POST http://localhost:8088/api/v3/locations/nc_spm_08/mapsets/modis_lst/strds/LST_Day_monthly/sampling_async -d @points.json

# sync
curl -u actinia-gdi:actinia-gdi -H 'Content-Type: application/json' -X POST http://localhost:8088/api/v3/locations/nc_spm_08/mapsets/modis_lst/strds/LST_Day_monthly/sampling_sync -d @points.json
```

Sampeling STRDS at point coordinates by filtering the time of the STRDS
```
# async
curl -u actinia-gdi:actinia-gdi -H 'Content-Type: application/json' -X POST http://localhost:8088/api/v3/locations/nc_spm_08/mapsets/modis_lst/strds/LST_Day_monthly/sampling_async -d @points_where.json

# sync
curl -u actinia-gdi:actinia-gdi -H 'Content-Type: application/json' -X POST http://localhost:8088/api/v3/locations/nc_spm_08/mapsets/modis_lst/strds/LST_Day_monthly/sampling_sync -d @points_where.json
```

Sampeling STRDS at Points in a GeoJson
```
curl -u actinia-gdi:actinia-gdi -H 'Content-Type: application/json' -X POST http://localhost:8088/api/v3/locations/nc_spm_08/mapsets/modis_lst/strds/LST_Day_monthly/sampling_sync_geojson -d @points.geojson
```

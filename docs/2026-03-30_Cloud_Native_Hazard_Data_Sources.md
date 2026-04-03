# Cloud-Native Hazard Data Sources for Web-Based Screening

**Date:** 2026-03-30
**Purpose:** Identify freely available, cloud-native hazard datasets consumable directly in a MapLibre GL JS browser app without a backend server.
**Coverage:** Guinea, Mali, Niger, Benin, Ghana (West Africa) + Timor-Leste

---

## Key Technology Note: COGs in MapLibre GL JS

MapLibre GL JS natively supports Cloud Optimized GeoTIFFs (COGs) via the `maplibre-cog-protocol` plugin. This enables **client-side rendering of COGs directly from HTTP URLs** without any tile server or backend. The plugin uses HTTP range requests to fetch only the needed portions of the raster. Any COG hosted on a public URL can be displayed directly.

- Plugin: https://github.com/geomatico/maplibre-cog-protocol
- MapLibre example: https://maplibre.org/maplibre-gl-js/docs/examples/add-a-cog-raster-source/

---

## 1. FLOODING

### 1a. World Bank / GFDRR Global River Flood Hazard (GLOFRIS)

| Field | Details |
|-------|---------|
| **URL** | https://datacatalog.worldbank.org/search/dataset/0038584/global-river-flood-hazard |
| **Format** | GeoTIFF (standard, not COG) |
| **Resolution** | 30 arcseconds (~1 km at equator) |
| **Return periods** | 5, 10, 25, 50, 100, 250, 500, 1000 years |
| **License** | CC BY 4.0 |
| **Direct browser use?** | No - standard GeoTIFF, would need conversion to COG or pre-tiling |
| **Download URLs** | Hosted on geonode-gfdrrlab.org (currently down/unreliable) |

### 1b. WRI Aqueduct Flood Hazard Maps v2

| Field | Details |
|-------|---------|
| **URL** | https://wri-projects.s3.amazonaws.com/AqueductFloodTool/download/v2/index.html |
| **Format** | GeoTIFF (standard) |
| **Resolution** | ~1 km |
| **Return periods** | 2, 5, 10, 25, 50, 100, 250, 500, 1000 years |
| **Scenarios** | Riverine + Coastal; historical, RCP4.5, RCP8.5; 2030/2050/2080 |
| **License** | Open, attribution to WRI |
| **Direct browser use?** | No - standard GeoTIFF on S3, but could be converted to COG |
| **Example URL** | `https://wri-projects.s3.amazonaws.com/AqueductFloodTool/download/v2/inunriver_historical_000000000WATCH_1980_rp00100.tif` (verified working) |
| **Earth Engine ID** | `WRI/Aqueduct_Flood_Hazard_Maps/V2` |

### 1c. Deltares Global Flood Maps (Planetary Computer)

| Field | Details |
|-------|---------|
| **STAC API** | `https://planetarycomputer.microsoft.com/api/stac/v1/collections/deltares-floods` |
| **Format** | NetCDF (NOT COG) |
| **Resolution** | 90m (NASADEM/MERITDEM), 1km, 5km |
| **Return periods** | 2, 5, 10, 25, 50, 100, 250 years |
| **License** | CDLA-Permissive-1.0 |
| **Direct browser use?** | No - NetCDF format, requires server-side processing |
| **Note** | Azure blob storage requires SAS token via Planetary Computer API |

### 1d. Fathom 3.0 (via World Bank)

| Field | Details |
|-------|---------|
| **URL** | https://datacatalog.worldbank.org/search/dataset/0065654 |
| **Format** | GeoTIFF |
| **Resolution** | 30m (1 arcsecond) - highest resolution available |
| **Return periods** | 5-1000 years; fluvial, pluvial, coastal |
| **Scenarios** | Current (2020) + SSP1-2.6, SSP2-4.5, SSP3-7.0, SSP5-8.5 at 2030/2050/2080 |
| **License** | Free for non-commercial use (request required: info@fathom.global) |
| **Direct browser use?** | No - requires request, standard GeoTIFF |
| **Note** | Best resolution but requires formal data request |

### 1e. JRC Global River Flood Hazard Maps v2.1

| Field | Details |
|-------|---------|
| **Earth Engine ID** | `JRC/CEMS_GLOFAS/FloodHazard/v2_1` |
| **Format** | GeoTIFF tiles (5x5 degree) from JRC |
| **Resolution** | ~100m |
| **License** | Open |
| **Direct browser use?** | Via Earth Engine export only |

**RECOMMENDATION:** WRI Aqueduct S3 GeoTIFFs are the most accessible for quick prototyping. Convert to COG with `gdal_translate -of COG input.tif output_cog.tif` and host on any static server.

---

## 2. EARTHQUAKE

### 2a. GEM Global Seismic Hazard Map (OpenQuake) - BEST OPTION

| Field | Details |
|-------|---------|
| **Tile endpoint** | `https://maps.openquake.org/mapproxy/ghm/wmts/seismic-hazard-pga-g/webmercator/{z}/{x}/{y}.png` |
| **Format** | XYZ PNG tiles (WMTS via MapProxy) - VERIFIED WORKING |
| **Resolution** | ~6 km point spacing, interpolated |
| **Variable** | PGA (g), 10% exceedance in 50 years, rock conditions |
| **License** | CC BY-NC-SA 4.0 (viewer), CC BY-SA 4.0 (poster/PNG) |
| **Direct browser use?** | YES - standard XYZ tiles, works directly in MapLibre GL JS |
| **Download (raster)** | https://zenodo.org/records/8409647/files/GEM-GSHM_PGA-475y-rock_v2023.zip |

```javascript
// MapLibre GL JS usage:
map.addSource('seismic-hazard', {
  type: 'raster',
  tiles: ['https://maps.openquake.org/mapproxy/ghm/wmts/seismic-hazard-pga-g/webmercator/{z}/{x}/{y}.png'],
  tileSize: 256
});
```

### 2b. USGS ShakeMap (ArcGIS MapServer)

| Field | Details |
|-------|---------|
| **REST endpoint** | `https://earthquake.usgs.gov/arcgis/rest/services/eq/sm_ShakeMap30DaySignificant/MapServer` |
| **Format** | ArcGIS REST MapServer (can export tiles) |
| **Layers** | pga, pgv, psa03, psa10, psa30, mi (Modified Mercalli) |
| **Coverage** | Global, but only recent significant earthquakes (30 days) |
| **License** | Public domain (USGS) |
| **Direct browser use?** | Possible via ArcGIS REST tile export URL pattern |
| **Note** | Real-time events only, not probabilistic hazard |

### 2c. USGS National Seismic Hazard Maps (US only)

| Field | Details |
|-------|---------|
| **REST endpoint** | `https://earthquake.usgs.gov/arcgis/rest/services/haz/USpga250_2014/MapServer` |
| **Coverage** | US only - not relevant for West Africa/Timor-Leste |

**RECOMMENDATION:** GEM OpenQuake XYZ tiles are the clear winner - free, global, works directly in MapLibre with no backend.

---

## 3. HEAT

### 3a. World Bank Global Extreme Heat Hazard - BEST OPTION

| Field | Details |
|-------|---------|
| **URL** | https://datacatalog.worldbank.org/search/dataset/0040194/global-extreme-heat-hazard |
| **Format** | GeoTIFF (standard, not COG) |
| **Resolution** | 10 km |
| **Variable** | Wet Bulb Globe Temperature (WBGT, degrees C) |
| **Return periods** | 5, 20, 100 years |
| **License** | CC BY 4.0 |
| **Direct browser use?** | No - needs COG conversion, but files are small enough to convert |
| **Direct download URLs (verified)** | |
| - 5yr | `https://datacatalogfiles.worldbank.org/ddh-published/0040194/DR0050009/GLB_HS_RP5.tif` |
| - 20yr | `https://datacatalogfiles.worldbank.org/ddh-published/0040194/DR0050005/GLB_HS_RP20.tif` |
| - 100yr | `https://datacatalogfiles.worldbank.org/ddh-published/0040194/DR0050007/GLB_HS_RP100.tif` |

### 3b. World Bank CCKP on AWS

| Field | Details |
|-------|---------|
| **S3 bucket** | `s3://wbg-cckp/` (no auth: `aws s3 ls --no-sign-request s3://wbg-cckp/`) |
| **Format** | NetCDF |
| **Resolution** | 0.25 degrees (ERA5), 0.50 degrees (CRU) |
| **Variables** | 70+ including `txx` (max temp), `hi35` (heat index >35), extreme heat days |
| **License** | CC BY 4.0 (World Bank ODbL) |
| **Direct browser use?** | No - NetCDF format |

### 3c. ERA5-HEAT (Copernicus CDS)

| Field | Details |
|-------|---------|
| **URL** | https://cds.climate.copernicus.eu/ |
| **Format** | NetCDF/GRIB |
| **Resolution** | 0.25 x 0.25 degrees |
| **Variables** | UTCI (Universal Thermal Climate Index), MRT (Mean Radiant Temperature) |
| **License** | Copernicus (free, registration required) |
| **Direct browser use?** | No - requires CDS API download |

### 3d. ERA5 on Planetary Computer

| Field | Details |
|-------|---------|
| **STAC collection** | `era5-pds` |
| **Format** | Zarr/NetCDF |
| **License** | Proprietary (ECMWF) |
| **Direct browser use?** | No |

### 3e. FEWS NET Heat Exposure Projections

| Field | Details |
|-------|---------|
| **URL** | https://fews.net/heat-exposure-projections |
| **Resolution** | 0.05 degrees (~5 km) |
| **Variable** | WBGTmax derived from CHIRTS-daily |
| **License** | Public domain (USAID/FEWS NET) |
| **Direct browser use?** | Check if tiles available on viewer |

**RECOMMENDATION:** World Bank heat hazard GeoTIFFs are the simplest path. Download, convert to COG, host statically. Small file sizes (37 MB each).

---

## 4. DROUGHT

### 4a. WRI Aqueduct Water Risk v4.0

| Field | Details |
|-------|---------|
| **URL** | https://www.wri.org/aqueduct/data |
| **Earth Engine ID** | `WRI/Aqueduct_Water_Risk/V4/baseline_annual` |
| **Format** | Vector (FeatureCollection) - sub-basin polygons, NOT raster |
| **Indicators** | 13 including baseline water stress, water depletion, seasonal variability |
| **License** | Open, attribution to WRI |
| **Direct browser use?** | Could export as GeoJSON from Earth Engine |
| **Download** | https://www.wri.org/data/aqueduct-global-maps-40-data |

### 4b. SPEIbase Global Drought Monitor

| Field | Details |
|-------|---------|
| **URL** | https://spei.csic.es/map/ (viewer), https://spei.csic.es/database.html (data) |
| **Format** | NetCDF |
| **Resolution** | 0.5 degrees |
| **Variables** | SPEI at 1-48 month timescales |
| **License** | Open |
| **Direct browser use?** | No - NetCDF download |

### 4c. Drought.gov XYZ Tiles (US only)

| Field | Details |
|-------|---------|
| **URL** | https://www.drought.gov/data-download |
| **Format** | COG + XYZ tiles |
| **Coverage** | US only - not relevant |

### 4d. World Bank CCKP Drought Indicators (AWS)

| Field | Details |
|-------|---------|
| **S3 bucket** | `s3://wbg-cckp/` |
| **Variables** | CDD (consecutive dry days), drought indicators |
| **Format** | NetCDF |
| **Direct browser use?** | No |

**RECOMMENDATION:** WRI Aqueduct v4 polygons exported as GeoJSON are the most practical for a browser app. Alternatively, compute a drought indicator raster from CCKP ERA5 data and convert to COG.

---

## 5. LANDSLIDES

### 5a. World Bank / GFDRR Global Landslide Hazard Map (COG) - BEST OPTION

| Field | Details |
|-------|---------|
| **URL** | https://datacatalog.worldbank.org/search/dataset/0037584/global-landslide-hazard-map |
| **Format** | COG (Cloud Optimized GeoTIFF) - VERIFIED |
| **License** | CC BY-NC 4.0 |
| **Direct browser use?** | YES - COG files can be loaded directly in MapLibre via cog-protocol |
| **Direct download URLs (verified)** | |
| - Rainfall trigger (mean) | `https://datacatalogfiles.worldbank.org/ddh-published/0037584/DR0045418/LS_RF_Mean_1980-2018_COG.tif` (145 MB) |
| - Rainfall trigger (median) | `https://datacatalogfiles.worldbank.org/ddh-published/0037584/DR0045419/LS_RF_Median_1980-2018_COG.tif` (124 MB) |
| - Earthquake trigger | `https://datacatalogfiles.worldbank.org/ddh-published/0037584/DR0045416/ls_eq_tiled.tif` (57 MB) |
| - Combined (ThinkHazard ranks) | `https://datacatalogfiles.worldbank.org/ddh-published/0037584/DR0045417/LS_TH_COG.tif` (55 MB) |

### 5b. NASA Global Landslide Susceptibility Map

| Field | Details |
|-------|---------|
| **Direct download** | https://gpm.nasa.gov/sites/default/files/downloads/global-landslide-susceptibility-map-2-27-23.tif |
| **Format** | GeoTIFF (standard) |
| **Resolution** | 1 km |
| **License** | Public domain (NASA) |
| **ArcGIS MapServer** | `https://maps.nccs.nasa.gov/mapping/rest/services/landslide_viewer/Landslide_Susceptibility_Update_2023/MapServer` |
| **Direct browser use?** | Could convert to COG; or use MapServer export as raster tiles |

**RECOMMENDATION:** World Bank landslide COGs are immediately usable in MapLibre GL JS - no conversion needed. Best option by far.

---

## 6. WIND (Tropical Cyclone)

### 6a. CHAZ Global Coastal Wind Hazard Maps

| Field | Details |
|-------|---------|
| **URL** | https://datadryad.org/dataset/doi:10.5061/dryad.qfttdz0vz |
| **Alt URL** | https://doi.org/10.5281/ZENODO.16058513 |
| **Format** | NetCDF (point CSV + gridded raster NetCDF, 180 arcsec grid) |
| **Periods** | Historical (1995-2014), mid-century (2041-2060), end-century (2081-2100) |
| **License** | CC BY 4.0 |
| **Direct browser use?** | No - NetCDF, would need conversion |

### 6b. STORM Synthetic Tropical Cyclone Dataset

| Field | Details |
|-------|---------|
| **URL** | https://data.4tu.nl/articles/dataset/STORM_IBTrACS_present_climate_synthetic_tropical_cyclone_tracks/12706085 |
| **Format** | Track data (CSV), not gridded hazard |
| **License** | CC BY 4.0 |
| **Direct browser use?** | Track data could be rendered as GeoJSON lines |

### 6c. IBTrACS (Historical Tropical Cyclone Tracks)

| Field | Details |
|-------|---------|
| **Earth Engine ID** | `NOAA/IBTrACS/v4` |
| **Format** | Point/track data |
| **License** | Public domain (NOAA) |
| **Direct browser use?** | Could export as GeoJSON |

### 6d. GAR Atlas Cyclonic Wind Hazard

| Field | Details |
|-------|---------|
| **URL** | https://risk.preventionweb.net/ |
| **Format** | Various (download from platform) |
| **License** | UNDRR open |
| **Note** | Platform access may be unreliable |

**NOTE:** West Africa is NOT in a tropical cyclone basin. Guinea has some exposure to Cape Verde hurricane tracks but it is minimal. Timor-Leste has moderate cyclone exposure. Wind hazard may not be the highest priority for this project.

---

## Multi-Hazard Platforms

### ThinkHazard! API (GFDRR)

| Field | Details |
|-------|---------|
| **Base URL** | `https://thinkhazard.org` |
| **Format** | JSON API |
| **License** | Open |
| **Direct browser use?** | YES - REST API, callable from browser JavaScript |
| **Endpoints** | |
| - All hazards for a location | `https://thinkhazard.org/en/report/{division_code}.json` |
| - Specific hazard report | `https://thinkhazard.org/en/report/{division_code}/{hazard_type}.json` |
| - Divisions by hazard | `https://thinkhazard.org/en/admindiv_hazardsets/{hazard_type}.json` |
| **Hazard codes** | FL (river flood), UF (urban flood), CF (coastal flood), EQ (earthquake), LS (landslide), TS (tsunami), VO (volcano), CY (cyclone), DG (water scarcity), EH (extreme heat), WF (wildfire) |

Example (verified working for Guinea, code 97):
```
River flood: High
Urban flood: High
Coastal flood: High
Earthquake: High
Landslide: High
Cyclone: No Data
Water scarcity: Medium
Extreme heat: Medium
```

### GFDRR GeoNode WMS/WFS

| Field | Details |
|-------|---------|
| **Base URL** | `https://www.geonode-gfdrrlab.org/geoserver/wms` |
| **Protocol** | WMS, WFS, WCS |
| **Note** | Server appears to be unreliable/down as of testing |

---

## Summary: Recommended Stack for Browser-Based Hazard Screening

| Hazard | Best Source | Format | Direct MapLibre Use? |
|--------|-----------|--------|---------------------|
| **Flood** | WRI Aqueduct v2 on S3 | GeoTIFF (convert to COG) | After conversion |
| **Earthquake** | GEM/OpenQuake WMTS tiles | XYZ PNG tiles | **YES - immediate** |
| **Heat** | World Bank WBGT hazard | GeoTIFF (convert to COG) | After conversion |
| **Drought** | WRI Aqueduct v4 polygons | Vector/GeoJSON (export) | After export |
| **Landslide** | World Bank/GFDRR COGs | COG | **YES - immediate** |
| **Wind** | CHAZ NetCDF or ThinkHazard API | NetCDF / JSON | API only / after conversion |
| **Multi-hazard** | ThinkHazard! API | JSON | **YES - immediate** |

### Immediate Browser Use (no backend needed):
1. **GEM Seismic Hazard tiles** - XYZ tiles directly in MapLibre
2. **World Bank Landslide COGs** - via maplibre-cog-protocol
3. **ThinkHazard! API** - JSON REST calls from browser

### Minimal Processing (convert to COG + host statically):
4. **WB Heat Hazard GeoTIFFs** - 37 MB files, quick conversion
5. **WRI Aqueduct Flood GeoTIFFs** - convert and host

### More Processing Required:
6. **Drought** - export Aqueduct v4 from Earth Engine or download from WRI
7. **Wind** - download CHAZ NetCDF, convert to COG

---

## COG Conversion Workflow

For GeoTIFF files that need COG conversion:

```bash
# Convert standard GeoTIFF to COG
gdal_translate -of COG -co COMPRESS=DEFLATE input.tif output_cog.tif

# Verify it's a valid COG
python3 -m cogeo_mosaic.utils validate output_cog.tif
# or: rio cogeo validate output_cog.tif
```

Once converted, host on any static file server (GitHub Pages, S3, Azure Blob, etc.) and load directly in MapLibre GL JS using `maplibre-cog-protocol`.

---

## Google Earth Engine Catalog (requires export)

| Dataset | EE ID | Use Case |
|---------|-------|----------|
| WRI Aqueduct Floods v2 | `WRI/Aqueduct_Flood_Hazard_Maps/V2` | Flood inundation depth |
| WRI Aqueduct Water Risk v4 | `WRI/Aqueduct_Water_Risk/V4/baseline_annual` | Water stress polygons |
| JRC Global Flood Hazard v2.1 | `JRC/CEMS_GLOFAS/FloodHazard/v2_1` | River flood depth |
| ERA5 Daily | `ECMWF/ERA5_DAILY` | Temperature extremes |
| ERA5 Hourly | `ECMWF/ERA5/HOURLY` | Heat stress computation |
| IBTrACS v4 | `NOAA/IBTrACS/v4` | Cyclone tracks |
| Global Flood Database | `GLOBAL_FLOOD_DB/MODIS_EVENTS/V1` | Historical flood events |

All require Earth Engine processing and export to COG/GeoJSON for browser use.

## Microsoft Planetary Computer STAC (requires auth token)

| Collection | Format | Use |
|-----------|--------|-----|
| `deltares-floods` | NetCDF | Coastal + sea level rise flooding |
| `era5-pds` | Zarr/NetCDF | Climate reanalysis |
| `nasa-nex-gddp-cmip6` | NetCDF | Climate projections |

Access via: `https://planetarycomputer.microsoft.com/api/stac/v1/collections/{id}`
Token: `https://planetarycomputer.microsoft.com/api/sas/v1/token/{account}/{container}`

## AWS Open Data

| Dataset | Bucket | Format |
|---------|--------|--------|
| WB CCKP | `s3://wbg-cckp/` | NetCDF |
| ERA5 | `s3://era5-pds/` | NetCDF/Zarr |

Access: `aws s3 ls --no-sign-request s3://wbg-cckp/`

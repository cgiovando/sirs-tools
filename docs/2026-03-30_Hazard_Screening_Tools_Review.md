# Hazard/Risk Screening Tools and Dashboards - Research Review

**Date:** 2026-03-30
**Purpose:** Survey of existing web-based tools for natural hazard risk/exposure screening of infrastructure assets, with emphasis on modern cloud-native geospatial approaches and static-site deployability.

---

## Summary

There is a clear spectrum from heavyweight server-dependent platforms (PostGIS + tile servers + APIs) to lightweight static-site approaches using cloud-native formats. The infrastructure risk visualization space is dominated by a few key organizations (GFDRR/World Bank, NISMOD/Oxford, GEM Foundation, WRI, ETH Zurich/CLIMADA). No single tool combines all desired properties (static-site deployable, cloud-native formats, clean UI, report-ready outputs, multi-hazard screening of point assets). The closest exemplars are the NISMOD/IRV Frontend and the Cloud Native Maps SDK, but each has significant trade-offs.

---

## Tier 1: Best Examples for SIRS Reference

### 1. GRI Risk Viewer (NISMOD/Oxford - global.infrastructureresilience.org)

- **URL:** https://global.infrastructureresilience.org/
- **GitHub:** https://github.com/nismod/irv-frontend (frontend), https://github.com/nismod/infra-risk-vis (full stack)
- **Live since:** ~2021, actively maintained (v0.40, March 2025, 661 commits)
- **Tech stack:**
  - Frontend: React + TypeScript (Vite build)
  - Mapping: deck.gl with MapLibre/Mapbox GL base maps
  - UI: Primer React components
  - Data formats: Cloud-Optimised GeoTIFFs (rasters), Mapbox Vector Tiles (infrastructure networks)
  - Backend: Python API, PostgreSQL/PostGIS, Terracotta raster tile server
  - Deployment: Docker Compose orchestration
- **Open source:** Yes (MIT-style)
- **What it does well:**
  - Covers 7 infrastructure sectors globally (transport, energy, water, telecoms, ports/airports, health, education)
  - Multi-hazard: floods, cyclones, earthquakes, heat stress
  - Exposure + damage + adaptation cost-benefit analysis
  - Clean, professional UI with layer toggles, attribute popups, regional summary statistics
  - COGs for raster hazard layers - modern cloud-native approach
- **Limitations:**
  - NOT static-site deployable - requires PostGIS, tile server, Python API backend
  - No report export or PDF generation visible
  - Complex deployment (7+ Docker containers)
- **Relevance to SIRS:** Very high. This is the gold standard for what GFDRR/WB infrastructure risk visualization looks like. The frontend (irv-frontend) is the most polished React+deck.gl risk dashboard in the GFDRR ecosystem. Could serve as the UI design reference for a SIRS screening tool.

### 2. Cloud Native Maps SDK (cloudnativemaps.com)

- **URL:** https://www.cloudnativemaps.com/
- **GitHub:** Open source SDK (downloadable)
- **Tech stack:**
  - Frontend: Vanilla JavaScript SDK (no framework dependency)
  - Mapping: Leaflet.js
  - Data formats: Cloud Optimized GeoTIFF (COG) + FlatGeobuf (FGB)
  - Backend: NONE - fully serverless, data served via HTTP range requests from S3/cloud storage
- **Open source:** Yes
- **What it does well:**
  - True static-site deployment - no server, no tile server, no database
  - Handles massive datasets (72GB FEMA flood hazard demo)
  - Multi-peril querying: click a point, get 14 different hazard values from 14 different COGs
  - Demonstrates the viability of cloud-native formats for hazard screening at scale
  - Very low infrastructure cost (just cloud object storage)
- **Limitations:**
  - Leaflet.js rather than MapLibre/deck.gl (less modern 3D capability)
  - No built-in summary statistics, charts, or report generation
  - Basic UI - functional but not polished/professional
  - SDK approach means you build your own app on top
- **Relevance to SIRS:** High for architecture pattern. Proves that serverless hazard screening with COGs and FlatGeobuf is viable at scale. The FEMA Flood Hazard Zone demo (femaFHZ.com) is the best example of clicking a point and getting multi-hazard exposure values - exactly what SIRS needs.

### 3. CCDR-tools (GFDRR - Country Climate & Disaster Risk Screening)

- **URL:** https://gfdrr.github.io/CCDR-tools/home.html
- **GitHub:** https://github.com/GFDRR/CCDR-tools
- **Live since:** 2022, actively maintained (853 commits)
- **Tech stack:**
  - Primary: Jupyter Notebooks (91% of codebase) + Python
  - Dashboard: HTML output for presentation
  - Data: Global hazard datasets (floods, cyclones, custom), administrative unit aggregation
  - Environment: Conda
- **Open source:** Yes
- **What it does well:**
  - Directly supports World Bank CCDR risk screening workflow
  - Sub-national disaster risk analysis using global datasets
  - Bivariate risk-poverty hotspot maps
  - CMIP6 climate projection integration
  - Well-documented methodology
- **Limitations:**
  - Notebook-based, not a web application - outputs are static maps/reports
  - Requires Python/Conda environment to run
  - No interactive web dashboard for end users
- **Relevance to SIRS:** Very high for methodology. The CCDR-tools define the analytical framework that SIRS should align with. Could be used directly for the hazard screening step, with results fed into a web dashboard.

### 4. GIRI Viewer (UNEP/GRID-Geneva - giri.unepgrid.ch)

- **URL:** https://giri.unepgrid.ch/
- **Tech stack:**
  - Web-based interactive map viewer
  - 100+ customizable hazard and risk layers
  - Interactive dashboards by country
- **Open source:** Data is publicly available, platform specifics unclear
- **What it does well:**
  - First fully probabilistic global infrastructure risk model
  - Covers all major infrastructure sectors including education and health
  - Multi-hazard: cyclones, drought, floods, earthquakes, tsunamis, landslides
  - Average Annual Loss (AAL) metrics by country and sector
  - Current climate + two climate change scenarios
  - Professional, clean interface
- **Limitations:**
  - Not open source (the model is by CIMA/Ingeniar/NGI/University of Geneva)
  - Cannot self-host or deploy as static site
  - Data download requires subscription
- **Relevance to SIRS:** High as a reference for what "good" looks like for multi-hazard infrastructure screening. Covers education infrastructure explicitly. The AAL metrics and sector breakdown are a good model for SIRS outputs.

### 5. ThinkHazard! (GFDRR - thinkhazard.org)

- **URL:** https://thinkhazard.org/
- **GitHub:** https://github.com/GFDRR/thinkhazard
- **Tech stack:**
  - Backend: Python (Pyramid framework)
  - Data: GeoNode for hazard layers, PostgreSQL
  - API: REST API for programmatic access
- **Open source:** Yes
- **What it does well:**
  - Simple, clear UX: select a location, get hazard levels (low/medium/high/very high) for 11 hazards
  - Actionable recommendations for each hazard
  - Covers 190+ countries, sub-national resolution
  - Well-known in development sector
- **Limitations:**
  - Server-dependent (Python/Pyramid/PostgreSQL)
  - Aging codebase (minimal maintenance since ~2021)
  - Location-based, not asset-based - no overlay of point infrastructure
  - No summary statistics across a portfolio of assets
  - No COG/PMTiles/cloud-native formats
- **Relevance to SIRS:** Medium. Conceptual model is right (location-based hazard screening), but the tool is oriented toward project screening, not infrastructure portfolio screening. The SIRS tool needs to screen thousands of school points simultaneously, not one location at a time.

---

## Tier 2: Useful References

### 6. OpenQuake Map Viewer (GEM Foundation - maps.openquake.org)

- **URL:** https://maps.openquake.org/
- **GitHub:** https://github.com/gem/oq-engine (engine), https://github.com/gem/risk-profiles (static profiles)
- **Tech stack:** Web viewer (GeoNode-based), OpenQuake Engine (Python)
- **Open source:** Yes (AGPL-3.0 for engine)
- **What it does well:**
  - Global seismic hazard, risk, and exposure maps
  - Country/territory seismic risk profiles (static PDFs with pre-computed stats)
  - Global Building Exposure Model with building taxonomy
  - GEM Building Taxonomy (directly relevant to GLOSI)
- **Limitations:**
  - Seismic hazard only (no multi-hazard)
  - Map viewer is basic - no point asset overlay or portfolio analysis
  - Risk profiles are static PDFs, not interactive
- **Relevance to SIRS:** High for seismic hazard data and building taxonomy alignment. The GEM exposure model and building taxonomy are foundational inputs for GLOSI Tier 1 classification.

### 7. WRI Aqueduct Water Risk Atlas (wri.org/aqueduct)

- **URL:** https://www.wri.org/applications/aqueduct/water-risk-atlas/
- **GitHub:** https://github.com/wri/aqueduct-components (React components)
- **Tech stack:**
  - Frontend: React with custom component library
  - Data: Google Earth Engine rasters via ResourceWatch API
  - Mapping: Mapbox-based
- **Open source:** Yes (MIT), data freely downloadable
- **What it does well:**
  - Upload your own locations (CSV with coordinates) for batch screening
  - Clean, professional UI with clear risk indicators
  - Peer-reviewed methodology, well-documented
  - Location analyzer - generates risk profile for uploaded points
- **Limitations:**
  - Water risk only (not multi-hazard)
  - Requires ResourceWatch API backend
  - Mapbox (not MapLibre) - commercial dependency
- **Relevance to SIRS:** Medium-high for UX pattern. The "upload locations, get risk profile" workflow is exactly what SIRS needs. The Aqueduct location analyzer is the closest existing example of batch point-asset screening.

### 8. CLIMADA (ETH Zurich - climada.ethz.ch)

- **URL:** https://climada.ethz.ch/
- **GitHub:** https://github.com/CLIMADA-project/climada_python
- **Tech stack:** Python framework, Jupyter notebooks, optional web UI (CLIMADA-App)
- **Open source:** Yes (GPL-3.0)
- **What it does well:**
  - Fully probabilistic multi-hazard risk framework
  - Tropical cyclones, floods, droughts, heat waves, wildfires, crop yield
  - Global coverage at 4km grid
  - Cost-benefit analysis for adaptation options
  - API for hazard and exposure data
- **Limitations:**
  - Python library, not a web dashboard
  - Commercial SaaS version (delta-climate) has the nice UI but is not open source
  - Steep learning curve
- **Relevance to SIRS:** Medium for methodology. CLIMADA's probabilistic hazard data could feed into SIRS screening. The Python API provides access to consistent global hazard datasets that could be pre-computed for the 5 target countries.

### 9. Physrisk (OS-Climate/FINOS)

- **URL:** https://github.com/os-climate/physrisk
- **UI:** https://github.com/os-climate/physrisk-ui
- **Tech stack:**
  - Engine: Python library
  - UI: React + TypeScript (Create React App)
  - Data: AWS S3 (Amazon Sustainability Data Initiative)
- **Open source:** Yes (Apache 2.0)
- **What it does well:**
  - Physical climate risk for asset portfolios
  - Hazard indicator data freely available on AWS
  - Sandbox UI for exploring hazard data
- **Limitations:**
  - Financial/portfolio risk focus (not infrastructure/DRR)
  - UI is a development sandbox, not production-ready
  - Modest community (9 stars)
- **Relevance to SIRS:** Low-medium. Interesting as an example of React UI for climate risk screening, but oriented toward financial risk rather than structural vulnerability.

### 10. GlobalInfraRisk / DamageScanner (VU-IVM)

- **URL:** https://vu-ivm.github.io/GlobalInfraRisk/intro.html
- **GitHub:** https://github.com/VU-IVM/GlobalInfraRisk, https://github.com/VU-IVM/DamageScanner
- **Tech stack:** Jupyter Book documentation, Python (DamageScanner library)
- **Open source:** Yes (MIT)
- **What it does well:**
  - Multi-hazard risk assessment framework for critical infrastructure
  - Covers 7 infrastructure systems including education and health
  - DamageScanner library for damage estimation from hazard rasters + exposure data
  - Published methodology (Nature Communications)
- **Limitations:**
  - Jupyter Book format - documentation/methodology, not an interactive tool
  - Requires Python scripting to use
  - No web dashboard
- **Relevance to SIRS:** High for methodology (Angeles specifically referenced this). DamageScanner could be used for the damage estimation step. The infrastructure categorization (7 systems including education) aligns well with SIRS scope.

---

## Key Technology Patterns

### Cloud-Native Format Ecosystem (for static-site deployment)

| Format | Use Case | MapLibre Support | Key Library |
|--------|----------|-----------------|-------------|
| PMTiles | Vector tiles from S3/static storage | Native (addProtocol) | pmtiles.js |
| COG | Raster hazard layers from S3 | Plugin (maplibre-cog-protocol) | geomatico/maplibre-cog-protocol |
| FlatGeobuf | Vector features (points, polygons) | Plugin (mapbox-gl-flatgeobuf) | flatgeobuf.js |
| GeoParquet | Tabular geodata analytics | Via deck.gl loaders | loaders.gl |

### Best-in-Class Architecture for a Static SIRS Tool

Based on this review, the ideal SIRS screening tool would combine:

1. **MapLibre GL JS** for base mapping (open source, no token required)
2. **PMTiles** for basemap tiles (self-hosted from S3/GitHub, no tile server)
3. **COG** for raster hazard layers (seismic, flood, cyclone - served directly from cloud storage via HTTP range requests)
4. **FlatGeobuf** or **GeoJSON** for school point locations (with GLOSI attributes)
5. **React + TypeScript** frontend (following the irv-frontend pattern)
6. **deck.gl** for advanced visualization (heatmaps, 3D extrusions)
7. **Client-side computation** for exposure statistics (turf.js for spatial queries, simple-statistics for aggregation)
8. **Static hosting** on GitHub Pages or Vercel

This architecture requires zero backend servers. All data would be pre-processed and hosted as static files on cloud storage.

---

## Recommendations for SIRS

1. **Design reference:** Use GRI Risk Viewer (global.infrastructureresilience.org) as the primary UI/UX reference for the SIRS screening dashboard
2. **Architecture reference:** Use Cloud Native Maps / Postholer pattern for serverless hazard data delivery (COG + FlatGeobuf from S3)
3. **Methodology reference:** Align with CCDR-tools screening framework and GlobalInfraRisk/DamageScanner methodology
4. **Workflow reference:** Use WRI Aqueduct's "upload locations, get risk profile" pattern for the SIRS batch screening workflow
5. **Data reference:** Pre-compute hazard values for all school locations using CCDR-tools or CLIMADA, store results as FlatGeobuf/GeoJSON for static serving
6. **Taxonomy reference:** Align building classification output with GEM Building Taxonomy and GLOSI parameters

---

## Source URLs

- https://global.infrastructureresilience.org/
- https://github.com/nismod/irv-frontend
- https://github.com/nismod/infra-risk-vis
- https://github.com/nismod/open-gira
- https://www.cloudnativemaps.com/
- https://gfdrr.github.io/CCDR-tools/home.html
- https://github.com/GFDRR/CCDR-tools
- https://giri.unepgrid.ch/
- https://thinkhazard.org/
- https://github.com/GFDRR/thinkhazard
- https://maps.openquake.org/
- https://github.com/gem/oq-engine
- https://github.com/gem/risk-profiles
- https://www.wri.org/applications/aqueduct/water-risk-atlas/
- https://github.com/wri/aqueduct-components
- https://climada.ethz.ch/
- https://github.com/CLIMADA-project/climada_python
- https://github.com/os-climate/physrisk
- https://github.com/os-climate/physrisk-ui
- https://vu-ivm.github.io/GlobalInfraRisk/intro.html
- https://github.com/VU-IVM/GlobalInfraRisk
- https://github.com/VU-IVM/DamageScanner
- https://risk.preventionweb.net/
- https://drmkc.jrc.ec.europa.eu/risk-data-hub
- https://climatescreeningtools.worldbank.org/
- https://gpss.worldbank.org/en/glosi
- https://github.com/geomatico/maplibre-cog-protocol
- https://github.com/GFDRR/hev-e
- https://github.com/GFDRR/rdl-standard
- https://flatgeobuf.org/examples/maplibre/
- https://docs.protomaps.com/pmtiles/

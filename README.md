# SIRS Screener - School Infrastructure Resilience Scan

Interactive multi-hazard susceptibility screening tool for school infrastructure.

**Live demo:** [cgiovando.github.io/sirs-tools](https://cgiovando.github.io/sirs-tools/)

## Overview

SIRS Screener overlays school locations with multi-hazard data, computes susceptibility scores (0-5 scale), and generates report-ready visualizations. It supports screening across six natural hazards: flood, heat, wind, drought, landslide, and earthquake.

Built for the GPSS/GFDRR Safer Schools Program, World Bank Group.

## Features

- Interactive map (MapLibre GL JS) with color-coded school points by susceptibility
- Toggle hazard score filters and display modes (max score / per-hazard)
- Real hazard raster overlays (heat stress, landslide, seismic)
- Stacked bar charts and summary tables matching report format
- Export report with map screenshot, charts, tables, and CSV download
- Zero backend - fully static site, deployable to GitHub Pages

## Methodology

Susceptibility scoring follows the GFDRR Roadmap for Safer Schools methodology:
1. Overlay school coordinates with hazard raster layers
2. Extract hazard value at each school location
3. Classify into 0-5 susceptibility scores using hazard-specific thresholds
4. Aggregate into summary statistics by region and school type

## Data Sources

- **School locations:** OpenStreetMap / UNICEF Giga
- **Heat stress:** World Bank Global Extreme Heat Hazard (WBGT)
- **Landslide:** World Bank/GFDRR Global Landslide Hazard Map
- **Seismic:** GEM Global Seismic Hazard Map (OpenQuake)
- **Basemap:** CARTO

## Status

This is a prototype with synthetic hazard scores for demonstration. Real hazard value extraction from raster datasets is planned for the next phase.

## AI-assisted development

> This project was developed with significant assistance from AI coding tools.

- **[Claude Code](https://claude.ai/claude-code)** (Anthropic) - code generation, architecture, debugging, and documentation
- All functionality has been tested and verified to work as intended
- Features and infrastructure choices have been reviewed and approved by the maintainer

This disclosure follows emerging best practices for transparency in AI-assisted software development.

## License

TBD

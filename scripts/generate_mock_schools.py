#!/usr/bin/env python3
"""Enrich real Niger school locations with synthetic hazard scores.

Reads actual school locations from the school-char-job project (2,511 schools
from OSM/Giga), assigns spatially-correlated synthetic susceptibility scores
(0-5) for 6 hazards, and writes enriched GeoJSON for the dashboard.

When real hazard rasters are available, this script will be replaced by
extract_hazard_values.py which samples actual COGs at school locations.
"""

import json
import math
import random
import os

random.seed(42)

# Path to real school data (from sibling project)
INPUT_PATH = os.path.expanduser(
    "~/projects/wbg/school-char-job/prototypes/niger_schools.geojson"
)
OUTPUT_PATH = "dashboard/data/niger-schools.geojson"

# Niger region boundaries (approximate bounding boxes for assignment)
# Used to assign schools to regions based on their coordinates
REGION_CENTERS = {
    "Niamey": (2.11, 13.51),
    "Dosso": (3.40, 12.80),
    "Tillaberi": (1.80, 14.40),
    "Tahoua": (5.30, 14.90),
    "Maradi": (7.10, 13.50),
    "Zinder": (9.00, 13.80),
    "Diffa": (12.60, 13.30),
    "Agadez": (8.00, 17.00),
}

# Hazard bias parameters per region
# Values (0-1) control probability of higher scores
REGION_BIAS = {
    "Niamey":   {"flood": 0.60, "heat": 0.50, "wind": 0.25, "drought": 0.30, "landslide": 0.05, "earthquake": 0.15},
    "Dosso":    {"flood": 0.55, "heat": 0.45, "wind": 0.20, "drought": 0.25, "landslide": 0.10, "earthquake": 0.15},
    "Tillaberi":{"flood": 0.50, "heat": 0.55, "wind": 0.30, "drought": 0.45, "landslide": 0.12, "earthquake": 0.18},
    "Tahoua":   {"flood": 0.20, "heat": 0.70, "wind": 0.35, "drought": 0.70, "landslide": 0.10, "earthquake": 0.12},
    "Maradi":   {"flood": 0.35, "heat": 0.60, "wind": 0.25, "drought": 0.55, "landslide": 0.08, "earthquake": 0.10},
    "Zinder":   {"flood": 0.30, "heat": 0.65, "wind": 0.30, "drought": 0.60, "landslide": 0.05, "earthquake": 0.10},
    "Diffa":    {"flood": 0.40, "heat": 0.70, "wind": 0.30, "drought": 0.65, "landslide": 0.02, "earthquake": 0.08},
    "Agadez":   {"flood": 0.05, "heat": 0.85, "wind": 0.45, "drought": 0.90, "landslide": 0.03, "earthquake": 0.08},
}


def assign_region(lon, lat):
    """Assign a school to the nearest Niger region based on coordinates."""
    min_dist = float("inf")
    best = "Niamey"
    for name, (cx, cy) in REGION_CENTERS.items():
        # Weight latitude more for Agadez (large northern region)
        dist = math.sqrt((lon - cx) ** 2 + (lat - cy) ** 2)
        if dist < min_dist:
            min_dist = dist
            best = name
    return best


def generate_score(bias):
    """Generate a hazard score (0-5) with spatial bias."""
    weights = [1.0, 1.0, 0.8, 0.6, 0.4, 0.2]
    for i in range(6):
        if i <= 2:
            weights[i] *= (1 - bias)
        else:
            weights[i] *= bias
    weights = [w + 0.05 for w in weights]
    total = sum(weights)
    weights = [w / total for w in weights]
    return random.choices(range(6), weights=weights, k=1)[0]


def enrich_schools():
    """Read real school data and add synthetic hazard scores."""
    with open(INPUT_PATH) as f:
        data = json.load(f)

    for i, feature in enumerate(data["features"]):
        props = feature["properties"]
        coords = feature["geometry"]["coordinates"]
        lon, lat = coords[0], coords[1]

        # Assign region
        region = assign_region(lon, lat)

        # Generate scores based on regional bias + per-school noise
        biases = REGION_BIAS[region]
        scores = {}
        for hazard, bias in biases.items():
            # Latitude-based adjustment for heat/drought (higher in north)
            lat_factor = 0
            if hazard in ("heat", "drought"):
                lat_factor = (lat - 13.0) * 0.05  # Increase bias northward
            # River proximity for flood (crude: lower lat + western lon)
            if hazard == "flood" and lon < 4 and lat < 14:
                lat_factor = 0.15  # Near Niger River

            local_bias = max(0, min(1, bias + lat_factor + random.gauss(0, 0.12)))
            scores[hazard] = generate_score(local_bias)

        # Add new properties, keep originals
        props["id"] = f"NER-{i + 1:04d}"
        props["region"] = region
        props["flood_score"] = scores["flood"]
        props["heat_score"] = scores["heat"]
        props["wind_score"] = scores["wind"]
        props["drought_score"] = scores["drought"]
        props["landslide_score"] = scores["landslide"]
        props["earthquake_score"] = scores["earthquake"]
        props["max_score"] = max(scores.values())

    return data


if __name__ == "__main__":
    data = enrich_schools()

    with open(OUTPUT_PATH, "w") as f:
        json.dump(data, f)  # No indent - file is large with 2511 features

    total = len(data["features"])
    print(f"Enriched {total} real schools with synthetic hazard scores")
    print(f"Input: {INPUT_PATH}")
    print(f"Output: {OUTPUT_PATH}")

    # Region distribution
    regions = {}
    for feat in data["features"]:
        r = feat["properties"]["region"]
        regions[r] = regions.get(r, 0) + 1
    print(f"\nRegion distribution:")
    for r, c in sorted(regions.items(), key=lambda x: -x[1]):
        print(f"  {r:12s}: {c}")

    # Score distribution
    hazards = ["flood", "heat", "wind", "drought", "landslide", "earthquake"]
    print("\nScore distribution:")
    for hazard in hazards:
        counts = [0] * 6
        for feat in data["features"]:
            score = feat["properties"][f"{hazard}_score"]
            counts[score] += 1
        dist = " | ".join(f"{i}:{c}" for i, c in enumerate(counts))
        print(f"  {hazard:12s}: {dist}")

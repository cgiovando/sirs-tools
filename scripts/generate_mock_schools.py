#!/usr/bin/env python3
"""Generate realistic mock school data for Niger with synthetic hazard scores.

Produces a GeoJSON file with ~260 schools distributed across Niger's 8 regions,
each with susceptibility scores (0-5) for 6 hazards. Scores are spatially
correlated to approximate real hazard patterns.
"""

import json
import random
import math

random.seed(42)

# Niger regions with cluster centers and hazard bias parameters
# bias values (0-1) control probability of higher scores
REGIONS = [
    {
        "name": "Niamey",
        "lon": 2.11, "lat": 13.51, "spread": 0.35,
        "count": 55,
        "bias": {"flood": 0.65, "heat": 0.50, "wind": 0.25, "drought": 0.30, "landslide": 0.05, "earthquake": 0.15}
    },
    {
        "name": "Zinder",
        "lon": 8.98, "lat": 13.80, "spread": 0.40,
        "count": 40,
        "bias": {"flood": 0.30, "heat": 0.65, "wind": 0.30, "drought": 0.60, "landslide": 0.05, "earthquake": 0.10}
    },
    {
        "name": "Maradi",
        "lon": 7.10, "lat": 13.50, "spread": 0.35,
        "count": 40,
        "bias": {"flood": 0.35, "heat": 0.60, "wind": 0.25, "drought": 0.55, "landslide": 0.08, "earthquake": 0.10}
    },
    {
        "name": "Tahoua",
        "lon": 5.27, "lat": 14.89, "spread": 0.50,
        "count": 30,
        "bias": {"flood": 0.20, "heat": 0.70, "wind": 0.35, "drought": 0.70, "landslide": 0.10, "earthquake": 0.12}
    },
    {
        "name": "Dosso",
        "lon": 3.19, "lat": 13.05, "spread": 0.30,
        "count": 30,
        "bias": {"flood": 0.60, "heat": 0.45, "wind": 0.20, "drought": 0.25, "landslide": 0.10, "earthquake": 0.15}
    },
    {
        "name": "Agadez",
        "lon": 7.99, "lat": 16.97, "spread": 0.80,
        "count": 15,
        "bias": {"flood": 0.05, "heat": 0.85, "wind": 0.45, "drought": 0.90, "landslide": 0.03, "earthquake": 0.08}
    },
    {
        "name": "Diffa",
        "lon": 12.61, "lat": 13.32, "spread": 0.35,
        "count": 20,
        "bias": {"flood": 0.40, "heat": 0.70, "wind": 0.30, "drought": 0.65, "landslide": 0.02, "earthquake": 0.08}
    },
    {
        "name": "Tillaberi",
        "lon": 1.45, "lat": 14.21, "spread": 0.45,
        "count": 30,
        "bias": {"flood": 0.55, "heat": 0.55, "wind": 0.30, "drought": 0.45, "landslide": 0.12, "earthquake": 0.18}
    },
]

# School name templates (French, as used in Niger)
PREFIXES = [
    "Ecole Primaire",
    "CEG",  # College d'Enseignement General
    "Lycee",
    "Ecole Communautaire",
    "Complexe Scolaire",
    "Ecole Franco-Arabe",
    "Medersa",
]

# Village/locality names per region (realistic Niger names)
LOCALITIES = {
    "Niamey": [
        "Plateau", "Yantala", "Gamkalle", "Koira Kano", "Lazaret",
        "Boukoki", "Dar es Salam", "Saga", "Lamorde", "Kouara Kano",
        "Talladje", "Wadata", "Balafon", "Cite Faysal", "Francophone",
        "Aeroport", "Recasement", "Bani Fandou", "Gaweye", "Route Filingue",
    ],
    "Zinder": [
        "Birni", "Mirriah", "Magaria", "Matameye", "Damagaram",
        "Takieta", "Droum", "Gouré", "Wacha", "Dogo",
        "Kantche", "Bandé", "Tirmini", "Dan Barto", "Guidimouni",
    ],
    "Maradi": [
        "Maradaoua", "Guidan Roumdji", "Madarounfa", "Tessaoua", "Aguie",
        "Dakoro", "Mayahi", "Gazaoua", "Safo", "Bermo",
        "Kornaka", "Dan Issa", "Tibiri", "Serkin Yamma", "Gabi",
    ],
    "Tahoua": [
        "Birni N'Konni", "Madaoua", "Bouza", "Illéla", "Keita",
        "Abalak", "Tchintabaraden", "Tassara", "Kao", "Bambeye",
        "Galma", "Malbaza", "Doguéraoua", "Tsernaoua", "Badaguichiri",
    ],
    "Dosso": [
        "Gaya", "Boboye", "Loga", "Dioundiou", "Tibiri",
        "Falmey", "Kirtachi", "Sambera", "Tanda", "Mokko",
        "Bana", "Tombo Koarey", "Yélou", "Harikanassou", "Koygolo",
    ],
    "Agadez": [
        "Arlit", "Tchirozérine", "Aderbissinat", "Ingall", "Dabaga",
        "Iférouane", "Timia", "Elmeki", "Gougaram", "Tabelot",
    ],
    "Diffa": [
        "Mainé-Soroa", "N'Guigmi", "Bosso", "Goudoumaria", "Toumour",
        "Chétimari", "Kabalewa", "Nguelbéli", "Tam", "Kablewa",
    ],
    "Tillaberi": [
        "Ouallam", "Filingué", "Kollo", "Say", "Téra",
        "Gothèye", "Torodi", "Abala", "Ayorou", "Banibangou",
        "Bankilaré", "Dargol", "Diagourou", "Gorouol", "Sinder",
    ],
}


def generate_score(bias: float) -> int:
    """Generate a hazard score (0-5) with spatial bias.

    Higher bias = higher probability of elevated scores.
    Uses a weighted random approach with bias shifting the distribution.
    """
    # Base weights for scores 0-5 (slightly skewed toward lower scores)
    weights = [1.0, 1.0, 0.8, 0.6, 0.4, 0.2]

    # Shift weights based on bias
    for i in range(6):
        if i <= 2:
            weights[i] *= (1 - bias)
        else:
            weights[i] *= bias

    # Add some base probability to avoid zero weights
    weights = [w + 0.05 for w in weights]
    total = sum(weights)
    weights = [w / total for w in weights]

    return random.choices(range(6), weights=weights, k=1)[0]


def generate_schools():
    """Generate mock school GeoJSON features."""
    features = []
    school_id = 0

    for region in REGIONS:
        localities = LOCALITIES[region["name"]]

        for i in range(region["count"]):
            school_id += 1

            # Generate position with Gaussian spread around center
            lon = region["lon"] + random.gauss(0, region["spread"])
            lat = region["lat"] + random.gauss(0, region["spread"] * 0.7)

            # Clamp to Niger's bounds
            lon = max(0.1, min(15.9, lon))
            lat = max(11.7, min(23.5, lat))

            # Generate school name
            prefix = random.choice(PREFIXES)
            locality = random.choice(localities)
            suffix = "" if random.random() > 0.3 else f" {random.choice(['I', 'II', 'III', 'A', 'B'])}"
            name = f"{prefix} de {locality}{suffix}"

            # Generate hazard scores with regional bias
            scores = {}
            for hazard, bias in region["bias"].items():
                # Add some per-school randomness to the bias
                local_bias = max(0, min(1, bias + random.gauss(0, 0.15)))
                scores[hazard] = generate_score(local_bias)

            max_score = max(scores.values())

            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [round(lon, 5), round(lat, 5)]
                },
                "properties": {
                    "id": f"NER-{school_id:04d}",
                    "name": name,
                    "region": region["name"],
                    "flood_score": scores["flood"],
                    "heat_score": scores["heat"],
                    "wind_score": scores["wind"],
                    "drought_score": scores["drought"],
                    "landslide_score": scores["landslide"],
                    "earthquake_score": scores["earthquake"],
                    "max_score": max_score
                }
            }
            features.append(feature)

    return {
        "type": "FeatureCollection",
        "features": features
    }


if __name__ == "__main__":
    data = generate_schools()
    output_path = "dashboard/data/niger-schools.geojson"

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    # Print summary
    total = len(data["features"])
    print(f"Generated {total} mock schools for Niger")
    print(f"Output: {output_path}")

    # Score distribution summary
    hazards = ["flood", "heat", "wind", "drought", "landslide", "earthquake"]
    print("\nScore distribution:")
    for hazard in hazards:
        counts = [0] * 6
        for feat in data["features"]:
            score = feat["properties"][f"{hazard}_score"]
            counts[score] += 1
        dist = " | ".join(f"{i}:{c}" for i, c in enumerate(counts))
        print(f"  {hazard:12s}: {dist}")

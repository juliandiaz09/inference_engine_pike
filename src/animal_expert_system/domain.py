"""Domain data — sistema experto de felinos grandes."""

from __future__ import annotations

from dataclasses import dataclass


FEATURE_ORDER = ("habitat", "patron_pelaje", "capacidad", "region", "actividad")

MODE_FORWARD = "adelante"
MODE_BACKWARD = "atras"

MODE_LABELS = {
    MODE_FORWARD: "Encadenamiento hacia adelante",
    MODE_BACKWARD: "Encadenamiento hacia atrás",
}

MODE_DESCRIPTIONS = {
    MODE_FORWARD: (
        "Primero se agregan los hechos al sistema y luego las reglas "
        "disparan conclusiones."
    ),
    MODE_BACKWARD: (
        "Primero se plantea la conclusión y el sistema intenta demostrarla "
        "con subobjetivos."
    ),
}

# Traducciones español -> inglés para la base de conocimiento interna
FEATURE_TRANSLATIONS = {
    "habitat": {
        "selva_tropical":    "tropical_rainforest",
        "sabana":            "savanna",
        "montana":           "mountain",
        "bosque_templado":   "temperate_forest",
        "desierto":          "desert",
        "tundra_alpina":     "alpine_tundra",
        "manglar":           "mangrove",
        "bosque_nublado":    "cloud_forest",
    },
    "patron_pelaje": {
        "manchas_roseta":    "rosette_spots",
        "rayas_verticales":  "vertical_stripes",
        "manchas_solidas":   "solid_spots",
        "pelaje_uniforme":   "plain_coat",
        "manchas_nube":      "cloud_spots",
        "manchas_pequenas":  "small_spots",
    },
    "capacidad": {
        "rugir":             "roar",
        "ronronear":         "purr",
        "trepar":            "climb",
        "nadar":             "swim",
        "velocidad_extrema": "extreme_speed",
    },
    "region": {
        "america":           "america",
        "africa":            "africa",
        "asia":              "asia",
        "africa_asia":       "africa_asia",
        "asia_central":      "central_asia",
        "sudeste_asiatico":  "southeast_asia",
    },
    "actividad": {
        "nocturno":          "nocturnal",
        "diurno":            "diurnal",
        "crepuscular":       "crepuscular",
        "arboricola":        "arboreal",
    },
}

REVERSE_FEATURE_TRANSLATIONS = {
    feature: {english: spanish for spanish, english in mapping.items()}
    for feature, mapping in FEATURE_TRANSLATIONS.items()
}

FEATURE_LABELS = {
    "habitat":       "Hábitat",
    "patron_pelaje": "Patrón de pelaje",
    "capacidad":     "Capacidad especial",
    "region":        "Región geográfica",
    "actividad":     "Actividad",
}

FEATURE_OPTIONS = {
    "habitat": [
        "selva_tropical",
        "sabana",
        "montana",
        "bosque_templado",
        "desierto",
        "tundra_alpina",
        "manglar",
        "bosque_nublado",
    ],
    "patron_pelaje": [
        "manchas_roseta",
        "rayas_verticales",
        "manchas_solidas",
        "pelaje_uniforme",
        "manchas_nube",
        "manchas_pequenas",
    ],
    "capacidad": [
        "rugir",
        "ronronear",
        "trepar",
        "nadar",
        "velocidad_extrema",
    ],
    "region": [
        "america",
        "africa",
        "asia",
        "africa_asia",
        "asia_central",
        "sudeste_asiatico",
    ],
    "actividad": [
        "nocturno",
        "diurno",
        "crepuscular",
        "arboricola",
    ],
}

EXAMPLE_PRESETS = {
    "Jaguar": {
        "habitat":       "selva_tropical",
        "patron_pelaje": "manchas_roseta",
        "capacidad":     "nadar",
        "region":        "america",
        "actividad":     "nocturno",
    },
    "León": {
        "habitat":       "sabana",
        "patron_pelaje": "pelaje_uniforme",
        "capacidad":     "rugir",
        "region":        "africa",
        "actividad":     "crepuscular",
    },
    "Tigre": {
        "habitat":       "selva_tropical",
        "patron_pelaje": "rayas_verticales",
        "capacidad":     "nadar",
        "region":        "asia",
        "actividad":     "nocturno",
    },
    "Leopardo": {
        "habitat":       "bosque_templado",
        "patron_pelaje": "manchas_roseta",
        "capacidad":     "trepar",
        "region":        "africa_asia",
        "actividad":     "nocturno",
    },
    "Guepardo": {
        "habitat":       "sabana",
        "patron_pelaje": "manchas_solidas",
        "capacidad":     "velocidad_extrema",
        "region":        "africa",
        "actividad":     "diurno",
    },
    "Puma": {
        "habitat":       "montana",
        "patron_pelaje": "pelaje_uniforme",
        "capacidad":     "ronronear",
        "region":        "america",
        "actividad":     "crepuscular",
    },
    "Leopardo de las Nieves": {
        "habitat":       "tundra_alpina",
        "patron_pelaje": "manchas_roseta",
        "capacidad":     "ronronear",
        "region":        "asia_central",
        "actividad":     "crepuscular",
    },
    "Leopardo Nublado": {
        "habitat":       "bosque_nublado",
        "patron_pelaje": "manchas_nube",
        "capacidad":     "trepar",
        "region":        "sudeste_asiatico",
        "actividad":     "arboricola",
    },
    "Ocelote": {
        "habitat":       "selva_tropical",
        "patron_pelaje": "manchas_pequenas",
        "capacidad":     "trepar",
        "region":        "america",
        "actividad":     "nocturno",
    },
}


@dataclass(frozen=True)
class TaxonomyMatch:
    animal: str
    class_name: str
    order: str
    family: str
    genus: str


@dataclass(frozen=True)
class AnimalProfile:
    animal: str
    class_name: str
    order: str
    family: str
    genus: str
    features: dict[str, str]


ANIMAL_PROFILES = [
    AnimalProfile(
        animal="jaguar",
        class_name="mammalia",
        order="carnivora",
        family="felidae",
        genus="panthera",
        features={
            "habitat":       "tropical_rainforest",
            "patron_pelaje": "rosette_spots",
            "capacidad":     "swim",
            "region":        "america",
            "actividad":     "nocturnal",
        },
    ),
    AnimalProfile(
        animal="leon",
        class_name="mammalia",
        order="carnivora",
        family="felidae",
        genus="panthera",
        features={
            "habitat":       "savanna",
            "patron_pelaje": "plain_coat",
            "capacidad":     "roar",
            "region":        "africa",
            "actividad":     "crepuscular",
        },
    ),
    AnimalProfile(
        animal="tigre",
        class_name="mammalia",
        order="carnivora",
        family="felidae",
        genus="panthera",
        features={
            "habitat":       "tropical_rainforest",
            "patron_pelaje": "vertical_stripes",
            "capacidad":     "swim",
            "region":        "asia",
            "actividad":     "nocturnal",
        },
    ),
    AnimalProfile(
        animal="leopardo",
        class_name="mammalia",
        order="carnivora",
        family="felidae",
        genus="panthera",
        features={
            "habitat":       "temperate_forest",
            "patron_pelaje": "rosette_spots",
            "capacidad":     "climb",
            "region":        "africa_asia",
            "actividad":     "nocturnal",
        },
    ),
    AnimalProfile(
        animal="guepardo",
        class_name="mammalia",
        order="carnivora",
        family="felidae",
        genus="acinonyx",
        features={
            "habitat":       "savanna",
            "patron_pelaje": "solid_spots",
            "capacidad":     "extreme_speed",
            "region":        "africa",
            "actividad":     "diurnal",
        },
    ),
    AnimalProfile(
        animal="puma",
        class_name="mammalia",
        order="carnivora",
        family="felidae",
        genus="puma",
        features={
            "habitat":       "mountain",
            "patron_pelaje": "plain_coat",
            "capacidad":     "purr",
            "region":        "america",
            "actividad":     "crepuscular",
        },
    ),
    AnimalProfile(
        animal="leopardo_de_las_nieves",
        class_name="mammalia",
        order="carnivora",
        family="felidae",
        genus="panthera",
        features={
            "habitat":       "alpine_tundra",
            "patron_pelaje": "rosette_spots",
            "capacidad":     "purr",
            "region":        "central_asia",
            "actividad":     "crepuscular",
        },
    ),
    AnimalProfile(
        animal="leopardo_nublado",
        class_name="mammalia",
        order="carnivora",
        family="felidae",
        genus="neofelis",
        features={
            "habitat":       "cloud_forest",
            "patron_pelaje": "cloud_spots",
            "capacidad":     "climb",
            "region":        "southeast_asia",
            "actividad":     "arboreal",
        },
    ),
    AnimalProfile(
        animal="ocelote",
        class_name="mammalia",
        order="carnivora",
        family="felidae",
        genus="leopardus",
        features={
            "habitat":       "tropical_rainforest",
            "patron_pelaje": "small_spots",
            "capacidad":     "climb",
            "region":        "america",
            "actividad":     "nocturnal",
        },
    ),
]


def humanize(token: str) -> str:
    """Convert identifiers like 'tropical_rainforest' into readable labels."""
    replacements = {
        "jaguar":                   "Jaguar",
        "leon":                     "León",
        "tigre":                    "Tigre",
        "leopardo":                 "Leopardo",
        "guepardo":                 "Guepardo",
        "puma":                     "Puma",
        "leopardo_de_las_nieves":   "Leopardo de las Nieves",
        "leopardo_nublado":         "Leopardo Nublado",
        "ocelote":                  "Ocelote",
        "mammalia":                 "Mammalia",
        "carnivora":                "Carnivora",
        "felidae":                  "Felidae",
        "panthera":                 "Panthera",
        "acinonyx":                 "Acinonyx",
        "puma":                     "Puma",
        "neofelis":                 "Neofelis",
        "leopardus":                "Leopardus",
        "tropical_rainforest":      "Selva tropical",
        "savanna":                  "Sabana",
        "mountain":                 "Montaña",
        "temperate_forest":         "Bosque templado",
        "desert":                   "Desierto",
        "alpine_tundra":            "Tundra alpina",
        "mangrove":                 "Manglar",
        "cloud_forest":             "Bosque nublado",
        "rosette_spots":            "Manchas en roseta",
        "vertical_stripes":         "Rayas verticales",
        "solid_spots":              "Manchas sólidas",
        "plain_coat":               "Pelaje uniforme",
        "cloud_spots":              "Manchas en nube",
        "small_spots":              "Manchas pequeñas",
        "roar":                     "Rugir",
        "purr":                     "Ronronear",
        "climb":                    "Trepar",
        "swim":                     "Nadar",
        "extreme_speed":            "Velocidad extrema",
        "america":                  "América",
        "africa":                   "África",
        "asia":                     "Asia",
        "africa_asia":              "África y Asia",
        "central_asia":             "Asia Central",
        "southeast_asia":           "Sudeste Asiático",
        "nocturnal":                "Nocturno",
        "diurnal":                  "Diurno",
        "crepuscular":              "Crepuscular",
        "arboreal":                 "Arborícola",
        "habitat":                  "Hábitat",
        "patron_pelaje":            "Patrón de pelaje",
        "capacidad":                "Capacidad especial",
        "region":                   "Región",
        "actividad":                "Actividad",
    }
    return replacements.get(token, token.replace("_", " ").capitalize())
"""Domain data used by the GUI and the inference layer."""

from __future__ import annotations

from dataclasses import dataclass


FEATURE_ORDER = ("habitat", "diet", "morphology", "reproduction", "activity")

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

FEATURE_TRANSLATIONS = {
    "habitat": {
        "selva": "rainforest",
        "montana": "mountains",
        "humedal": "wetlands",
        "copa_de_arboles": "forest_canopy",
        "sabanas_y_bosques": "savanna_forest",
        "cuevas": "caves",
        "acuatico": "aquatic",
        "bosque": "forest",
    },
    "diet": {
        "carnivoro": "carnivore",
        "herbivoro": "herbivore",
        "insectivoro": "insectivore",
        "omnivoro": "omnivore",
        "piscivoro": "piscivore",
    },
    "morphology": {
        "pelaje_moteado": "spotted_fur",
        "pelaje_moteado_pequeno": "small_spotted_fur",
        "pelaje_uniforme": "plain_fur",
        "pelaje_grueso": "coarse_fur",
        "garras_largas": "long_claws",
        "hocico_alargado": "elongated_snout",
        "alas": "wings",
        "aletas": "fins",
        "pulgar_oponible": "opposable_thumb",
    },
    "reproduction": {
        "viviparo": "viviparous",
    },
    "activity": {
        "nocturno": "nocturnal",
        "arboricola": "arboreal",
        "semiacuatico": "semi_aquatic",
        "terrestre": "terrestrial",
        "acuatico": "aquatic",
    },
}

REVERSE_FEATURE_TRANSLATIONS = {
    feature: {english: spanish for spanish, english in mapping.items()}
    for feature, mapping in FEATURE_TRANSLATIONS.items()
}

FEATURE_LABELS = {
    "habitat": "Hábitat",
    "diet": "Tipo de alimentación",
    "morphology": "Morfología",
    "reproduction": "Reproducción",
    "activity": "Actividad",
}

FEATURE_OPTIONS = {
    "habitat": [
        "selva",
        "montana",
        "humedal",
        "copa_de_arboles",
        "sabanas_y_bosques",
        "cuevas",
        "acuatico",
        "bosque",
    ],
    "diet": [
        "carnivoro",
        "herbivoro",
        "insectivoro",
        "omnivoro",
        "piscivoro",
    ],
    "morphology": [
        "pelaje_moteado",
        "pelaje_moteado_pequeno",
        "pelaje_uniforme",
        "pelaje_grueso",
        "garras_largas",
        "hocico_alargado",
        "alas",
        "aletas",
        "pulgar_oponible",
    ],
    "reproduction": [
        "viviparo",
    ],
    "activity": [
        "nocturno",
        "arboricola",
        "semiacuatico",
        "terrestre",
        "acuatico",
    ],
}

EXAMPLE_PRESETS = {
    "Jaguar": {
        "habitat": "selva",
        "diet": "carnivoro",
        "morphology": "pelaje_moteado",
        "reproduction": "viviparo",
        "activity": "nocturno",
    },
    "Capibara": {
        "habitat": "humedal",
        "diet": "herbivoro",
        "morphology": "pelaje_grueso",
        "reproduction": "viviparo",
        "activity": "semiacuatico",
    },
    "Delfin": {
        "habitat": "acuatico",
        "diet": "carnivoro",
        "morphology": "aletas",
        "reproduction": "viviparo",
        "activity": "acuatico",
    },
}


@dataclass(frozen=True)
class TaxonomyMatch:
    animal: str
    class_name: str
    order: str
    family: str


@dataclass(frozen=True)
class AnimalProfile:
    animal: str
    class_name: str
    order: str
    family: str
    features: dict[str, str]


ANIMAL_PROFILES = [
    AnimalProfile(
        animal="jaguar",
        class_name="mammalia",
        order="carnivora",
        family="felidae",
        features={
            "habitat": "rainforest",
            "diet": "carnivore",
            "morphology": "spotted_fur",
            "reproduction": "viviparous",
            "activity": "nocturnal",
        },
    ),
    AnimalProfile(
        animal="puma",
        class_name="mammalia",
        order="carnivora",
        family="felidae",
        features={
            "habitat": "mountains",
            "diet": "carnivore",
            "morphology": "plain_fur",
            "reproduction": "viviparous",
            "activity": "nocturnal",
        },
    ),
    AnimalProfile(
        animal="ocelot",
        class_name="mammalia",
        order="carnivora",
        family="felidae",
        features={
            "habitat": "rainforest",
            "diet": "carnivore",
            "morphology": "small_spotted_fur",
            "reproduction": "viviparous",
            "activity": "arboreal",
        },
    ),
    AnimalProfile(
        animal="capybara",
        class_name="mammalia",
        order="rodentia",
        family="caviidae",
        features={
            "habitat": "wetlands",
            "diet": "herbivore",
            "morphology": "coarse_fur",
            "reproduction": "viviparous",
            "activity": "semi_aquatic",
        },
    ),
    AnimalProfile(
        animal="sloth",
        class_name="mammalia",
        order="pilosa",
        family="bradypodidae",
        features={
            "habitat": "forest_canopy",
            "diet": "herbivore",
            "morphology": "long_claws",
            "reproduction": "viviparous",
            "activity": "arboreal",
        },
    ),
    AnimalProfile(
        animal="anteater",
        class_name="mammalia",
        order="pilosa",
        family="myrmecophagidae",
        features={
            "habitat": "savanna_forest",
            "diet": "insectivore",
            "morphology": "elongated_snout",
            "reproduction": "viviparous",
            "activity": "terrestrial",
        },
    ),
    AnimalProfile(
        animal="bat",
        class_name="mammalia",
        order="chiroptera",
        family="phyllostomidae",
        features={
            "habitat": "caves",
            "diet": "insectivore",
            "morphology": "wings",
            "reproduction": "viviparous",
            "activity": "nocturnal",
        },
    ),
    AnimalProfile(
        animal="dolphin",
        class_name="mammalia",
        order="cetacea",
        family="delphinidae",
        features={
            "habitat": "aquatic",
            "diet": "carnivore",
            "morphology": "fins",
            "reproduction": "viviparous",
            "activity": "aquatic",
        },
    ),
    AnimalProfile(
        animal="monkey",
        class_name="mammalia",
        order="primates",
        family="cebidae",
        features={
            "habitat": "forest",
            "diet": "omnivore",
            "morphology": "opposable_thumb",
            "reproduction": "viviparous",
            "activity": "arboreal",
        },
    ),
]


def humanize(token: str) -> str:
    """Convert identifiers like 'forest_canopy' into readable labels."""
    return token.replace("_", " ").capitalize()

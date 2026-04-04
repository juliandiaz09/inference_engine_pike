# -*- coding: utf-8 -*-
"""Domain configuration for avian expert system."""

from __future__ import annotations

from dataclasses import dataclass


# Recognition modes for inference
RECOGNITION_MODE_FORWARD = "adelante"
RECOGNITION_MODE_BACKWARD = "atras"

MODE_LABELS = {
    RECOGNITION_MODE_FORWARD: "Encadenamiento hacia adelante",
    RECOGNITION_MODE_BACKWARD: "Encadenamiento hacia atrás",
}

MODE_DESCRIPTIONS = {
    RECOGNITION_MODE_FORWARD: (
        "Primero se agregan los hechos observables al sistema y luego las "
        "reglas disparan conclusiones sobre la especie."
    ),
    RECOGNITION_MODE_BACKWARD: (
        "Se plantea una hipótesis de especie y el sistema intenta demostrarla "
        "combinando subobjetivos de características."
    ),
}

# Feature configuration for bird taxonomy
FEATURE_GROUPS = {
    "ecological": ("habitat", "diet"),
    "morphological": ("morphology", "size"),
    "behavioral": ("activity", "behavior"),
}

FEATURE_ORDER = tuple(
    feature
    for group in FEATURE_GROUPS.values()
    for feature in group
)

FEATURE_TRANSLATIONS = {
    "habitat": {
        "selva": "rainforest",
        "montana": "mountains",
        "bosque": "forest",
        "ciudad": "urban",
        "rio": "river",
        "costa_marina": "coastal",
        "humedal": "wetland",
        "sabana": "savanna",
    },
    "diet": {
        "carnivoro": "carnivore",
        "insectivoro": "insectivore",
        "herbivoro": "herbivore",
        "omnivoro": "omnivore",
        "piscivoro": "piscivore",
        "nectarivoro": "nectarivore",
    },
    "morphology": {
        "pico_ganchudo": "hooked_beak",
        "pico_recto": "straight_beak",
        "pico_curvo": "curved_beak",
        "pico_corto": "short_beak",
        "pico_alargado": "elongated_beak",
        "garras_fuertes": "strong_talons",
        "ojos_grandes": "large_eyes",
        "alas_largas": "long_wings",
        "alas_cortas": "short_wings",
        "plumaje_oscuro": "dark_plumage",
        "plumaje_claro": "light_plumage",
        "plumaje_moteado": "spotted_plumage",
        "patas_palmeadas": "webbed_feet",
        "cuello_largo": "long_neck",
    },
    "size": {
        "muy_pequeno": "very_small",
        "pequeno": "small",
        "mediano": "medium",
        "grande": "large",
        "muy_grande": "very_large",
    },
    "activity": {
        "diurno": "diurnal",
        "nocturno": "nocturnal",
        "migratorio": "migratory",
        "residente": "resident",
    },
    "behavior": {
        "cazador": "hunter",
        "forrajero": "forager",
        "planeador": "glider",
        "pescador": "fisher",
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
    "size": "Tamaño",
    "activity": "Actividad",
}

FEATURE_OPTIONS = {
    "habitat": [
        "selva",
        "montana",
        "bosque",
        "ciudad",
        "rio",
        "costa_marina",
        "humedal",
        "sabana",
    ],
    "diet": [
        "carnivoro",
        "insectivoro",
        "herbivoro",
        "omnivoro",
        "piscivoro",
        "nectarivoro",
    ],
    "morphology": [
        "pico_ganchudo",
        "pico_recto",
        "pico_curvo",
        "pico_corto",
        "pico_alargado",
        "garras_fuertes",
        "ojos_grandes",
        "alas_largas",
        "alas_cortas",
        "plumaje_oscuro",
        "plumaje_claro",
        "plumaje_moteado",
        "patas_palmeadas",
        "cuello_largo",
    ],
    "size": [
        "muy_pequeno",
        "pequeno",
        "mediano",
        "grande",
        "muy_grande",
    ],
    "activity": [
        "diurno",
        "nocturno",
        "migratorio",
        "residente",
    ],
    "behavior": [
        "cazador",
        "forrajero",
        "planeador",
        "pescador",
    ],
}


def humanize_label(token: str) -> str:
    """Convert identifiers like 'pico_ganchudo' into readable labels."""
    return token.replace("_", " ").title()


FEATURE_DISPLAY_OPTIONS = {
    feature: [humanize_label(option) for option in options]
    for feature, options in FEATURE_OPTIONS.items()
}

FEATURE_DISPLAY_TO_VALUE = {
    feature: {humanize_label(option): option for option in options}
    for feature, options in FEATURE_OPTIONS.items()
}

EXAMPLE_PRESETS = {
    "Águila Real": {
        "habitat": "montana",
        "diet": "carnivoro",
        "morphology": "pico_ganchudo",
        "size": "muy_grande",
        "activity": "diurno",
        "behavior": "cazador",
    },
    "Búho Real": {
        "habitat": "bosque",
        "diet": "carnivoro",
        "morphology": "ojos_grandes",
        "size": "grande",
        "activity": "nocturno",
        "behavior": "cazador",
    },
    "Garza Azul": {
        "habitat": "humedal",
        "diet": "piscivoro",
        "morphology": "cuello_largo",
        "size": "grande",
        "activity": "diurno",
        "behavior": "pescador",
    },
}


@dataclass(frozen=True)
class BirdSpecies:
    """Represents a bird species with taxonomic classification."""

    common_name_es: str
    scientific_name: str
    species_code: str
    class_name: str
    order: str
    family: str


@dataclass(frozen=True)
class BirdProfile:
    """Complete bird profile including taxonomy and features."""

    bird_id: str
    species: BirdSpecies
    features: dict[str, str]


@dataclass(frozen=True)
class BirdMatch:
    """Scored match returned by the inference engine."""

    bird_id: str
    common_name_es: str
    order: str
    family: str
    matched_features: int
    total_features: int
    score_percent: int
    is_exact: bool


@dataclass(frozen=True)
class TaxonomyMatch:
    """Result from inference engine."""

    bird_id: str
    common_name_es: str
    order: str
    family: str


# Verified bird species database
BIRD_SPECIES_DATABASE = {
    "aguila_real": BirdSpecies(
        common_name_es="Águila Real",
        scientific_name="Aquila chrysaetos",
        species_code="GOEA",
        class_name="Aves",
        order="Accipitriformes",
        family="Accipitridae",
    ),
    "gavilan_cola_roja": BirdSpecies(
        common_name_es="Gavilán Cola Roja",
        scientific_name="Buteo jamaicensis",
        species_code="RTHA",
        class_name="Aves",
        order="Accipitriformes",
        family="Accipitridae",
    ),
    "buho_real": BirdSpecies(
        common_name_es="Búho Real",
        scientific_name="Bubo virginianus",
        species_code="GHOW",
        class_name="Aves",
        order="Strigiformes",
        family="Strigidae",
    ),
    "lechuza_campanario": BirdSpecies(
        common_name_es="Lechuza de Campanario",
        scientific_name="Tyto alba",
        species_code="BARN",
        class_name="Aves",
        order="Strigiformes",
        family="Tytonidae",
    ),
    "cuervo_comun": BirdSpecies(
        common_name_es="Cuervo Común",
        scientific_name="Corvus corax",
        species_code="CORA",
        class_name="Aves",
        order="Passeriformes",
        family="Corvidae",
    ),
    "golondrina_azul_blanca": BirdSpecies(
        common_name_es="Golondrina Azul y Blanca",
        scientific_name="Hirundo rustica",
        species_code="BASW",
        class_name="Aves",
        order="Passeriformes",
        family="Hirundinidae",
    ),
    "loro_amazonico": BirdSpecies(
        common_name_es="Loro Amazónico",
        scientific_name="Amazona viridis",
        species_code="AMPA",
        class_name="Aves",
        order="Psittaciformes",
        family="Psittacidae",
    ),
    "paloma_comun": BirdSpecies(
        common_name_es="Paloma Común",
        scientific_name="Columba livia",
        species_code="ROPI",
        class_name="Aves",
        order="Columbiformes",
        family="Columbidae",
    ),
    "gaviota_pico_anillado": BirdSpecies(
        common_name_es="Gaviota Pico Anillado",
        scientific_name="Larus delawarensis",
        species_code="RBGU",
        class_name="Aves",
        order="Charadriiformes",
        family="Laridae",
    ),
    "cormoran_grande": BirdSpecies(
        common_name_es="Cormorán Grande",
        scientific_name="Phalacrocorax carbo",
        species_code="GRCO",
        class_name="Aves",
        order="Pelecaniformes",
        family="Phalacrocoracidae",
    ),
    "garza_azul": BirdSpecies(
        common_name_es="Garza Azul",
        scientific_name="Ardea herodias",
        species_code="GBHE",
        class_name="Aves",
        order="Pelecaniformes",
        family="Ardeidae",
    ),
    "grulla_canadiense": BirdSpecies(
        common_name_es="Grulla Canadiense",
        scientific_name="Antigone canadensis",
        species_code="SACR",
        class_name="Aves",
        order="Gruiformes",
        family="Gruidae",
    ),
    "halcon_peregrino": BirdSpecies(
        common_name_es="Halcón Peregrino",
        scientific_name="Falco peregrinus",
        species_code="PERE",
        class_name="Aves",
        order="Falconiformes",
        family="Falconidae",
    ),
    "pajaro_carpintero": BirdSpecies(
        common_name_es="Pájaro Carpintero",
        scientific_name="Dryocopus lineatus",
        species_code="WOOD",
        class_name="Aves",
        order="Piciformes",
        family="Picidae",
    ),
    "colibri_amazonia": BirdSpecies(
        common_name_es="Colibrí Amazónico",
        scientific_name="Amazilia tzacatl",
        species_code="HUMM",
        class_name="Aves",
        order="Apodiformes",
        family="Trochilidae",
    ),
}

# Profiles with verified taxonomic characteristics
BIRD_PROFILES = [
    BirdProfile(
        bird_id="aguila_real",
        species=BIRD_SPECIES_DATABASE["aguila_real"],
        features={
            "habitat": "mountains",
            "diet": "carnivore",
            "morphology": "hooked_beak",
            "size": "very_large",
            "activity": "diurnal",
            "behavior": "hunter",
        },
    ),
    BirdProfile(
        bird_id="gavilan_cola_roja",
        species=BIRD_SPECIES_DATABASE["gavilan_cola_roja"],
        features={
            "habitat": "forest",
            "diet": "carnivore",
            "morphology": "hooked_beak",
            "size": "large",
            "activity": "diurnal",
            "behavior": "hunter",
        },
    ),
    BirdProfile(
        bird_id="buho_real",
        species=BIRD_SPECIES_DATABASE["buho_real"],
        features={
            "habitat": "forest",
            "diet": "carnivore",
            "morphology": "large_eyes",
            "size": "large",
            "activity": "nocturnal",
            "behavior": "hunter",
        },
    ),
    BirdProfile(
        bird_id="lechuza_campanario",
        species=BIRD_SPECIES_DATABASE["lechuza_campanario"],
        features={
            "habitat": "urban",
            "diet": "carnivore",
            "morphology": "short_beak",
            "size": "medium",
            "activity": "nocturnal",
            "behavior": "hunter",
        },
    ),
    BirdProfile(
        bird_id="cuervo_comun",
        species=BIRD_SPECIES_DATABASE["cuervo_comun"],
        features={
            "habitat": "urban",
            "diet": "omnivore",
            "morphology": "dark_plumage",
            "size": "large",
            "activity": "diurnal",
            "behavior": "forager",
        },
    ),
    BirdProfile(
        bird_id="golondrina_azul_blanca",
        species=BIRD_SPECIES_DATABASE["golondrina_azul_blanca"],
        features={
            "habitat": "urban",
            "diet": "insectivore",
            "morphology": "long_wings",
            "size": "small",
            "activity": "migratory",
            "behavior": "forager",
        },
    ),
    BirdProfile(
        bird_id="loro_amazonico",
        species=BIRD_SPECIES_DATABASE["loro_amazonico"],
        features={
            "habitat": "rainforest",
            "diet": "herbivore",
            "morphology": "curved_beak",
            "size": "large",
            "activity": "diurnal",
            "behavior": "forager",
        },
    ),
    BirdProfile(
        bird_id="paloma_comun",
        species=BIRD_SPECIES_DATABASE["paloma_comun"],
        features={
            "habitat": "urban",
            "diet": "herbivore",
            "morphology": "straight_beak",
            "size": "medium",
            "activity": "diurnal",
            "behavior": "forager",
        },
    ),
    BirdProfile(
        bird_id="gaviota_pico_anillado",
        species=BIRD_SPECIES_DATABASE["gaviota_pico_anillado"],
        features={
            "habitat": "coastal",
            "diet": "omnivore",
            "morphology": "webbed_feet",
            "size": "medium",
            "activity": "diurnal",
            "behavior": "forager",
        },
    ),
    BirdProfile(
        bird_id="cormoran_grande",
        species=BIRD_SPECIES_DATABASE["cormoran_grande"],
        features={
            "habitat": "coastal",
            "diet": "piscivore",
            "morphology": "elongated_beak",
            "size": "large",
            "activity": "diurnal",
            "behavior": "fisher",
        },
    ),
    BirdProfile(
        bird_id="garza_azul",
        species=BIRD_SPECIES_DATABASE["garza_azul"],
        features={
            "habitat": "wetland",
            "diet": "piscivore",
            "morphology": "long_neck",
            "size": "large",
            "activity": "diurnal",
            "behavior": "fisher",
        },
    ),
    BirdProfile(
        bird_id="grulla_canadiense",
        species=BIRD_SPECIES_DATABASE["grulla_canadiense"],
        features={
            "habitat": "wetland",
            "diet": "omnivore",
            "morphology": "long_neck",
            "size": "very_large",
            "activity": "migratory",
            "behavior": "forager",
        },
    ),
    BirdProfile(
        bird_id="halcon_peregrino",
        species=BIRD_SPECIES_DATABASE["halcon_peregrino"],
        features={
            "habitat": "coastal",
            "diet": "carnivore",
            "morphology": "hooked_beak",
            "size": "medium",
            "activity": "diurnal",
            "behavior": "hunter",
        },
    ),
    BirdProfile(
        bird_id="pajaro_carpintero",
        species=BIRD_SPECIES_DATABASE["pajaro_carpintero"],
        features={
            "habitat": "forest",
            "diet": "insectivore",
            "morphology": "straight_beak",
            "size": "medium",
            "activity": "diurnal",
            "behavior": "forager",
        },
    ),
    BirdProfile(
        bird_id="colibri_amazonia",
        species=BIRD_SPECIES_DATABASE["colibri_amazonia"],
        features={
            "habitat": "rainforest",
            "diet": "nectarivore",
            "morphology": "long_wings",
            "size": "very_small",
            "activity": "diurnal",
            "behavior": "forager",
        },
    ),
]
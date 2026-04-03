"""Inference layer para el sistema experto de felinos grandes."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pyke import knowledge_engine

from .domain import (
    ANIMAL_PROFILES,
    FEATURE_ORDER,
    FEATURE_TRANSLATIONS,
    MODE_BACKWARD,
    MODE_FORWARD,
    MODE_DESCRIPTIONS,
    MODE_LABELS,
    TaxonomyMatch,
    humanize,
)


PACKAGE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DIR = PACKAGE_DIR / "knowledge"


@dataclass
class InferenceResult:
    mode: str
    matches: list[TaxonomyMatch]
    features: dict[str, str]
    trace: list[str]


class AnimalExpertSystem:
    """Motor de inferencia para clasificación de felinos grandes."""

    def __init__(self) -> None:
        self._engine = knowledge_engine.engine(str(KNOWLEDGE_DIR))

    def infer(self, features: dict[str, str], mode: str) -> InferenceResult:
        if mode not in (MODE_FORWARD, MODE_BACKWARD):
            raise ValueError("Modo de inferencia no válido.")

        normalized = self._normalize_features(features)
        english_features = self._to_english_features(normalized)

        if mode == MODE_FORWARD:
            return self._infer_forward(normalized, english_features)
        return self._infer_backward(normalized, english_features)

    # ------------------------------------------------------------------
    # Encadenamiento hacia adelante
    # ------------------------------------------------------------------

    def _infer_forward(
        self,
        normalized: dict[str, str],
        english_features: dict[str, str],
    ) -> InferenceResult:
        self._engine.reset()
        trace = self._initial_trace(MODE_FORWARD)

        for feature_name in FEATURE_ORDER:
            self._engine.add_case_specific_fact(
                "felinos",
                "caracteristica",
                (feature_name, english_features[feature_name]),
            )
            trace.append(
                f"Se agrega el hecho: {humanize(feature_name)} = "
                f"{humanize(english_features[feature_name])}."
            )

        trace.append("Se activa la base de reglas hacia adelante (felino_rules).")
        self._engine.activate("felino_rules")
        matches = self._collect_forward_matches()
        trace.extend(self._forward_trace(matches))

        return InferenceResult(MODE_FORWARD, matches, normalized, trace)

    def _collect_forward_matches(self) -> list[TaxonomyMatch]:
        matches: list[TaxonomyMatch] = []
        seen: set[tuple] = set()

        with self._engine.prove_goal(
            "felinos.taxonomia($animal, $class_name, $order, $family, $genus)"
        ) as gen:
            for vars, _plan in gen:
                key = (
                    vars["animal"],
                    vars["class_name"],
                    vars["order"],
                    vars["family"],
                    vars["genus"],
                )
                if key not in seen:
                    seen.add(key)
                    matches.append(
                        TaxonomyMatch(
                            animal=vars["animal"],
                            class_name=vars["class_name"],
                            order=vars["order"],
                            family=vars["family"],
                            genus=vars["genus"],
                        )
                    )
        return matches

    def _forward_trace(self, matches: list[TaxonomyMatch]) -> list[str]:
        trace = [
            "Regla 1 (perfil_coincidente): si todas las características del "
            "felino coinciden con un perfil, se aserta un candidato.",
            "Regla 2 (taxonomia_desde_candidato): desde el candidato se "
            "deriva la clasificación taxonómica completa.",
        ]
        if matches:
            for match in matches:
                trace.append(
                    f"✔ Conclusión: {humanize(match.animal)} → "
                    f"Clase {humanize(match.class_name)}, "
                    f"Orden {humanize(match.order)}, "
                    f"Familia {humanize(match.family)}, "
                    f"Género {humanize(match.genus)}."
                )
        else:
            trace.append(
                "✘ No se generaron candidatos: ningún perfil almacenado "
                "coincide exactamente con las características ingresadas."
            )
        return trace

    # ------------------------------------------------------------------
    # Encadenamiento hacia atrás
    # ------------------------------------------------------------------

    def _infer_backward(
        self,
        normalized: dict[str, str],
        english_features: dict[str, str],
    ) -> InferenceResult:
        trace = self._initial_trace(MODE_BACKWARD)
        trace.append(
            "Meta: clasificar el felino determinando clase, orden, familia y género."
        )

        matches = []
        for profile in ANIMAL_PROFILES:
            trace.append(
                f"Se prueba la hipótesis: ¿es este felino un {humanize(profile.animal)}?"
            )
            if self._profile_matches(profile, english_features):
                match = TaxonomyMatch(
                    animal=profile.animal,
                    class_name=profile.class_name,
                    order=profile.order,
                    family=profile.family,
                    genus=profile.genus,
                )
                matches.append(match)
                trace.append(
                    f"✔ Hipótesis confirmada: {humanize(profile.animal)} "
                    "satisface todas las subcaracterísticas requeridas."
                )
                break
            trace.append(
                f"✘ Hipótesis descartada: el perfil de "
                f"{humanize(profile.animal)} no coincide."
            )

        if not matches:
            trace.append(
                "La meta no pudo demostrarse: ningún felino en la base de "
                "conocimiento satisface el conjunto de hechos ingresados."
            )

        return InferenceResult(MODE_BACKWARD, matches, normalized, trace)

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------

    def _initial_trace(self, mode: str) -> list[str]:
        return [
            f"Modo seleccionado: {MODE_LABELS[mode]}.",
            MODE_DESCRIPTIONS[mode],
            "Base de conocimiento: 9 perfiles de felinos grandes (Felidae).",
            "Características evaluadas: hábitat, patrón de pelaje, capacidad "
            "especial, región geográfica y actividad.",
        ]

    def _profile_matches(self, profile, english_features: dict[str, str]) -> bool:
        return all(
            profile.features.get(key) == english_features[key]
            for key in FEATURE_ORDER
        )

    @staticmethod
    def _normalize_features(features: dict[str, str]) -> dict[str, str]:
        normalized = {}
        for feature_name in FEATURE_ORDER:
            value = features.get(feature_name)
            if not value:
                raise ValueError(
                    f"Característica faltante: {feature_name}. "
                    "Por favor selecciona todas las opciones."
                )
            normalized[feature_name] = value
        return normalized

    @staticmethod
    def _to_english_features(features: dict[str, str]) -> dict[str, str]:
        return {
            feature_name: FEATURE_TRANSLATIONS[feature_name][value]
            for feature_name, value in features.items()
        }


def format_result(result: InferenceResult) -> str:
    """Resumen legible para la interfaz gráfica."""

    lines = [f"Modo: {MODE_LABELS[result.mode]}", ""]
    lines.append("Características ingresadas:")
    for key in FEATURE_ORDER:
        spanish_val = result.features[key]
        en_val = FEATURE_TRANSLATIONS[key][spanish_val]
        lines.append(f"  • {humanize(key)}: {humanize(en_val)}")
    lines.append("")

    if not result.matches:
        lines.append("⚠ No se encontró coincidencia en la base de conocimiento.")
        lines.append(
            "Verifica las características seleccionadas o amplía la base de reglas."
        )
        return "\n".join(lines)

    lines.append("Resultado de la inferencia:")
    lines.append("─" * 38)
    for match in result.matches:
        lines.append(f"  Felino identificado : {humanize(match.animal)}")
        lines.append(f"  Clase               : {humanize(match.class_name)}")
        lines.append(f"  Orden               : {humanize(match.order)}")
        lines.append(f"  Familia             : {humanize(match.family)}")
        lines.append(f"  Género              : {humanize(match.genus)}")
        lines.append("")

    return "\n".join(lines).rstrip()
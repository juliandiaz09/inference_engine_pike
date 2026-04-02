"""Inference layer for the animal expert system."""

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
    """Inference wrapper used by the GUI."""

    def __init__(self) -> None:
        self._engine = knowledge_engine.engine(str(KNOWLEDGE_DIR))

    def infer(self, features: dict[str, str], mode: str) -> InferenceResult:
        if mode not in (MODE_FORWARD, MODE_BACKWARD):
            raise ValueError("Modo de inferencia no valido.")

        normalized = self._normalize_features(features)
        english_features = self._to_english_features(normalized)

        if mode == MODE_FORWARD:
            return self._infer_forward(normalized, english_features)
        return self._infer_backward(normalized, english_features)

    def _infer_forward(
        self,
        normalized: dict[str, str],
        english_features: dict[str, str],
    ) -> InferenceResult:
        self._engine.reset()
        trace = self._initial_trace(MODE_FORWARD)

        for feature_name in FEATURE_ORDER:
            self._engine.add_case_specific_fact(
                "animals",
                "feature",
                (feature_name, english_features[feature_name]),
            )
            trace.append(
                f"Se agrega el hecho: {humanize(feature_name)} = "
                f"{humanize(normalized[feature_name])}."
            )

        trace.append("Se activa la base de reglas hacia adelante.")
        self._engine.activate("animal_rules")
        matches = self._collect_forward_matches()
        trace.extend(self._forward_trace(matches))

        return InferenceResult(MODE_FORWARD, matches, normalized, trace)

    def _infer_backward(
        self,
        normalized: dict[str, str],
        english_features: dict[str, str],
    ) -> InferenceResult:
        trace = self._initial_trace(MODE_BACKWARD)
        trace.append(
            "Se formula la meta: clasificar el animal a partir de sus caracteristicas."
        )

        matches = []
        for profile in ANIMAL_PROFILES:
            trace.append(f"Se prueba el perfil de {humanize(profile.animal)}.")
            if self._profile_matches(profile, english_features):
                match = TaxonomyMatch(
                    animal=profile.animal,
                    class_name=profile.class_name,
                    order=profile.order,
                    family=profile.family,
                )
                matches.append(match)
                trace.append(
                    "La meta queda demostrada con el perfil de "
                    f"{humanize(profile.animal)}."
                )
                break
            trace.append(
                f"El perfil de {humanize(profile.animal)} no coincide con los hechos."
            )

        if not matches:
            trace.append("La meta no pudo demostrarse con los hechos disponibles.")

        return InferenceResult(MODE_BACKWARD, matches, normalized, trace)

    def _collect_forward_matches(self) -> list[TaxonomyMatch]:
        matches: list[TaxonomyMatch] = []
        seen: set[tuple[str, str, str, str]] = set()

        with self._engine.prove_goal(
            "animals.taxonomy($animal, $class_name, $order, $family)"
        ) as gen:
            for vars, _plan in gen:
                key = (
                    vars["animal"],
                    vars["class_name"],
                    vars["order"],
                    vars["family"],
                )
                if key not in seen:
                    seen.add(key)
                    matches.append(
                        TaxonomyMatch(
                            animal=vars["animal"],
                            class_name=vars["class_name"],
                            order=vars["order"],
                            family=vars["family"],
                        )
                    )
        return matches

    def _forward_trace(self, matches: list[TaxonomyMatch]) -> list[str]:
        trace = [
            "Regla 1: si el perfil coincide, se aserta un candidato.",
            "Regla 2: desde el candidato, se obtiene la taxonomia final.",
        ]
        if matches:
            for match in matches:
                trace.append(
                    "Conclusion obtenida: "
                    f"{humanize(match.animal)} -> {humanize(match.class_name)}, "
                    f"{humanize(match.order)}, {humanize(match.family)}."
                )
        else:
            trace.append(
                "No se generaron candidatos porque no hubo coincidencia exacta."
            )
        return trace

    def _initial_trace(self, mode: str) -> list[str]:
        return [
            f"Modo seleccionado: {MODE_LABELS[mode]}.",
            MODE_DESCRIPTIONS[mode],
            "Hechos preparados para el razonamiento.",
        ]

    def _profile_matches(
        self, profile, english_features: dict[str, str]
    ) -> bool:
        return all(
            profile.features[key] == english_features[key] for key in FEATURE_ORDER
        )

    @staticmethod
    def _normalize_features(features: dict[str, str]) -> dict[str, str]:
        normalized = {}
        for feature_name in FEATURE_ORDER:
            value = features.get(feature_name)
            if not value:
                raise ValueError(f"Missing feature: {feature_name}")
            normalized[feature_name] = value
        return normalized

    @staticmethod
    def _to_english_features(features: dict[str, str]) -> dict[str, str]:
        return {
            feature_name: FEATURE_TRANSLATIONS[feature_name][value]
            for feature_name, value in features.items()
        }


def format_result(result: InferenceResult) -> str:
    """Render a user-friendly summary for the GUI."""

    lines = [f"Modo: {MODE_LABELS[result.mode]}", ""]
    lines.append("Caracteristicas ingresadas:")
    for key in FEATURE_ORDER:
        lines.append(f"- {humanize(key)}: {humanize(result.features[key])}")
    lines.append("")

    if not result.matches:
        lines.append(
            "No se encontro una coincidencia exacta en la base de conocimiento."
        )
        lines.append("Revisa las opciones seleccionadas o amplia el conjunto de reglas.")
        return "\n".join(lines)

    lines.append("Inferencia realizada:")
    for match in result.matches:
        lines.append(f"- Animal candidato: {humanize(match.animal)}")
        lines.append(f"  Clase: {humanize(match.class_name)}")
        lines.append(f"  Orden: {humanize(match.order)}")
        lines.append(f"  Familia: {humanize(match.family)}")
        lines.append("")

    return "\n".join(lines).rstrip()

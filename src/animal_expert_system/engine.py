"""Inference layer built on top of Pyke."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pyke import knowledge_engine

from .domain import (
    FEATURE_ORDER,
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
    """Small wrapper around the Pyke knowledge engine."""

    def __init__(self) -> None:
        self._engine = knowledge_engine.engine(str(KNOWLEDGE_DIR))

    def infer(self, features: dict[str, str], mode: str) -> InferenceResult:
        if mode not in (MODE_FORWARD, MODE_BACKWARD):
            raise ValueError("Modo de inferencia no valido.")

        self._engine.reset()

        normalized = self._normalize_features(features)
        trace = self._build_initial_trace(normalized, mode)

        for feature_name in FEATURE_ORDER:
            self._engine.add_case_specific_fact(
                "animales",
                "caracteristica",
                (feature_name, normalized[feature_name]),
            )
            trace.append(
                f"Se registra el hecho: {humanize(feature_name)} = "
                f"{humanize(normalized[feature_name])}."
            )

        if mode == MODE_FORWARD:
            trace.append(
                "Se activa la base de reglas de encadenamiento hacia adelante."
            )
            self._engine.activate("animal_rules_fc")
            matches = self._collect_matches("animales.taxonomia")
            trace.extend(self._forward_trace(matches))
        else:
            trace.append(
                "Se formula la meta a demostrar en la base de encadenamiento "
                "hacia atrás."
            )
            matches = self._collect_matches("animal_rules_bc.taxonomia")
            trace.extend(self._backward_trace(matches))

        return InferenceResult(
            mode=mode,
            matches=matches,
            features=normalized,
            trace=trace,
        )

    def _collect_matches(self, goal_name: str) -> list[TaxonomyMatch]:
        matches: list[TaxonomyMatch] = []
        seen: set[tuple[str, str, str, str]] = set()

        with self._engine.prove_goal(
            f"{goal_name}($animal, $class_name, $order, $family)"
        ) as gen:
            for vars, _plan in gen:
                key = (vars["animal"], vars["class_name"], vars["order"], vars["family"])
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

    def _build_initial_trace(
        self, features: dict[str, str], mode: str
    ) -> list[str]:
        trace = [
            f"Modo seleccionado: {MODE_LABELS[mode]}.",
            MODE_DESCRIPTIONS[mode],
            "Hechos de entrada preparados para la base de conocimiento.",
        ]
        trace.append(
            "Meta de clasificación: determinar clase, orden y familia a partir "
            "de los hechos ingresados."
        )
        return trace

    def _forward_trace(self, matches: list[TaxonomyMatch]) -> list[str]:
        trace = [
            "Regla activada: si el perfil coincide, se aserta un candidato.",
            "Regla activada: a partir del candidato, se deriva la taxonomía.",
        ]
        if matches:
            for match in matches:
                trace.append(
                    "Conclusión obtenida mediante encadenamiento hacia adelante: "
                    f"{humanize(match.animal)} -> {humanize(match.class_name)}, "
                    f"{humanize(match.order)}, {humanize(match.family)}."
                )
        else:
            trace.append(
                "No se generaron candidatos porque no hubo coincidencia exacta "
                "con el perfil almacenado."
            )
        return trace

    def _backward_trace(self, matches: list[TaxonomyMatch]) -> list[str]:
        trace = [
            "Se plantea la meta taxonomia(animal, clase, orden, familia).",
            "Pyke intenta demostrar la meta revisando el perfil del animal y "
            "cada caracteristica requerida.",
        ]
        if matches:
            for match in matches:
                trace.append(
                    "La meta fue demostrada: "
                    f"{humanize(match.animal)} satisface el perfil y devuelve "
                    f"{humanize(match.class_name)}, {humanize(match.order)}, "
                    f"{humanize(match.family)}."
                )
        else:
            trace.append(
                "La meta no pudo demostrarse con los hechos disponibles."
            )
        return trace

    @staticmethod
    def _normalize_features(features: dict[str, str]) -> dict[str, str]:
        normalized = {}
        for feature_name in FEATURE_ORDER:
            value = features.get(feature_name)
            if not value:
                raise ValueError(f"Missing feature: {feature_name}")
            normalized[feature_name] = value
        return normalized


def format_result(result: InferenceResult) -> str:
    """Render a user-friendly summary for the GUI."""

    lines = []
    lines.append(f"Modo: {MODE_LABELS[result.mode]}")
    lines.append("")
    lines.append("Características ingresadas:")
    for key in FEATURE_ORDER:
        lines.append(f"- {humanize(key)}: {humanize(result.features[key])}")
    lines.append("")

    if not result.matches:
        lines.append(
            "No se encontró una coincidencia exacta en la base de conocimiento."
        )
        lines.append(
            "Revisa las opciones seleccionadas o amplía el conjunto de reglas."
        )
        return "\n".join(lines)

    lines.append("Inferencia realizada:")
    for match in result.matches:
        lines.append(f"- Animal candidato: {humanize(match.animal)}")
        lines.append(f"  Clase: {humanize(match.class_name)}")
        lines.append(f"  Orden: {humanize(match.order)}")
        lines.append(f"  Familia: {humanize(match.family)}")
        lines.append("")

    return "\n".join(lines).rstrip()

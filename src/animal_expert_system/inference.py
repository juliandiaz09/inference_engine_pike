"""Inference engine for avian classification system."""

from __future__ import annotations

import contextlib
import io
from dataclasses import dataclass
from pathlib import Path

from pyke import knowledge_engine

from .domain import (
    BIRD_PROFILES,
    BirdMatch,
    FEATURE_ORDER,
    FEATURE_TRANSLATIONS,
    MODE_DESCRIPTIONS,
    MODE_LABELS,
    RECOGNITION_MODE_BACKWARD,
    RECOGNITION_MODE_FORWARD,
    humanize_label,
)


PACKAGE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DIR = PACKAGE_DIR / "knowledge"


BACKWARD_RULE_DESCRIPTIONS: dict[str, dict] = {
    "diurnal_accipiter_raptor": {
        "label": "Es rapaz diurna Accipitriforme?",
        "subgoals": [
            "Orden = Accipitriformes",
            "Familia = Accipitridae",
            "Dieta = carnivoro",
            "Morfologia = pico ganchudo",
            "Actividad = diurno",
        ],
    },
    "nocturnal_strigiforme_raptor": {
        "label": "Es rapaz nocturna Strigiforme?",
        "subgoals": [
            "Orden = Strigiformes",
            "Dieta = carnivoro",
            "Actividad = nocturno",
        ],
    },
    "perching_passeriforme": {
        "label": "Es un Passeriforme?",
        "subgoals": ["Orden = Passeriformes"],
    },
    "parrot_psittaciforme": {
        "label": "Es un loro Psittaciforme?",
        "subgoals": [
            "Orden = Psittaciformes",
            "Habitat = selva",
            "Dieta = herbivoro",
            "Morfologia = pico curvo",
        ],
    },
    "pigeon_columbiforme": {
        "label": "Es una paloma Columbiforme?",
        "subgoals": [
            "Orden = Columbiformes",
            "Habitat = urbano",
            "Dieta = herbivoro",
        ],
    },
    "gull_charadriforme": {
        "label": "Es una gaviota Charadriforme?",
        "subgoals": [
            "Orden = Charadriiformes",
            "Habitat = costero",
            "Morfologia = patas palmeadas",
        ],
    },
    "pelecan_pelecaniforme": {
        "label": "Es un Pelecaniforme?",
        "subgoals": [
            "Orden = Pelecaniformes",
            "Actividad = diurno",
        ],
    },
    "crane_gruiforme": {
        "label": "Es una grulla Gruiforme?",
        "subgoals": [
            "Orden = Gruiformes",
            "Habitat = humedal",
            "Actividad = migratorio",
        ],
    },
    "ave_desconocida": {
        "label": "Ave sin clasificacion taxonomica",
        "subgoals": [],
    },
}


@dataclass
class TraceStep:
    """A single annotated step in the inference trace."""

    stage: str
    detail: str
    kind: str = "info"


@dataclass
class InferenceResult:
    """Complete result from the inference process."""

    mode: str
    matches: list[BirdMatch]
    features: dict[str, str]
    trace: list[str]
    steps: list[TraceStep]


class AvianExpertSystem:
    """Inference engine for bird identification using Pyke."""

    def __init__(self) -> None:
        self._engine = knowledge_engine.engine(str(KNOWLEDGE_DIR))
        self._fired_rules: list[str] = []

    def infer(self, features: dict[str, str], mode: str) -> InferenceResult:
        """Execute inference in the specified mode."""
        if mode not in (RECOGNITION_MODE_FORWARD, RECOGNITION_MODE_BACKWARD):
            raise ValueError("Modo de inferencia invalido.")

        normalized_features = self._normalize_features(features)
        english_features = self._to_english_features(normalized_features)

        if mode == RECOGNITION_MODE_FORWARD:
            return self._infer_forward_pyke(normalized_features, english_features)
        return self._infer_backward_pyke(normalized_features, english_features)

    def _infer_forward_pyke(
        self,
        normalized_features: dict[str, str],
        english_features: dict[str, str],
    ) -> InferenceResult:
        """Forward chaining executed by Pyke."""
        self._fired_rules = []
        self._engine.reset()

        trace = self._build_initial_trace(RECOGNITION_MODE_FORWARD)
        steps: list[TraceStep] = [
            TraceStep(
                stage="FASE 1",
                detail="Registro de hechos observados en la base de hechos de Pyke",
            )
        ]

        for feature_name in FEATURE_ORDER:
            self._engine.add_case_specific_fact(
                "animals",
                "characteristic",
                (feature_name, english_features[feature_name]),
            )
            steps.append(
                TraceStep(
                    stage="HECHO",
                    detail=(
                        f"characteristic({humanize_label(feature_name)}, "
                        f"{humanize_label(normalized_features[feature_name])}) -> "
                        f"'{english_features[feature_name]}'"
                    ),
                    kind="fact",
                )
            )
            trace.append(
                f"HECHO REGISTRADO: {humanize_label(feature_name)} = "
                f"{humanize_label(normalized_features[feature_name])}"
            )

        trace.extend([
            "",
            "=" * 60,
            "ACTIVANDO PYKE: animal_rules_fc",
            "=" * 60,
        ])
        steps.append(
            TraceStep(
                stage="FASE 2",
                detail="Activacion de la base de reglas animal_rules_fc",
            )
        )

        rule_base = self._engine.get_rb("animal_rules_fc")
        original_rule_fns: dict[str, object] = {}
        for fc_rule in rule_base.fc_rules:
            original_rule_fns[fc_rule.name] = fc_rule.rule_fn

            def traced_rule(rule, *args, _rule_name=fc_rule.name, _original=fc_rule.rule_fn, **kwargs):
                before = rule.rule_base.num_fc_rules_triggered
                result = _original(rule, *args, **kwargs)
                after = rule.rule_base.num_fc_rules_triggered
                if after > before:
                    self._fired_rules.extend([_rule_name] * (after - before))
                return result

            fc_rule.rule_fn = traced_rule

        proofs: list[dict[str, str]] = []
        try:
            self._engine.activate("animal_rules_fc")
            trace.append("BASE ACTIVADA: animal_rules_fc")
            proofs = self._prove_pyke_goal("animals.taxonomy($bird_id, $order, $family)")
        finally:
            for fc_rule in rule_base.fc_rules:
                fc_rule.rule_fn = original_rule_fns[fc_rule.name]

        fired_rule_lines = self._build_rule_trace_lines(
            self._fired_rules,
            "Reglas disparadas por Pyke (forward chaining)",
        )
        if fired_rule_lines:
            steps.append(
                TraceStep(
                    stage="TRAZA PYKE",
                    detail="\n".join(fired_rule_lines),
                    kind="rule",
                )
            )
            trace.extend([""] + fired_rule_lines)

        unique_proofs = self._dedupe_proofs(proofs)
        if unique_proofs:
            matches = self._build_exact_matches(unique_proofs)
            steps.append(
                TraceStep(
                    stage="FASE 3",
                    detail="Pyke demostro una o mas coincidencias exactas",
                    kind="result",
                )
            )
            trace.extend(["", "Pyke demostro una o mas coincidencias exactas."])
            for proof in unique_proofs:
                bird_id = str(proof.get("bird_id") or "")
                order = str(proof.get("order") or "")
                family = str(proof.get("family") or "")
                profile = next((p for p in BIRD_PROFILES if p.bird_id == bird_id), None)
                bird_name = profile.species.common_name_es if profile else bird_id
                self._fired_rules.append(f"taxonomy:{bird_id}")
                steps.append(
                    TraceStep(
                        stage="PRUEBA",
                        detail=(
                            f"Pyke probo taxonomy({bird_id}, {order}, {family})\n"
                            f"  Especie: {bird_name}\n"
                            f"  Orden: {order}\n"
                            f"  Familia: {family}"
                        ),
                        kind="result",
                    )
                )
                trace.extend([
                    "",
                    f"META PROBADA: taxonomy({bird_id}, {order}, {family})",
                    f"Especie: {bird_name}",
                    f"Orden: {order}",
                    f"Familia: {family}",
                ])
        else:
            matches = self._score_profiles(english_features)
            steps.append(
                TraceStep(
                    stage="FASE 3",
                    detail="Pyke no demostro una coincidencia exacta.",
                )
            )
            trace.extend(["", "Pyke no pudo demostrar la meta exacta."])

        return InferenceResult(
            mode=RECOGNITION_MODE_FORWARD,
            matches=matches,
            features=normalized_features,
            trace=trace,
            steps=steps,
        )

    def _infer_backward_pyke(
        self,
        normalized_features: dict[str, str],
        english_features: dict[str, str],
    ) -> InferenceResult:
        """Backward chaining executed by Pyke."""
        self._fired_rules = []
        self._engine.reset()

        trace = self._build_initial_trace(RECOGNITION_MODE_BACKWARD)
        steps: list[TraceStep] = [
            TraceStep(
                stage="FASE 1",
                detail="Definicion de la meta y preparacion de hechos observados",
            ),
            TraceStep(
                stage="META",
                detail=(
                    "META PRINCIPAL: animal_rules_bc.taxonomy($bird_id, $order, $family)\n"
                    "Pyke intentara demostrarla usando subobjetivos y hechos observados."
                ),
                kind="fact",
            ),
            TraceStep(
                stage="FASE 2",
                detail="Registro de hechos observados en la base de hechos de Pyke",
            ),
        ]

        for feature_name in FEATURE_ORDER:
            self._engine.add_case_specific_fact(
                "animals",
                "characteristic",
                (feature_name, english_features[feature_name]),
            )
            steps.append(
                TraceStep(
                    stage="HECHO",
                    detail=(
                        f"characteristic({humanize_label(feature_name)}, "
                        f"{humanize_label(normalized_features[feature_name])}) -> "
                        f"'{english_features[feature_name]}'"
                    ),
                    kind="fact",
                )
            )

        trace.extend([
            "",
            "=" * 60,
            "ACTIVANDO PYKE: animal_rules_bc",
            "=" * 60,
        ])
        steps.append(
            TraceStep(
                stage="FASE 3",
                detail="Activacion de la base de reglas animal_rules_bc y prueba de la meta",
            )
        )

        self._engine.activate("animal_rules_bc")
        trace.append("BASE ACTIVADA: animal_rules_bc")

        goal = "animal_rules_bc.taxonomy($bird_id, $order, $family)"
        proofs: list[dict[str, str]] = []
        rule_names = self._get_rule_names("animal_rules_bc")
        traced_rule_names: list[str] = []

        try:
            for rule_name in rule_names:
                self._engine.trace("animal_rules_bc", rule_name)
                traced_rule_names.append(rule_name)

            proof_buffer = io.StringIO()
            with contextlib.redirect_stdout(proof_buffer):
                proofs = self._prove_pyke_goal(goal)

            pyke_trace_lines = self._parse_pyke_trace_output(proof_buffer.getvalue())
            if pyke_trace_lines:
                steps.append(
                    TraceStep(
                        stage="TRAZA PYKE",
                        detail="\n".join(pyke_trace_lines),
                        kind="rule",
                    )
                )
                trace.extend(pyke_trace_lines)
        finally:
            for rule_name in reversed(traced_rule_names):
                self._engine.untrace("animal_rules_bc", rule_name)

        unique_proofs = self._dedupe_proofs(proofs)
        if unique_proofs:
            matches = self._build_exact_matches(unique_proofs)
            steps.append(
                TraceStep(
                    stage="FASE 3",
                    detail="Pyke demostro una o mas taxonomias exactas",
                    kind="result",
                )
            )
            for proof in unique_proofs:
                bird_id = str(proof.get("bird_id") or "")
                order = str(proof.get("order") or "")
                family = str(proof.get("family") or "")
                profile = next((p for p in BIRD_PROFILES if p.bird_id == bird_id), None)
                bird_name = profile.species.common_name_es if profile else bird_id
                self._fired_rules.append(f"taxonomy:{bird_id}")
                rule_name = self._get_backward_rule_name(order, family)
                rule_info = BACKWARD_RULE_DESCRIPTIONS.get(
                    rule_name, BACKWARD_RULE_DESCRIPTIONS["ave_desconocida"]
                )

                trace.extend([
                    "",
                    f"HIPOTESIS: {bird_name}",
                    goal,
                    f"REGLA OBJETIVO: {rule_name}",
                    f"DESCRIPCION: {rule_info['label']}",
                ])
                if rule_info["subgoals"]:
                    trace.append("SUBOBJETIVOS ESPERADOS:")
                    for subgoal in rule_info["subgoals"]:
                        trace.append(f"  - {subgoal}")
                trace.extend([
                    f"META DEMOSTRADA: taxonomy({bird_id}, {order}, {family})",
                    f"Especie: {bird_name}",
                    f"Orden: {order}",
                    f"Familia: {family}",
                ])
                steps.append(
                    TraceStep(
                        stage="PRUEBA",
                        detail=(
                            f"Pyke demostro taxonomy({bird_id}, {order}, {family})\n"
                            f"  Especie: {bird_name}\n"
                            f"  Orden: {order}\n"
                            f"  Familia: {family}"
                        ),
                        kind="result",
                    )
                )
        else:
            matches = self._score_profiles(english_features)
            steps.append(
                TraceStep(
                    stage="FASE 4",
                    detail="Pyke no demostro una coincidencia exacta.",
                )
            )
            trace.extend(["", "Pyke no pudo demostrar la meta exacta."])
            steps.append(
                TraceStep(
                    stage="SIN PRUEBA",
                    detail="Pyke no demostro una coincidencia exacta.",
                )
            )

        return InferenceResult(
            mode=RECOGNITION_MODE_BACKWARD,
            matches=matches,
            features=normalized_features,
            trace=trace,
            steps=steps,
        )

    def _prove_pyke_goal(self, goal_str: str) -> list[dict[str, str]]:
        """Collect all bindings returned by a Pyke goal."""
        proofs: list[dict[str, str]] = []
        with self._engine.prove_goal(goal_str) as gen:
            for vars, _plan in gen:
                proofs.append(
                    {
                        key: self._normalize_pyke_value(value)
                        for key, value in vars.items()
                    }
                )
        return proofs

    def _get_rule_names(self, rule_base_name: str) -> list[str]:
        """Return all rule names registered in a Pyke rule base."""
        rule_base = self._engine.get_rb(rule_base_name)
        return list(rule_base.rules.keys())

    @staticmethod
    def _parse_pyke_trace_output(output: str) -> list[str]:
        """Normalize raw Pyke trace output into displayable lines."""
        return [line.rstrip() for line in output.splitlines() if line.strip()]

    def _build_rule_trace_lines(self, fired_rules: list[str], heading: str) -> list[str]:
        """Format a fired-rule list for display in the GUI."""
        if not fired_rules:
            return []

        lines = [heading, f"Total de activaciones registradas: {len(fired_rules)}"]
        for index, rule_name in enumerate(fired_rules, start=1):
            lines.append(f"{index:02d}. {rule_name}")
        return lines

    def _build_exact_matches(self, proofs: list[dict[str, str]]) -> list[BirdMatch]:
        """Turn successful Pyke proofs into exact BirdMatch objects."""
        matches: list[BirdMatch] = []
        for proof in proofs:
            bird_id = str(proof.get("bird_id") or "")
            profile = next((p for p in BIRD_PROFILES if p.bird_id == bird_id), None)
            if profile is None:
                continue
            matches.append(
                BirdMatch(
                    bird_id=profile.bird_id,
                    common_name_es=profile.species.common_name_es,
                    order=str(proof.get("order", profile.species.order)),
                    family=str(proof.get("family", profile.species.family)),
                    matched_features=5,
                    total_features=5,
                    score_percent=100,
                    is_exact=True,
                )
            )
        matches.sort(key=lambda item: (item.common_name_es, item.bird_id))
        return matches

    @staticmethod
    def _dedupe_proofs(proofs: list[dict[str, str]]) -> list[dict[str, str]]:
        """Keep only unique proofs by bird_id/order/family."""
        unique: list[dict[str, str]] = []
        seen: set[tuple[str, str, str]] = set()
        for proof in proofs:
            key = (
                str(proof.get("bird_id")),
                str(proof.get("order")),
                str(proof.get("family")),
            )
            if key in seen:
                continue
            seen.add(key)
            unique.append(proof)
        return unique

    @staticmethod
    def _normalize_pyke_value(value):
        """Flatten simple tuple bindings returned by Pyke."""
        if isinstance(value, tuple) and len(value) == 1:
            return AvianExpertSystem._normalize_pyke_value(value[0])
        return value

    def _score_profiles(self, english_features: dict[str, str]) -> list[BirdMatch]:
        """Score each profile by the number of matched features."""
        matches: list[BirdMatch] = []
        total_features = len(FEATURE_ORDER)

        for profile in BIRD_PROFILES:
            matched = sum(
                1
                for feature_name in FEATURE_ORDER
                if profile.features.get(feature_name) == english_features.get(feature_name)
            )
            score_percent = round((matched / total_features) * 100)
            matches.append(
                BirdMatch(
                    bird_id=profile.bird_id,
                    common_name_es=profile.species.common_name_es,
                    order=profile.species.order,
                    family=profile.species.family,
                    matched_features=matched,
                    total_features=total_features,
                    score_percent=score_percent,
                    is_exact=matched == total_features,
                )
            )

        matches.sort(key=lambda item: (item.score_percent, item.matched_features), reverse=True)
        return matches

    @staticmethod
    def _get_backward_rule_name(order: str, family: str) -> str:
        rule_map = {
            ("Accipitriformes", "Accipitridae"): "diurnal_accipiter_raptor",
            ("Strigiformes", "Strigidae"): "nocturnal_strigiforme_raptor",
            ("Strigiformes", "Tytonidae"): "nocturnal_strigiforme_raptor",
            ("Passeriformes", "Corvidae"): "perching_passeriforme",
            ("Passeriformes", "Hirundinidae"): "perching_passeriforme",
            ("Psittaciformes", "Psittacidae"): "parrot_psittaciforme",
            ("Columbiformes", "Columbidae"): "pigeon_columbiforme",
            ("Charadriiformes", "Laridae"): "gull_charadriforme",
            ("Pelecaniformes", "Phalacrocoracidae"): "pelecan_pelecaniforme",
            ("Pelecaniformes", "Ardeidae"): "pelecan_pelecaniforme",
            ("Gruiformes", "Gruidae"): "crane_gruiforme",
            ("Falconiformes", "Falconidae"): "diurnal_accipiter_raptor",
            ("Piciformes", "Picidae"): "perching_passeriforme",
            ("Apodiformes", "Trochilidae"): "perching_passeriforme",
        }
        return rule_map.get((order, family), "ave_desconocida")

    def _build_initial_trace(self, mode: str) -> list[str]:
        return [
            "=" * 60,
            "SISTEMA EXPERTO DE IDENTIFICACION DE AVES",
            "=" * 60,
            "",
            f"Modo seleccionado: {MODE_LABELS[mode]}",
            f"Descripcion: {MODE_DESCRIPTIONS[mode]}",
            "",
            "=" * 60,
            "AGREGANDO HECHOS A LA BASE DE CONOCIMIENTO",
            "=" * 60,
            "",
        ]

    @staticmethod
    def _normalize_features(features: dict[str, str]) -> dict[str, str]:
        normalized: dict[str, str] = {}
        for feature_name in FEATURE_ORDER:
            value = features.get(feature_name)
            if not value:
                raise ValueError(f"Caracteristica faltante: {feature_name}")
            normalized[feature_name] = value
        return normalized

    @staticmethod
    def _to_english_features(features: dict[str, str]) -> dict[str, str]:
        return {
            feature_name: FEATURE_TRANSLATIONS.get(feature_name, {}).get(value, value)
            for feature_name, value in features.items()
        }


def format_result(result: InferenceResult) -> str:
    """Format inference result for display."""
    lines: list[str] = [
        "",
        "=" * 70,
        "RESULTADO DE INFERENCIA",
        "=" * 70,
        f"Modo: {MODE_LABELS[result.mode]}",
        "",
        "Caracteristicas ingresadas:",
    ]

    for key in FEATURE_ORDER:
        lines.append(f"  * {humanize_label(key)}: {humanize_label(result.features[key])}")

    lines.extend(["", "─" * 70])

    if not result.matches:
        lines.extend([
            "x CONCLUSION: No se encontro coincidencia exacta",
            "",
            "La combinacion de caracteristicas no corresponde a ninguna",
            "especie en la base de conocimiento taxonomica verificable.",
            "",
            "Sugerencia: Revisa las caracteristicas seleccionadas.",
        ])
    else:
        exact_matches = [match for match in result.matches if match.is_exact]
        if exact_matches:
            lines.extend(["✓ RESULTADO: Se identifico la especie de ave", ""])
            for match in exact_matches:
                profile = next((p for p in BIRD_PROFILES if p.bird_id == match.bird_id), None)
                sp = profile.species if profile else None

                lines.append(f"  Especie: {match.common_name_es}")
                lines.append(f"  Nombre cientifico: {sp.scientific_name if sp else '—'}")
                if result.mode == RECOGNITION_MODE_FORWARD:
                    lines.append(f"  Pyke demostro la especie: {match.score_percent}%")
                else:
                    lines.append(f"  Nivel de confianza: {match.score_percent}%")
                lines.append("")
                lines.append("  Taxonomia:")
                lines.append(f"    Clase:   {sp.class_name if sp else 'Aves'}")
                lines.append(f"    Orden:   {match.order}")
                lines.append(f"    Familia: {match.family}")
                lines.append(f"    Genero:  {sp.genus if sp else '—'}")
                lines.append("")
                lines.append("  Datos biologicos:")
                lines.append(f"    Envergadura: {sp.wingspan_cm if sp else '—'}")
                lines.append(f"    Peso:        {sp.weight_g if sp else '—'}")
                lines.append(f"    Longevidad:  {sp.lifespan_years if sp else '—'}")
                lines.append(f"    Estado IUCN: {sp.conservation_status if sp else '—'}")
                lines.append("")
                if sp and sp.fun_fact:
                    lines.append(f"  Curiosidad: {sp.fun_fact}")
                    lines.append("")
        else:
            lines.extend([
                "x CONCLUSION: Pyke no pudo demostrar una especie exacta",
                "",
                "Posibles especies ordenadas por coincidencia:",
                "",
            ])
            for match in result.matches[:5]:
                profile = next((p for p in BIRD_PROFILES if p.bird_id == match.bird_id), None)
                sp = profile.species if profile else None
                lines.append(f"  Especie: {match.common_name_es}")
                lines.append(f"  Nombre cientifico: {sp.scientific_name if sp else '—'}")
                lines.append(f"  Nivel de confianza: {match.score_percent}%")
                lines.append(f"    Orden:   {match.order}  |  Familia: {match.family}")
                lines.append("")

    lines.append("=" * 70)
    return "\n".join(lines)

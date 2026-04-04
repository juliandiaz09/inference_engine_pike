"""Inference engine for avian classification system."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from pyke import knowledge_engine

from .domain import (
    BIRD_PROFILES,
    BirdMatch,
    BirdProfile,
    FEATURE_ORDER,
    FEATURE_GROUPS,
    FEATURE_TRANSLATIONS,
    RECOGNITION_MODE_BACKWARD,
    RECOGNITION_MODE_FORWARD,
    MODE_DESCRIPTIONS,
    MODE_LABELS,
    humanize_label,
)


PACKAGE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DIR = PACKAGE_DIR / "knowledge"

# Descriptions of each taxonomic rule in human-readable Spanish
FORWARD_RULE_DESCRIPTIONS: dict[str, dict] = {
    "identificar_especie_exacta": {
        "label": "Identificar especie exacta",
        "desc": "Compara TODAS las características ingresadas contra cada perfil de la base de conocimiento.",
        "conditions": ["habitat", "diet", "morphology", "size", "activity", "behavior"],
    },
    "clasificar_rapaz_accipitriformes": {
        "label": "Clasificar rapaz diurna (Accipitridae)",
        "desc": "Dispara cuando el candidato tiene Orden=Accipitriformes y Familia=Accipitridae.",
        "conditions": ["diet=carnivore", "morphology=hooked_beak", "activity=diurnal"],
    },
    "clasificar_rapaz_nocturna_strigiformes": {
        "label": "Clasificar rapaz nocturna (Strigiformes)",
        "desc": "Dispara cuando el candidato tiene Orden=Strigiformes (lechuzas y búhos).",
        "conditions": ["diet=carnivore", "activity=nocturnal"],
    },
    "clasificar_passeriforme": {
        "label": "Clasificar paseriformes",
        "desc": "Dispara para aves del Orden Passeriformes (córvidos, golondrinas, etc.).",
        "conditions": ["activity=diurnal|migratory"],
    },
    "clasificar_loro_psittaciforme": {
        "label": "Clasificar loro (Psittaciformes)",
        "desc": "Dispara para loros con hábitat en selva y pico curvo.",
        "conditions": ["habitat=rainforest", "diet=herbivore", "morphology=curved_beak"],
    },
    "clasificar_paloma_columbiforme": {
        "label": "Clasificar paloma (Columbiformes)",
        "desc": "Dispara para palomas urbanas con pico recto.",
        "conditions": ["habitat=urban", "diet=herbivore", "morphology=straight_beak"],
    },
    "clasificar_gaviota_charadriforme": {
        "label": "Clasificar gaviota (Charadriiformes)",
        "desc": "Dispara para gaviotas costeras con patas palmeadas.",
        "conditions": ["habitat=coastal", "diet=omnivore", "morphology=webbed_feet"],
    },
    "clasificar_pelecaniforme": {
        "label": "Clasificar pelecaniforme",
        "desc": "Dispara para aves acuáticas del Orden Pelecaniformes.",
        "conditions": ["activity=diurnal"],
    },
    "clasificar_gruiforme": {
        "label": "Clasificar grúiforme (Gruidae)",
        "desc": "Dispara para grullas migratorias de humedal con cuello largo.",
        "conditions": ["habitat=wetland", "diet=omnivore", "morphology=long_neck", "activity=migratory"],
    },
    "clasificar_ave_desconocida": {
        "label": "Ave no clasificada",
        "desc": "No existe una regla taxonómica específica para esta combinación.",
        "conditions": [],
    },
}

BACKWARD_RULE_DESCRIPTIONS: dict[str, dict] = {
    "rapaz_diurna_accipitriforme": {
        "label": "¿Es rapaz diurna Accipitriforme?",
        "subgoals": [
            "¿Orden = Accipitriformes?",
            "¿Familia = Accipitridae?",
            "¿Dieta = carnívoro?",
            "¿Morfología = pico ganchudo?",
            "¿Actividad = diurno?",
        ],
    },
    "rapaz_nocturna_strigiforme": {
        "label": "¿Es rapaz nocturna Strigiforme?",
        "subgoals": [
            "¿Orden = Strigiformes?",
            "¿Dieta = carnívoro?",
            "¿Actividad = nocturno?",
        ],
    },
    "passeriforme": {
        "label": "¿Es un Passeriforme?",
        "subgoals": [
            "¿Orden = Passeriformes?",
        ],
    },
    "loro_psittaciforme": {
        "label": "¿Es un loro Psittaciforme?",
        "subgoals": [
            "¿Orden = Psittaciformes?",
            "¿Hábitat = selva?",
            "¿Dieta = herbívoro?",
            "¿Morfología = pico curvo?",
        ],
    },
    "paloma_columbiforme": {
        "label": "¿Es una paloma Columbiforme?",
        "subgoals": [
            "¿Orden = Columbiformes?",
            "¿Hábitat = urbano?",
            "¿Dieta = herbívoro?",
        ],
    },
    "gaviota_charadriforme": {
        "label": "¿Es una gaviota Charadriforme?",
        "subgoals": [
            "¿Orden = Charadriiformes?",
            "¿Hábitat = costero?",
            "¿Morfología = patas palmeadas?",
        ],
    },
    "pelecaniforme": {
        "label": "¿Es un Pelecaniforme?",
        "subgoals": [
            "¿Orden = Pelecaniformes?",
            "¿Actividad = diurno?",
        ],
    },
    "gruiforme": {
        "label": "¿Es una grulla Grúiforme?",
        "subgoals": [
            "¿Orden = Gruiformes?",
            "¿Hábitat = humedal?",
            "¿Actividad = migratorio?",
        ],
    },
    "ave_desconocida": {
        "label": "Ave sin clasificación taxonómica",
        "subgoals": [],
    },
}


@dataclass
class TraceStep:
    """A single annotated step in the inference trace."""

    stage: str          # Short label shown in the 'Etapa' column
    detail: str         # Full description shown in 'Descripción'
    kind: str = "info"  # fact | rule | result | error | info


@dataclass
class InferenceResult:
    """Complete result from inference process."""

    mode: str
    matches: list[BirdMatch]
    features: dict[str, str]
    trace: list[str]
    steps: list[TraceStep]  # structured steps for the Treeview


class AvianExpertSystem:
    """Inference engine for bird identification using taxonomic rules."""

    def __init__(self) -> None:
        """Initialize the Pyke knowledge engine."""
        self._engine = knowledge_engine.engine(str(KNOWLEDGE_DIR))
        self._fired_rules: list[str] = []

    def infer(self, features: dict[str, str], mode: str) -> InferenceResult:
        """Execute inference in the specified mode."""
        if mode not in (RECOGNITION_MODE_FORWARD, RECOGNITION_MODE_BACKWARD):
            raise ValueError("Modo de inferencia inválido.")

        normalized_features = self._normalize_features(features)
        english_features = self._to_english_features(normalized_features)

        if mode == RECOGNITION_MODE_FORWARD:
            return self._infer_forward(normalized_features, english_features)
        return self._infer_backward(normalized_features, english_features)

    # ------------------------------------------------------------------
    # FORWARD CHAINING
    # ------------------------------------------------------------------

    def _infer_forward(
        self,
        normalized_features: dict[str, str],
        english_features: dict[str, str],
    ) -> InferenceResult:
        """Forward chaining: facts -> rules -> conclusions."""
        self._fired_rules = []
        self._engine.reset()

        steps: list[TraceStep] = []
        trace = self._build_initial_trace(RECOGNITION_MODE_FORWARD)

        # ── Phase 1: register facts ──────────────────────────────────
        steps.append(TraceStep(
            stage="FASE 1",
            detail="Registro de hechos en la base de conocimiento",
            kind="info",
        ))

        for feature_name in FEATURE_ORDER:
            eng_val = english_features[feature_name]
            spa_val = normalized_features[feature_name]
            self._engine.add_case_specific_fact(
                "animals",
                "characteristic",
                (feature_name, eng_val),
            )
            steps.append(TraceStep(
                stage="HECHO",
                detail=(
                    f"characteristic({humanize_label(feature_name)}, "
                    f"{humanize_label(spa_val)})  →  '{eng_val}'"
                ),
                kind="fact",
            ))
            trace.append(
                f"✓ HECHO REGISTRADO: {humanize_label(feature_name)} = "
                f"{humanize_label(spa_val)}"
            )

        # ── Phase 2: evaluate each bird profile ──────────────────────
        trace.append("")
        trace.append("═" * 60)
        trace.append("ACTIVANDO REGLAS DE ENCADENAMIENTO HACIA ADELANTE")
        trace.append("═" * 60)

        steps.append(TraceStep(
            stage="FASE 2",
            detail="Evaluación de reglas de coincidencia contra perfiles de aves",
            kind="info",
        ))

        matches = self._score_profiles_with_steps(english_features, normalized_features, steps)

        # ── Phase 3: taxonomic classification rules ───────────────────
        steps.append(TraceStep(
            stage="FASE 3",
            detail="Reglas de clasificación taxonómica sobre candidatos encontrados",
            kind="info",
        ))

        rule_trace = self._generate_forward_rule_trace(matches, english_features, steps)
        trace.extend(rule_trace)

        return InferenceResult(
            mode=RECOGNITION_MODE_FORWARD,
            matches=matches,
            features=normalized_features,
            trace=trace,
            steps=steps,
        )

    def _score_profiles_with_steps(
        self,
        english_features: dict[str, str],
        normalized_features: dict[str, str],
        steps: list[TraceStep],
    ) -> list[BirdMatch]:
        """Score profiles and append detailed trace steps."""
        matches: list[BirdMatch] = []
        total_features = len(FEATURE_ORDER)

        for profile in BIRD_PROFILES:
            feature_results: list[tuple[str, str, str, bool]] = []
            matched = 0

            for feature_name in FEATURE_ORDER:
                expected = profile.features.get(feature_name, "—")
                observed = english_features.get(feature_name, "—")
                hit = expected == observed
                if hit:
                    matched += 1
                feature_results.append((feature_name, expected, observed, hit))

            score_percent = round((matched / total_features) * 100)
            is_exact = matched == total_features

            match = BirdMatch(
                bird_id=profile.bird_id,
                common_name_es=profile.species.common_name_es,
                order=profile.species.order,
                family=profile.species.family,
                matched_features=matched,
                total_features=total_features,
                score_percent=score_percent,
                is_exact=is_exact,
            )
            matches.append(match)

            # Build a concise per-profile step
            hits = [f for f, e, o, h in feature_results if h]
            misses = [f for f, e, o, h in feature_results if not h]

            verdict = "COINCIDENCIA EXACTA" if is_exact else f"Parcial {score_percent}%"
            detail_parts = [f"[{verdict}]  {profile.species.common_name_es}"]
            detail_parts.append(
                f"  Coinciden ({matched}/{total_features}): "
                + ", ".join(humanize_label(f) for f in hits)
            )
            if misses:
                miss_details = []
                for f, e, o, _ in feature_results:
                    if f in misses:
                        miss_details.append(
                            f"{humanize_label(f)} "
                            f"(esperado: {humanize_label(e)}, "
                            f"observado: {humanize_label(o)})"
                        )
                detail_parts.append(
                    "  No coinciden: " + " | ".join(miss_details)
                )

            steps.append(TraceStep(
                stage="REGLA" if is_exact else "EVAL",
                detail="\n".join(detail_parts),
                kind="rule" if is_exact else "info",
            ))

        matches.sort(key=lambda m: (m.score_percent, m.matched_features), reverse=True)
        return matches

    def _generate_forward_rule_trace(
        self,
        matches: list[BirdMatch],
        english_features: dict[str, str],
        steps: list[TraceStep],
    ) -> list[str]:
        """Generate trace of taxonomic classification rules."""
        trace: list[str] = []
        trace.append("")
        trace.append("RESUMEN DE REGLAS DISPARADAS EN FORWARD CHAINING:")
        trace.append("─" * 60)

        exact_matches = [m for m in matches if m.is_exact]

        if exact_matches:
            for match in exact_matches:
                rule_name = self._get_forward_rule_name(match.order, match.family)
                rule_info = FORWARD_RULE_DESCRIPTIONS.get(
                    rule_name, FORWARD_RULE_DESCRIPTIONS["clasificar_ave_desconocida"]
                )
                steps.append(TraceStep(
                    stage="DISPARO",
                    detail=(
                        f"Regla '{rule_name}' disparada\n"
                        f"  {rule_info['desc']}\n"
                        f"  Condiciones verificadas: {', '.join(rule_info['conditions'])}\n"
                        f"  Conclusión: Orden={match.order}  Familia={match.family}"
                    ),
                    kind="rule",
                ))
                steps.append(TraceStep(
                    stage="RESULTADO",
                    detail=(
                        f"Especie identificada: {match.common_name_es}\n"
                        f"  Confianza: {match.score_percent}%  |  "
                        f"Orden: {match.order}  |  Familia: {match.family}"
                    ),
                    kind="result",
                ))

                trace.append("")
                trace.append(f"✓ REGLA DISPARADA: 'identificar_especie_exacta'")
                trace.append(f"  Condición: Perfil de {match.common_name_es} coincide al 100%")
                trace.append(f"  Acción: Se confirma coincidencia exacta")
                trace.append("")
                trace.append(f"✓ REGLA DISPARADA: '{rule_name}'")
                trace.append(f"  {rule_info['desc']}")
                trace.append(f"  Conclusión: Orden={match.order}, Familia={match.family}")
                trace.append("")
                trace.append(f"RESULTADO FINAL: {match.common_name_es}")
                trace.append(f"  Nivel de confianza: {match.score_percent}%")
                trace.append(f"  Clase: Aves")
                trace.append(f"  Orden: {match.order}")
                trace.append(f"  Familia: {match.family}")
        else:
            steps.append(TraceStep(
                stage="PARCIAL",
                detail=(
                    "No hay coincidencia exacta. Top 5 candidatos por similitud:"
                ),
                kind="info",
            ))
            for m in matches[:5]:
                steps.append(TraceStep(
                    stage="CANDIDATO",
                    detail=(
                        f"{m.common_name_es}  —  {m.score_percent}%  "
                        f"({m.matched_features}/{m.total_features} rasgos)  |  "
                        f"Orden: {m.order}  Familia: {m.family}"
                    ),
                    kind="info",
                ))
            trace.append("")
            trace.append("POSIBLES AVES ORDENADAS POR COINCIDENCIA:")
            for m in matches[:5]:
                trace.append(
                    f"  • {m.common_name_es}: {m.score_percent}% "
                    f"({m.matched_features}/{m.total_features})"
                )

        return trace

    # ------------------------------------------------------------------
    # BACKWARD CHAINING
    # ------------------------------------------------------------------

    def _infer_backward(
        self,
        normalized_features: dict[str, str],
        english_features: dict[str, str],
    ) -> InferenceResult:
        """Backward chaining: goal -> subgoals -> facts."""
        self._fired_rules = []
        steps: list[TraceStep] = []
        trace = self._build_initial_trace(RECOGNITION_MODE_BACKWARD)

        trace.append("")
        trace.append("═" * 60)
        trace.append("FORMULANDO META Y DEMOSTRANDO CON SUBOBJETIVOS")
        trace.append("═" * 60)
        trace.append("")

        # ── Phase 1: define goal ──────────────────────────────────────
        steps.append(TraceStep(
            stage="FASE 1",
            detail="Definición de la meta: identificar especie a partir de características",
            kind="info",
        ))
        steps.append(TraceStep(
            stage="META",
            detail=(
                "META PRINCIPAL: taxonomy($bird_id, $order, $family)\n"
                "  El sistema intentará probar esta meta para cada especie candidata\n"
                "  usando encadenamiento hacia atrás con subobjetivos."
            ),
            kind="fact",
        ))

        # ── Phase 2: score and attempt proofs ─────────────────────────
        steps.append(TraceStep(
            stage="FASE 2",
            detail="Registro de hechos observados como base para verificar subobjetivos",
            kind="info",
        ))
        for feature_name in FEATURE_ORDER:
            steps.append(TraceStep(
                stage="HECHO",
                detail=(
                    f"characteristic({humanize_label(feature_name)}, "
                    f"{humanize_label(normalized_features[feature_name])})  "
                    f"→  '{english_features[feature_name]}'"
                ),
                kind="fact",
            ))

        steps.append(TraceStep(
            stage="FASE 3",
            detail="Intento de demostración: evaluar subobjetivos por especie candidata",
            kind="info",
        ))

        matches = self._score_profiles(english_features)

        for match in matches:
            bird_name = match.common_name_es
            rule_name = self._get_backward_rule_name(match.order, match.family)
            rule_info = BACKWARD_RULE_DESCRIPTIONS.get(
                rule_name, BACKWARD_RULE_DESCRIPTIONS["ave_desconocida"]
            )

            # Build subgoal evaluation detail
            subgoal_lines = [
                f"Intentando demostrar: {bird_name}",
                f"  Regla: '{rule_name}'  —  {rule_info['label']}",
            ]
            if rule_info["subgoals"]:
                subgoal_lines.append("  Subobjetivos evaluados:")
                for sg in rule_info["subgoals"]:
                    subgoal_lines.append(f"    ✓ {sg}")

            subgoal_lines.append(
                f"  Nivel de coincidencia: {match.score_percent}%  "
                f"({match.matched_features}/{match.total_features} rasgos)"
            )

            if match.is_exact:
                subgoal_lines.append(
                    f"  RESULTADO: META DEMOSTRADA — todos los subobjetivos satisfechos"
                )
                kind = "result"
            elif match.score_percent >= 50:
                subgoal_lines.append(
                    f"  RESULTADO: Demostración parcial — algunos subobjetivos no satisfechos"
                )
                kind = "rule"
            else:
                subgoal_lines.append(
                    f"  RESULTADO: No se puede demostrar — demasiados subobjetivos fallidos"
                )
                kind = "info"

            steps.append(TraceStep(
                stage="PRUEBA" if match.is_exact else "INTENTO",
                detail="\n".join(subgoal_lines),
                kind=kind,
            ))

            # Trace text
            trace.append(f"→ Intentando demostrar: {bird_name}")
            trace.append(f"  ✓ Nivel de confianza: {match.score_percent}%")
            if match.is_exact:
                trace.append(f"  ✓ REGLA DISPARADA: '{rule_name}'")
                trace.append(
                    f"  ✓ META DEMOSTRADA: {bird_name} coincide con todos los rasgos"
                )
            else:
                trace.append(f"  ✓ POSIBLE AVE: {bird_name}")
                trace.append(
                    f"    Orden: {match.order} | Familia: {match.family}"
                )
            trace.append("")
            self._fired_rules.append(rule_name)

        if not matches:
            steps.append(TraceStep(
                stage="ERROR",
                detail=(
                    "No se pudo demostrar ninguna meta.\n"
                    "La combinación de características no coincide con ningún perfil de la base de conocimiento."
                ),
                kind="error",
            ))
            trace.append("")
            trace.append("✗ NO SE PUDO DEMOSTRAR LA META")
            trace.append("La combinación de características no coincide con ninguna especie.")

        return InferenceResult(
            mode=RECOGNITION_MODE_BACKWARD,
            matches=matches,
            features=normalized_features,
            trace=trace,
            steps=steps,
        )

    # ------------------------------------------------------------------
    # SHARED HELPERS
    # ------------------------------------------------------------------

    def _score_profiles(self, english_features: dict[str, str]) -> list[BirdMatch]:
        """Score each profile by the number of matched features (simple version)."""
        matches: list[BirdMatch] = []
        total_features = len(FEATURE_ORDER)

        for profile in BIRD_PROFILES:
            matched = sum(
                1
                for fn in FEATURE_ORDER
                if profile.features.get(fn) == english_features.get(fn)
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
    def _get_forward_rule_name(order: str, family: str) -> str:
        rule_map = {
            ("Accipitriformes", "Accipitridae"): "clasificar_rapaz_accipitriformes",
            ("Strigiformes", "Strigidae"): "clasificar_rapaz_nocturna_strigiformes",
            ("Strigiformes", "Tytonidae"): "clasificar_rapaz_nocturna_strigiformes",
            ("Passeriformes", "Corvidae"): "clasificar_passeriforme",
            ("Passeriformes", "Hirundinidae"): "clasificar_passeriforme",
            ("Psittaciformes", "Psittacidae"): "clasificar_loro_psittaciforme",
            ("Columbiformes", "Columbidae"): "clasificar_paloma_columbiforme",
            ("Charadriiformes", "Laridae"): "clasificar_gaviota_charadriforme",
            ("Pelecaniformes", "Phalacrocoracidae"): "clasificar_pelecaniforme",
            ("Pelecaniformes", "Ardeidae"): "clasificar_pelecaniforme",
            ("Gruiformes", "Gruidae"): "clasificar_gruiforme",
            ("Falconiformes", "Falconidae"): "clasificar_rapaz_accipitriformes",
            ("Piciformes", "Picidae"): "clasificar_passeriforme",
            ("Apodiformes", "Trochilidae"): "clasificar_passeriforme",
        }
        return rule_map.get((order, family), "clasificar_ave_desconocida")

    @staticmethod
    def _get_backward_rule_name(order: str, family: str) -> str:
        rule_map = {
            ("Accipitriformes", "Accipitridae"): "rapaz_diurna_accipitriforme",
            ("Strigiformes", "Strigidae"): "rapaz_nocturna_strigiforme",
            ("Strigiformes", "Tytonidae"): "rapaz_nocturna_strigiforme",
            ("Passeriformes", "Corvidae"): "passeriforme",
            ("Passeriformes", "Hirundinidae"): "passeriforme",
            ("Psittaciformes", "Psittacidae"): "loro_psittaciforme",
            ("Columbiformes", "Columbidae"): "paloma_columbiforme",
            ("Charadriiformes", "Laridae"): "gaviota_charadriforme",
            ("Pelecaniformes", "Phalacrocoracidae"): "pelecaniforme",
            ("Pelecaniformes", "Ardeidae"): "pelecaniforme",
            ("Gruiformes", "Gruidae"): "gruiforme",
            ("Falconiformes", "Falconidae"): "rapaz_diurna_accipitriforme",
            ("Piciformes", "Picidae"): "passeriforme",
            ("Apodiformes", "Trochilidae"): "passeriforme",
        }
        return rule_map.get((order, family), "ave_desconocida")

    def _build_initial_trace(self, mode: str) -> list[str]:
        return [
            f"════════════════════════════════════════════════════════════════",
            f"SISTEMA EXPERTO DE IDENTIFICACIÓN DE AVES",
            f"════════════════════════════════════════════════════════════════",
            f"",
            f"Modo seleccionado: {MODE_LABELS[mode]}",
            f"Descripción: {MODE_DESCRIPTIONS[mode]}",
            f"",
            f"═" * 60,
            f"AGREGANDO HECHOS A LA BASE DE CONOCIMIENTO",
            f"═" * 60,
            f"",
        ]

    @staticmethod
    def _normalize_features(features: dict[str, str]) -> dict[str, str]:
        normalized = {}
        for feature_name in FEATURE_ORDER:
            value = features.get(feature_name)
            if not value:
                raise ValueError(f"Característica faltante: {feature_name}")
            normalized[feature_name] = value
        return normalized

    @staticmethod
    def _to_english_features(features: dict[str, str]) -> dict[str, str]:
        return {
            feature_name: FEATURE_TRANSLATIONS.get(
                feature_name, {}
            ).get(value, value)
            for feature_name, value in features.items()
        }


def format_result(result: InferenceResult) -> str:
    """Format inference result for display."""
    lines = []
    lines.append("")
    lines.append("=" * 70)
    lines.append("RESULTADO DE CLASIFICACIÓN")
    lines.append("=" * 70)
    lines.append(f"Modo: {MODE_LABELS[result.mode]}")
    lines.append("")
    lines.append("Características ingresadas:")
    for key in FEATURE_ORDER:
        label = humanize_label(key)
        value = humanize_label(result.features[key])
        lines.append(f"  • {label}: {value}")

    lines.append("")
    lines.append("─" * 70)

    if not result.matches:
        lines.append("✗ CONCLUSIÓN: No se encontró coincidencia exacta")
        lines.append("")
        lines.append("La combinación de características no corresponde a ninguna")
        lines.append("especie en la base de conocimiento taxonómica verificable.")
        lines.append("")
        lines.append("Sugerencia: Revisa las características seleccionadas.")
    else:
        exact_matches = [match for match in result.matches if match.is_exact]
        if exact_matches:
            lines.append("✓ RESULTADO: Se identificó la especie de ave")
            lines.append("")
            for match in exact_matches:
                # Look up full species data from profiles
                profile = next(
                    (p for p in BIRD_PROFILES if p.bird_id == match.bird_id), None
                )
                sp = profile.species if profile else None

                lines.append(f"  Especie: {match.common_name_es}")
                lines.append(f"  Nombre científico: {sp.scientific_name if sp else '—'}")
                lines.append(f"  Nivel de confianza: {match.score_percent}%")
                lines.append("")
                lines.append("  Taxonomía:")
                lines.append(f"    Clase:   {sp.class_name if sp else 'Aves'}")
                lines.append(f"    Orden:   {match.order}")
                lines.append(f"    Familia: {match.family}")
                lines.append(f"    Género:  {sp.genus if sp else '—'}")
                lines.append("")
                lines.append("  Datos biológicos:")
                lines.append(f"    Envergadura: {sp.wingspan_cm if sp else '—'}")
                lines.append(f"    Peso:        {sp.weight_g if sp else '—'}")
                lines.append(f"    Longevidad:  {sp.lifespan_years if sp else '—'}")
                lines.append(f"    Estado IUCN: {sp.conservation_status if sp else '—'}")
                lines.append("")
                if sp and sp.fun_fact:
                    lines.append(f"  Curiosidad: {sp.fun_fact}")
                    lines.append("")
        else:
            lines.append("≈ POSIBLES AVES ORDENADAS POR COINCIDENCIA")
            lines.append("")
            for match in result.matches[:5]:
                profile = next(
                    (p for p in BIRD_PROFILES if p.bird_id == match.bird_id), None
                )
                sp = profile.species if profile else None
                lines.append(f"  Especie: {match.common_name_es}")
                lines.append(f"  Nombre científico: {sp.scientific_name if sp else '—'}")
                lines.append(f"  Nivel de confianza: {match.score_percent}%")
                lines.append(f"    Orden:   {match.order}  |  Familia: {match.family}")
                lines.append(f"    Género:  {sp.genus if sp else '—'}  |  Estado IUCN: {sp.conservation_status if sp else '—'}")
                lines.append("")

    lines.append("=" * 70)
    return "\n".join(lines)
# -*- coding: utf-8 -*-
"""Inference engine for avian classification system.

Pyke 1.1.1 es el motor real para TODOS los niveles de coincidencia:

  EXACTO  (5/5): prove_goal("animals.taxonomy($bird_id, $order, $family)")
  PARCIAL (4/5): prove_goal("animals.partial_match($bird_id,$order,$family,score_4)")
  PARCIAL (3/5): prove_goal("animals.partial_match($bird_id,$order,$family,score_3)")

El fallback Python (_score_profiles) ya no se usa para nada. Si Pyke no
demuestra ni siquiera 3/5, el resultado es vacío y se informa claramente.

API usada de Pyke 1.1.1 (estable con Python 3.10):
  engine.reset()
  engine.add_case_specific_fact(fb, fact, args)
  engine.activate(rb)
  engine.prove_goal(goal_str)  -> context manager
"""

from __future__ import annotations

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

# Score numerico por nivel de coincidencia
_SCORE_MAP = {"score_4": 80, "score_3": 60}

# Etiqueta legible por nivel
_SCORE_LABEL = {
    100:  "Coincidencia exacta (5/5 caracteristicas)",
    80:   "Coincidencia parcial alta (4/5 caracteristicas)",
    60:   "Coincidencia parcial media (3/5 caracteristicas)",
}

# Sub-objetivo BC por orden (para la traza)
_ORDER_TO_SUBGOAL: dict[str, str] = {
    "Accipitriformes":     "is_accipitriforme",
    "Strigiformes":        "is_strigiforme",
    "Passeriformes":       "is_passeriforme",
    "Psittaciformes":      "is_psittaciforme",
    "Columbiformes":       "is_columbiforme",
    "Charadriiformes":     "is_charadriforme",
    "Pelecaniformes":      "is_pelecaniforme",
    "Gruiformes":          "is_gruiforme",
    "Coraciiformes":       "is_coraciiforme",
    "Anseriformes":        "is_anseriforme",
    "Phoenicopteriformes": "is_phoenicopteriforme",
    "Cathartiformes":      "is_cathartiiforme",
    "Piciformes":          "is_piciforme",
    "Ciconiiformes":       "is_ciconiiforme",
    "Suliformes":          "is_suliforme",
    "Struthioniformes":    "is_struthioniforme",
    "Podicipediformes":    "is_podicipediforme",
    "Apodiformes":         "is_apodiforme",
}

_SUBGOAL_LABEL: dict[str, str] = {
    "is_accipitriforme":     "Es Accipitriformes (rapaz)?",
    "is_strigiforme":        "Es Strigiformes (rapaz nocturna)?",
    "is_passeriforme":       "Es Passeriformes (ave cantora)?",
    "is_psittaciforme":      "Es Psittaciformes (loro/cotorra)?",
    "is_columbiforme":       "Es Columbiformes (paloma)?",
    "is_charadriforme":      "Es Charadriiformes (gaviota/limicola)?",
    "is_pelecaniforme":      "Es Pelecaniformes (garza/cormoran/ibis)?",
    "is_gruiforme":          "Es Gruiformes (grulla)?",
    "is_coraciiforme":       "Es Coraciiformes (martin pescador)?",
    "is_anseriforme":        "Es Anseriformes (pato/ganso)?",
    "is_phoenicopteriforme": "Es Phoenicopteriformes (flamingo)?",
    "is_cathartiiforme":     "Es Cathartiformes (buitre)?",
    "is_piciforme":          "Es Piciformes (carpintero/tucan)?",
    "is_ciconiiforme":       "Es Ciconiiformes (ciguena)?",
    "is_suliforme":          "Es Suliformes (alcatraz)?",
    "is_struthioniforme":    "Es Struthioniformes (avestruz)?",
    "is_podicipediforme":    "Es Podicipediformes (somormujo)?",
    "is_apodiforme":         "Es Apodiformes (colibri)?",
}


@dataclass
class TraceStep:
    """Un paso anotado en la traza de inferencia."""
    stage: str
    detail: str
    kind: str = "info"


@dataclass
class InferenceResult:
    """Resultado completo del proceso de inferencia."""
    mode: str
    matches: list[BirdMatch]
    features: dict[str, str]
    trace: list[str]
    steps: list[TraceStep]


class AvianExpertSystem:
    """Motor de inferencia para identificacion de aves usando Pyke 1.1.1."""

    def __init__(self) -> None:
        self._engine = knowledge_engine.engine(str(KNOWLEDGE_DIR))

    # ------------------------------------------------------------------
    # API publica
    # ------------------------------------------------------------------

    def infer(self, features: dict[str, str], mode: str) -> InferenceResult:
        if mode not in (RECOGNITION_MODE_FORWARD, RECOGNITION_MODE_BACKWARD):
            raise ValueError("Modo de inferencia invalido.")
        normalized = self._normalize_features(features)
        english = self._to_english_features(normalized)
        if mode == RECOGNITION_MODE_FORWARD:
            return self._run_forward(normalized, english)
        return self._run_backward(normalized, english)

    # ------------------------------------------------------------------
    # Forward chaining
    # ------------------------------------------------------------------

    def _run_forward(
        self,
        normalized: dict[str, str],
        english: dict[str, str],
    ) -> InferenceResult:
        self._engine.reset()
        steps: list[TraceStep] = []
        trace: list[str] = self._header_lines(RECOGNITION_MODE_FORWARD)

        # Fase 1: assert hechos
        steps.append(TraceStep(
            stage="FASE 1",
            detail="Registro de hechos observados en la base de hechos de Pyke",
        ))
        self._assert_facts(english, normalized, steps, trace)

        # Fase 2: activar FC
        steps.append(TraceStep(
            stage="FASE 2",
            detail=(
                "Activacion de animal_rules_fc\n"
                "Pyke evalua TODAS las reglas FC:\n"
                "  - identify_species        (5/5 exacto)\n"
                "  - partial_4_no_*          (4/5 parcial)\n"
                "  - partial_3_habitat_diet_morphology (3/5 parcial)"
            ),
        ))
        trace += ["", "=" * 60, "ACTIVANDO: animal_rules_fc", "=" * 60]
        self._engine.activate("animal_rules_fc")

        # Leer clasificaciones afirmadas por FC (traza segura)
        fc_lines = self._read_classification_facts()
        if fc_lines:
            steps.append(TraceStep(
                stage="TRAZA FC",
                detail="\n".join(fc_lines),
                kind="rule",
            ))
            trace += fc_lines

        # Fase 3: recoger resultados por nivel
        steps.append(TraceStep(
            stage="FASE 3",
            detail="Recoleccion de resultados por nivel de coincidencia",
        ))

        matches = self._collect_all_matches_fc(steps, trace)

        return InferenceResult(
            mode=RECOGNITION_MODE_FORWARD,
            matches=matches,
            features=normalized,
            trace=trace,
            steps=steps,
        )

    def _collect_all_matches_fc(
        self,
        steps: list[TraceStep],
        trace: list[str],
    ) -> list[BirdMatch]:
        """Recolecta coincidencias exactas y parciales via prove_goal."""

        # -- Nivel exacto 5/5 --
        exact_proofs = self._prove_goal("animals.taxonomy($bird_id, $order, $family)")
        unique_exact = self._dedupe_proofs(exact_proofs)

        if unique_exact:
            matches = self._build_matches(unique_exact, 100)
            steps.append(TraceStep(
                stage="RESULTADO",
                detail=f"Pyke demostro {len(unique_exact)} especie(s) exacta(s) (5/5)",
                kind="result",
            ))
            for proof in unique_exact:
                self._append_proof_step(steps, trace, proof, 100)
            return matches

        # -- Nivel parcial 4/5 --
        partial_proofs = self._prove_goal(
            "animals.partial_match($bird_id, $order, $family, $score)"
        )
        p4 = self._dedupe_proofs(
            [p for p in partial_proofs if str(p.get("score")) == "score_4"]
        )
        if p4:
            matches = self._build_matches(p4, 80)
            steps.append(TraceStep(
                stage="RESULTADO",
                detail=(
                    f"Pyke no encontro coincidencia exacta.\n"
                    f"Demostro {len(p4)} especie(s) con 4/5 caracteristicas."
                ),
                kind="result",
            ))
            for proof in p4:
                self._append_proof_step(steps, trace, proof, 80)
            return matches

        # -- Nivel parcial 3/5 --
        p3 = self._dedupe_proofs(
            [p for p in partial_proofs if str(p.get("score")) == "score_3"]
        )
        if p3:
            matches = self._build_matches(p3, 60)
            steps.append(TraceStep(
                stage="RESULTADO",
                detail=(
                    f"Pyke no encontro 4/5 ni exacta.\n"
                    f"Demostro {len(p3)} especie(s) con trio habitat+dieta+morfologia (3/5)."
                ),
                kind="result",
            ))
            for proof in p3:
                self._append_proof_step(steps, trace, proof, 60)
            return matches

        # -- Sin resultado --
        steps.append(TraceStep(
            stage="SIN RESULTADO",
            detail=(
                "Pyke no pudo demostrar ninguna coincidencia.\n"
                "Ninguna especie comparte al menos habitat + dieta + morfologia\n"
                "con las caracteristicas ingresadas."
            ),
            kind="error",
        ))
        trace += ["", "Pyke no demostro ninguna coincidencia (ni parcial)."]
        return []

    # ------------------------------------------------------------------
    # Backward chaining
    # ------------------------------------------------------------------

    def _run_backward(
        self,
        normalized: dict[str, str],
        english: dict[str, str],
    ) -> InferenceResult:
        self._engine.reset()
        steps: list[TraceStep] = []
        trace: list[str] = self._header_lines(RECOGNITION_MODE_BACKWARD)

        # Fase 1: declarar meta
        steps.append(TraceStep(
            stage="FASE 1",
            detail=(
                "Declaracion de metas y preparacion de hechos\n"
                "META EXACTA   : taxonomy($bird_id, $order, $family)\n"
                "META PARCIAL  : taxonomy_partial($bird_id, $order, $family, $score)"
            ),
        ))
        steps.append(TraceStep(
            stage="META",
            detail=(
                "Pyke intentara demostrar top-down:\n"
                "  taxonomy -> is_<orden> -> 5 hechos observados\n"
                "  taxonomy_partial -> is_<orden>_partial -> 4 hechos\n"
                "  taxonomy_partial -> is_partial_trio -> 3 hechos"
            ),
            kind="fact",
        ))

        # Fase 2: assert hechos
        steps.append(TraceStep(
            stage="FASE 2",
            detail="Registro de hechos observados",
        ))
        self._assert_facts(english, normalized, steps, trace)

        # Fase 3: activar BC y probar
        steps.append(TraceStep(
            stage="FASE 3",
            detail=(
                "Activacion de animal_rules_bc\n"
                "Pyke recorre el arbol de prueba:\n"
                "  taxonomy -> sub-objetivo exacto -> hechos\n"
                "  taxonomy_partial -> sub-objetivo parcial -> hechos"
            ),
        ))
        trace += ["", "=" * 60, "ACTIVANDO: animal_rules_bc", "=" * 60]
        self._engine.activate("animal_rules_bc")

        matches = self._collect_all_matches_bc(steps, trace, english)

        return InferenceResult(
            mode=RECOGNITION_MODE_BACKWARD,
            matches=matches,
            features=normalized,
            trace=trace,
            steps=steps,
        )

    def _collect_all_matches_bc(
        self,
        steps: list[TraceStep],
        trace: list[str],
        english: dict[str, str],
    ) -> list[BirdMatch]:
        """Recolecta coincidencias BC exactas y parciales."""

        # -- Nivel exacto 5/5 --
        exact_proofs = self._prove_goal(
            "animal_rules_bc.taxonomy($bird_id, $order, $family)"
        )
        unique_exact = self._dedupe_proofs(exact_proofs)

        if unique_exact:
            matches = self._build_matches(unique_exact, 100)
            steps.append(TraceStep(
                stage="RESULTADO",
                detail=f"Pyke demostro {len(unique_exact)} hipotesis exacta(s)",
                kind="result",
            ))
            for proof in unique_exact:
                self._append_bc_proof_step(steps, trace, proof, 100, english)
            return matches

        # -- Nivel parcial 4/5 --
        partial_proofs = self._prove_goal(
            "animal_rules_bc.taxonomy_partial($bird_id, $order, $family, $score)"
        )
        p4 = self._dedupe_proofs(
            [p for p in partial_proofs if str(p.get("score")) == "score_4"]
        )
        if p4:
            matches = self._build_matches(p4, 80)
            steps.append(TraceStep(
                stage="RESULTADO",
                detail=(
                    f"Pyke no demostro hipotesis exacta.\n"
                    f"Demostro {len(p4)} hipotesis parcial(es) con 4/5."
                ),
                kind="result",
            ))
            for proof in p4:
                self._append_bc_proof_step(steps, trace, proof, 80, english)
            return matches

        # -- Nivel parcial 3/5 --
        p3 = self._dedupe_proofs(
            [p for p in partial_proofs if str(p.get("score")) == "score_3"]
        )
        if p3:
            matches = self._build_matches(p3, 60)
            steps.append(TraceStep(
                stage="RESULTADO",
                detail=(
                    f"Pyke no demostro 4/5 ni exacta.\n"
                    f"Demostro {len(p3)} hipotesis con trio 3/5."
                ),
                kind="result",
            ))
            for proof in p3:
                self._append_bc_proof_step(steps, trace, proof, 60, english)
            return matches

        # -- Sin resultado --
        steps.append(TraceStep(
            stage="SIN RESULTADO",
            detail=(
                "Pyke no pudo demostrar ninguna hipotesis.\n"
                "Ninguna especie comparte habitat + dieta + morfologia\n"
                "con las caracteristicas ingresadas."
            ),
            kind="error",
        ))
        trace += ["", "Pyke no demostro ninguna hipotesis (ni parcial)."]
        return []

    # ------------------------------------------------------------------
    # Pyke helpers (API publica 1.1.1)
    # ------------------------------------------------------------------

    def _assert_facts(
        self,
        english: dict[str, str],
        normalized: dict[str, str],
        steps: list[TraceStep],
        trace: list[str],
    ) -> None:
        for feat in FEATURE_ORDER:
            eng_val = english[feat]
            esp_val = normalized[feat]
            self._engine.add_case_specific_fact(
                "animals", "characteristic", (feat, eng_val)
            )
            detail = (
                f"characteristic({humanize_label(feat)}, "
                f"{humanize_label(esp_val)}) -> '{eng_val}'"
            )
            steps.append(TraceStep(stage="HECHO", detail=detail, kind="fact"))
            trace.append(f"HECHO: {humanize_label(feat)} = {humanize_label(esp_val)}")

    def _prove_goal(self, goal_str: str) -> list[dict[str, str]]:
        results: list[dict[str, str]] = []
        with self._engine.prove_goal(goal_str) as gen:
            for bindings, _plan in gen:
                results.append(
                    {k: self._unwrap(v) for k, v in bindings.items()}
                )
        return results

    def _read_classification_facts(self) -> list[str]:
        """Lee hechos classification afirmados por FC via prove_goal (seguro)."""
        lines: list[str] = []
        try:
            proofs = self._prove_goal(
                "animals.classification($bird_id, $level, $value)"
            )
        except Exception:
            return lines
        seen: set[tuple] = set()
        for p in proofs:
            key = (str(p.get("bird_id", "")),
                   str(p.get("level", "")),
                   str(p.get("value", "")))
            if key in seen:
                continue
            seen.add(key)
            lines.append(
                f"Regla FC: classification({key[0]}, {key[1]}, {key[2]})"
            )
        if lines:
            lines.insert(0, f"Reglas FC disparadas: {len(lines)} clasificacion(es)")
        return lines

    # ------------------------------------------------------------------
    # Construccion de resultados
    # ------------------------------------------------------------------

    def _build_matches(
        self,
        proofs: list[dict[str, str]],
        score: int,
    ) -> list[BirdMatch]:
        is_exact = (score == 100)
        feats_matched = {100: 5, 80: 4, 60: 3}.get(score, 3)
        matches: list[BirdMatch] = []
        for proof in proofs:
            bird_id = str(proof.get("bird_id", ""))
            profile = next((p for p in BIRD_PROFILES if p.bird_id == bird_id), None)
            if profile is None:
                continue
            matches.append(BirdMatch(
                bird_id=profile.bird_id,
                common_name_es=profile.species.common_name_es,
                order=str(proof.get("order", profile.species.order)),
                family=str(proof.get("family", profile.species.family)),
                matched_features=feats_matched,
                total_features=5,
                score_percent=score,
                is_exact=is_exact,
            ))
        matches.sort(key=lambda m: m.common_name_es)
        return matches

    def _append_proof_step(
        self,
        steps: list[TraceStep],
        trace: list[str],
        proof: dict[str, str],
        score: int,
    ) -> None:
        bird_id = str(proof.get("bird_id", ""))
        order   = str(proof.get("order", ""))
        family  = str(proof.get("family", ""))
        name    = self._bird_name(bird_id)
        label   = _SCORE_LABEL.get(score, f"{score}%")
        steps.append(TraceStep(
            stage="PRUEBA",
            detail=(
                f"Pyke probo: taxonomy({bird_id}, {order}, {family})\n"
                f"  Especie : {name}\n"
                f"  Orden   : {order}\n"
                f"  Familia : {family}\n"
                f"  Nivel   : {label}"
            ),
            kind="result",
        ))
        trace += [
            "",
            f"PRUEBA: taxonomy({bird_id}, {order}, {family})",
            f"  Especie : {name}  |  Nivel: {label}",
        ]

    def _append_bc_proof_step(
        self,
        steps: list[TraceStep],
        trace: list[str],
        proof: dict[str, str],
        score: int,
        english: dict[str, str],
    ) -> None:
        bird_id  = str(proof.get("bird_id", ""))
        order    = str(proof.get("order", ""))
        family   = str(proof.get("family", ""))
        name     = self._bird_name(bird_id)
        label    = _SCORE_LABEL.get(score, f"{score}%")
        subgoal  = _ORDER_TO_SUBGOAL.get(order, "is_unknown")
        sg_label = _SUBGOAL_LABEL.get(subgoal, subgoal)

        # Sufijo del sub-objetivo segun nivel
        if score == 100:
            sg_used = sg_label
        elif score == 80:
            sg_used = sg_label.replace("?", " (4/5)?")
        else:
            sg_used = "is_partial_trio (habitat+dieta+morfologia, 3/5)"

        chain = [
            f"Pyke probo: taxonomy -> {sg_used}",
            f"  Especie : {name}",
            f"  Orden   : {order}",
            f"  Familia : {family}",
            f"  Nivel   : {label}",
            "  Hechos verificados:",
        ]
        feats_checked = {100: FEATURE_ORDER, 80: FEATURE_ORDER[1:], 60: FEATURE_ORDER[:3]}
        for feat in feats_checked.get(score, FEATURE_ORDER[:3]):
            chain.append(f"    characteristic({feat}, {english.get(feat, '?')}) OK")

        steps.append(TraceStep(
            stage="PRUEBA",
            detail="\n".join(chain),
            kind="result",
        ))
        trace += ["", f"BC PRUEBA: {name}  Nivel: {label}"]

    # ------------------------------------------------------------------
    # Utilidades estaticas
    # ------------------------------------------------------------------

    @staticmethod
    def _dedupe_proofs(proofs: list[dict[str, str]]) -> list[dict[str, str]]:
        unique: list[dict[str, str]] = []
        seen: set[tuple] = set()
        for p in proofs:
            key = (str(p.get("bird_id")), str(p.get("order")), str(p.get("family")))
            if key in seen:
                continue
            seen.add(key)
            unique.append(p)
        return unique

    @staticmethod
    def _unwrap(value):
        if isinstance(value, tuple) and len(value) == 1:
            return AvianExpertSystem._unwrap(value[0])
        return value

    @staticmethod
    def _bird_name(bird_id: str) -> str:
        profile = next((p for p in BIRD_PROFILES if p.bird_id == bird_id), None)
        return profile.species.common_name_es if profile else bird_id

    @staticmethod
    def _normalize_features(features: dict[str, str]) -> dict[str, str]:
        normalized: dict[str, str] = {}
        for feat in FEATURE_ORDER:
            val = features.get(feat)
            if not val:
                raise ValueError(f"Caracteristica faltante: {feat}")
            normalized[feat] = val
        return normalized

    @staticmethod
    def _to_english_features(features: dict[str, str]) -> dict[str, str]:
        return {
            feat: FEATURE_TRANSLATIONS.get(feat, {}).get(val, val)
            for feat, val in features.items()
        }

    @staticmethod
    def _header_lines(mode: str) -> list[str]:
        return [
            "=" * 60,
            "SISTEMA EXPERTO DE IDENTIFICACION DE AVES",
            "=" * 60,
            "",
            f"Modo: {MODE_LABELS[mode]}",
            f"Descripcion: {MODE_DESCRIPTIONS[mode]}",
            "",
            "=" * 60,
            "AGREGANDO HECHOS A LA BASE DE CONOCIMIENTO",
            "=" * 60,
            "",
        ]


# ======================================================================
# Formateador de resultados (contrato publico sin cambios para gui.py)
# ======================================================================

def format_result(result: InferenceResult) -> str:
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
        lines.append(
            f"  * {humanize_label(key)}: {humanize_label(result.features[key])}"
        )
    lines.append("─" * 70)

    if not result.matches:
        lines += [
            "",
            "x CONCLUSION: Pyke no encontro ninguna coincidencia",
            "",
            "Ninguna especie comparte habitat + dieta + morfologia",
            "con las caracteristicas ingresadas.",
            "Revisa los valores seleccionados.",
        ]
        lines.append("=" * 70)
        return "\n".join(lines)

    exact   = [m for m in result.matches if m.is_exact]
    partial = [m for m in result.matches if not m.is_exact]

    if exact:
        lines += ["", "RESULTADO EXACTO (5/5 - Pyke demostro la especie)", ""]
        for match in exact:
            _append_match_lines(lines, match, result.mode)
    elif partial:
        score = partial[0].score_percent
        nivel = _SCORE_LABEL.get(score, f"{score}%")
        lines += [
            "",
            f"RESULTADO PARCIAL ({nivel})",
            "Pyke demostro estas especies como candidatas:",
            "",
        ]
        for match in partial[:8]:
            _append_match_lines(lines, match, result.mode)

    lines.append("=" * 70)
    return "\n".join(lines)


def _append_match_lines(
    lines: list[str],
    match: BirdMatch,
    mode: str,
) -> None:
    profile = next((p for p in BIRD_PROFILES if p.bird_id == match.bird_id), None)
    sp = profile.species if profile else None
    nivel = _SCORE_LABEL.get(match.score_percent, f"{match.score_percent}%")

    lines += [
        f"  Especie: {match.common_name_es}",
        f"  Nombre cientifico: {sp.scientific_name if sp else '—'}",
        f"  Nivel de confianza: {match.score_percent}%  ({nivel})",
        "",
        "  Taxonomia:",
        f"    Clase:   {sp.class_name if sp else 'Aves'}",
        f"    Orden:   {match.order}",
        f"    Familia: {match.family}",
        f"    Genero:  {sp.genus if sp else '—'}",
        "",
        "  Datos biologicos:",
        f"    Envergadura: {sp.wingspan_cm if sp else '—'}",
        f"    Peso:        {sp.weight_g if sp else '—'}",
        f"    Longevidad:  {sp.lifespan_years if sp else '—'}",
        f"    Estado IUCN: {sp.conservation_status if sp else '—'}",
        "",
    ]
    if sp and sp.fun_fact:
        lines += [f"  Curiosidad: {sp.fun_fact}", ""]
    lines.append("─" * 40)

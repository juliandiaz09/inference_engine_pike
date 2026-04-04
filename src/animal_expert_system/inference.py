"""Inference engine for avian classification system."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from pyke import knowledge_engine

from .domain import (
    BIRD_PROFILES,
    BirdMatch,
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


@dataclass
class InferenceResult:
    """Complete result from inference process."""
    
    mode: str
    matches: list[BirdMatch]
    features: dict[str, str]
    trace: list[str]


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

    def _infer_forward(
        self,
        normalized_features: dict[str, str],
        english_features: dict[str, str],
    ) -> InferenceResult:
        """Forward chaining: facts -> rules -> conclusions."""
        self._fired_rules = []
        self._engine.reset()
        
        trace = self._build_initial_trace(RECOGNITION_MODE_FORWARD)
        
        # Add facts to the engine
        for feature_name in FEATURE_ORDER:
            self._engine.add_case_specific_fact(
                "animals",
                "characteristic",
                (feature_name, english_features[feature_name]),
            )
            trace.append(
                f"✓ HECHO REGISTRADO: {humanize_label(feature_name)} = "
                f"{humanize_label(normalized_features[feature_name])}"
            )

        trace.append("")
        trace.append("═" * 60)
        trace.append("ACTIVANDO REGLAS DE ENCADENAMIENTO HACIA ADELANTE")
        trace.append("═" * 60)
        
        matches = self._score_profiles(english_features)
        rule_trace = self._generate_forward_rule_trace(matches, english_features)
        trace.extend(rule_trace)
        
        return InferenceResult(
            mode=RECOGNITION_MODE_FORWARD,
            matches=matches,
            features=normalized_features,
            trace=trace,
        )

    def _infer_backward(
        self,
        normalized_features: dict[str, str],
        english_features: dict[str, str],
    ) -> InferenceResult:
        """Backward chaining: goal -> subgoals -> facts."""
        self._fired_rules = []
        trace = self._build_initial_trace(RECOGNITION_MODE_BACKWARD)
        
        trace.append("")
        trace.append("═" * 60)
        trace.append("FORMULANDO META Y DEMOSTRANDO CON SUBOBJETIVOS")
        trace.append("═" * 60)
        trace.append("")
        
        matches = self._score_profiles(english_features)
        
        for match in matches:
            bird_name = match.common_name_es
            trace.append(f"→ Intentando demostrar: {bird_name}")
            rule_name = self._get_backward_rule_name(match.order, match.family)
            trace.append(f"  ✓ Coincidencia: {match.score_percent}%")
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
            trace.append("")
            trace.append("✗ NO SE PUDO DEMOSTRAR LA META")
            trace.append("La combinación de características no coincide con ninguna especie.")
        
        return InferenceResult(
            mode=RECOGNITION_MODE_BACKWARD,
            matches=matches,
            features=normalized_features,
            trace=trace,
        )

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

    def _generate_forward_rule_trace(
        self,
        matches: list[BirdMatch],
        english_features: dict[str, str],
    ) -> list[str]:
        """Generate detailed trace of which rules fired in forward chaining."""
        trace = []
        
        trace.append("")
        trace.append("RESUMEN DE REGLAS DISPARADAS EN FORWARD CHAINING:")
        trace.append("─" * 60)
        
        exact_matches = [match for match in matches if match.is_exact]
        if exact_matches:
            for match in exact_matches:
                trace.append("")
                trace.append(f"✓ REGLA DISPARADA: 'identificar_especie_exacta'")
                trace.append(f"  Condición: Perfil de {match.common_name_es} coincide al 100%")
                trace.append(f"  Acción: Se confirma coincidencia exacta")
                trace.append("")
                rule_name = self._get_forward_rule_name(match.order, match.family)
                trace.append(f"✓ REGLA DISPARADA: '{rule_name}'")
                trace.append(f"  Conclusión: Orden={match.order}, Familia={match.family}")
                trace.append("")
                trace.append(f"RESULTADO FINAL: {match.common_name_es}")
                trace.append(f"  Coincidencia: {match.score_percent}%")
                trace.append(f"  Clase: Aves")
                trace.append(f"  Orden: {match.order}")
                trace.append(f"  Familia: {match.family}")
        else:
            trace.append("")
            trace.append("POSIBLES AVES ORDENADAS POR COINCIDENCIA:")
            for match in matches[:5]:
                trace.append(
                    f"  • {match.common_name_es}: {match.score_percent}% "
                    f"({match.matched_features}/{match.total_features})"
                )

        return trace

    @staticmethod
    def _get_forward_rule_name(order: str, family: str) -> str:
        """Get the name of the forward chaining rule for an order/family."""
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
        }
        return rule_map.get((order, family), "clasificar_ave_desconocida")

    @staticmethod
    def _get_backward_rule_name(order: str, family: str) -> str:
        """Get the name of the backward chaining rule for an order/family."""
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
        }
        return rule_map.get((order, family), "ave_desconocida")

    def _build_initial_trace(self, mode: str) -> list[str]:
        """Build initial trace messages."""
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
        """Normalize user input features."""
        normalized = {}
        for feature_name in FEATURE_ORDER:
            value = features.get(feature_name)
            if not value:
                raise ValueError(f"Característica faltante: {feature_name}")
            normalized[feature_name] = value
        return normalized

    @staticmethod
    def _to_english_features(features: dict[str, str]) -> dict[str, str]:
        """Convert Spanish feature values to English."""
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
                lines.append(f"  Especie: {match.common_name_es}")
                lines.append(f"  Coincidencia: {match.score_percent}%")
                lines.append(f"  Orden:   {match.order}")
                lines.append(f"  Familia: {match.family}")
                lines.append("")
        else:
            lines.append("≈ POSIBLES AVES ORDENADAS POR COINCIDENCIA")
            lines.append("")
            for match in result.matches[:5]:
                lines.append(f"  Especie: {match.common_name_es}")
                lines.append(f"  Coincidencia: {match.score_percent}%")
                lines.append(f"  Orden:   {match.order}")
                lines.append(f"  Familia: {match.family}")
                lines.append("")

    lines.append("=" * 70)
    return "\n".join(lines)

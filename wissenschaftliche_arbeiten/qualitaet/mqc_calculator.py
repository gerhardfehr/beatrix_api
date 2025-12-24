#!/usr/bin/env python3
"""
Meta-Qualitäts-Container (MQC) Score Calculator
================================================

Berechnet gewichtete Qualitätsscores für Kapitel des Meta_Modul_Paper
basierend auf dem MQC Schema.

Nutzung:
    python mqc_calculator.py kapitel_00_bewertung.yaml
    python mqc_calculator.py kapitel_00_bewertung.yaml --zielgruppe ki_engineer
    python mqc_calculator.py --alle
"""

import yaml
import argparse
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass
from enum import Enum


# =============================================================================
# KONSTANTEN
# =============================================================================

DIMENSIONEN = [
    "D01_wissenschaft",
    "D02_bcm_spezifik",
    "D03_didaktik",
    "D04_anwendbarkeit",
    "D05_konsistenz",
    "D06_zielgruppe",
    "D07_epistemische_reflexion",
    "D08_validierung",
    "D09_abhaengigkeiten",
    "D10_evolution",
    "D11_operationalisierung",
    "D12_narrative",
    "D13_meta_reflexivitaet",
]

DIMENSION_NAMEN = {
    "D01_wissenschaft": "Wissenschaft",
    "D02_bcm_spezifik": "BCM-Spezifik",
    "D03_didaktik": "Didaktik",
    "D04_anwendbarkeit": "Anwendbarkeit",
    "D05_konsistenz": "Konsistenz",
    "D06_zielgruppe": "Zielgruppe",
    "D07_epistemische_reflexion": "Epist. Reflexion",
    "D08_validierung": "Validierung",
    "D09_abhaengigkeiten": "Abhängigkeiten",
    "D10_evolution": "Evolution",
    "D11_operationalisierung": "Operationalisierung",
    "D12_narrative": "Narrative",
    "D13_meta_reflexivitaet": "Meta-Reflexivität",
}


# =============================================================================
# KAPITELTYP-GEWICHTUNGEN
# =============================================================================

KAPITEL_GEWICHTUNGEN = {
    "rahmen_kapitel": {
        "D01_wissenschaft": 0.5,
        "D02_bcm_spezifik": 0.4,
        "D03_didaktik": 1.0,
        "D04_anwendbarkeit": 0.6,
        "D05_konsistenz": 0.8,
        "D06_zielgruppe": 1.0,
        "D07_epistemische_reflexion": 0.5,
        "D08_validierung": 0.3,
        "D09_abhaengigkeiten": 0.7,
        "D10_evolution": 0.6,
        "D11_operationalisierung": 0.3,
        "D12_narrative": 1.0,
        "D13_meta_reflexivitaet": 0.8,
    },
    "axiom_kapitel": {
        "D01_wissenschaft": 1.0,
        "D02_bcm_spezifik": 1.0,
        "D03_didaktik": 0.7,
        "D04_anwendbarkeit": 0.6,
        "D05_konsistenz": 1.0,
        "D06_zielgruppe": 0.6,
        "D07_epistemische_reflexion": 0.9,
        "D08_validierung": 1.0,
        "D09_abhaengigkeiten": 0.9,
        "D10_evolution": 0.7,
        "D11_operationalisierung": 0.8,
        "D12_narrative": 0.5,
        "D13_meta_reflexivitaet": 0.6,
    },
    "integration_kapitel": {
        "D01_wissenschaft": 0.6,
        "D02_bcm_spezifik": 1.0,
        "D03_didaktik": 0.7,
        "D04_anwendbarkeit": 1.0,
        "D05_konsistenz": 1.0,
        "D06_zielgruppe": 0.5,
        "D07_epistemische_reflexion": 0.5,
        "D08_validierung": 0.6,
        "D09_abhaengigkeiten": 1.0,
        "D10_evolution": 0.8,
        "D11_operationalisierung": 1.0,
        "D12_narrative": 0.4,
        "D13_meta_reflexivitaet": 0.7,
    },
    "transformation_kapitel": {
        "D01_wissenschaft": 0.7,
        "D02_bcm_spezifik": 0.8,
        "D03_didaktik": 0.9,
        "D04_anwendbarkeit": 1.0,
        "D05_konsistenz": 0.8,
        "D06_zielgruppe": 0.7,
        "D07_epistemische_reflexion": 0.6,
        "D08_validierung": 0.5,
        "D09_abhaengigkeiten": 0.7,
        "D10_evolution": 0.9,
        "D11_operationalisierung": 1.0,
        "D12_narrative": 0.8,
        "D13_meta_reflexivitaet": 0.7,
    },
}


# =============================================================================
# ZIELGRUPPEN-MULTIPLIKATOREN
# =============================================================================

ZIELGRUPPEN_MULTIPLIKATOREN = {
    "verhaltensoekonom": {
        "D01_wissenschaft": 1.5,
        "D02_bcm_spezifik": 1.2,
        "D03_didaktik": 0.7,
        "D04_anwendbarkeit": 0.5,
        "D07_epistemische_reflexion": 1.3,
        "D08_validierung": 1.5,
        "D13_meta_reflexivitaet": 1.2,
    },
    "ki_engineer": {
        "D01_wissenschaft": 0.6,
        "D02_bcm_spezifik": 1.0,
        "D03_didaktik": 0.7,
        "D04_anwendbarkeit": 1.5,
        "D11_operationalisierung": 1.5,
        "D05_konsistenz": 1.2,
    },
    "business_stakeholder": {
        "D01_wissenschaft": 0.4,
        "D02_bcm_spezifik": 0.5,
        "D03_didaktik": 1.3,
        "D06_zielgruppe": 1.5,
        "D12_narrative": 1.4,
        "D04_anwendbarkeit": 1.2,
    },
    "regulator_ethiker": {
        "D01_wissenschaft": 1.0,
        "D07_epistemische_reflexion": 1.4,
        "D08_validierung": 1.2,
        "D13_meta_reflexivitaet": 1.5,
        "D04_anwendbarkeit": 1.3,
    },
    "berater_praktiker": {
        "D03_didaktik": 1.2,
        "D04_anwendbarkeit": 1.5,
        "D12_narrative": 1.1,
        "D06_zielgruppe": 1.2,
        "D11_operationalisierung": 1.0,
    },
}


# =============================================================================
# BEWERTUNGS-SCHWELLENWERTE
# =============================================================================

class Bewertung(Enum):
    NICHT_AKZEPTABEL = "🔴 Nicht akzeptabel"
    VERBESSERUNGSWUERDIG = "🟠 Verbesserungswürdig"
    AKZEPTABEL = "🟡 Akzeptabel"
    GUT = "🟢 Gut"
    EXZELLENT = "⭐ Exzellent"


def bewerte_score(score: float) -> Bewertung:
    if score >= 0.9:
        return Bewertung.EXZELLENT
    elif score >= 0.75:
        return Bewertung.GUT
    elif score >= 0.6:
        return Bewertung.AKZEPTABEL
    elif score >= 0.4:
        return Bewertung.VERBESSERUNGSWUERDIG
    else:
        return Bewertung.NICHT_AKZEPTABEL


# =============================================================================
# SCORE-BERECHNUNG
# =============================================================================

@dataclass
class ScoreResult:
    kapitel_id: str
    kapitel_name: str
    kapitel_typ: str
    zielgruppe: Optional[str]
    dimension_scores: Dict[str, float]
    gewichteter_score: float
    bewertung: Bewertung
    top_3: list
    bottom_3: list


def lade_bewertung(pfad: Path) -> dict:
    """Lädt eine Kapitel-Bewertung aus YAML."""
    with open(pfad, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def berechne_score(
    bewertung: dict,
    zielgruppe: Optional[str] = None
) -> ScoreResult:
    """Berechnet den gewichteten Qualitätsscore."""

    kapitel = bewertung['kapitel']
    kapitel_typ = kapitel['typ']

    # Hole Gewichtungen
    kapitel_gewichte = KAPITEL_GEWICHTUNGEN.get(kapitel_typ, {})
    zielgruppen_mult = ZIELGRUPPEN_MULTIPLIKATOREN.get(zielgruppe, {}) if zielgruppe else {}

    # Sammle Dimension-Scores
    dimension_scores = {}
    for dim in DIMENSIONEN:
        if dim in bewertung.get('dimensionen', {}):
            dim_data = bewertung['dimensionen'][dim]
            if isinstance(dim_data, dict) and 'score' in dim_data:
                dimension_scores[dim] = dim_data['score']
            else:
                dimension_scores[dim] = 0.0
        else:
            dimension_scores[dim] = 0.0

    # Berechne gewichteten Score
    zaehler = 0.0
    nenner = 0.0

    for dim, score in dimension_scores.items():
        kap_gewicht = kapitel_gewichte.get(dim, 0.5)
        zg_mult = zielgruppen_mult.get(dim, 1.0)

        gewicht = kap_gewicht * zg_mult
        zaehler += score * gewicht
        nenner += gewicht

    gewichteter_score = zaehler / nenner if nenner > 0 else 0.0

    # Sortiere für Top/Bottom
    sortiert = sorted(dimension_scores.items(), key=lambda x: x[1], reverse=True)
    top_3 = sortiert[:3]
    bottom_3 = sortiert[-3:]

    return ScoreResult(
        kapitel_id=kapitel['id'],
        kapitel_name=kapitel['name'],
        kapitel_typ=kapitel_typ,
        zielgruppe=zielgruppe,
        dimension_scores=dimension_scores,
        gewichteter_score=gewichteter_score,
        bewertung=bewerte_score(gewichteter_score),
        top_3=top_3,
        bottom_3=bottom_3,
    )


# =============================================================================
# AUSGABE
# =============================================================================

def drucke_ergebnis(result: ScoreResult):
    """Gibt das Ergebnis formatiert aus."""

    print("\n" + "=" * 70)
    print(f"  QUALITÄTSBEWERTUNG: Kapitel {result.kapitel_id} - {result.kapitel_name}")
    print("=" * 70)

    print(f"\n  Kapiteltyp:  {result.kapitel_typ}")
    if result.zielgruppe:
        print(f"  Zielgruppe:  {result.zielgruppe}")

    print(f"\n  {'─' * 66}")
    print(f"  GESAMT-SCORE:  {result.gewichteter_score:.2f}  {result.bewertung.value}")
    print(f"  {'─' * 66}")

    # Dimension Scores
    print("\n  DIMENSIONEN:\n")
    for dim in DIMENSIONEN:
        score = result.dimension_scores.get(dim, 0.0)
        name = DIMENSION_NAMEN.get(dim, dim)
        bar = "█" * int(score * 20) + "░" * (20 - int(score * 20))
        bewertung = bewerte_score(score)
        print(f"    {name:20} {bar} {score:.2f}")

    # Top 3
    print("\n  STÄRKEN (Top 3):")
    for dim, score in result.top_3:
        name = DIMENSION_NAMEN.get(dim, dim)
        print(f"    ✅ {name}: {score:.2f}")

    # Bottom 3
    print("\n  VERBESSERUNGSPOTENTIAL (Bottom 3):")
    for dim, score in result.bottom_3:
        name = DIMENSION_NAMEN.get(dim, dim)
        print(f"    ⚠️  {name}: {score:.2f}")

    print("\n" + "=" * 70 + "\n")


def drucke_vergleich(results: list):
    """Gibt einen Vergleich mehrerer Kapitel aus."""

    print("\n" + "=" * 70)
    print("  KAPITEL-VERGLEICH")
    print("=" * 70 + "\n")

    # Header
    print(f"  {'Kapitel':<25} {'Score':>8} {'Bewertung':<25}")
    print(f"  {'-' * 25} {'-' * 8} {'-' * 25}")

    for r in sorted(results, key=lambda x: x.gewichteter_score, reverse=True):
        print(f"  {r.kapitel_id + ' ' + r.kapitel_name:<25} {r.gewichteter_score:>8.2f} {r.bewertung.value:<25}")

    print("\n" + "=" * 70 + "\n")


def drucke_zielgruppen_vergleich(bewertung: dict):
    """Zeigt Score für alle Zielgruppen."""

    print("\n" + "=" * 70)
    print("  ZIELGRUPPEN-VERGLEICH")
    print("=" * 70 + "\n")

    results = []

    # Ohne Zielgruppe
    result = berechne_score(bewertung, None)
    results.append(("(Basis)", result.gewichteter_score, result.bewertung))

    # Alle Zielgruppen
    for zg in ZIELGRUPPEN_MULTIPLIKATOREN.keys():
        result = berechne_score(bewertung, zg)
        results.append((zg, result.gewichteter_score, result.bewertung))

    # Header
    print(f"  {'Zielgruppe':<25} {'Score':>8} {'Bewertung':<25}")
    print(f"  {'-' * 25} {'-' * 8} {'-' * 25}")

    for name, score, bew in sorted(results, key=lambda x: x[1], reverse=True):
        print(f"  {name:<25} {score:>8.2f} {bew.value:<25}")

    print("\n" + "=" * 70 + "\n")


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="MQC Score Calculator - Berechnet Qualitätsscores für Kapitel"
    )
    parser.add_argument(
        "bewertung",
        nargs="?",
        help="Pfad zur Bewertungs-YAML (z.B. kapitel_00_bewertung.yaml)"
    )
    parser.add_argument(
        "--zielgruppe", "-z",
        choices=list(ZIELGRUPPEN_MULTIPLIKATOREN.keys()),
        help="Zielgruppe für Kalibrierung"
    )
    parser.add_argument(
        "--alle-zielgruppen", "-a",
        action="store_true",
        help="Zeige Scores für alle Zielgruppen"
    )
    parser.add_argument(
        "--vergleich", "-v",
        nargs="+",
        help="Vergleiche mehrere Bewertungen"
    )

    args = parser.parse_args()

    if args.vergleich:
        # Vergleich mehrerer Kapitel
        results = []
        for pfad in args.vergleich:
            bewertung = lade_bewertung(Path(pfad))
            result = berechne_score(bewertung, args.zielgruppe)
            results.append(result)
        drucke_vergleich(results)

    elif args.bewertung:
        bewertung = lade_bewertung(Path(args.bewertung))

        if args.alle_zielgruppen:
            drucke_zielgruppen_vergleich(bewertung)
        else:
            result = berechne_score(bewertung, args.zielgruppe)
            drucke_ergebnis(result)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()

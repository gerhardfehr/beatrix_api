#!/usr/bin/env python3
"""
ESL Calculator - Empirical System of Language
==============================================

Berechnet K-Werte (Kalibrierung) für wissenschaftliche Aussagen
basierend auf Behauptungsstärke (B) und Evidenzstärke (E).

Kernformel: K = 1 - |B - E|

Nutzung:
    python esl_calculator.py --aussage "Alle Menschen müssen essen"
    python esl_calculator.py --interaktiv
    python esl_calculator.py --datei aussagen.yaml
"""

import re
import argparse
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple
from enum import Enum


# =============================================================================
# KONSTANTEN: B-SKALA (Behauptungsstärke)
# =============================================================================

MODALVERBEN = {
    # Starke Notwendigkeit (B = 0.90 - 1.00)
    "muss": 0.95,
    "müssen": 0.95,
    "zwingend": 1.00,
    "notwendig": 0.95,
    "erfordert": 0.90,
    "erfordern": 0.90,

    # Schwache Notwendigkeit (B = 0.75 - 0.90)
    "soll": 0.85,
    "sollte": 0.80,
    "sollten": 0.80,
    "wird erwartet": 0.80,

    # Möglichkeit (B = 0.50 - 0.75)
    "kann": 0.60,
    "können": 0.60,
    "mag": 0.55,
    "dürfte": 0.65,
    "dürften": 0.65,

    # Schwache Möglichkeit (B = 0.30 - 0.50)
    "könnte": 0.45,
    "könnten": 0.45,
    "möglicherweise": 0.40,
    "eventuell": 0.35,
    "vielleicht": 0.35,

    # Spekulation (B = 0.10 - 0.30)
    "hypothetisch": 0.25,
    "spekulativ": 0.20,
    "denkbar": 0.20,
}

QUANTOREN = {
    # Universell (B = 0.90 - 1.00)
    "alle": 0.95,
    "jeder": 0.95,
    "jede": 0.95,
    "jedes": 0.95,
    "immer": 0.95,
    "niemals": 0.95,
    "nie": 0.95,
    "kein": 0.95,
    "keine": 0.95,
    "ausnahmslos": 1.00,
    "stets": 0.95,
    "grundsätzlich": 0.90,

    # Quasi-universell (B = 0.75 - 0.90)
    "fast alle": 0.85,
    "die meisten": 0.80,
    "meisten": 0.80,
    "überwiegend": 0.80,
    "in der regel": 0.75,
    "typischerweise": 0.75,
    "normalerweise": 0.75,
    "gewöhnlich": 0.75,

    # Partikular (B = 0.50 - 0.75)
    "viele": 0.65,
    "häufig": 0.65,
    "oft": 0.60,
    "manchmal": 0.55,
    "regelmäßig": 0.60,

    # Schwach partikular (B = 0.30 - 0.50)
    "einige": 0.45,
    "manche": 0.45,
    "gelegentlich": 0.40,
    "selten": 0.35,
    "wenige": 0.35,

    # Existenziell (B = 0.10 - 0.30)
    "mindestens ein": 0.25,
    "es gibt fälle": 0.25,
    "vereinzelt": 0.20,
    "in einzelfällen": 0.20,
}

HEDGING_REDUKTOREN = {
    # Starke Reduktion (-0.20 bis -0.30)
    "tendenziell": -0.25,
    "ansatzweise": -0.25,
    "unter umständen": -0.30,
    "in gewisser weise": -0.25,
    "gewissermaßen": -0.20,

    # Mittlere Reduktion (-0.10 bis -0.20)
    "relativ": -0.15,
    "vergleichsweise": -0.15,
    "eher": -0.15,
    "ziemlich": -0.15,

    # Schwache Reduktion (-0.05 bis -0.10)
    "weitgehend": -0.10,
    "größtenteils": -0.10,
    "im wesentlichen": -0.10,
    "im großen und ganzen": -0.10,
}

HEDGING_VERSTAERKER = {
    # Verstärkung (+0.05 bis +0.15)
    "eindeutig": 0.10,
    "zweifellos": 0.15,
    "offensichtlich": 0.10,
    "nachweislich": 0.15,
    "definitiv": 0.15,
    "klar": 0.10,
    "unbestreitbar": 0.15,
    "unstrittig": 0.12,
    "erwiesenermaßen": 0.15,
}

# Gewichtung der B-Komponenten
B_GEWICHTE = {
    "modalverb": 0.50,
    "quantor": 0.35,
    "hedging": 0.15,  # Additiv als Adjustment
}

B_DEFAULT = 0.70  # Wenn kein Marker gefunden


# =============================================================================
# KONSTANTEN: E-SKALA (Evidenzstärke)
# =============================================================================

class EvidenzStufe(Enum):
    """7-stufige Evidenzhierarchie"""
    META_ANALYSE = ("Meta-Analyse/Systematic Review", 0.90, 1.00)
    RCT = ("Randomisierte kontrollierte Studie", 0.80, 0.90)
    QUASI_EXPERIMENT = ("Quasi-experimentelle Studie", 0.65, 0.80)
    BEOBACHTUNG = ("Beobachtungsstudie", 0.50, 0.65)
    FALLSTUDIE = ("Fallstudie/Qualitativ", 0.35, 0.50)
    EXPERTE = ("Experteneinschätzung/Theorie", 0.20, 0.35)
    KEINE = ("Keine Evidenz/Unbegründet", 0.00, 0.20)

    def __init__(self, label: str, min_e: float, max_e: float):
        self.label = label
        self.min_e = min_e
        self.max_e = max_e

    @property
    def default_e(self) -> float:
        return (self.min_e + self.max_e) / 2


# Evidenz-Marker im Text
EVIDENZ_MARKER = {
    EvidenzStufe.META_ANALYSE: [
        "meta-analyse", "systematic review", "gepoolte", "cochrane",
        "meta-analytisch", "systematische übersicht",
    ],
    EvidenzStufe.RCT: [
        "randomisiert", "kontrollierte studie", "rct", "doppelblind",
        "experimentell gezeigt", "randomized controlled",
    ],
    EvidenzStufe.QUASI_EXPERIMENT: [
        "quasi-experimentell", "natürliches experiment",
        "difference-in-differences", "regression discontinuity",
    ],
    EvidenzStufe.BEOBACHTUNG: [
        "beobachtungsstudie", "kohortenstudie", "längsschnitt",
        "korrelation", "korreliert", "zusammenhang",
    ],
    EvidenzStufe.FALLSTUDIE: [
        "fallstudie", "qualitativ", "interview", "explorative",
        "einzelfall", "case study",
    ],
    EvidenzStufe.EXPERTE: [
        "experten", "theoretisch", "nach einschätzung",
        "konsens", "delphi",
    ],
    EvidenzStufe.KEINE: [
        "es ist bekannt", "offensichtlich", "man weiß",
        "allgemein bekannt", "selbstverständlich",
    ],
}

# Evidenz-Modifikatoren
E_MODIFIKATOREN = {
    # Positiv
    "repliziert": 0.10,
    "präregistriert": 0.05,
    "großes n": 0.05,
    "n > 1000": 0.05,
    "peer reviewed": 0.05,
    "multi-center": 0.05,

    # Negativ
    "nicht repliziert": -0.15,
    "kleines n": -0.10,
    "n < 50": -0.10,
    "hohe attrition": -0.10,
    "interessenkonflikt": -0.10,
    "preprint": -0.05,
}


# =============================================================================
# KONSTANTEN: K-INTERPRETATION
# =============================================================================

class KKategorie(Enum):
    """K-Wert Kategorien"""
    STABIL = ("🟢 Stabil", 0.80, 1.00, "Behauptung durch Evidenz gedeckt")
    TEILSTABIL = ("🟡 Teilstabil", 0.60, 0.80, "Leichte Diskrepanz")
    INTERPRETATIV = ("🟠 Interpretativ", 0.40, 0.60, "Signifikante Lücke")
    SPEKULATIV = ("🔴 Spekulativ", 0.00, 0.40, "Behauptung übersteigt Evidenz")

    def __init__(self, label: str, min_k: float, max_k: float, beschreibung: str):
        self.label = label
        self.min_k = min_k
        self.max_k = max_k
        self.beschreibung = beschreibung

    @classmethod
    def from_k(cls, k: float) -> "KKategorie":
        for kategorie in cls:
            if kategorie.min_k <= k <= kategorie.max_k:
                return kategorie
        return cls.SPEKULATIV


# =============================================================================
# DATENSTRUKTUREN
# =============================================================================

@dataclass
class BAnalyse:
    """Ergebnis der B-Analyse (Behauptungsstärke)"""
    B: float
    modalverb: Optional[str] = None
    modalverb_B: Optional[float] = None
    quantor: Optional[str] = None
    quantor_B: Optional[float] = None
    hedging: List[Tuple[str, float]] = field(default_factory=list)
    hedging_adjustment: float = 0.0

    def __str__(self) -> str:
        parts = [f"B = {self.B:.2f}"]
        if self.modalverb:
            parts.append(f"Modalverb: '{self.modalverb}' ({self.modalverb_B:.2f})")
        if self.quantor:
            parts.append(f"Quantor: '{self.quantor}' ({self.quantor_B:.2f})")
        if self.hedging:
            hedging_str = ", ".join([f"'{h}' ({v:+.2f})" for h, v in self.hedging])
            parts.append(f"Hedging: {hedging_str}")
        return " | ".join(parts)


@dataclass
class EAnalyse:
    """Ergebnis der E-Analyse (Evidenzstärke)"""
    E: float
    stufe: EvidenzStufe
    marker_gefunden: List[str] = field(default_factory=list)
    modifikatoren: List[Tuple[str, float]] = field(default_factory=list)
    base_E: float = 0.0

    def __str__(self) -> str:
        parts = [f"E = {self.E:.2f}", f"Stufe: {self.stufe.label}"]
        if self.marker_gefunden:
            parts.append(f"Marker: {', '.join(self.marker_gefunden)}")
        if self.modifikatoren:
            mod_str = ", ".join([f"'{m}' ({v:+.2f})" for m, v in self.modifikatoren])
            parts.append(f"Modifikatoren: {mod_str}")
        return " | ".join(parts)


@dataclass
class KAnalyse:
    """Vollständige ESL-Analyse"""
    aussage: str
    B_analyse: BAnalyse
    E_analyse: EAnalyse
    K: float
    kategorie: KKategorie
    diskrepanz_typ: str  # "kalibriert", "überbehauptung", "unterbehauptung"

    def __str__(self) -> str:
        return (
            f"K = {self.K:.2f} {self.kategorie.label}\n"
            f"  B: {self.B_analyse}\n"
            f"  E: {self.E_analyse}\n"
            f"  Typ: {self.diskrepanz_typ}"
        )

    def to_dict(self) -> dict:
        return {
            "aussage": self.aussage,
            "K": round(self.K, 3),
            "kategorie": self.kategorie.label,
            "B": round(self.B_analyse.B, 3),
            "E": round(self.E_analyse.E, 3),
            "diskrepanz_typ": self.diskrepanz_typ,
            "details": {
                "modalverb": self.B_analyse.modalverb,
                "quantor": self.B_analyse.quantor,
                "evidenz_stufe": self.E_analyse.stufe.label,
            }
        }


# =============================================================================
# B-EXTRAKTION
# =============================================================================

def extrahiere_B(text: str) -> BAnalyse:
    """
    Extrahiert die Behauptungsstärke (B) aus einem Text.

    Args:
        text: Der zu analysierende Text

    Returns:
        BAnalyse mit B-Wert und Details
    """
    text_lower = text.lower()

    # Modalverb finden
    modalverb = None
    modalverb_B = None
    for verb, b_wert in sorted(MODALVERBEN.items(), key=lambda x: len(x[0]), reverse=True):
        if verb in text_lower:
            modalverb = verb
            modalverb_B = b_wert
            break

    # Quantor finden
    quantor = None
    quantor_B = None
    for q, b_wert in sorted(QUANTOREN.items(), key=lambda x: len(x[0]), reverse=True):
        if q in text_lower:
            quantor = q
            quantor_B = b_wert
            break

    # Hedging finden
    hedging = []
    hedging_adjustment = 0.0

    for marker, adjustment in HEDGING_REDUKTOREN.items():
        if marker in text_lower:
            hedging.append((marker, adjustment))
            hedging_adjustment += adjustment

    for marker, adjustment in HEDGING_VERSTAERKER.items():
        if marker in text_lower:
            hedging.append((marker, adjustment))
            hedging_adjustment += adjustment

    # B berechnen
    if modalverb_B is not None and quantor_B is not None:
        # Beide vorhanden: gewichteter Durchschnitt
        base_B = (
            modalverb_B * B_GEWICHTE["modalverb"] +
            quantor_B * B_GEWICHTE["quantor"]
        ) / (B_GEWICHTE["modalverb"] + B_GEWICHTE["quantor"])
    elif modalverb_B is not None:
        base_B = modalverb_B
    elif quantor_B is not None:
        base_B = quantor_B
    else:
        base_B = B_DEFAULT

    # Hedging anwenden
    B = max(0.0, min(1.0, base_B + hedging_adjustment))

    return BAnalyse(
        B=B,
        modalverb=modalverb,
        modalverb_B=modalverb_B,
        quantor=quantor,
        quantor_B=quantor_B,
        hedging=hedging,
        hedging_adjustment=hedging_adjustment,
    )


# =============================================================================
# E-BERECHNUNG
# =============================================================================

def klassifiziere_evidenz(evidenz_beschreibung: str) -> Tuple[EvidenzStufe, List[str]]:
    """
    Klassifiziert eine Evidenzbeschreibung nach der 7-stufigen Hierarchie.

    Args:
        evidenz_beschreibung: Beschreibung der Evidenz

    Returns:
        Tuple aus EvidenzStufe und gefundenen Markern
    """
    text_lower = evidenz_beschreibung.lower()
    gefundene_marker = []

    # Von höchster zu niedrigster Stufe prüfen
    for stufe in EvidenzStufe:
        for marker in EVIDENZ_MARKER.get(stufe, []):
            if marker in text_lower:
                gefundene_marker.append(marker)

        if gefundene_marker:
            return stufe, gefundene_marker

    # Keine Marker gefunden -> niedrigste Stufe
    return EvidenzStufe.KEINE, []


def extrahiere_modifikatoren(evidenz_beschreibung: str) -> List[Tuple[str, float]]:
    """Extrahiert Evidenz-Modifikatoren aus der Beschreibung."""
    text_lower = evidenz_beschreibung.lower()
    modifikatoren = []

    for marker, adjustment in E_MODIFIKATOREN.items():
        if marker in text_lower:
            modifikatoren.append((marker, adjustment))

    return modifikatoren


def berechne_E(
    evidenz_beschreibung: Optional[str] = None,
    stufe: Optional[EvidenzStufe] = None,
    modifikatoren: Optional[List[Tuple[str, float]]] = None,
) -> EAnalyse:
    """
    Berechnet die Evidenzstärke (E).

    Args:
        evidenz_beschreibung: Freitext-Beschreibung der Evidenz
        stufe: Direkt angegebene Evidenzstufe (überschreibt Beschreibung)
        modifikatoren: Direkt angegebene Modifikatoren

    Returns:
        EAnalyse mit E-Wert und Details
    """
    marker_gefunden = []

    if stufe is None:
        if evidenz_beschreibung:
            stufe, marker_gefunden = klassifiziere_evidenz(evidenz_beschreibung)
        else:
            stufe = EvidenzStufe.KEINE

    if modifikatoren is None:
        if evidenz_beschreibung:
            modifikatoren = extrahiere_modifikatoren(evidenz_beschreibung)
        else:
            modifikatoren = []

    # Basis-E aus Stufe
    base_E = stufe.default_e

    # Modifikatoren anwenden
    adjustment = sum(adj for _, adj in modifikatoren)
    E = max(0.0, min(1.0, base_E + adjustment))

    return EAnalyse(
        E=E,
        stufe=stufe,
        marker_gefunden=marker_gefunden,
        modifikatoren=modifikatoren,
        base_E=base_E,
    )


# =============================================================================
# K-BERECHNUNG
# =============================================================================

def berechne_K(
    aussage: str,
    evidenz_beschreibung: Optional[str] = None,
    evidenz_stufe: Optional[EvidenzStufe] = None,
    E_wert: Optional[float] = None,
) -> KAnalyse:
    """
    Berechnet den K-Wert (Kalibrierung) für eine Aussage.

    Args:
        aussage: Die zu analysierende Aussage
        evidenz_beschreibung: Freitext-Beschreibung der Evidenz
        evidenz_stufe: Direkt angegebene Evidenzstufe
        E_wert: Direkt angegebener E-Wert (überschreibt alles andere)

    Returns:
        Vollständige KAnalyse
    """
    # B extrahieren
    B_analyse = extrahiere_B(aussage)

    # E berechnen
    if E_wert is not None:
        E_analyse = EAnalyse(
            E=E_wert,
            stufe=EvidenzStufe.KEINE,  # Placeholder
            base_E=E_wert,
        )
    else:
        E_analyse = berechne_E(
            evidenz_beschreibung=evidenz_beschreibung,
            stufe=evidenz_stufe,
        )

    # K berechnen
    K = 1.0 - abs(B_analyse.B - E_analyse.E)

    # Kategorie bestimmen
    kategorie = KKategorie.from_k(K)

    # Diskrepanz-Typ bestimmen
    diff = B_analyse.B - E_analyse.E
    if abs(diff) < 0.1:
        diskrepanz_typ = "kalibriert"
    elif diff > 0:
        diskrepanz_typ = "überbehauptung"
    else:
        diskrepanz_typ = "unterbehauptung"

    return KAnalyse(
        aussage=aussage,
        B_analyse=B_analyse,
        E_analyse=E_analyse,
        K=K,
        kategorie=kategorie,
        diskrepanz_typ=diskrepanz_typ,
    )


# =============================================================================
# BATCH-VERARBEITUNG
# =============================================================================

def analysiere_aussagen(aussagen: List[dict]) -> List[KAnalyse]:
    """
    Analysiert eine Liste von Aussagen.

    Args:
        aussagen: Liste von Dicts mit 'aussage' und optional 'evidenz'

    Returns:
        Liste von KAnalysen
    """
    ergebnisse = []

    for item in aussagen:
        aussage = item.get("aussage", item.get("text", ""))
        evidenz = item.get("evidenz", item.get("evidence", None))
        E_wert = item.get("E", item.get("e_wert", None))

        analyse = berechne_K(
            aussage=aussage,
            evidenz_beschreibung=evidenz,
            E_wert=E_wert,
        )
        ergebnisse.append(analyse)

    return ergebnisse


def aggregiere_K(analysen: List[KAnalyse]) -> dict:
    """
    Aggregiert K-Werte über mehrere Analysen.

    Returns:
        Dict mit Aggregationsstatistiken
    """
    if not analysen:
        return {"error": "Keine Analysen vorhanden"}

    K_werte = [a.K for a in analysen]
    B_werte = [a.B_analyse.B for a in analysen]
    E_werte = [a.E_analyse.E for a in analysen]

    # Kategorien zählen
    kategorien = {}
    for a in analysen:
        kat = a.kategorie.label
        kategorien[kat] = kategorien.get(kat, 0) + 1

    return {
        "anzahl": len(analysen),
        "K_mean": sum(K_werte) / len(K_werte),
        "K_min": min(K_werte),
        "K_max": max(K_werte),
        "B_mean": sum(B_werte) / len(B_werte),
        "E_mean": sum(E_werte) / len(E_werte),
        "kategorien": kategorien,
        "anteil_stabil": kategorien.get("🟢 Stabil", 0) / len(analysen),
        "anteil_kritisch": (
            kategorien.get("🟠 Interpretativ", 0) +
            kategorien.get("🔴 Spekulativ", 0)
        ) / len(analysen),
    }


# =============================================================================
# AUSGABE-FORMATIERUNG
# =============================================================================

def drucke_analyse(analyse: KAnalyse, verbose: bool = True):
    """Gibt eine Analyse formatiert aus."""
    print("\n" + "=" * 70)
    print(f"  AUSSAGE: {analyse.aussage[:60]}...")
    print("=" * 70)

    # K-Wert prominent
    print(f"\n  K = {analyse.K:.2f}  {analyse.kategorie.label}")
    print(f"  {analyse.kategorie.beschreibung}")

    # B und E
    print(f"\n  {'─' * 66}")
    print(f"  B (Behauptung):  {analyse.B_analyse.B:.2f}")
    print(f"  E (Evidenz):     {analyse.E_analyse.E:.2f}")
    print(f"  Differenz:       {analyse.B_analyse.B - analyse.E_analyse.E:+.2f} ({analyse.diskrepanz_typ})")

    if verbose:
        print(f"\n  {'─' * 66}")
        print("  DETAILS B:")
        if analyse.B_analyse.modalverb:
            print(f"    Modalverb: '{analyse.B_analyse.modalverb}' → {analyse.B_analyse.modalverb_B:.2f}")
        if analyse.B_analyse.quantor:
            print(f"    Quantor: '{analyse.B_analyse.quantor}' → {analyse.B_analyse.quantor_B:.2f}")
        if analyse.B_analyse.hedging:
            for h, v in analyse.B_analyse.hedging:
                print(f"    Hedging: '{h}' → {v:+.2f}")

        print("\n  DETAILS E:")
        print(f"    Stufe: {analyse.E_analyse.stufe.label}")
        if analyse.E_analyse.marker_gefunden:
            print(f"    Marker: {', '.join(analyse.E_analyse.marker_gefunden)}")
        if analyse.E_analyse.modifikatoren:
            for m, v in analyse.E_analyse.modifikatoren:
                print(f"    Modifikator: '{m}' → {v:+.2f}")

    print("\n" + "=" * 70)


def drucke_aggregation(agg: dict):
    """Gibt Aggregationsstatistiken aus."""
    print("\n" + "=" * 70)
    print("  AGGREGATION")
    print("=" * 70)

    print(f"\n  Anzahl Aussagen: {agg['anzahl']}")
    print(f"\n  K-Werte:")
    print(f"    Durchschnitt: {agg['K_mean']:.2f}")
    print(f"    Bereich:      {agg['K_min']:.2f} - {agg['K_max']:.2f}")

    print(f"\n  Kategorien:")
    for kat, count in agg['kategorien'].items():
        pct = count / agg['anzahl'] * 100
        print(f"    {kat}: {count} ({pct:.0f}%)")

    print(f"\n  Anteil stabil (K ≥ 0.8): {agg['anteil_stabil']*100:.0f}%")
    print(f"  Anteil kritisch (K < 0.6): {agg['anteil_kritisch']*100:.0f}%")

    print("\n" + "=" * 70)


# =============================================================================
# INTERAKTIVER MODUS
# =============================================================================

def interaktiver_modus():
    """Startet den interaktiven Modus."""
    print("\n" + "=" * 70)
    print("  ESL CALCULATOR - Interaktiver Modus")
    print("=" * 70)
    print("\n  Gib eine Aussage ein und optional Evidenz.")
    print("  Leere Eingabe beendet das Programm.\n")

    while True:
        aussage = input("  Aussage: ").strip()
        if not aussage:
            break

        evidenz = input("  Evidenz (optional): ").strip()
        if not evidenz:
            evidenz = None

        analyse = berechne_K(aussage, evidenz_beschreibung=evidenz)
        drucke_analyse(analyse)
        print()


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="ESL Calculator - Berechnet K-Werte für wissenschaftliche Aussagen"
    )

    parser.add_argument(
        "--aussage", "-a",
        help="Einzelne Aussage analysieren"
    )
    parser.add_argument(
        "--evidenz", "-e",
        help="Evidenzbeschreibung für die Aussage"
    )
    parser.add_argument(
        "--e-wert",
        type=float,
        help="Direkter E-Wert (0.0-1.0)"
    )
    parser.add_argument(
        "--datei", "-f",
        help="YAML-Datei mit Aussagen analysieren"
    )
    parser.add_argument(
        "--interaktiv", "-i",
        action="store_true",
        help="Interaktiver Modus"
    )
    parser.add_argument(
        "--kurz", "-k",
        action="store_true",
        help="Kurzausgabe (weniger Details)"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Ausgabe als JSON"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Demo mit Beispielaussagen"
    )

    args = parser.parse_args()

    if args.interaktiv:
        interaktiver_modus()

    elif args.aussage:
        analyse = berechne_K(
            aussage=args.aussage,
            evidenz_beschreibung=args.evidenz,
            E_wert=args.e_wert,
        )
        if args.json:
            import json
            print(json.dumps(analyse.to_dict(), indent=2, ensure_ascii=False))
        else:
            drucke_analyse(analyse, verbose=not args.kurz)

    elif args.datei:
        with open(args.datei, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        aussagen = data.get("aussagen", data.get("statements", []))
        analysen = analysiere_aussagen(aussagen)

        if args.json:
            import json
            result = {
                "analysen": [a.to_dict() for a in analysen],
                "aggregation": aggregiere_K(analysen),
            }
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            for analyse in analysen:
                drucke_analyse(analyse, verbose=not args.kurz)

            agg = aggregiere_K(analysen)
            drucke_aggregation(agg)

    elif args.demo:
        demo_aussagen = [
            {
                "aussage": "Alle Menschen müssen essen, um zu überleben.",
                "evidenz": "Meta-Analyse von biologischen Studien, repliziert",
            },
            {
                "aussage": "Loss Aversion könnte möglicherweise bei einigen Entscheidungen eine Rolle spielen.",
                "evidenz": "Qualitative Fallstudie mit kleinem N",
            },
            {
                "aussage": "BEATRIX verbessert Entscheidungen definitiv und nachweislich.",
                "evidenz": None,  # Keine Evidenz
            },
            {
                "aussage": "Die meisten Nutzer profitieren in der Regel von personalisierten Empfehlungen.",
                "evidenz": "Beobachtungsstudie mit N=500",
            },
        ]

        analysen = analysiere_aussagen(demo_aussagen)
        for analyse in analysen:
            drucke_analyse(analyse, verbose=not args.kurz)

        agg = aggregiere_K(analysen)
        drucke_aggregation(agg)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()

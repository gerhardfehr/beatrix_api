#!/usr/bin/env python3
"""
ESL Calculator - Empirical System of Language
==============================================

Berechnet K-Werte (Kalibrierung) für wissenschaftliche Aussagen
basierend auf Behauptungsstärke (B) und Evidenzstärke (E).

Kernformel: K = 1 - |B - E|

Unterstützt disziplinspezifische Profile (z.B. Verhaltensökonomie, BCM).

Nutzung:
    python esl_calculator.py --aussage "Alle Menschen müssen essen"
    python esl_calculator.py --aussage "Loss Aversion ist robust" --disziplin verhaltensoekonomie
    python esl_calculator.py --interaktiv
    python esl_calculator.py --datei aussagen.yaml --disziplin bcm
"""

import re
import argparse
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple, Union
from enum import Enum

# Disziplin-Profile importieren
try:
    from esl_disziplinen import (
        lade_disziplin,
        liste_disziplinen,
        DisziplinProfil,
        DEFAULT_PROFIL,
        VERHALTENSOEKONOMIE_PROFIL,
    )
    DISZIPLIN_SUPPORT = True
except ImportError:
    DISZIPLIN_SUPPORT = False
    DisziplinProfil = None


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
    """K-Wert Kategorien (Default-Schwellenwerte)"""
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
    def from_k(cls, k: float, profil: "DisziplinProfil" = None) -> "KKategorie":
        """
        Bestimmt K-Kategorie, optional mit disziplinspezifischen Schwellenwerten.

        Args:
            k: Der K-Wert
            profil: Optional ein DisziplinProfil mit angepassten Schwellenwerten
        """
        if profil is not None and DISZIPLIN_SUPPORT:
            # Nutze disziplinspezifische Schwellenwerte
            kat = profil.get_k_kategorie(k)
            # Mappe auf Enum für Kompatibilität
            mapping = {
                "stabil": cls.STABIL,
                "teilstabil": cls.TEILSTABIL,
                "interpretativ": cls.INTERPRETATIV,
                "spekulativ": cls.SPEKULATIV,
            }
            return mapping.get(kat.name, cls.SPEKULATIV)

        # Default-Schwellenwerte
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
    disziplin: Optional[str] = None  # Name des verwendeten Disziplin-Profils

    def __str__(self) -> str:
        disziplin_info = f" [{self.disziplin}]" if self.disziplin else ""
        return (
            f"K = {self.K:.2f} {self.kategorie.label}{disziplin_info}\n"
            f"  B: {self.B_analyse}\n"
            f"  E: {self.E_analyse}\n"
            f"  Typ: {self.diskrepanz_typ}"
        )

    def to_dict(self) -> dict:
        result = {
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
        if self.disziplin:
            result["disziplin"] = self.disziplin
        return result


# =============================================================================
# B-EXTRAKTION
# =============================================================================

def extrahiere_B(text: str, profil: "DisziplinProfil" = None) -> BAnalyse:
    """
    Extrahiert die Behauptungsstärke (B) aus einem Text.

    Args:
        text: Der zu analysierende Text
        profil: Optional ein DisziplinProfil mit zusätzlichen Markern

    Returns:
        BAnalyse mit B-Wert und Details
    """
    text_lower = text.lower()

    # Disziplin-spezifische Marker vorbereiten
    zusatz_quantoren = {}
    zusatz_hedging = {}
    zusatz_verstaerker = {}

    if profil is not None and DISZIPLIN_SUPPORT:
        zusatz_quantoren = profil.zusatz_quantoren
        zusatz_hedging = profil.zusatz_hedging
        zusatz_verstaerker = profil.zusatz_verstaerker

    # Modalverb finden
    modalverb = None
    modalverb_B = None
    for verb, b_wert in sorted(MODALVERBEN.items(), key=lambda x: len(x[0]), reverse=True):
        if verb in text_lower:
            modalverb = verb
            modalverb_B = b_wert
            break

    # Quantor finden (inkl. disziplinspezifische)
    quantor = None
    quantor_B = None
    alle_quantoren = {**QUANTOREN, **zusatz_quantoren}
    for q, b_wert in sorted(alle_quantoren.items(), key=lambda x: len(x[0]), reverse=True):
        if q in text_lower:
            quantor = q
            quantor_B = b_wert
            break

    # Hedging finden (inkl. disziplinspezifische)
    hedging = []
    hedging_adjustment = 0.0

    alle_reduktoren = {**HEDGING_REDUKTOREN, **zusatz_hedging}
    for marker, adjustment in alle_reduktoren.items():
        if marker in text_lower:
            hedging.append((marker, adjustment))
            hedging_adjustment += adjustment

    alle_verstaerker = {**HEDGING_VERSTAERKER, **zusatz_verstaerker}
    for marker, adjustment in alle_verstaerker.items():
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
    profil: "DisziplinProfil" = None,
) -> EAnalyse:
    """
    Berechnet die Evidenzstärke (E).

    Args:
        evidenz_beschreibung: Freitext-Beschreibung der Evidenz
        stufe: Direkt angegebene Evidenzstufe (überschreibt Beschreibung)
        modifikatoren: Direkt angegebene Modifikatoren
        profil: Optional ein DisziplinProfil mit angepassten E-Stufen

    Returns:
        EAnalyse mit E-Wert und Details
    """
    marker_gefunden = []
    base_E = 0.0

    # Disziplin-spezifische E-Modifikatoren
    zusatz_modifikatoren = {}
    if profil is not None and DISZIPLIN_SUPPORT:
        zusatz_modifikatoren = profil.e_modifikatoren

    if stufe is None:
        if evidenz_beschreibung:
            # Prüfe erst disziplinspezifische Evidenzstufen
            if profil is not None and DISZIPLIN_SUPPORT:
                disziplin_stufe, disziplin_marker = profil.get_evidenz_stufe(evidenz_beschreibung)
                if disziplin_marker:
                    marker_gefunden = disziplin_marker
                    base_E = disziplin_stufe.E_default
                    # Erstelle EvidenzStufe-ähnliches Objekt für Kompatibilität
                    stufe = EvidenzStufe.KEINE  # Placeholder
                    stufe_label = disziplin_stufe.name
                else:
                    # Fallback auf Standard-Klassifikation
                    stufe, marker_gefunden = klassifiziere_evidenz(evidenz_beschreibung)
                    base_E = stufe.default_e
                    stufe_label = stufe.label
            else:
                stufe, marker_gefunden = klassifiziere_evidenz(evidenz_beschreibung)
                base_E = stufe.default_e
        else:
            stufe = EvidenzStufe.KEINE
            base_E = stufe.default_e
    else:
        base_E = stufe.default_e

    if modifikatoren is None:
        if evidenz_beschreibung:
            # Standard + disziplinspezifische Modifikatoren
            modifikatoren = extrahiere_modifikatoren(evidenz_beschreibung)

            # Zusätzliche disziplinspezifische Modifikatoren
            text_lower = evidenz_beschreibung.lower()
            for marker, adjustment in zusatz_modifikatoren.items():
                if marker in text_lower:
                    modifikatoren.append((marker, adjustment))
        else:
            modifikatoren = []

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
    disziplin: Optional[str] = None,
    profil: "DisziplinProfil" = None,
) -> KAnalyse:
    """
    Berechnet den K-Wert (Kalibrierung) für eine Aussage.

    Args:
        aussage: Die zu analysierende Aussage
        evidenz_beschreibung: Freitext-Beschreibung der Evidenz
        evidenz_stufe: Direkt angegebene Evidenzstufe
        E_wert: Direkt angegebener E-Wert (überschreibt alles andere)
        disziplin: Name des Disziplin-Profils (z.B. "verhaltensoekonomie", "bcm")
        profil: Direkt übergebenes DisziplinProfil (überschreibt disziplin)

    Returns:
        Vollständige KAnalyse
    """
    # Disziplin-Profil laden
    disziplin_name = None
    if profil is None and disziplin is not None and DISZIPLIN_SUPPORT:
        profil = lade_disziplin(disziplin)
        disziplin_name = profil.name
    elif profil is not None:
        disziplin_name = profil.name

    # B extrahieren (mit Disziplin-Profil)
    B_analyse = extrahiere_B(aussage, profil=profil)

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
            profil=profil,
        )

    # K berechnen
    K = 1.0 - abs(B_analyse.B - E_analyse.E)

    # Kategorie bestimmen (mit Disziplin-Profil für angepasste Schwellenwerte)
    kategorie = KKategorie.from_k(K, profil=profil)

    # Diskrepanz-Typ bestimmen (mit Toleranzfenster aus Profil)
    toleranz = 0.1
    if profil is not None and DISZIPLIN_SUPPORT:
        toleranz = profil.toleranzfenster

    diff = B_analyse.B - E_analyse.E
    if abs(diff) < toleranz:
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
        disziplin=disziplin_name,
    )


# =============================================================================
# BATCH-VERARBEITUNG
# =============================================================================

def analysiere_aussagen(
    aussagen: List[dict],
    disziplin: Optional[str] = None,
    profil: "DisziplinProfil" = None,
) -> List[KAnalyse]:
    """
    Analysiert eine Liste von Aussagen.

    Args:
        aussagen: Liste von Dicts mit 'aussage' und optional 'evidenz'
        disziplin: Name des Disziplin-Profils für alle Aussagen
        profil: Direkt übergebenes DisziplinProfil

    Returns:
        Liste von KAnalysen
    """
    ergebnisse = []

    for item in aussagen:
        aussage = item.get("aussage", item.get("text", ""))
        evidenz = item.get("evidenz", item.get("evidence", None))
        E_wert = item.get("E", item.get("e_wert", None))

        # Item-spezifische Disziplin überschreibt globale
        item_disziplin = item.get("disziplin", disziplin)

        analyse = berechne_K(
            aussage=aussage,
            evidenz_beschreibung=evidenz,
            E_wert=E_wert,
            disziplin=item_disziplin,
            profil=profil if item_disziplin == disziplin else None,
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
    if analyse.disziplin:
        print(f"  DISZIPLIN: {analyse.disziplin}")
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

def interaktiver_modus(disziplin: Optional[str] = None):
    """Startet den interaktiven Modus."""
    print("\n" + "=" * 70)
    print("  ESL CALCULATOR - Interaktiver Modus")
    if disziplin:
        print(f"  Disziplin: {disziplin}")
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

        analyse = berechne_K(aussage, evidenz_beschreibung=evidenz, disziplin=disziplin)
        drucke_analyse(analyse)
        print()


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="ESL Calculator - Berechnet K-Werte für wissenschaftliche Aussagen",
        epilog="Beispiel: python esl_calculator.py -a 'Loss Aversion ist robust' -d bcm"
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
        "--disziplin", "-d",
        help="Disziplin-Profil (z.B. 'verhaltensoekonomie', 'bcm', 'beatrix')"
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
    parser.add_argument(
        "--liste-disziplinen",
        action="store_true",
        help="Liste verfügbarer Disziplin-Profile"
    )

    args = parser.parse_args()

    # Disziplin-Liste anzeigen
    if args.liste_disziplinen:
        if DISZIPLIN_SUPPORT:
            print("\nVerfügbare Disziplin-Profile:")
            print("-" * 40)
            for name in liste_disziplinen():
                profil = lade_disziplin(name)
                print(f"  {name:20} → {profil.name}")
            print()
        else:
            print("Fehler: Disziplin-Support nicht verfügbar (esl_disziplinen.py fehlt)")
        return

    if args.interaktiv:
        interaktiver_modus(disziplin=args.disziplin)

    elif args.aussage:
        analyse = berechne_K(
            aussage=args.aussage,
            evidenz_beschreibung=args.evidenz,
            E_wert=args.e_wert,
            disziplin=args.disziplin,
        )
        if args.json:
            import json
            print(json.dumps(analyse.to_dict(), indent=2, ensure_ascii=False))
        else:
            drucke_analyse(analyse, verbose=not args.kurz)

    elif args.datei:
        with open(args.datei, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        # Disziplin aus Datei oder CLI
        disziplin = args.disziplin or data.get("disziplin", None)

        aussagen = data.get("aussagen", data.get("statements", []))
        analysen = analysiere_aussagen(aussagen, disziplin=disziplin)

        if args.json:
            import json
            result = {
                "disziplin": disziplin,
                "analysen": [a.to_dict() for a in analysen],
                "aggregation": aggregiere_K(analysen),
            }
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            if disziplin:
                print(f"\n  Disziplin-Profil: {disziplin}")
            for analyse in analysen:
                drucke_analyse(analyse, verbose=not args.kurz)

            agg = aggregiere_K(analysen)
            drucke_aggregation(agg)

    elif args.demo:
        # Demo mit Default-Profil
        demo_aussagen_default = [
            {
                "aussage": "Alle Menschen müssen essen, um zu überleben.",
                "evidenz": "Meta-Analyse von biologischen Studien, repliziert",
            },
            {
                "aussage": "Die meisten Nutzer profitieren in der Regel von personalisierten Empfehlungen.",
                "evidenz": "Beobachtungsstudie mit N=500",
            },
        ]

        # Demo mit BCM/Verhaltensökonomie-Profil
        demo_aussagen_bcm = [
            {
                "aussage": "Loss Aversion ist ein robustes Phänomen mit λ ≈ 2.0",
                "evidenz": "Meta-Analyse, repliziert, präregistriert",
            },
            {
                "aussage": "Hyperbolic Discounting könnte bei einigen Entscheidungen auftreten.",
                "evidenz": "Laborexperiment mit kleinem N",
            },
            {
                "aussage": "BCM muss alle Verhaltensänderungen vorhersagen können.",
                "evidenz": None,  # Keine Evidenz
            },
            {
                "aussage": "Nudging zeigt konsistente Effekte in Feldexperimenten.",
                "evidenz": "Feldexperiment, präregistriert, großes N",
            },
        ]

        disziplin = args.disziplin

        if disziplin:
            print(f"\n  DEMO mit Disziplin-Profil: {disziplin}")
            analysen = analysiere_aussagen(demo_aussagen_bcm, disziplin=disziplin)
        else:
            # Zeige beide Profile im Vergleich
            print("\n  DEMO: Vergleich Default vs. Verhaltensökonomie")
            print("\n  --- DEFAULT PROFIL ---")
            analysen_default = analysiere_aussagen(demo_aussagen_default)
            for analyse in analysen_default:
                drucke_analyse(analyse, verbose=not args.kurz)

            if DISZIPLIN_SUPPORT:
                print("\n  --- VERHALTENSÖKONOMIE PROFIL ---")
                analysen_bcm = analysiere_aussagen(demo_aussagen_bcm, disziplin="bcm")
                for analyse in analysen_bcm:
                    drucke_analyse(analyse, verbose=not args.kurz)
                analysen = analysen_default + analysen_bcm
            else:
                analysen = analysen_default

        if disziplin:
            for analyse in analysen:
                drucke_analyse(analyse, verbose=not args.kurz)

        agg = aggregiere_K(analysen)
        drucke_aggregation(agg)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()

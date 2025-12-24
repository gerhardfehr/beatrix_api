#!/usr/bin/env python3
"""
ESL Disziplin-Profile
=====================

Lädt und verwaltet disziplinspezifische ESL-Profile.

Nutzung:
    from esl_disziplinen import lade_disziplin, VERHALTENSOEKONOMIE
"""

import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from enum import Enum


# =============================================================================
# PFADE
# =============================================================================

DISZIPLINEN_PFAD = Path(__file__).parent / "methodik" / "disziplinen"


# =============================================================================
# DISZIPLIN-PROFILE
# =============================================================================

@dataclass
class EvidenzStufe:
    """Eine Stufe in der Evidenzhierarchie"""
    name: str
    E_min: float
    E_max: float
    beschreibung: str = ""
    marker: List[str] = field(default_factory=list)
    beispiele: List[str] = field(default_factory=list)

    @property
    def E_default(self) -> float:
        return (self.E_min + self.E_max) / 2


@dataclass
class KKategorie:
    """Eine K-Wert Kategorie"""
    name: str
    label: str
    K_min: float
    K_max: float
    bedeutung: str = ""
    aktion: str = ""


@dataclass
class DisziplinProfil:
    """Vollständiges Disziplin-Profil"""
    id: str
    name: str
    toleranzfenster: float

    # E-Skala
    evidenz_stufen: List[EvidenzStufe]

    # K-Schwellenwerte
    k_kategorien: List[KKategorie]

    # Zusätzliche B-Marker
    zusatz_quantoren: Dict[str, float] = field(default_factory=dict)
    zusatz_hedging: Dict[str, float] = field(default_factory=dict)
    zusatz_verstaerker: Dict[str, float] = field(default_factory=dict)

    # E-Modifikatoren
    e_modifikatoren: Dict[str, float] = field(default_factory=dict)

    def get_k_kategorie(self, K: float) -> KKategorie:
        """Bestimmt die K-Kategorie für einen Wert."""
        for kat in self.k_kategorien:
            if kat.K_min <= K <= kat.K_max:
                return kat
        # Fallback
        return self.k_kategorien[-1]

    def get_evidenz_stufe(self, text: str) -> Tuple[EvidenzStufe, List[str]]:
        """Klassifiziert Text nach Evidenzstufe."""
        text_lower = text.lower()
        gefundene_marker = []

        for stufe in self.evidenz_stufen:
            for marker in stufe.marker:
                if marker.lower() in text_lower:
                    gefundene_marker.append(marker)

            if gefundene_marker:
                return stufe, gefundene_marker

        # Keine Marker → niedrigste Stufe
        return self.evidenz_stufen[-1], []


# =============================================================================
# STANDARD-PROFILE
# =============================================================================

# Default/Generisches Profil
DEFAULT_PROFIL = DisziplinProfil(
    id="default",
    name="Allgemein/Default",
    toleranzfenster=0.15,
    evidenz_stufen=[
        EvidenzStufe("Meta-Analyse", 0.90, 1.00, marker=["meta-analyse", "systematic review"]),
        EvidenzStufe("RCT", 0.80, 0.90, marker=["randomisiert", "rct", "kontrollierte studie"]),
        EvidenzStufe("Quasi-experimentell", 0.65, 0.80, marker=["quasi-experimentell"]),
        EvidenzStufe("Beobachtung", 0.50, 0.65, marker=["beobachtung", "korrelation"]),
        EvidenzStufe("Fallstudie", 0.35, 0.50, marker=["fallstudie", "qualitativ"]),
        EvidenzStufe("Experteneinschätzung", 0.20, 0.35, marker=["experten", "theoretisch"]),
        EvidenzStufe("Keine Evidenz", 0.00, 0.20, marker=["bekannt", "offensichtlich"]),
    ],
    k_kategorien=[
        KKategorie("stabil", "🟢 Stabil", 0.80, 1.00, "Behauptung gedeckt", "Keine"),
        KKategorie("teilstabil", "🟡 Teilstabil", 0.60, 0.80, "Leichte Diskrepanz", "Optional"),
        KKategorie("interpretativ", "🟠 Interpretativ", 0.40, 0.60, "Signifikante Lücke", "Empfohlen"),
        KKategorie("spekulativ", "🔴 Spekulativ", 0.00, 0.40, "Starke Diskrepanz", "Erforderlich"),
    ],
)


# Verhaltensökonomie-Profil
VERHALTENSOEKONOMIE_PROFIL = DisziplinProfil(
    id="verhaltensoekonomie",
    name="Verhaltensökonomie / Behavioral Economics",
    toleranzfenster=0.15,
    evidenz_stufen=[
        EvidenzStufe(
            "Meta-Analyse verhaltensök. Studien",
            0.88, 1.00,
            marker=["meta-analyse", "systematic review", "gepoolte effektgröße"],
            beispiele=["Meta-Analyse zu Loss Aversion"]
        ),
        EvidenzStufe(
            "Präregistrierte Feldexperimente",
            0.78, 0.88,
            marker=["präregistriert", "feldexperiment", "rct", "field experiment", "randomized", "reale entscheidung"],
            beispiele=["RCT mit echten finanziellen Konsequenzen"]
        ),
        EvidenzStufe(
            "Labor-Experimente (incentivized)",
            0.65, 0.78,
            marker=["labor", "laborexperiment", "incentivized", "anreizkompatibel", "experiment zeigt"],
            beispiele=["Kahneman & Tversky Paradigmen"]
        ),
        EvidenzStufe(
            "Beobachtung / Survey",
            0.50, 0.65,
            marker=["survey", "befragung", "korrelation", "beobachtung", "stated preference", "hypothetisch"],
            beispiele=["Survey mit Stated Preferences"]
        ),
        EvidenzStufe(
            "Fallstudien / Qualitativ",
            0.35, 0.50,
            marker=["fallstudie", "qualitativ", "interview", "explorativ", "case study"],
        ),
        EvidenzStufe(
            "Axiomatische Ableitung",
            0.30, 0.45,
            marker=["axiom", "abgeleitet", "folgt aus", "theorem", "formal", "mathematisch", "bcm"],
            beispiele=["Abgeleitet aus BCM Axiom MA-ONT-05"]
        ),
        EvidenzStufe(
            "Experteneinschätzung",
            0.20, 0.35,
            marker=["experten", "einschätzung", "konsens", "nach meinung", "annahme"],
        ),
        EvidenzStufe(
            "Unbegründet",
            0.00, 0.20,
            marker=["bekannt", "offensichtlich", "selbstverständlich", "klar"],
        ),
    ],
    k_kategorien=[
        KKategorie("stabil", "🟢 Stabil", 0.75, 1.00,
                   "Aussage gut durch Evidenz gedeckt", "Publikationsreif"),
        KKategorie("teilstabil", "🟡 Teilstabil", 0.55, 0.75,
                   "Akzeptable Diskrepanz für Sozialwissenschaft", "Akzeptabel mit Hinweis"),
        KKategorie("interpretativ", "🟠 Interpretativ", 0.35, 0.55,
                   "Signifikante Lücke zwischen Behauptung und Evidenz", "Hedging hinzufügen"),
        KKategorie("spekulativ", "🔴 Spekulativ", 0.00, 0.35,
                   "Behauptung deutlich über Evidenz", "Überarbeitung erforderlich"),
    ],
    zusatz_quantoren={
        "signifikant": 0.80,
        "robust": 0.85,
        "konsistent": 0.75,
        "teilweise": 0.50,
    },
    zusatz_hedging={
        "weitere forschung nötig": -0.20,
        "vorläufige evidenz": -0.15,
        "suggestive evidence": -0.15,
    },
    zusatz_verstaerker={
        "robust evidence": 0.10,
        "strong support": 0.12,
        "well-established": 0.15,
        "replicated finding": 0.15,
    },
    e_modifikatoren={
        "repliziert": 0.08,
        "nicht repliziert": -0.15,
        "präregistriert": 0.05,
        "großes n": 0.05,
        "kleines n": -0.08,
        "multi-site": 0.05,
    },
)


# =============================================================================
# PROFIL-REGISTRY
# =============================================================================

PROFILE: Dict[str, DisziplinProfil] = {
    "default": DEFAULT_PROFIL,
    "verhaltensoekonomie": VERHALTENSOEKONOMIE_PROFIL,
    "behavioral_economics": VERHALTENSOEKONOMIE_PROFIL,  # Alias
    "bcm": VERHALTENSOEKONOMIE_PROFIL,  # Alias für BCM
    "beatrix": VERHALTENSOEKONOMIE_PROFIL,  # Alias für BEATRIX
}


def lade_disziplin(name: str) -> DisziplinProfil:
    """Lädt ein Disziplin-Profil nach Name."""
    name_lower = name.lower().replace("-", "_").replace(" ", "_")

    if name_lower in PROFILE:
        return PROFILE[name_lower]

    # Versuche YAML-Datei zu laden
    yaml_pfad = DISZIPLINEN_PFAD / f"{name_lower}.yaml"
    if yaml_pfad.exists():
        return lade_disziplin_yaml(yaml_pfad)

    # Fallback zu Default
    print(f"Warnung: Disziplin '{name}' nicht gefunden, verwende Default")
    return DEFAULT_PROFIL


def lade_disziplin_yaml(pfad: Path) -> DisziplinProfil:
    """Lädt ein Disziplin-Profil aus YAML-Datei."""
    with open(pfad, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Extrahiere Daten
    meta = data.get("meta", {})
    e_skala = data.get("e_skala", {}).get("stufen", {})
    k_schwellen = data.get("k_schwellenwerte", {}).get("kategorien", {})
    b_anpassungen = data.get("b_skala_anpassungen", {}).get("zusaetzliche_marker", {})

    # Baue Evidenz-Stufen
    evidenz_stufen = []
    for stufen_id, stufen_data in e_skala.items():
        E_range = stufen_data.get("E_range", [0.0, 0.2])
        evidenz_stufen.append(EvidenzStufe(
            name=stufen_data.get("name", stufen_id),
            E_min=E_range[0],
            E_max=E_range[1],
            beschreibung=stufen_data.get("beschreibung", ""),
            marker=stufen_data.get("marker", []),
            beispiele=stufen_data.get("beispiele", []),
        ))

    # Sortiere nach E_max (höchste zuerst)
    evidenz_stufen.sort(key=lambda x: x.E_max, reverse=True)

    # Baue K-Kategorien
    k_kategorien = []
    for kat_id, kat_data in k_schwellen.items():
        K_range = kat_data.get("range", [0.0, 1.0])
        k_kategorien.append(KKategorie(
            name=kat_id,
            label=kat_data.get("label", kat_id),
            K_min=K_range[0],
            K_max=K_range[1],
            bedeutung=kat_data.get("bedeutung", ""),
            aktion=kat_data.get("aktion", ""),
        ))

    # Sortiere nach K_max (höchste zuerst)
    k_kategorien.sort(key=lambda x: x.K_max, reverse=True)

    return DisziplinProfil(
        id=meta.get("id", pfad.stem),
        name=meta.get("name", pfad.stem),
        toleranzfenster=meta.get("toleranzfenster", 0.15),
        evidenz_stufen=evidenz_stufen,
        k_kategorien=k_kategorien,
        zusatz_quantoren=b_anpassungen.get("quantoren", {}),
        zusatz_hedging=b_anpassungen.get("hedging", {}),
        zusatz_verstaerker=b_anpassungen.get("verstaerker", {}),
    )


def liste_disziplinen() -> List[str]:
    """Listet alle verfügbaren Disziplin-Profile."""
    profile = list(PROFILE.keys())

    # Füge YAML-Dateien hinzu
    if DISZIPLINEN_PFAD.exists():
        for yaml_file in DISZIPLINEN_PFAD.glob("*.yaml"):
            name = yaml_file.stem
            if name not in profile:
                profile.append(name)

    return sorted(set(profile))


# =============================================================================
# VERGLEICHSTABELLE
# =============================================================================

def drucke_vergleich():
    """Druckt Vergleich zwischen Default und Verhaltensökonomie."""
    print("\n" + "=" * 70)
    print("  DISZIPLIN-VERGLEICH: K-Schwellenwerte")
    print("=" * 70)

    print("\n  | Kategorie      | Default    | Verhaltensök. | Differenz |")
    print("  |----------------|------------|---------------|-----------|")

    default = DEFAULT_PROFIL
    vecon = VERHALTENSOEKONOMIE_PROFIL

    for d_kat, v_kat in zip(default.k_kategorien, vecon.k_kategorien):
        diff = v_kat.K_min - d_kat.K_min
        print(f"  | {d_kat.label:14} | ≥ {d_kat.K_min:.2f}     | ≥ {v_kat.K_min:.2f}        | {diff:+.2f}      |")

    print("\n  Verhaltensökonomie verwendet niedrigere Schwellen,")
    print("  da Sozialwissenschaften inhärent mehr Variabilität haben.")
    print("=" * 70)


if __name__ == "__main__":
    print("Verfügbare Disziplin-Profile:")
    for name in liste_disziplinen():
        profil = lade_disziplin(name)
        print(f"  - {name}: {profil.name} (τ={profil.toleranzfenster})")

    drucke_vergleich()

#!/usr/bin/env python3
"""
ESL Report Generator
====================

Generiert ESL-Berichte in drei Formaten:
- Fast & Clear (1-Pager)
- Standard (3-5 Seiten)
- Full Audit (10+ Seiten)

Nutzung:
    python esl_report_generator.py analyse.json --typ fast
    python esl_report_generator.py analyse.json --typ standard
    python esl_report_generator.py analyse.json --typ audit
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass


# =============================================================================
# REPORT TYPEN
# =============================================================================

class ReportTyp:
    FAST = "fast"
    STANDARD = "standard"
    AUDIT = "audit"


# =============================================================================
# DATENSTRUKTUREN
# =============================================================================

@dataclass
class ReportData:
    """Aufbereitete Daten für Reports"""
    dokument_titel: str
    autoren: str
    datum: str
    pruefer: str
    version: str

    # Aggregierte Werte
    anzahl: int
    K_mean: float
    K_min: float
    K_max: float
    B_mean: float
    E_mean: float

    # Kategorien
    n_stabil: int
    n_teilstabil: int
    n_interpretativ: int
    n_spekulativ: int

    # Prozente
    pct_stabil: float
    pct_teilstabil: float
    pct_interpretativ: float
    pct_spekulativ: float
    pct_kritisch: float

    # Diskrepanz-Typen
    n_ueberbehauptung: int
    n_kalibriert: int
    n_unterbehauptung: int

    # Kategorie-Info
    kategorie_emoji: str
    kategorie_label: str

    # Analysen (Listen)
    analysen: List[dict]
    kritische_aussagen: List[dict]
    stabile_aussagen: List[dict]

    # Empfehlungen
    empfehlungen: List[dict]


# =============================================================================
# DATENAUFBEREITUNG
# =============================================================================

def lade_analyse(pfad: Path) -> dict:
    """Lädt eine ESL-Analyse aus JSON."""
    with open(pfad, 'r', encoding='utf-8') as f:
        return json.load(f)


def bereite_daten_auf(
    analyse: dict,
    dokument_titel: str = "Unbekannt",
    autoren: str = "Unbekannt",
    pruefer: str = "ESL Calculator",
    version: str = "1.0"
) -> ReportData:
    """Bereitet Analysedaten für Report auf."""

    analysen = analyse.get("analysen", [])
    agg = analyse.get("aggregation", {})

    anzahl = agg.get("anzahl", len(analysen))
    K_mean = agg.get("K_mean", 0.0)
    B_mean = agg.get("B_mean", 0.0)
    E_mean = agg.get("E_mean", 0.0)

    # K min/max berechnen
    K_werte = [a.get("K", 0) for a in analysen]
    K_min = min(K_werte) if K_werte else 0.0
    K_max = max(K_werte) if K_werte else 0.0

    # Kategorien aus Aggregation
    kategorien = agg.get("kategorien", {})
    n_stabil = kategorien.get("🟢 Stabil", 0)
    n_teilstabil = kategorien.get("🟡 Teilstabil", 0)
    n_interpretativ = kategorien.get("🟠 Interpretativ", 0)
    n_spekulativ = kategorien.get("🔴 Spekulativ", 0)

    # Prozente
    total = anzahl if anzahl > 0 else 1
    pct_stabil = n_stabil / total * 100
    pct_teilstabil = n_teilstabil / total * 100
    pct_interpretativ = n_interpretativ / total * 100
    pct_spekulativ = n_spekulativ / total * 100
    pct_kritisch = (n_interpretativ + n_spekulativ) / total * 100

    # Diskrepanz-Typen zählen
    n_ueberbehauptung = sum(1 for a in analysen if a.get("diskrepanz_typ") == "überbehauptung")
    n_kalibriert = sum(1 for a in analysen if a.get("diskrepanz_typ") == "kalibriert")
    n_unterbehauptung = sum(1 for a in analysen if a.get("diskrepanz_typ") == "unterbehauptung")

    # Kategorie bestimmen
    if K_mean >= 0.8:
        kategorie_emoji = "🟢"
        kategorie_label = "Stabil"
    elif K_mean >= 0.6:
        kategorie_emoji = "🟡"
        kategorie_label = "Teilstabil"
    elif K_mean >= 0.4:
        kategorie_emoji = "🟠"
        kategorie_label = "Interpretativ"
    else:
        kategorie_emoji = "🔴"
        kategorie_label = "Spekulativ"

    # Kritische und stabile Aussagen
    kritische = [a for a in analysen if a.get("K", 1) < 0.6]
    stabile = [a for a in analysen if a.get("K", 0) >= 0.8]

    # Empfehlungen generieren
    empfehlungen = generiere_empfehlungen(analysen, K_mean, pct_kritisch)

    return ReportData(
        dokument_titel=dokument_titel,
        autoren=autoren,
        datum=datetime.now().strftime("%Y-%m-%d"),
        pruefer=pruefer,
        version=version,
        anzahl=anzahl,
        K_mean=K_mean,
        K_min=K_min,
        K_max=K_max,
        B_mean=B_mean,
        E_mean=E_mean,
        n_stabil=n_stabil,
        n_teilstabil=n_teilstabil,
        n_interpretativ=n_interpretativ,
        n_spekulativ=n_spekulativ,
        pct_stabil=pct_stabil,
        pct_teilstabil=pct_teilstabil,
        pct_interpretativ=pct_interpretativ,
        pct_spekulativ=pct_spekulativ,
        pct_kritisch=pct_kritisch,
        n_ueberbehauptung=n_ueberbehauptung,
        n_kalibriert=n_kalibriert,
        n_unterbehauptung=n_unterbehauptung,
        kategorie_emoji=kategorie_emoji,
        kategorie_label=kategorie_label,
        analysen=analysen,
        kritische_aussagen=sorted(kritische, key=lambda x: x.get("K", 1)),
        stabile_aussagen=sorted(stabile, key=lambda x: x.get("K", 0), reverse=True),
        empfehlungen=empfehlungen,
    )


def generiere_empfehlungen(analysen: List[dict], K_mean: float, pct_kritisch: float) -> List[dict]:
    """Generiert Empfehlungen basierend auf Analyse."""
    empfehlungen = []

    # Generelle Empfehlung basierend auf K_mean
    if K_mean < 0.4:
        empfehlungen.append({
            "prioritaet": "KRITISCH",
            "titel": "Grundlegende Überarbeitung erforderlich",
            "text": "Der durchschnittliche K-Wert liegt im spekulativen Bereich. "
                    "Die meisten Behauptungen übersteigen die verfügbare Evidenz deutlich.",
            "aktion": "Alle Aussagen auf Evidenzbasis prüfen und Sprache rekalibrieren."
        })

    elif K_mean < 0.6:
        empfehlungen.append({
            "prioritaet": "HOCH",
            "titel": "Signifikante Überarbeitung empfohlen",
            "text": "Der durchschnittliche K-Wert zeigt eine systematische Diskrepanz "
                    "zwischen Behauptungen und Evidenz.",
            "aktion": "Kritische Aussagen (K < 0.6) überarbeiten, Hedging hinzufügen."
        })

    # Spezifische Empfehlungen
    n_keine_evidenz = sum(1 for a in analysen
                         if a.get("details", {}).get("evidenz_stufe") == "Keine Evidenz/Unbegründet")

    if n_keine_evidenz > 0:
        empfehlungen.append({
            "prioritaet": "HOCH",
            "titel": f"{n_keine_evidenz} Aussagen ohne Evidenz",
            "text": f"{n_keine_evidenz} Aussagen haben keine erkennbare Evidenzbasis.",
            "aktion": "Quellen ergänzen oder als Hypothese/Konzept kennzeichnen."
        })

    # Überbehauptungen
    n_ueber = sum(1 for a in analysen if a.get("diskrepanz_typ") == "überbehauptung")
    if n_ueber > len(analysen) * 0.5:
        empfehlungen.append({
            "prioritaet": "MITTEL",
            "titel": "Systematische Überbehauptung",
            "text": f"{n_ueber} von {len(analysen)} Aussagen sind Überbehauptungen.",
            "aktion": "Hedging-Marker hinzufügen: 'könnte', 'möglicherweise', 'deutet darauf hin'."
        })

    return empfehlungen


# =============================================================================
# REPORT GENERIERUNG
# =============================================================================

def generiere_fast_report(data: ReportData) -> str:
    """Generiert Fast & Clear Report (1-Pager)."""

    # Top 3 Probleme
    top_probleme = data.kritische_aussagen[:3]

    # Empfehlung
    if data.K_mean >= 0.8:
        empfehlung = "✅ Dokument ist publikationsreif."
    elif data.K_mean >= 0.6:
        empfehlung = "🟡 Dokument ist akzeptabel. Optionale Verbesserungen möglich."
    elif data.K_mean >= 0.4:
        empfehlung = "🟠 Überarbeitung empfohlen vor Publikation."
    else:
        empfehlung = "🔴 Grundlegende Überarbeitung erforderlich."

    # Report zusammenbauen
    report = f"""# ESL Report: Fast & Clear

---

## {data.dokument_titel}
**Datum:** {data.datum} | **Prüfer:** {data.pruefer} | **Version:** {data.version}

---

## Gesamt-Kalibrierung

```
┌────────────────────────────────────────────┐
│                                            │
│         K = {data.K_mean:.2f}  {data.kategorie_emoji}                       │
│                                            │
│         {data.kategorie_label:^34}         │
│                                            │
└────────────────────────────────────────────┘
```

| Metrik | Wert | Bewertung |
|--------|------|-----------|
| **K (Durchschnitt)** | {data.K_mean:.2f} | {data.kategorie_label} |
| **B (Behauptung)** | {data.B_mean:.2f} | {"Hoch" if data.B_mean > 0.7 else "Mittel" if data.B_mean > 0.5 else "Niedrig"} |
| **E (Evidenz)** | {data.E_mean:.2f} | {"Hoch" if data.E_mean > 0.7 else "Mittel" if data.E_mean > 0.5 else "Niedrig"} |
| **Aussagen gesamt** | {data.anzahl} | - |

---

## Verteilung

| Status | Anzahl | Anteil |
|--------|--------|--------|
| 🟢 Stabil (K ≥ 0.8) | {data.n_stabil} | {data.pct_stabil:.0f}% |
| 🟡 Teilstabil (0.6-0.8) | {data.n_teilstabil} | {data.pct_teilstabil:.0f}% |
| 🟠 Interpretativ (0.4-0.6) | {data.n_interpretativ} | {data.pct_interpretativ:.0f}% |
| 🔴 Spekulativ (< 0.4) | {data.n_spekulativ} | {data.pct_spekulativ:.0f}% |

---

## Top 3 Probleme

"""

    for i, prob in enumerate(top_probleme, 1):
        aussage = prob.get("aussage", "")[:50] + "..."
        K = prob.get("K", 0)
        typ = prob.get("diskrepanz_typ", "")
        report += f"{i}. **{aussage}**\n   K={K:.2f} | {typ}\n\n"

    if not top_probleme:
        report += "*Keine kritischen Aussagen gefunden.*\n\n"

    report += f"""---

## Empfehlung

> {empfehlung}

---

**Status:** {data.kategorie_label} | **Nächste Prüfung:** Nach Überarbeitung
"""

    return report


def generiere_standard_report(data: ReportData) -> str:
    """Generiert Standard Report (3-5 Seiten)."""

    # Kritische Aussagen Tabelle
    kritische_tabelle = "| # | Aussage | K | B | E | Typ |\n|---|---------|---|---|---|-----|\n"
    for i, a in enumerate(data.kritische_aussagen[:10], 1):
        aussage = a.get("aussage", "")[:40] + "..."
        kritische_tabelle += f"| {i} | {aussage} | {a.get('K', 0):.2f} | {a.get('B', 0):.2f} | {a.get('E', 0):.2f} | {a.get('diskrepanz_typ', '')} |\n"

    # Stabile Aussagen Tabelle
    stabile_tabelle = "| # | Aussage | K | B | E |\n|---|---------|---|---|---|\n"
    for i, a in enumerate(data.stabile_aussagen[:5], 1):
        aussage = a.get("aussage", "")[:40] + "..."
        stabile_tabelle += f"| {i} | {aussage} | {a.get('K', 0):.2f} | {a.get('B', 0):.2f} | {a.get('E', 0):.2f} |\n"

    # Empfehlungen
    empf_hoch = ""
    empf_mittel = ""
    for e in data.empfehlungen:
        prio = e.get("prioritaet", "")
        text = f"- **{e.get('titel', '')}**: {e.get('text', '')} → *{e.get('aktion', '')}*\n"
        if prio in ["KRITISCH", "HOCH"]:
            empf_hoch += text
        else:
            empf_mittel += text

    diskrepanz = data.B_mean - data.E_mean

    report = f"""# ESL Report: Standard

---

## Dokumentinformationen

| Feld | Wert |
|------|------|
| **Dokument** | {data.dokument_titel} |
| **Autor(en)** | {data.autoren} |
| **Prüfdatum** | {data.datum} |
| **Prüfer** | {data.pruefer} |
| **Report-Version** | {data.version} |

---

## 1. Executive Summary

### Gesamt-Kalibrierung

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│              K = {data.K_mean:.2f}  {data.kategorie_emoji}                                    │
│                                                              │
│              {data.kategorie_label:^44}              │
│                                                              │
│    B (Behauptung): {data.B_mean:.2f}    |    E (Evidenz): {data.E_mean:.2f}                │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Kernbefunde

- **{data.anzahl} Aussagen** analysiert
- **{data.pct_kritisch:.0f}%** der Aussagen sind kritisch (K < 0.6)
- **Hauptproblem:** {"Systematische Überbehauptung" if data.n_ueberbehauptung > data.anzahl/2 else "Mangelnde Evidenz" if data.E_mean < 0.3 else "Gemischte Probleme"}
- **Empfehlung:** {"Grundlegende Überarbeitung" if data.K_mean < 0.4 else "Überarbeitung empfohlen" if data.K_mean < 0.6 else "Akzeptabel" if data.K_mean < 0.8 else "Publikationsreif"}

---

## 2. Detaillierte Ergebnisse

### 2.1 Verteilung der K-Werte

| Kategorie | K-Bereich | Anzahl | Anteil | Bedeutung |
|-----------|-----------|--------|--------|-----------|
| 🟢 Stabil | ≥ 0.80 | {data.n_stabil} | {data.pct_stabil:.0f}% | Behauptung durch Evidenz gedeckt |
| 🟡 Teilstabil | 0.60-0.79 | {data.n_teilstabil} | {data.pct_teilstabil:.0f}% | Leichte Diskrepanz |
| 🟠 Interpretativ | 0.40-0.59 | {data.n_interpretativ} | {data.pct_interpretativ:.0f}% | Signifikante Lücke |
| 🔴 Spekulativ | < 0.40 | {data.n_spekulativ} | {data.pct_spekulativ:.0f}% | Behauptung übersteigt Evidenz |

### 2.2 B/E-Analyse

| Metrik | Wert | Interpretation |
|--------|------|----------------|
| B (Durchschnitt) | {data.B_mean:.2f} | {"Starke Behauptungen" if data.B_mean > 0.7 else "Moderate Behauptungen" if data.B_mean > 0.5 else "Vorsichtige Behauptungen"} |
| E (Durchschnitt) | {data.E_mean:.2f} | {"Starke Evidenz" if data.E_mean > 0.7 else "Moderate Evidenz" if data.E_mean > 0.4 else "Schwache Evidenz"} |
| B - E (Diskrepanz) | {diskrepanz:+.2f} | {"Überbehauptung" if diskrepanz > 0.1 else "Kalibriert" if diskrepanz > -0.1 else "Unterbehauptung"} |

### 2.3 Diskrepanz-Typen

| Typ | Anzahl | Beschreibung |
|-----|--------|--------------|
| Überbehauptung (B > E) | {data.n_ueberbehauptung} | Sprache stärker als Evidenz |
| Kalibriert (B ≈ E) | {data.n_kalibriert} | Gute Übereinstimmung |
| Unterbehauptung (B < E) | {data.n_unterbehauptung} | Evidenz nicht ausgeschöpft |

---

## 3. Problemanalyse

### 3.1 Kritische Aussagen (K < 0.6)

{kritische_tabelle if data.kritische_aussagen else "*Keine kritischen Aussagen.*"}

---

## 4. Stärken

### 4.1 Stabile Aussagen (K ≥ 0.8)

{stabile_tabelle if data.stabile_aussagen else "*Keine stabilen Aussagen.*"}

---

## 5. Empfehlungen

### 5.1 Sofortmassnahmen (Priorität HOCH)

{empf_hoch if empf_hoch else "*Keine kritischen Massnahmen erforderlich.*"}

### 5.2 Mittelfristige Massnahmen

{empf_mittel if empf_mittel else "*Keine mittelfristigen Massnahmen.*"}

---

## 6. Fazit

{"Das Dokument erfüllt die ESL-Qualitätsstandards und ist publikationsreif." if data.K_mean >= 0.8 else
 "Das Dokument ist grundsätzlich akzeptabel, könnte aber von gezielten Verbesserungen profitieren." if data.K_mean >= 0.6 else
 "Das Dokument zeigt signifikante Diskrepanzen zwischen Behauptungen und Evidenz. Eine Überarbeitung wird empfohlen." if data.K_mean >= 0.4 else
 "Das Dokument erfüllt die ESL-Qualitätsstandards nicht. Eine grundlegende Überarbeitung ist erforderlich."}

---

**Report generiert am:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
"""

    return report


def generiere_audit_report(data: ReportData) -> str:
    """Generiert Full Audit Report (10+ Seiten)."""
    # Für Kürze hier nur die Kernstruktur
    # In Produktion würde das Template vollständig gefüllt

    # Alle Aussagen Detail
    alle_detail = ""
    for i, a in enumerate(data.analysen, 1):
        alle_detail += f"""
### Aussage {i}

> {a.get("aussage", "")}

| Metrik | Wert |
|--------|------|
| K | {a.get("K", 0):.3f} |
| B | {a.get("B", 0):.3f} |
| E | {a.get("E", 0):.3f} |
| Kategorie | {a.get("kategorie", "")} |
| Diskrepanz | {a.get("diskrepanz_typ", "")} |

**Details:**
- Modalverb: {a.get("details", {}).get("modalverb") or "-"}
- Quantor: {a.get("details", {}).get("quantor") or "-"}
- Evidenzstufe: {a.get("details", {}).get("evidenz_stufe") or "-"}

---
"""

    # Verbesserungsvorschläge
    verbesserungen = ""
    for i, a in enumerate(data.kritische_aussagen, 1):
        aussage = a.get("aussage", "")
        K = a.get("K", 0)
        typ = a.get("diskrepanz_typ", "")

        if typ == "überbehauptung":
            vorschlag = "Hedging hinzufügen ('könnte', 'möglicherweise') oder Evidenz stärken"
        elif typ == "unterbehauptung":
            vorschlag = "Behauptung stärken - Evidenz wird nicht ausgeschöpft"
        else:
            vorschlag = "Prüfen und rekalibrieren"

        verbesserungen += f"""
### {i}. {aussage[:50]}...

- **Aktuell:** K = {K:.2f} ({typ})
- **Empfehlung:** {vorschlag}

"""

    report = f"""# ESL Full Audit Report

---

## Deckblatt

| | |
|---|---|
| **Dokument** | {data.dokument_titel} |
| **Autor(en)** | {data.autoren} |
| **Prüfdatum** | {data.datum} |
| **Prüfer** | {data.pruefer} |
| **Report-ID** | ESL-{datetime.now().strftime("%Y%m%d%H%M")} |
| **ESL-Methodik** | v1.0 |

---

## Executive Summary

### Gesamt-Kalibrierung

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║                    K = {data.K_mean:.2f}  {data.kategorie_emoji}                                  ║
║                                                                  ║
║                    {data.kategorie_label:^46}                    ║
║                                                                  ║
║      B (Behauptung): {data.B_mean:.2f}      |      E (Evidenz): {data.E_mean:.2f}             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

### Kernbefunde

| Metrik | Wert | Status |
|--------|------|--------|
| Aussagen gesamt | {data.anzahl} | - |
| K (Durchschnitt) | {data.K_mean:.2f} | {data.kategorie_emoji} |
| K (Minimum) | {data.K_min:.2f} | - |
| K (Maximum) | {data.K_max:.2f} | - |
| Anteil stabil | {data.pct_stabil:.0f}% | {"✅" if data.pct_stabil >= 50 else "⚠️"} |
| Anteil kritisch | {data.pct_kritisch:.0f}% | {"✅" if data.pct_kritisch <= 30 else "⚠️"} |

---

## Detailanalyse aller Aussagen

{alle_detail}

---

## Verbesserungsvorschläge

{verbesserungen}

---

## Methodik

### ESL-Formel

```
K = 1 - |B - E|

B = Behauptungsstärke (Modalverben 50%, Quantoren 35%, Hedging 15%)
E = Evidenzstärke (7-stufige Hierarchie)
K = Kalibrierungsgrad (0.0 - 1.0)
```

### Schwellenwerte

| K-Wert | Kategorie | Aktion |
|--------|-----------|--------|
| ≥ 0.80 | 🟢 Stabil | Keine |
| 0.60-0.79 | 🟡 Teilstabil | Optional |
| 0.40-0.59 | 🟠 Interpretativ | Empfohlen |
| < 0.40 | 🔴 Spekulativ | Erforderlich |

---

## Rohdaten (JSON)

```json
{json.dumps({"analysen": data.analysen, "aggregation": {"K_mean": data.K_mean, "B_mean": data.B_mean, "E_mean": data.E_mean}}, indent=2, ensure_ascii=False)[:2000]}...
```

---

**Report generiert:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Archiv:** berichte/audit/{datetime.now().strftime("%Y%m%d")}/
"""

    return report


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="ESL Report Generator - Generiert ESL-Berichte"
    )
    parser.add_argument(
        "analyse",
        help="Pfad zur ESL-Analyse (JSON)"
    )
    parser.add_argument(
        "--typ", "-t",
        choices=["fast", "standard", "audit"],
        default="standard",
        help="Report-Typ (default: standard)"
    )
    parser.add_argument(
        "--titel",
        default="Unbekanntes Dokument",
        help="Dokumenttitel"
    )
    parser.add_argument(
        "--autoren",
        default="Unbekannt",
        help="Autor(en)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output-Datei (default: stdout)"
    )

    args = parser.parse_args()

    # Analyse laden
    analyse = lade_analyse(Path(args.analyse))

    # Daten aufbereiten
    data = bereite_daten_auf(
        analyse,
        dokument_titel=args.titel,
        autoren=args.autoren,
    )

    # Report generieren
    if args.typ == "fast":
        report = generiere_fast_report(data)
    elif args.typ == "audit":
        report = generiere_audit_report(data)
    else:
        report = generiere_standard_report(data)

    # Ausgabe
    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"Report gespeichert: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()

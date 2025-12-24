# ESL Full Audit Report

---

## Deckblatt

| | |
|---|---|
| **Dokument** | {dokument_titel} |
| **Autor(en)** | {autoren} |
| **Dokumentversion** | {dokument_version} |
| **Prüfdatum** | {datum} |
| **Prüfer** | {pruefer} |
| **Report-ID** | {report_id} |
| **ESL-Methodik** | v1.0 |
| **Klassifikation** | {klassifikation} |

---

## Inhaltsverzeichnis

1. [Executive Summary](#1-executive-summary)
2. [Gesamtergebnis](#2-gesamtergebnis)
3. [Detailanalyse aller Aussagen](#3-detailanalyse-aller-aussagen)
4. [Musteranalyse](#4-musteranalyse)
5. [Vergleichsanalyse](#5-vergleichsanalyse)
6. [Empfehlungen](#6-empfehlungen)
7. [Verbesserungsvorschläge pro Aussage](#7-verbesserungsvorschläge-pro-aussage)
8. [Methodik-Dokumentation](#8-methodik-dokumentation)
9. [Limitationen](#9-limitationen)
10. [Anhänge](#10-anhänge)

---

## 1. Executive Summary

### 1.1 Gesamt-Kalibrierung

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║                    K = {K_mean:.2f}  {kategorie_emoji}                        ║
║                                                                  ║
║              {kategorie_label:^54}              ║
║                                                                  ║
║      B (Behauptung): {B_mean:.2f}      |      E (Evidenz): {E_mean:.2f}       ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

### 1.2 Kernbefunde

| Metrik | Wert | Status |
|--------|------|--------|
| Aussagen gesamt | {anzahl} | - |
| K (Durchschnitt) | {K_mean:.2f} | {kategorie_emoji} |
| K (Minimum) | {K_min:.2f} | - |
| K (Maximum) | {K_max:.2f} | - |
| Anteil stabil | {pct_stabil}% | {status_stabil} |
| Anteil kritisch | {pct_kritisch}% | {status_kritisch} |

### 1.3 Gesamtbewertung

{gesamtbewertung_text}

### 1.4 Handlungsempfehlung

```
{handlungsempfehlung_box}
```

---

## 2. Gesamtergebnis

### 2.1 Verteilung der K-Werte

#### Tabelle

| Kategorie | K-Bereich | Anzahl | Anteil | Kumulativ |
|-----------|-----------|--------|--------|-----------|
| 🟢 Stabil | ≥ 0.80 | {n_stabil} | {pct_stabil}% | {kum_stabil}% |
| 🟡 Teilstabil | 0.60-0.79 | {n_teilstabil} | {pct_teilstabil}% | {kum_teilstabil}% |
| 🟠 Interpretativ | 0.40-0.59 | {n_interpretativ} | {pct_interpretativ}% | {kum_interpretativ}% |
| 🔴 Spekulativ | < 0.40 | {n_spekulativ} | {pct_spekulativ}% | 100% |

#### Visualisierung

```
Stabil        {bar_stabil}  {pct_stabil}%
Teilstabil    {bar_teilstabil}  {pct_teilstabil}%
Interpretativ {bar_interpretativ}  {pct_interpretativ}%
Spekulativ    {bar_spekulativ}  {pct_spekulativ}%
```

### 2.2 B/E-Analyse

#### Behauptungsstärke (B)

| Metrik | Wert |
|--------|------|
| B (Durchschnitt) | {B_mean:.2f} |
| B (Minimum) | {B_min:.2f} |
| B (Maximum) | {B_max:.2f} |
| B (Standardabweichung) | {B_std:.2f} |

**Interpretation:** {b_interpretation_detail}

#### Evidenzstärke (E)

| Metrik | Wert |
|--------|------|
| E (Durchschnitt) | {E_mean:.2f} |
| E (Minimum) | {E_min:.2f} |
| E (Maximum) | {E_max:.2f} |
| E (Standardabweichung) | {E_std:.2f} |

**Interpretation:** {e_interpretation_detail}

#### Evidenzstufen-Verteilung

| Stufe | Anzahl | Anteil |
|-------|--------|--------|
| Meta-Analyse | {n_meta} | {pct_meta}% |
| RCT | {n_rct} | {pct_rct}% |
| Quasi-experimentell | {n_quasi} | {pct_quasi}% |
| Beobachtung | {n_beob} | {pct_beob}% |
| Fallstudie | {n_fall} | {pct_fall}% |
| Experteneinschätzung | {n_experte} | {pct_experte}% |
| Keine Evidenz | {n_keine} | {pct_keine}% |

### 2.3 Diskrepanz-Analyse

| Typ | Definition | Anzahl | Anteil |
|-----|------------|--------|--------|
| Überbehauptung | B - E > 0.1 | {n_ueberbehauptung} | {pct_ueberbehauptung}% |
| Kalibriert | |B - E| ≤ 0.1 | {n_kalibriert} | {pct_kalibriert}% |
| Unterbehauptung | B - E < -0.1 | {n_unterbehauptung} | {pct_unterbehauptung}% |

---

## 3. Detailanalyse aller Aussagen

{alle_aussagen_detail}

---

## 4. Musteranalyse

### 4.1 Sprachliche Muster

#### Modalverben

| Modalverb | Häufigkeit | Durchschn. B |
|-----------|------------|--------------|
{modalverb_tabelle}

#### Quantoren

| Quantor | Häufigkeit | Durchschn. B |
|---------|------------|--------------|
{quantor_tabelle}

#### Hedging

| Marker | Häufigkeit | Adjustment |
|--------|------------|------------|
{hedging_tabelle}

### 4.2 Evidenz-Muster

{evidenz_muster}

### 4.3 Korrelationen

| Korrelation | Wert | Interpretation |
|-------------|------|----------------|
| B vs. E | {korr_be:.2f} | {korr_be_interp} |
| B vs. K | {korr_bk:.2f} | {korr_bk_interp} |
| E vs. K | {korr_ek:.2f} | {korr_ek_interp} |

---

## 5. Vergleichsanalyse

### 5.1 Vergleich mit ESL-Benchmarks

| Benchmark | Wert | Dieses Dokument | Differenz |
|-----------|------|-----------------|-----------|
| K (Ziel) | 0.80 | {K_mean:.2f} | {diff_k:+.2f} |
| Anteil stabil (Ziel) | 70% | {pct_stabil}% | {diff_stabil:+.0f}pp |
| Anteil kritisch (Max) | 20% | {pct_kritisch}% | {diff_kritisch:+.0f}pp |

### 5.2 Vergleich nach Abschnitten

{abschnitt_vergleich}

### 5.3 Historischer Vergleich

{historischer_vergleich}

---

## 6. Empfehlungen

### 6.1 Sofortmassnahmen (Priorität KRITISCH)

{empfehlungen_kritisch}

### 6.2 Hohe Priorität

{empfehlungen_hoch}

### 6.3 Mittlere Priorität

{empfehlungen_mittel}

### 6.4 Niedrige Priorität

{empfehlungen_niedrig}

### 6.5 Zusammenfassung Aufwand

| Priorität | Anzahl Massnahmen | Geschätzter Aufwand |
|-----------|-------------------|---------------------|
| Kritisch | {n_kritisch} | {aufwand_kritisch} |
| Hoch | {n_hoch} | {aufwand_hoch} |
| Mittel | {n_mittel} | {aufwand_mittel} |
| Niedrig | {n_niedrig} | {aufwand_niedrig} |

---

## 7. Verbesserungsvorschläge pro Aussage

{verbesserungen_pro_aussage}

---

## 8. Methodik-Dokumentation

### 8.1 ESL-Formel

```
K = 1 - |B - E|

Wobei:
- B = Behauptungsstärke (0.0 - 1.0)
- E = Evidenzstärke (0.0 - 1.0)
- K = Kalibrierungsgrad (0.0 - 1.0)
```

### 8.2 B-Skala

| Komponente | Gewicht | Beschreibung |
|------------|---------|--------------|
| Modalverben | 50% | muss=0.95, soll=0.85, kann=0.60, könnte=0.45 |
| Quantoren | 35% | alle=0.95, viele=0.65, einige=0.45 |
| Hedging | 15% | tendenziell=-0.25, definitiv=+0.15 |

### 8.3 E-Skala

| Stufe | E-Bereich | Beschreibung |
|-------|-----------|--------------|
| 1 | 0.90-1.00 | Meta-Analyse/Systematic Review |
| 2 | 0.80-0.90 | Randomisierte kontrollierte Studie |
| 3 | 0.65-0.80 | Quasi-experimentelle Studie |
| 4 | 0.50-0.65 | Beobachtungsstudie |
| 5 | 0.35-0.50 | Fallstudie/Qualitativ |
| 6 | 0.20-0.35 | Experteneinschätzung/Theorie |
| 7 | 0.00-0.20 | Keine Evidenz/Unbegründet |

### 8.4 Schwellenwerte

| K-Wert | Kategorie | Bedeutung | Aktion |
|--------|-----------|-----------|--------|
| ≥ 0.80 | Stabil | Behauptung gedeckt | Keine |
| 0.60-0.79 | Teilstabil | Leichte Diskrepanz | Optional überarbeiten |
| 0.40-0.59 | Interpretativ | Signifikante Lücke | Überarbeitung empfohlen |
| < 0.40 | Spekulativ | Starke Diskrepanz | Überarbeitung erforderlich |

### 8.5 Prüfprozess

1. Kernaussagen identifizieren
2. B-Werte extrahieren (automatisch + manuell)
3. E-Werte zuweisen (Evidenzhierarchie)
4. K-Werte berechnen
5. Muster analysieren
6. Empfehlungen ableiten

---

## 9. Limitationen

### 9.1 Methodische Limitationen

{methodische_limitationen}

### 9.2 Dokumentspezifische Limitationen

{dokument_limitationen}

### 9.3 Konfidenz der Analyse

| Aspekt | Konfidenz | Begründung |
|--------|-----------|------------|
| B-Extraktion | {konfidenz_b} | {begruendung_b} |
| E-Zuordnung | {konfidenz_e} | {begruendung_e} |
| K-Berechnung | {konfidenz_k} | {begruendung_k} |
| Empfehlungen | {konfidenz_emp} | {begruendung_emp} |

---

## 10. Anhänge

### 10.1 Rohdaten

{rohdaten_tabelle}

### 10.2 JSON-Export

```json
{json_export}
```

### 10.3 Änderungshistorie

| Version | Datum | Änderung | Autor |
|---------|-------|----------|-------|
{aenderungshistorie}

### 10.4 Glossar

| Begriff | Definition |
|---------|------------|
| B | Behauptungsstärke einer Aussage |
| E | Evidenzstärke, die eine Aussage stützt |
| K | Kalibrierungsgrad (1 - |B-E|) |
| ESL | Empirical System of Language |
| Überbehauptung | B deutlich größer als E |
| Unterbehauptung | E deutlich größer als B |

---

**Report generiert:** {generiert_am}
**Report-ID:** {report_id}
**Nächste Prüfung:** {naechste_pruefung}
**Archiviert:** {archiv_pfad}

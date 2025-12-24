# ESL Report: Standard

---

## Dokumentinformationen

| Feld | Wert |
|------|------|
| **Dokument** | {dokument_titel} |
| **Autor(en)** | {autoren} |
| **Prüfdatum** | {datum} |
| **Prüfer** | {pruefer} |
| **Report-Version** | {version} |
| **ESL-Methodik** | v1.0 |

---

## 1. Executive Summary

### Gesamt-Kalibrierung

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│              K = {K_mean:.2f}  {kategorie_emoji}                          │
│                                                              │
│         {kategorie_label:^50}         │
│                                                              │
│    B (Behauptung): {B_mean:.2f}    |    E (Evidenz): {E_mean:.2f}         │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Kernbefunde

- **{anzahl} Aussagen** analysiert
- **{pct_kritisch}%** der Aussagen sind kritisch (K < 0.6)
- **Hauptproblem:** {hauptproblem}
- **Empfehlung:** {empfehlung_kurz}

---

## 2. Detaillierte Ergebnisse

### 2.1 Verteilung der K-Werte

| Kategorie | K-Bereich | Anzahl | Anteil | Bedeutung |
|-----------|-----------|--------|--------|-----------|
| 🟢 Stabil | ≥ 0.80 | {n_stabil} | {pct_stabil}% | Behauptung durch Evidenz gedeckt |
| 🟡 Teilstabil | 0.60-0.79 | {n_teilstabil} | {pct_teilstabil}% | Leichte Diskrepanz |
| 🟠 Interpretativ | 0.40-0.59 | {n_interpretativ} | {pct_interpretativ}% | Signifikante Lücke |
| 🔴 Spekulativ | < 0.40 | {n_spekulativ} | {pct_spekulativ}% | Behauptung übersteigt Evidenz |

### 2.2 B/E-Analyse

| Metrik | Wert | Interpretation |
|--------|------|----------------|
| B (Durchschnitt) | {B_mean:.2f} | {b_interpretation} |
| E (Durchschnitt) | {E_mean:.2f} | {e_interpretation} |
| B - E (Diskrepanz) | {diskrepanz:+.2f} | {diskrepanz_interpretation} |

### 2.3 Diskrepanz-Typen

| Typ | Anzahl | Beschreibung |
|-----|--------|--------------|
| Überbehauptung (B > E) | {n_ueberbehauptung} | Sprache stärker als Evidenz |
| Kalibriert (B ≈ E) | {n_kalibriert} | Gute Übereinstimmung |
| Unterbehauptung (B < E) | {n_unterbehauptung} | Evidenz nicht ausgeschöpft |

---

## 3. Problemanalyse

### 3.1 Kritische Aussagen (K < 0.6)

{kritische_aussagen_tabelle}

### 3.2 Häufige Muster

{muster_analyse}

---

## 4. Stärken

### 4.1 Stabile Aussagen (K ≥ 0.8)

{stabile_aussagen_tabelle}

### 4.2 Positive Muster

{positive_muster}

---

## 5. Empfehlungen

### 5.1 Sofortmassnahmen (Priorität HOCH)

{empfehlungen_hoch}

### 5.2 Mittelfristige Massnahmen

{empfehlungen_mittel}

### 5.3 Optionale Verbesserungen

{empfehlungen_optional}

---

## 6. Fazit

{fazit}

---

## Anhang: Methodik

### ESL-Formel

```
K = 1 - |B - E|

B = Behauptungsstärke (Modalverben, Quantoren, Hedging)
E = Evidenzstärke (7-stufige Hierarchie)
K = Kalibrierungsgrad (0.0 - 1.0)
```

### Schwellenwerte

| K-Wert | Kategorie | Bedeutung |
|--------|-----------|-----------|
| ≥ 0.80 | Stabil | Publikationsreif |
| 0.60-0.79 | Teilstabil | Akzeptabel mit Hinweis |
| 0.40-0.59 | Interpretativ | Überarbeitung empfohlen |
| < 0.40 | Spekulativ | Überarbeitung erforderlich |

---

**Report generiert am:** {generiert_am}
**Nächste Prüfung empfohlen:** {naechste_pruefung}

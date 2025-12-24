# ESL Report: Fast & Clear (1-Pager)

---

## {dokument_titel}
**Datum:** {datum} | **Prüfer:** {pruefer} | **Version:** {version}

---

## Gesamt-Kalibrierung

```
┌────────────────────────────────────────────┐
│                                            │
│         K = {K_mean:.2f}  {kategorie_emoji}              │
│                                            │
│    {kategorie_label:^38}    │
│                                            │
└────────────────────────────────────────────┘
```

| Metrik | Wert | Bewertung |
|--------|------|-----------|
| **K (Durchschnitt)** | {K_mean:.2f} | {kategorie_label} |
| **B (Behauptung)** | {B_mean:.2f} | {b_bewertung} |
| **E (Evidenz)** | {E_mean:.2f} | {e_bewertung} |
| **Aussagen gesamt** | {anzahl} | - |

---

## Verteilung

| Status | Anzahl | Anteil |
|--------|--------|--------|
| 🟢 Stabil (K ≥ 0.8) | {n_stabil} | {pct_stabil}% |
| 🟡 Teilstabil (0.6-0.8) | {n_teilstabil} | {pct_teilstabil}% |
| 🟠 Interpretativ (0.4-0.6) | {n_interpretativ} | {pct_interpretativ}% |
| 🔴 Spekulativ (< 0.4) | {n_spekulativ} | {pct_spekulativ}% |

---

## Top 3 Probleme

1. **{problem_1_aussage}**
   K={problem_1_K:.2f} | {problem_1_typ}

2. **{problem_2_aussage}**
   K={problem_2_K:.2f} | {problem_2_typ}

3. **{problem_3_aussage}**
   K={problem_3_K:.2f} | {problem_3_typ}

---

## Empfehlung

{empfehlung_box}

---

**Status:** {status} | **Nächste Prüfung:** {naechste_pruefung}

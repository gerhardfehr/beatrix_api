# BCM λ-Elicitation: Methodik zur Lambda-Messung

> **Systematische Erhebung des Kooperations-Regulators λ**

© FehrAdvice & Partners AG, Zürich 2025

---

## Übersicht

Lambda (λ) ist der zentrale Parameter für die Interventions-Strategie. Diese Ressource beschreibt die wissenschaftlich fundierte Methodik zur λ-Erhebung.

---

## 1. λ-Konzept

### Definition

```
λ = Grad der kollektiven vs. individuellen Orientierung

λ → 0:  Reine Eigennutz-Maximierung (Homo oeconomicus)
λ → 1:  Reine Kollektiv-/Identitätsorientierung
```

### Zwei-Ebenen-Modell

```
λ_effektiv = f(λ_Person, Δλ_Kontext)

┌─────────────────────────────────────────────┐
│  EBENE 1: λ_Person (Trait)                  │
│  ─────────────────────────────              │
│  • Stabile Grundorientierung                │
│  • Geprägt durch: Persönlichkeit, Werte,    │
│    Kultur, Erfahrungen                      │
│  • Messbar: Einmalig, valide über Monate    │
├─────────────────────────────────────────────┤
│  EBENE 2: Δλ_Kontext (State)                │
│  ─────────────────────────────              │
│  • Situative Modulation (±0.2 bis ±0.3)     │
│  • Faktoren: Öffentlichkeit, Gruppengröße,  │
│    Anonymität, emotionaler Zustand          │
│  • Messbar: Situativ, kann schwanken        │
├─────────────────────────────────────────────┤
│  ERGEBNIS: λ_eff = λ_Person + Δλ_Kontext    │
│  ─────────────────────────────              │
│  • Constraint: λ_eff ∈ [0, 1]               │
│  • Dies ist der handlungsrelevante Wert     │
└─────────────────────────────────────────────┘
```

---

## 2. Verhaltenstypen (Fischbacher/Gächter/Fehr)

### Empirische Typologie

| Typ | Anteil | λ-Charakteristik | Beitrags-Funktion |
|-----|--------|------------------|-------------------|
| **ALTRUIST** | ~10% | λ hoch, konstant | Immer hoher Beitrag |
| **CONDITIONAL COOPERATOR** | ~50% | λ = f(Belief) | Steigt mit Beitrag anderer |
| **SELF-INTERESTED** | ~30% | λ ≈ 0 | Konstant niedrig/null |
| **OTHER** | ~10% | Variabel | Unklares Muster |

### Conditional Cooperators: Subtypen

```
┌─────────────────────────────────────────────────────┐
│  CONDITIONAL COOPERATOR (50% der Population)        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Subtyp A: STRATEGISCH                              │
│  • Motivation: Eigennutz-Maximierung                │
│  • Logik: "Wenn andere geben, lohnt sich meins"     │
│  • Beitrag: Leicht unter Durchschnitt anderer       │
│  • Formel: C_i = max(0, E[C_andere] - ε)            │
│                                                     │
│  Subtyp B: ALTRUISTISCH/REZIPROK                    │
│  • Motivation: Fairness, Reziprozität               │
│  • Logik: "Ich matche, was andere geben"            │
│  • Beitrag: ≈ Durchschnitt anderer                  │
│  • Formel: C_i ≈ E[C_andere]                        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Beitrags-Kurven

```
Eigener
Beitrag
    │
100%│                         _____ ALTRUIST
    │                      __/
    │                   __/
    │                __/    CONDITIONAL (altruistisch)
    │             __/
    │          __/
    │        _/____--------- CONDITIONAL (strategisch)
    │      _//
    │    _//
    │  _//
  0%│_//________________________ SELF-INTERESTED
    └───────────────────────────────────────────►
    0%                                        100%
                 Erwarteter Beitrag anderer
```

---

## 3. Labor-Methoden

### 3.1 Public Goods Game (Basis-Setup)

```yaml
setup:
  spieler_pro_gruppe: 4
  endowment: 20 CHF
  multiplikator: 1.6  # MPCR = 0.4

entscheidung:
  frage: "Wie viel von 20 CHF in den gemeinsamen Topf?"

auszahlung:
  formel: "π_i = (20 - C_i) + 0.4 × Σ C_j"

dilemma:
  individuell_optimal: 0 CHF (Free Riding)
  kollektiv_optimal: 20 CHF (alle zahlen alles)
```

### 3.2 Strategy Method (Goldstandard)

```yaml
methode: "Fischbacher, Gächter & Fehr (2001)"

ablauf:
  phase_1_unconditional:
    frage: "Wie viel zahlst du ein?"
    output: "C_u"

  phase_2_conditional:
    frage: "Wie viel zahlst du ein, WENN die anderen
            im Durchschnitt X einzahlen?"
    tabelle:
      - wenn_andere: 0  → mein_beitrag: ___
      - wenn_andere: 2  → mein_beitrag: ___
      - wenn_andere: 4  → mein_beitrag: ___
      - wenn_andere: 6  → mein_beitrag: ___
      - wenn_andere: 8  → mein_beitrag: ___
      - wenn_andere: 10 → mein_beitrag: ___
      - wenn_andere: 12 → mein_beitrag: ___
      - wenn_andere: 14 → mein_beitrag: ___
      - wenn_andere: 16 → mein_beitrag: ___
      - wenn_andere: 18 → mein_beitrag: ___
      - wenn_andere: 20 → mein_beitrag: ___
    output: "Contribution Schedule C(x)"

lambda_berechnung:
  formel: "λ = Steigung der Beitragsfunktion"
  methode: "Lineare Regression: C_i = α + λ × C_andere"

klassifikation:
  altruist: "Steigung ≈ 0 UND Niveau > 15"
  conditional_cooperator: "Steigung > 0 UND monoton"
  self_interested: "Niveau < 3 durchgehend"
```

### 3.3 Belief Elicitation

```yaml
methode: "Belief-basierte λ-Messung"

ablauf:
  phase_1:
    frage: "Wie viel zahlst du ein?"
    output: "C_i"

  phase_2:
    frage: "Was glaubst du: Wie viel zahlen die anderen
            im Durchschnitt ein?"
    output: "B_i (Belief)"
    incentive: "Bonus für korrekte Schätzung (±2)"

lambda_berechnung:
  formel: "λ = C_i / B_i"
  constraints: "Nur wenn B_i > 0"

interpretation:
  - "λ = 1.0: Perfekter Matcher"
  - "λ < 1.0: Strategisch unter anderen"
  - "λ > 1.0: Über-Kooperator"
  - "λ = 0.0: Free Rider"
```

### 3.4 Repeated Game (Dynamisch)

```yaml
methode: "Dynamische λ-Schätzung über Runden"

ablauf:
  runden: 10
  pro_runde:
    - entscheidung: "Beitrag C_i(t)"
    - feedback: "Durchschnitt andere C_andere(t)"
    - auszahlung: "π_i(t)"

lambda_berechnung:
  regression: "C_i(t) = α_i + λ_i × C_andere(t-1) + ε"
  output: "λ_i = Koeffizient für lagged Beitrag andere"

vorteile:
  - "Realistischeres Verhalten (mit Feedback)"
  - "Lernen und Anpassung sichtbar"

nachteile:
  - "End-Game-Effekte möglich"
  - "Strategisches Verhalten in späten Runden"
```

---

## 4. Komplett-Protokoll (Labor)

```yaml
experiment:
  name: "BCM λ-Elicitation"
  dauer: 60 Minuten
  teilnehmer: 40 (10 Gruppen à 4)
  vergütung: "Show-up Fee + Spielgewinn"

ablauf:

  phase_1_instruktion:
    dauer: 10 min
    inhalt:
      - Begrüßung, Anonymität erklären
      - Spielregeln erklären (mit Beispielen)
      - Verständnisfragen (Quiz)

  phase_2_praxis:
    dauer: 5 min
    inhalt:
      - 1 Proberunde ohne Auszahlung
      - Fragen klären

  phase_3_unconditional:
    dauer: 3 min
    messung: "C_u (unconditional contribution)"
    instruktion: "Wie viel von 20 CHF möchten Sie einzahlen?"

  phase_4_conditional:
    dauer: 10 min
    messung: "Contribution Schedule für 11 Levels (0, 2, 4, ..., 20)"
    instruktion: "Wie viel zahlen Sie ein, wenn die anderen
                  im Durchschnitt X einzahlen?"

  phase_5_belief:
    dauer: 3 min
    messung: "Belief über Ø Beitrag andere"
    instruktion: "Was glauben Sie: Wie viel zahlen die anderen
                  im Durchschnitt ein?"
    incentive: "1 CHF Bonus bei ±2 Genauigkeit"

  phase_6_repeated:
    dauer: 15 min
    messung: "5 Runden mit Feedback"
    ablauf_pro_runde:
      - Beitragsentscheidung (60 Sek.)
      - Feedback: Ø andere, eigene Auszahlung

  phase_7_survey:
    dauer: 5 min
    inhalt:
      - Demografie (Alter, Geschlecht, Bildung)
      - Manipulation Check
      - Verständnisfragen

  phase_8_auszahlung:
    dauer: 9 min
    ablauf:
      - Berechnung Gesamtgewinn
      - Individuelle Auszahlung (Bar oder Überweisung)

output_pro_person:
  - id: "Anonyme ID"
  - lambda_strategy: "Steigung aus Phase 4"
  - lambda_belief: "C_u / Belief aus Phase 5"
  - lambda_dynamic: "Regression aus Phase 6"
  - lambda_aggregiert: "Gewichteter Durchschnitt"
  - typ: "Klassifikation (Altruist/Conditional/Self-Int.)"
  - belief_accuracy: "Abweichung Belief von Realität"
```

---

## 5. Feld-Approximation (ohne Labor)

### 5.1 Survey-basierte λ-Schätzung

```yaml
fragebogen:
  name: "BCM λ-Quick-Assessment"
  items: 10
  dauer: 5 min

items_eigenes_lambda:
  q1:
    text: "Ich bin bereit, auf eigene Vorteile zu verzichten,
           wenn es der Gruppe hilft"
    skala: 1-5 (stimme nicht zu → stimme zu)

  q2:
    text: "Bei Entscheidungen denke ich zuerst an mich selbst"
    skala: 1-5 (invertiert)

  q3:
    text: "Das Wohl meiner Gemeinschaft ist mir wichtiger
           als mein persönlicher Vorteil"
    skala: 1-5

  q4:
    text: "Ich würde mehr für die Umwelt tun, wenn andere es auch tun"
    skala: 1-5 (Conditional-Indikator)

  q5:
    text: "Fairness ist mir wichtiger als Gewinn"
    skala: 1-5

items_belief_andere:
  q6:
    text: "Die meisten Menschen denken nur an sich selbst"
    skala: 1-5 (invertiert für Belief)

  q7:
    text: "Wenn ich kooperiere, werden andere das ausnutzen"
    skala: 1-5 (invertiert)

  q8:
    text: "Ich glaube, dass die meisten Menschen fair sind"
    skala: 1-5

  q9:
    text: "In meinem Umfeld halten sich die Leute an gemeinsame Regeln"
    skala: 1-5

  q10:
    text: "Andere würden auch auf Vorteile verzichten für die Gruppe"
    skala: 1-5

berechnung:
  lambda_eigen: "(Q1 + (6-Q2) + Q3 + Q5) / 20"
  lambda_belief: "(Q6_inv + Q7_inv + Q8 + Q9 + Q10) / 25"
  conditional_score: "Q4 / 5"

  typologie:
    altruist: "lambda_eigen > 0.7 AND conditional_score < 0.5"
    conditional: "conditional_score > 0.6"
    self_interested: "lambda_eigen < 0.3"
```

### 5.2 Verhaltensbasierte λ-Schätzung

```yaml
methode: "Revealed Preferences aus Vergangenheit"

fragen:
  - "Haben Sie in den letzten 12 Monaten gespendet?"
  - "Engagieren Sie sich ehrenamtlich?"
  - "Haben Sie schon mal einen Fehler zugegeben,
     obwohl Sie damit durchgekommen wären?"
  - "Trennen Sie Ihren Müll, auch wenn es niemand kontrolliert?"
  - "Würden Sie 100 CHF zurückgeben, die Sie
     versehentlich zu viel erhalten haben?"

scoring:
  jedes_ja: "+0.15 auf λ_base"
  maximum: "0.75"
  minimum: "0.00"
```

### 5.3 Kontextspezifische Messung

```yaml
beispiel_smartphone:

  frage_1:
    text: "Würdest du weniger am Phone sein,
           wenn deine Freunde auch weniger nutzen?"
    antworten:
      ja_definitiv: "Conditional Cooperator"
      vielleicht: "Partial Conditional"
      nein_unabhängig: "Altruist oder Self-Int."

  frage_2:
    text: "Wie viel Prozent deiner Klasse würden
           bei einer 'Phone-Free Lunch' Challenge mitmachen?"
    antwort: "Belief über andere"

  frage_3:
    text: "Würdest du mitmachen, auch wenn nur
           30% deiner Klasse mitmachen?"
    antworten:
      ja: "Hoher λ_eigen"
      nein: "Conditional, Belief-abhängig"

  klassifikation:
    altruist: "F1=nein_unabhängig AND F3=ja AND niedriger Konsum"
    conditional: "F1=ja_definitiv OR F1=vielleicht"
    self_interested: "F1=nein_unabhängig AND F3=nein"
```

---

## 6. λ-Aggregation

### Multi-Methoden-Ansatz

```yaml
wenn_labor_verfuegbar:
  lambda_final: |
    λ = 0.50 × λ_strategy
      + 0.30 × λ_belief
      + 0.20 × λ_dynamic

wenn_nur_survey:
  lambda_final: |
    λ = 0.60 × λ_survey
      + 0.40 × λ_revealed

kontext_modulation:
  lambda_effektiv: |
    λ_eff = λ_person + Δλ(Kontext)

    Δλ_faktoren:
      - oeffentlich_vs_privat: "+0.15 wenn beobachtet"
      - gruppengroesse: "+0.05 pro 10 Personen (max +0.2)"
      - anonymitaet: "-0.10 wenn anonym"
      - emotionaler_zustand: "±0.10"
```

---

## 7. Interventions-Mapping

### Nach Typ und λ

```
┌──────────────────┬────────────────────────────────────┐
│ Typ              │ Interventions-Strategie            │
├──────────────────┼────────────────────────────────────┤
│ ALTRUIST         │ • Stabilisieren, nicht demotivieren│
│ (λ hoch,         │ • Keine INCENTIVE (Crowding-out!)  │
│  konstant)       │ • IDENTITY verstärken              │
│                  │ • Als Role Model nutzen            │
├──────────────────┼────────────────────────────────────┤
│ CONDITIONAL      │ • SOCIAL PROOF (Belief korrigieren)│
│ COOPERATOR       │ • "X% machen bereits mit"          │
│ (λ = f(Belief))  │ • Transparenz über Beiträge andere │
│                  │ • Commitment Devices               │
├──────────────────┼────────────────────────────────────┤
│ SELF-INTERESTED  │ • INCENTIVE (individueller Nutzen) │
│ (λ ≈ 0)          │ • REGULATE (wenn nötig)            │
│                  │ • Framing auf Eigennutz            │
│                  │ • "Was bringt es DIR?"             │
└──────────────────┴────────────────────────────────────┘
```

### Belief-Korrektur (Kritisch für Conditional Cooperators)

```
Problem: Pluralistic Ignorance
─────────────────────────────
Realität:     70% würden kooperieren
Belief:       "Nur 30% kooperieren"
Verhalten:    → Reduzierter eigener Beitrag

Intervention: Belief korrigieren
─────────────────────────────
SOCIAL PROOF: "Tatsächlich sind 70% bereit mitzumachen"
              → Belief steigt
              → Eigener Beitrag steigt

Warnung: Nur wahre Zahlen verwenden!
         Falsche Claims zerstören Vertrauen
```

---

## 8. Qualitätssicherung

### Validitäts-Checks

```yaml
interne_validitaet:
  - test_retest: "Korrelation > 0.7 bei Wiederholung"
  - consistency: "λ_strategy ≈ λ_belief (r > 0.5)"

externe_validitaet:
  - verhaltens_korrelation: "λ korreliert mit realem Kooperationsverhalten"
  - prädiktive_power: "λ sagt Intervention-Response voraus"

manipulation_check:
  - verstaendnis: "Quiz-Score > 80%"
  - aufmerksamkeit: "Attention-Check bestanden"
  - ernsthaftigkeit: "Keine Random-Antworten (Varianz-Check)"
```

### Typische Probleme

| Problem | Erkennung | Lösung |
|---------|-----------|--------|
| Social Desirability | λ_survey >> λ_labor | Labor-Daten priorisieren |
| Hypothetical Bias | Survey ≠ Realverhalten | Incentivized Measures |
| Context Mismatch | Labor ≠ Feld | Kontextspezifische Messung |
| End-Game Effects | λ sinkt in letzten Runden | Letzte Runden ausschließen |

---

## 9. BCM-Integration

### Workflow-Einbindung

```
PHASE 1: DIAGNOSE
    │
    ├── Zielverhalten definieren
    ├── Zielgruppe identifizieren
    │
    └── λ ERHEBEN ←────────────────────┐
            │                          │
            ├── Labor (wenn möglich)   │
            ├── Survey (Quick)         │
            └── Revealed Preferences   │
                                       │
PHASE 2: ANALYSE                       │
    │                                  │
    ├── INU, KNU, IDN bewerten         │
    │                                  │
    └── λ-SEGMENTIERUNG                │
            │                          │
            ├── Altruist (~10%)        │
            ├── Conditional (~50%)     │
            └── Self-Int. (~30%)       │
                                       │
PHASE 4: DESIGN                        │
    │                                  │
    └── Intervention NACH λ-Typ ───────┘
```

### Axiom-Referenz

```
Relevante META-Axiome:
- MA-ONT-14: λ: Kooperations-Regulator
- MA-ONT-15: λ ∈ [0, 1]: Hybrid-Kontinuum
- MA-DYN-23: λ-Dynamik

Relevante WAX-Axiome:
- WAX-LAM-01 bis WAX-LAM-07: λ-Hybrid-Logik
```

---

## 10. Referenzen

### Primärliteratur

- Fischbacher, U., Gächter, S., & Fehr, E. (2001). Are people conditionally cooperative? Evidence from a public goods experiment. *Economics Letters*, 71(3), 397-404.
- Fehr, E., & Schmidt, K. M. (1999). A theory of fairness, competition, and cooperation. *Quarterly Journal of Economics*, 114(3), 817-868.
- Fehr, E., & Gächter, S. (2002). Altruistic punishment in humans. *Nature*, 415(6868), 137-140.

### Methodenliteratur

- Fischbacher, U. (2007). z-Tree: Zurich toolbox for ready-made economic experiments. *Experimental Economics*, 10(2), 171-178.
- Herrmann, B., Thöni, C., & Gächter, S. (2008). Antisocial punishment across societies. *Science*, 319(5868), 1362-1367.

---

*BEATRIX BCM 2.0 - λ-Elicitation v1.0*

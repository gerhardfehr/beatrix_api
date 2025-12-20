# BEATRIX BCM 2.0 - Claude Skill

> **Axiomatisches Framework für Verhaltensmodellierung und Interventions-Design**

© FehrAdvice & Partners AG, Zürich 2025

---

## Kurzübersicht

**BEATRIX** (Behavioral Economics Architecture for Transformation, Research, Intervention & eXperience) ist ein axiomatisches Framework zur Modellierung, Vorhersage und Steuerung menschlichen Verhaltens.

```
Φ_BCM = Φ_META ⊗ Ψ(Φ_INU ⊕ Φ_KNU ⊕ Φ_IDN) · Γ · τ · κ · λ
```

---

## Meta-Meta-Formel

### Minimale Form (3 Elemente)
```
Φ = Ψ(U) · Γ

Ψ = WIE (Kohärenz-Operator)
U = WAS (Nutzen-Variablen)
Γ = OB  (Governance-Constraints)
```

### Maximale Form (14 Dimensionen)

| # | Symbol | Dimension | Frage |
|---|--------|-----------|-------|
| 1 | Ω_ONT | Ontologie | Was existiert? |
| 2 | Ω_EPI | Epistemologie | Was wissen wir? |
| 3 | Ω_AXI | Axiologie | Was hat Wert? |
| 4 | U | Nutzen-Vektor | Was ist der Nutzen? |
| 5 | ω | Gewichtung | Wie wichtig? |
| 6 | ρ | Kontext | In welcher Situation? |
| 7 | σ | Subjekt | Für wen? |
| 8 | Ψ | Kohärenz | Wie kombinieren? |
| 9 | Γ | Governance | Was ist erlaubt? |
| 10 | τ | Zeit | Wann? |
| 11 | ∂ | Differenzial | Wie schnell? |
| 12 | μ | Meta-Evolution | Wie evolvieren Regeln? |
| 13 | κ | Komplementarität | Was bedingt sich gegenseitig? |
| 14 | λ | Spannungs-Regulator | Lokal vs. Global? |

---

## Modul-Architektur

```
                      ┌──────────────┐
                      │  Φ_META      │  GOVERNANCE
                      │   (7232)     │  100 Axiome
                      │  Grundformel │
                      └──────┬───────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
       ┌──────────┐   ┌──────────┐   ┌──────────┐
       │  Φ_INU   │   │  Φ_KNU   │   │  Φ_IDN   │  NUTZEN
       │  (7234)  │◄─►│  (7235)  │◄─►│  (7236)  │
       │ 59 Axiom │   │ 46 Axiom │   │ 70 Axiom │
       └────┬─────┘   └────┬─────┘   └────┬─────┘
            │              │              │
            └──────────────┼──────────────┘
                           ▼
                    ┌──────────────┐
                    │    AWX       │  AWARENESS
                    │   (7240)     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │    WAX       │  WILLINGNESS
                    │   (7243)     │  λ-Hybrid-Logik
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │    WTX       │  PROBABILITY
                    │   (7259)     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  BEHAVIOR    │  OUTPUT
                    │   CHANGE     │
                    └──────────────┘
```

---

## Module im Detail

### 7232 META - Meta-Axiome
- **100 Axiome** für Ontologie, Epistemologie, Governance, Dynamik
- **Funktion**: Grundformel-Generator und Validator
- **Formel**: `Φ_META = Ω_ONT · Ω_EPI · Ω_GOV · Ω_DYN`
- **Rolle**: Definiert abstrakte Variablen, Submodule liefern konkrete Werte

### 7234 INU - Individueller Nutzen
- **59 Axiome** für persönlichen Nutzen
- **FEPSDE-Dimensionen**: Financial, Emotional, Physical, Social, Digital, Ecological
- **Formel**: `Φ_INU = V_base + Σ[ω_d(G_d - λ_d·P_d)] + C + CB - CD`
- **Rolle**: Verfeinert U_ind in META-Grundformel

### 7235 KNU - Kollektiver Nutzen
- **46 Axiome** für Gruppennutzen
- **Themen**: Kooperation, Bestrafung (A31-A42), Destruktion (A43-A46, Dark Triad)
- **Formel**: `Φ_KNU = U_kol · ρ_K · Ψ_IDN · Ψ_INST · Ψ_DEST`
- **Rolle**: Verfeinert U_kol in META-Grundformel

### 7236 IDN - Identitätsnutzen
- **70 Axiome** für Identität
- **Themen**: Multiplizität, Komplementarität, Konflikte, Identity Journeys
- **Formel**: `Φ_IDN = Σ π_j · A_j · U_IDN^j`
- **Rolle**: Verfeinert U_idn in META-Grundformel

### 7243 WAX - Willingness
- **λ-Hybrid-Logik**: Balance zwischen additiv und komplementär
- **Formel**: `WAX = λ · WAX^compl + (1-λ) · WAX^add`
- **Dynamik**: `dλ/dt = α·AWX - β·UNS - γ·KOM`

---

## Schlüsselkonzepte

### Ψ - Kohärenz-Operator
Nicht-additive Kombination von Nutzen. Einfache Addition verletzt Arrow's Impossibility Theorem.

### κ - Komplementarität
Gegensätze, die sich gegenseitig bedingen:
- Individuum ↔ Kollektiv
- Nutzen ↔ Kosten
- Kurzfristig ↔ Langfristig
- Stabilität ↔ Wandel
- Kooperation ↔ Destruktion

### λ - Spannungs-Regulator
Balance zwischen lokaler Optimierung und Komplementarität:
```
U_eff = (1-λ) · U_lokal + λ · κ(U_lokal, U_komplement)

λ = 0.0  →  Reiner Egoist
λ = 0.5  →  Balance
λ = 1.0  →  Reiner Altruist
```

**Wichtig**: λ ist kontextabhängig, nicht statisch!

### MA_0.ES - Exponentielle Sättigung
Meta-Axiom (ohne Zahlenwert):
> "In Lern- und Entscheidungssystemen mit proportionaler Unsicherheitsreduktion konvergiert adaptive Effizienz gegen einen Zustand mit verbleibendem Unsicherheitsrest."

**Korollar ES-1** (mit Zahlenwert):
> "Der Übergangspunkt liegt bei ~63% Abbau (Rest ≈ 1/e ≈ 0.368)"

---

## Methodik

### Intra-Modul (innerhalb eines Moduls)
```
EBENE 1: Fundament-Axiome   → Existenzbedingungen
EBENE 2: Struktur-Axiome    → FEPSDE, Gewichtungen
EBENE 3: Operations-Axiome  → Berechnungslogik
EBENE 4: Dynamik-Axiome     → Zeit, Feedback
```

### Inter-Modul (zwischen Modulen)
```
META ──⊢── validiert ──→ INU, KNU, IDN
INU  ──↔── bidirektional ──↔── KNU, IDN
ALLE ──→── Input-Flow ──→ AWX → WAX → WTX
```

---

## Anwendungsfälle

| Use Case | Beschreibung |
|----------|--------------|
| **Verhaltensanalyse** | Analyse von Entscheidungen über INU/KNU/IDN |
| **Interventions-Design** | Design von Nudges und Verhaltensinterventionen |
| **Segmentierung** | Gruppierung nach Verhaltenstypen und λ-Werten |
| **Policy-Design** | Evidenzbasierte Politikgestaltung |
| **Journey-Optimierung** | Customer/Citizen Journey Analyse |
| **Change Management** | Organisationale Veränderungsprozesse |

---

## Constraints & Warnungen

### Epistemologisch
- **Nicht-normativ**: beschreibt, schreibt nicht vor
- **Kontextabhängig**: keine universellen Optima
- **Falsifizierbar**: Korollare sind empirisch testbar

### Methodologisch
- **Kohärenz-basiert**: keine einfache Addition von Nutzen
- **Meta-Axiome ohne Zahlenwerte** (Zahlen nur in Korollaren)
- **Design-Axiome sind Empfehlungen**, nicht Zwang

### Warnungen
- 1/e (0.37) ist **KEIN universelles Optimum**
- λ-Werte sind **kontextabhängig**
- Arrow's Theorem **verbietet einfache Aggregation**

---

## Wann BEATRIX nutzen?

**Ja:**
- Verhaltensänderung soll modelliert werden
- Interventionen müssen designt werden
- Nutzen-Trade-offs analysiert werden
- Identität und Kollektiv berücksichtigt werden müssen

**Nein:**
- Rein technische Optimierung ohne Verhalten
- Normative Vorgaben ohne empirische Basis
- Einfache lineare Modelle ausreichend

---

## API-Struktur

```
beatrix_api/
├── meta/meta.json      # 100 Meta-Axiome
├── inu/inu.json        # 59 INU-Axiome
├── knu/knu.json        # 46 KNU-Axiome
├── idn/idn.json        # 70 IDN-Axiome
├── awx/awx.json        # AWX-Axiome
├── wax/wax.json        # WAX mit λ-Logik
├── wtx/wtx.json        # 10 WTX-Axiome
├── context/context.json
├── seg/seg.json
└── skill/
    ├── beatrix-bcm.yaml
    └── BEATRIX_SKILL.md
```

---

## Referenzen

### Theoretische Grundlagen
- Kahneman & Tversky (1979): Prospect Theory
- Thaler & Sunstein (2008): Nudge
- Arrow (1951): Impossibility Theorem
- Simon (1955): Bounded Rationality
- Fehr & Schmidt (1999): Fairness

### BCM-Spezifisch
- FehrAdvice & Partners AG (2025): BCM 2.0 Handbook
- FehrAdvice & Partners AG (2025): BEATRIX Architecture
- FehrAdvice & Partners AG (2025): Meta-Axioms Reference

---

*BEATRIX BCM 2.0 - Verhaltensökonomisches Meta-Framework*

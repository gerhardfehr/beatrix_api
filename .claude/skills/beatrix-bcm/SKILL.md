---
name: beatrix-bcm
description: Axiomatisches Framework für Verhaltensmodellierung (BCM 2.0). Nutze diesen Skill wenn Verhaltensänderung modelliert, Interventionen designt, oder Nutzen-Trade-offs (individuell/kollektiv/Identität) analysiert werden sollen.
---

# BEATRIX BCM 2.0

Du bist ein Experte für das Behavioral Change Model (BCM) 2.0 von FehrAdvice & Partners AG. Du nutzt das axiomatische BEATRIX-Framework zur Analyse und zum Design von Verhaltensinterventionen.

## Meta-Meta-Formel

Die zentrale Grundformel von BCM:

```
Φ_BCM = Φ_META ⊗ Ψ(Φ_INU ⊕ Φ_KNU ⊕ Φ_IDN) · Γ · τ · κ · λ
```

### Minimale Form
```
Φ = Ψ(U) · Γ

Ψ = WIE (Kohärenz-Operator)
U = WAS (Nutzen-Variablen)
Γ = OB  (Governance-Constraints)
```

### Vollständige Dimensionen

| Symbol | Dimension | Frage |
|--------|-----------|-------|
| Ω_ONT | Ontologie | Was existiert? |
| Ω_EPI | Epistemologie | Was wissen wir? |
| Ω_AXI | Axiologie | Was hat Wert? |
| U | Nutzen-Vektor | Was ist der Nutzen? |
| ω | Gewichtung | Wie wichtig? |
| ρ | Kontext | In welcher Situation? |
| σ | Subjekt | Für wen? |
| Ψ | Kohärenz | Wie kombinieren? |
| Γ | Governance | Was ist erlaubt? |
| τ | Zeit | Wann? |
| ∂ | Differenzial | Wie schnell? |
| μ | Meta-Evolution | Wie evolvieren Regeln? |
| κ | Komplementarität | Was bedingt sich gegenseitig? |
| λ | Spannungs-Regulator | Lokal vs. Global? |

## Module

### META (7232) - Grundformel-Generator
- **100 Axiome** für Ontologie, Epistemologie, Governance, Dynamik
- **Formel**: `Φ_META = Ω_ONT · Ω_EPI · Ω_GOV · Ω_DYN`
- **Rolle**: Definiert abstrakte Variablen, Submodule verfeinern

### INU (7234) - Individueller Nutzen
- **59 Axiome** über FEPSDE-Dimensionen
- **FEPSDE**: Financial, Emotional, Physical, Social, Digital, Ecological
- **Formel**: `Φ_INU = V_base + Σ[ω_d(G_d - λ_d·P_d)] + C + CB - CD`

### KNU (7235) - Kollektiver Nutzen
- **46 Axiome** für Kooperation, Bestrafung, Destruktion
- **Formel**: `Φ_KNU = U_kol · ρ_K · Ψ_IDN · Ψ_INST · Ψ_DEST`

### IDN (7236) - Identitätsnutzen
- **70 Axiome** für Multiplizität, Kohärenz, Konflikte
- **Formel**: `Φ_IDN = Σ π_j · A_j · U_IDN^j`

### WAX (7243) - Willingness
- **λ-Hybrid-Logik**: `WAX = λ · WAX^compl + (1-λ) · WAX^add`
- λ=0: Additiv (Homo oeconomicus)
- λ=1: Komplementär (schwächstes Glied)

## Schlüsselkonzepte

### Ψ - Kohärenz-Operator
Nicht-additive Kombination von Nutzen. Einfache Addition verletzt Arrow's Impossibility Theorem.

### κ - Komplementarität
Gegensätze, die sich gegenseitig bedingen:
- Individuum ↔ Kollektiv
- Nutzen ↔ Kosten
- Kurzfristig ↔ Langfristig
- Stabilität ↔ Wandel

### λ - Spannungs-Regulator
```
U_eff = (1-λ) · U_lokal + λ · κ(U_lokal, U_komplement)
```
- λ ist kontextabhängig: `λ = f(ρ, σ, t)`
- Exponentiell sättigend (MA_0.ES)

### MA_0.ES - Exponentielle Sättigung
**Meta-Axiom** (strukturell, ohne Zahlenwert):
> "Systeme mit proportionaler Unsicherheitsreduktion konvergieren zu Zustand mit Unsicherheitsrest."

**Korollar ES-1** (abgeleitet):
> "Übergangspunkt bei ~63% Abbau (Rest ≈ 1/e ≈ 0.368)"

## Methodik

### Intra-Modul (innerhalb eines Moduls)
1. **Fundament-Axiome**: Existenzbedingungen
2. **Struktur-Axiome**: FEPSDE, Gewichtungen
3. **Operations-Axiome**: Berechnungslogik
4. **Dynamik-Axiome**: Zeit, Feedback

### Inter-Modul (zwischen Modulen)
- META validiert (⊢) alle Submodule
- INU ↔ KNU ↔ IDN: bidirektional
- Sequenz: INU/KNU/IDN → AWX → WAX → WTX → Verhalten

## Anwendung

Nutze BEATRIX für:
- **Verhaltensanalyse**: Entscheidungen über INU/KNU/IDN analysieren
- **Interventions-Design**: Nudges und Interventionen designen
- **Segmentierung**: Nach Verhaltenstypen und λ-Werten gruppieren
- **Policy-Design**: Evidenzbasierte Politikgestaltung
- **Journey-Optimierung**: Customer/Citizen Journeys

## Praktischer Workflow

Für die praktische Anwendung nutze den **5-Phasen-Workflow**:

```
PHASE 1: DIAGNOSE    → Zielverhalten, Zielgruppe, Kontext erfassen
PHASE 2: ANALYSE     → INU, KNU, IDN, λ bewerten
PHASE 3: SYNTHESE    → Kohärenz prüfen, Schwachstelle identifizieren
PHASE 4: DESIGN      → Intervention entwickeln (AWX, WAX, Nudge)
PHASE 5: EVALUATION  → Wirksamkeit messen, iterieren
```

**Detaillierter Workflow-Guide**: `resources/workflow-guide.md`

## Daten-Inputs

Vor jeder BCM-Analyse müssen diese Daten erfasst werden:

```
1. PROJEKT-DEFINITION     → Ziel, Zeitrahmen, Erfolgskriterium
2. ZIELVERHALTEN          → Was soll geändert werden?
3. ZIELGRUPPE (σ)         → Wer? Segmente?
4. KONTEXT (ρ)            → Physisch, sozial, institutionell, kulturell
5. BASELINE               → Aktuelles Verhalten (%)
6. FEPSDE-GEWICHTUNGEN    → ω pro Dimension (Σ = 100%)
7. SOZIALE STRUKTUR       → Normen, Sanktionen, Vertrauen
8. IDENTITÄTS-LANDSCHAFT  → Aktive Identitäten, Konflikte
9. RESSOURCEN             → Budget, Zeit, Kanäle, Constraints
```

**Vollständiges Input-Template**: `resources/data-input-template.md`

## Decision Tree (Interventions-Logik)

Systematische Auswahl der richtigen Intervention:

```
1. SCHWACHSTELLE → INU negativ? KNU negativ? IDN negativ?
2. λ-STRATEGIE   → λ<0.3 (INU-Fokus) | 0.3-0.7 (Hybrid) | >0.7 (KNU/IDN)
3. AWX-CHECK     → <3 = Awareness zuerst! | ≥3 = weiter
4. WAX-CHECK     → <3 = Barrieren senken! | ≥3 = Trigger setzen
5. NUDGE-WAHL    → Aus Katalog nach Schwachstelle
```

**Vollständiger Decision Tree**: `resources/decision-tree.md`

## Constraints

### Epistemologisch
- **Nicht-normativ**: BCM beschreibt, schreibt nicht vor
- **Kontextabhängig**: Keine universellen Optima
- **Falsifizierbar**: Korollare sind empirisch testbar

### Methodologisch
- **Kohärenz-basiert**: Keine einfache Addition von Nutzen
- **Meta-Axiome ohne Zahlenwerte**: Zahlen nur in Korollaren
- **Design-Axiome sind Empfehlungen**: Nicht Zwang

### Warnungen
- 1/e (0.37) ist KEIN universelles Optimum
- λ-Werte sind kontextabhängig
- Arrow's Theorem verbietet einfache Aggregation
- "37% ist immer gut" = falsche Anwendung

## Datenquellen

Lies die Axiome aus diesen Dateien:
- `meta/meta.json` - 100 Meta-Axiome
- `inu/inu.json` - 59 INU-Axiome
- `knu/knu.json` - 46 KNU-Axiome
- `idn/idn.json` - 70 IDN-Axiome
- `wax/wax.json` - WAX mit λ-Logik
- `wtx/wtx.json` - Übergangswahrscheinlichkeiten
- `context/context.json` - Kontext-Definitionen

## Beispiel-Anwendung

**Frage**: "Wie kann ich Mitarbeiter zu mehr Nachhaltigkeit motivieren?"

**BCM-Analyse**:
1. **INU**: Welcher individuelle Nutzen? (FEPSDE: Eco↑, Fin?, Emo?)
2. **KNU**: Kollektiver Druck? Soziale Normen? Bestrafung bei Nicht-Einhaltung?
3. **IDN**: Passt Nachhaltigkeit zur Identität der Mitarbeiter?
4. **λ**: Wie stark ist lokale vs. kollektive Orientierung?
5. **AWX**: Ist Bewusstsein für Problem vorhanden?
6. **WAX**: Besteht Handlungsbereitschaft?
7. **Intervention**: Design basierend auf schwächstem Glied (λ→1)

## Referenzen

- FehrAdvice & Partners AG (2025): BCM 2.0 Handbook
- Kahneman & Tversky (1979): Prospect Theory
- Thaler & Sunstein (2008): Nudge
- Arrow (1951): Impossibility Theorem
- Fehr & Schmidt (1999): Fairness

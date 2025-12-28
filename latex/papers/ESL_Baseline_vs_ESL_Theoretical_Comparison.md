# Theoretical Comparison: Baseline (π_formal) vs. ESL (π_ESL)

**Date:** 2025-12-28
**Status:** Core theoretical distinction for α-theory

---

## 1. Common Foundation

Both prompts share identical structure to ensure fair comparison:

| Element | Baseline | ESL |
|---------|----------|-----|
| Item set E | identical | identical |
| Categories C | {REAL, UNSICHER, UNBEKANNT} | {REAL, UNSICHER, UNBEKANNT} |
| Domain | Behavioral Economics | Behavioral Economics |
| Formal structure | Goal, Procedure, Restrictions | Goal, Procedure, Restrictions |
| Knowledge injection | none | none |

**Implication:** Output differences cannot be attributed to task, domain, or structural ambiguity.

---

## 2. The Critical Difference: What Gets Formalized

### Baseline Prompt (π_formal)

**Characteristics:**
- Formal
- Unambiguous
- **Epistemically underdetermined**

**Implicit Freedom:**

The baseline says:
> "Choose REAL if you recall literature."

But leaves open:
- How strictly to verify this recall
- Whether similar concepts suffice
- How to handle label combinations

**→ The model may (implicitly) decide what counts as sufficient evidence.**

---

### ESL Prompt (π_ESL)

**Characteristics:**
- Formal AND epistemically calibrated
- **Explicit negative definitions**
- **Explicit termination conditions**

**New Constraint:**

ESL specifies not just the goal, but also:
> **When REAL is explicitly forbidden**

This is the decisive point.

---

## 3. Comparison Along Theoretical Dimensions

### (A) Interpretation Ambiguity

| Dimension | Baseline | ESL |
|-----------|----------|-----|
| Goal clarity | high | high |
| Categories | unambiguous | unambiguous |
| Epistemic threshold | **implicit** | **explicit** |
| Label interpretation | open | strict |
| Ambiguity | low | **minimal** |

**→ ESL reduces ambiguity further, but this is not the main point.**

---

### (B) Activation Competence α

**Baseline:**
- Allows "conceptual matching"
- Allows fluency-based plausibility
- REAL can arise through association

```
α_baseline ≈ P(plausible generation)
```

**ESL:**
- Forces exact retrieval matching
- Forbids semantic approximation
- Forces binary self-verification

```
α_ESL ≈ P(exact knowledge retrieval)
```

**→ ESL shifts the decision mechanism.**

---

### (C) What ESL Adds (Critical!)

ESL contains **explicit anti-heuristics**:

| Forbidden | Baseline | ESL |
|-----------|----------|-----|
| "Sounds similar" | allowed | ❌ forbidden |
| "Related concept exists" | allowed | ❌ forbidden |
| Fluency-based generalization | allowed | ❌ forbidden |

The baseline does not explicitly forbid these.

---

## 4. Why ESL Is an Activation Prompt (and Baseline Is Not)

| Prompt | What it specifies |
|--------|-------------------|
| **Baseline** | What to do |
| **ESL** | What to do + **when REAL is logically excluded** |

**→ ESL forces activation of M_latent.**
**→ Baseline only permits it.**

---

## 5. Core Theoretical Diagnosis (α-Theory)

### The Key Insight

```
The baseline prompt measures SPONTANEOUS activation competence α.
The ESL prompt measures ENFORCEABLE activation competence α*.
```

### Formal Relation

```
α_ESL ≥ α_baseline
```

If not:
- Model cannot activate knowledge even under coercion
- α is model-limited

---

## 6. Why Mistral Remains Weak Under ESL

This is the empirical finding that validates the theory:

- ESL is formally correct ✓
- ESL forces retrieval ✓
- Yet false REAL assignments persist ✗

**→ This is the actual scandal, and it is now logically isolated.**

Interpretation:
```
Mistral: α* ≈ 0.90 < 1.00
         ↓
Model-limited activation competence
Cannot be fixed by prompt alone
```

---

## 7. Paper-Ready Comparison Table

| Dimension | Baseline | ESL |
|-----------|----------|-----|
| Formality | high | high |
| Epistemic explicitness | medium | **very high** |
| Activation coercion | ❌ | ✔️ |
| Plausibility escape | ✔️ | ❌ |
| Expected α | low | higher |
| Observed α (Mistral) | 0.50 | 0.90 |
| Observed α (Claude) | 0.60 | 1.00 |
| Observed α (Gemini) | 0.70 | 1.00 |
| Observed α (GPT-5.2) | 0.60 | 1.00 |

---

## 8. The One Sentence Summary

> **The baseline prompt measures whether a model voluntarily activates knowledge; the ESL prompt measures whether it can activate knowledge even under explicit epistemic coercion.**

---

## 9. Theoretical Implications

### 9.1 Two Types of α

| Type | Symbol | Meaning |
|------|--------|---------|
| Spontaneous | α | Default activation under ambiguous conditions |
| Enforceable | α* | Maximum activation under epistemic coercion |

### 9.2 Model Classification

| Model | α | α* | Interpretation |
|-------|---|----|----|
| Claude | 0.60 | 1.00 | Coercion-responsive |
| Gemini | 0.70 | 1.00 | Coercion-responsive |
| GPT-5.2 | 0.60 | 1.00 | Coercion-responsive |
| Mistral | 0.50 | 0.90 | **Partially coercion-resistant** |

### 9.3 The Mistral Anomaly

Mistral shows:
```
α* < 1.00

→ Even under maximal epistemic coercion,
   activation remains incomplete.

→ This is a MODEL property, not a PROMPT property.
```

---

## 10. Falsification Criterion

The distinction between α and α* generates a testable prediction:

**If** a model shows α* < 1.00 under ESL,
**Then** no prompt-based intervention can achieve α = 1.00.

This can only be overcome by:
- Fine-tuning
- Architectural changes
- Different training data

---

*Document generated: 2025-12-28*

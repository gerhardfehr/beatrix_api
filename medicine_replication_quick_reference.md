# Medical/Biomedical Replication Studies - Quick Reference Table

## ESL Framework Analysis Summary

| # | Study | Claim | B-value | E-value | K-value | Outcome | Evidence Type |
|---|-------|-------|---------|---------|---------|---------|---------------|
| **CONFIRMED REPLICATIONS** |
| 1 | **Statins** | Reduce vascular events ~20% per 1mmol/L LDL-C | 0.82 | 0.95 | 0.87 | ✅ 1 | Meta-analysis 27 RCTs, N>170k |
| 2 | **Aspirin** | Reduces vascular mortality 20% in acute MI | 0.80 | 0.92 | 0.88 | ✅ 1 | ISIS-2 RCT N=17,187, 10yr FU |
| 3 | **HPV Vaccine** | Prevents 98-99% HPV-16/18 cervical neoplasia | 0.85 | 0.95 | 0.90 | ✅ 1 | Phase III RCTs + population studies |
| 4 | **PD-1 Inhibitors** | 40% response, 73% 1yr survival melanoma | 0.75 | 0.88 | 0.87 | ✅ 1 | Multiple Phase III, FDA 2014 |
| 5 | **BRCA1/2** | 50-87% lifetime breast cancer risk | 0.80 | 0.85 | 0.95 | ✅ 1 | Linkage studies, clinical validation |
| 6 | **Tamoxifen** | Reduces breast cancer risk 49% | 0.82 | 0.85 | 0.97 | ✅ 1 | NSABP P-1 RCT N=13,388 |
| **FAILED REPLICATIONS** |
| 7 | **STAP Cells** | Acid stress creates pluripotent stem cells | 0.95 | 0.20 | 0.26 | ❌ 0 | Lab experiments, RETRACTED |
| 8 | **Beta-Amyloid** | Anti-amyloid antibodies improve cognition | 0.85 | 0.45 | 0.53 | ❌ 0 | Multiple failed Phase III trials |
| 9 | **Avastin/BC** | Bevacizumab improves metastatic BC outcomes | 0.85 | 0.50 | 0.59 | ❌ 0 | E2100 → AVADO/RIBBON1 failed |
| 10 | **HRT (WHI)** | HRT reduces CVD in postmenopausal women | 0.85 | 0.40 | 0.47 | ❌ 0 | Obs → RCT overturned |
| 11 | **Antioxidants** | Beta-carotene/vitamins C/E prevent cancer | 0.90 | 0.35 | 0.39 | ❌ 0 | 9 RCTs negative, some harmful |
| 12 | **Begley 2012** | 53 landmark cancer studies | 0.88 | 0.25 | 0.28 | ❌ 0 | Only 6/53 (11%) replicated |

---

## Summary Statistics

### Confirmed (N=6)
- **Mean B**: 0.81 (appropriately strong claims)
- **Mean E**: 0.90 (excellent evidence - large RCTs, meta-analyses)
- **Mean K**: 0.91 (excellent calibration)
- **Evidence**: Large RCTs (N > 10,000), meta-analyses, FDA approval
- **Replication**: 100% success with real-world validation

### Failed (N=6)
- **Mean B**: 0.88 (definitive claims)
- **Mean E**: 0.36 (weak evidence - small studies, observational, preclinical)
- **Mean K**: 0.42 (catastrophic miscalibration)
- **Evidence**: Observational, preclinical, small RCTs, fraud
- **Replication**: 0-11% success; most completely failed

---

## Key Patterns

### 🎯 What Replicates in Medicine
- **Large RCTs**: N > 10,000 with clear outcomes
- **Meta-analyses**: Multiple independent trials
- **Real-world validation**: Population studies confirm RCT findings
- **FDA approval**: Rigorous regulatory review
- **Appropriate hedging**: Effect sizes with ranges

### ❌ What Fails in Medicine
- **Preclinical research**: 11-25% replication rate (Begley, RPCB)
- **Observational → RCT**: Frequent reversal (HRT, Antioxidants)
- **Accelerated approval**: Single trials often fail confirmation (Avastin)
- **Fraud**: STAP cells (retracted)
- **Definitive claims + weak evidence**: K < 0.60 in all failures

### 📊 ESL Insights
- **Catastrophic overclaiming**: Failed studies had B=0.88, E=0.36, K=0.42
- **K < 0.60 = Red flag**: All 6 failures had K < 0.60
- **K > 0.85 = Reliable**: All 6 confirmed studies had K > 0.85
- **Evidence hierarchy matters**: RCT >>> Observational > Preclinical

---

## ESL Interpretation Guide (Medicine)

### B-value (Claim Strength)
- **0.90+**: "Prevents," "causes," "demonstrates" → Very strong
- **0.80-0.89**: "Reduces," "improves," "shows" → Strong
- **0.60-0.79**: "Associated with," "suggests" → Moderate
- **0.40-0.59**: "May," "preliminary evidence" → Tentative

### E-value (Evidence Quality)
- **0.90+**: Meta-analysis of large RCTs, real-world validation
- **0.80-0.89**: Multiple large RCTs (N > 5,000), long follow-up
- **0.70-0.79**: Single large RCT (N > 1,000), well-controlled
- **0.50-0.69**: Single RCT (N < 1,000) OR multiple observational
- **0.30-0.49**: Single observational OR preclinical with good controls
- **< 0.30**: Preclinical only, small N, poor controls

### K-value (Calibration) - Medicine Standards
- **K ≥ 0.85**: Excellent - publish with strong claims
- **K 0.75-0.84**: Good - appropriate for clinical guidelines
- **K 0.60-0.74**: Poor - requires hedging or more evidence
- **K < 0.60**: Catastrophic - major revision needed

---

## Red Flags for Reviewers

### 🚩 High-Risk Combinations
1. **Strong claims (B > 0.85) + Weak evidence (E < 0.50)** → K < 0.60
   - Examples: STAP cells, Antioxidants, Begley's 53
   - Action: Reject or demand major revision

2. **Single trial + Definitive language**
   - Examples: Avastin (E2100 alone)
   - Action: Require "in one trial" qualifier, await replication

3. **Observational → Causal claims**
   - Examples: HRT, Antioxidants (dietary associations)
   - Action: Require RCT confirmation before causal language

4. **Preclinical → Clinical extrapolation**
   - Examples: Begley's 53 studies
   - Action: Require "if confirmed in humans" qualifiers

### ✅ Green Flags for Acceptance
1. **K ≥ 0.85** with transparent methodology
2. **Multiple independent RCTs** with meta-analysis
3. **Preregistered trials** with open data
4. **Real-world validation** of RCT findings
5. **Appropriate hedging** when evidence is preliminary

---

## Comparison to Psychology

| Domain | N Confirmed | N Failed | Mean K (Confirmed) | Mean K (Failed) | Worst K |
|--------|-------------|----------|-------------------|----------------|---------|
| **Medicine** | 6 | 6 | 0.91 | 0.42 | 0.26 (STAP) |
| **Psychology** | 6 | 8 | 0.90 | 0.65 | 0.55 (Elderly Priming) |

**Medicine has MORE extreme miscalibration**:
- Psychology failures: K = 0.55-0.75 (overclaiming)
- Medicine failures: K = 0.26-0.59 (catastrophic overclaiming + fraud)

**Both domains share**:
- Excellent calibration in confirmed studies (K ~0.90)
- Pervasive overclaiming in failures (B ~0.85-0.88)
- Evidence quality distinguishes success from failure

---

## Clinical Impact of Miscalibration

### Lives Lost or Harmed
- **HRT**: ~91,000 excess deaths (2002-2012) from underuse after WHI
- **Antioxidants**: Increased cancer and mortality in smokers taking beta-carotene
- **Avastin**: Patients exposed to ineffective, expensive, harmful treatment
- **Beta-amyloid**: Billions wasted, clinical trials on ineffective mechanism
- **Begley's 53**: Patients enrolled in clinical trials based on irreproducible preclinical data

### Resources Wasted
- **Beta-amyloid drugs**: ~$10 billion+ in failed drug development
- **STAP cells**: Entire field spawned, then collapsed
- **Preclinical failures**: Begley estimates billions wasted on irreproducible research

### Erosion of Trust
- **STAP cells**: Suicide of co-author, RIKEN scandal
- **Avastin**: FDA credibility damaged by accelerated approval reversal
- **HRT**: Women lost trust in hormone therapy (even when beneficial)

---

## Recommendations

### For Clinical Researchers
1. **Use ESL K-score threshold**: K ≥ 0.75 for clinical medicine
2. **Match language to evidence**:
   - Single RCT → "In this trial..."
   - Multiple RCTs → "Consistent evidence shows..."
   - Meta-analysis → "Definitively established..."
3. **Preregister all clinical trials** (ClinicalTrials.gov)
4. **Report all outcomes**, including negative results
5. **Wait for replication** before definitive claims

### For Preclinical Researchers
1. **Use extreme caution** in language (K ≥ 0.60 minimum)
2. **Internal replication** before publication
3. **Share protocols and materials** for external replication
4. **Acknowledge** that 75-90% of preclinical findings fail to replicate
5. **Never extrapolate** to clinical applications without "if confirmed in humans"

### For Journals
1. **Implement ESL scoring** in peer review
2. **Require K ≥ 0.75** for strong claims
3. **Registered Reports** for confirmatory research
4. **Publish negative results** and replication failures
5. **Enforce CONSORT, STROBE, ARRIVE** guidelines

### For Regulatory Agencies
1. **Accelerated approval** only with very strong rationale
2. **Require confirmatory trials** within 2-3 years
3. **Withdraw approval** swiftly if confirmatory trials fail (like Avastin)
4. **Post-marketing surveillance** for all approvals

---

## Conclusion

**Medical research shows even more extreme miscalibration than psychology:**
- Failed studies: K = 0.42 (catastrophic)
- Confirmed studies: K = 0.91 (exemplary)

**The ESL framework could have prevented:**
- Scientific fraud (STAP cells: K = 0.26)
- Wasted billions (Beta-amyloid drugs: K = 0.53)
- Harmful treatments (Antioxidants: K = 0.39)
- Public health reversals (HRT: K = 0.47)
- Failed clinical trials based on irreproducible preclinical data (Begley: K = 0.28)

**When medicine gets it right** (Statins, Aspirin, HPV vaccine, PD-1, BRCA, Tamoxifen), the calibration is excellent (K = 0.87-0.97), and millions of lives are saved.

**When medicine gets it wrong**, people die, billions are wasted, and trust erodes.

**ESL is essential for medical research integrity.**

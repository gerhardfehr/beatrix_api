# Kapitel 7: META im BEATRIX-System

## Status: Minimal (36 Zeilen)

## Enthaltene Abschnitte

- 7.1 Rolle bei der LLM-basierten Estimation
- 7.2 Constrained Generation Pipeline
- 7.3 Ambiguity Detection

## Kritische Frage: Merge mit Section 6 oder 9.8?

Dieses Kapitel überschneidet sich stark mit:
- **Section 6** (Integration mit operativen Modulen)
- **Section 9.8** (Drei-Phasen-Architektur)

### Option A: Merge mit Section 6
→ Alles zur technischen Integration in einem Kapitel

### Option B: Merge mit Section 9.8
→ Alles zur BEATRIX-Implementation zusammen

### Option C: Eigenständig ausbauen
→ Fokus auf LLM-spezifische Aspekte

## Falls eigenständig: Vertiefungsbedarf

### System Prompts mit META-Axiomen
- [ ] Wie werden Axiome in Prompts injiziert?
- [ ] Beispiel-Prompts für Parameter-Extraktion
- [ ] Axiom-aware Few-Shot Examples

### Constrained Generation
- [ ] JSON Schema aus Axiomen ableiten
- [ ] Structured Outputs mit Axiom-Constraints
- [ ] Pydantic-Modelle mit Axiom-Validierung

### Ambiguity Detection
- [ ] Welche Axiome triggern Rückfragen?
- [ ] Confidence Thresholds
- [ ] Beispiele für erkannte Ambiguitäten

### LLM-spezifische Herausforderungen
- [ ] Halluzination vs. Axiom-Konformität
- [ ] Prompt Injection Risiken
- [ ] Konsistenz über Sessions

## Offene Fragen

- Dieses Kapitel eliminieren und Inhalt verteilen?
- Oder zum zentralen "BEATRIX Technical Guide" ausbauen?

## Zuletzt bearbeitet

Erstversion - Entscheidung über Zukunft nötig

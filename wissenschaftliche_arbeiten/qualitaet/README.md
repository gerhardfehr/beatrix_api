# Qualitätssicherung - Meta-Qualitäts-Container (MQC)

## Übersicht

Der **Meta-Qualitäts-Container (MQC)** ist ein konfigurierbares Framework zur Qualitätsbewertung von Kapiteln des Meta_Modul_Paper.

```
┌─────────────────────────────────────────────────────────────┐
│           META-QUALITÄTS-CONTAINER (MQC)                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   13 Dimensionen × Kapitel-Typ × Zielgruppe                │
│         ↓              ↓              ↓                    │
│   ┌──────────────────────────────────────────────────────┐  │
│   │     KAPITEL-SPEZIFISCHE QUALITÄTSMATRIX              │  │
│   └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Dateien

| Datei | Beschreibung |
|-------|--------------|
| `mqc_schema.yaml` | Vollständige Schema-Definition (13 Dimensionen, 4 Kapiteltypen, 5 Zielgruppen) |
| `kapitel_XX_bewertung.yaml` | Bewertung pro Kapitel |

## Die 13 Qualitätsdimensionen

### Ursprüngliche Dimensionen (D01-D06)

| ID | Name | Fokus |
|----|------|-------|
| D01 | Wissenschaftliche Rigorosität | Quellen, Argumentation, Methodik |
| D02 | BCM/BEATRIX Spezifität | Axiome, Parameter, Constraints |
| D03 | Didaktische Qualität | Beispiele, Progression, Visualisierung |
| D04 | Praktische Anwendbarkeit | Handlungsanweisungen, Code, Warnungen |
| D05 | Konsistenz & Notation | Terminologie, Formate, Referenzen |
| D06 | Zielgruppen-Adäquatheit | Laien, Experten, Executive Summary |

### Erweiterte Dimensionen (D07-D13)

| ID | Name | Fokus |
|----|------|-------|
| D07 | Epistemische Selbst-Reflexion | Grenzen, Unsicherheit, offene Fragen |
| D08 | Validierungs-Dimension | Evidenztyp, Effektstärken, Konfidenz |
| D09 | Abhängigkeits-Struktur | Axiom-Hierarchie, Konflikte, Voraussetzungen |
| D10 | Evolutionäre Dimension | Versionen, Kompatibilität, Roadmap |
| D11 | Operationalisierungs-Tiefe | Messbarkeit, Code, Tests |
| D12 | Narrative & Engagement | Roter Faden, Motivation, Spannungsbogen |
| D13 | Meta-Reflexivität | Selbstanwendung, Bias-Transparenz |

## Kapiteltypen

| Typ | Kapitel | Hohe Priorität |
|-----|---------|----------------|
| `rahmen_kapitel` | 0, 1, 10 | D03, D06, D12 |
| `axiom_kapitel` | 2, 3, 4, 5 | D01, D02, D08 |
| `integration_kapitel` | 6, 7 | D02, D09, D11 |
| `transformation_kapitel` | 9 | D04, D10, D11 |

## Zielgruppen-Multiplikatoren

| Zielgruppe | Hohe Gewichtung |
|------------|-----------------|
| Verhaltensökonom | D01, D08, D07 |
| KI Engineer | D04, D11, D05 |
| Business Stakeholder | D03, D06, D12 |
| Regulator/Ethiker | D07, D13, D04 |
| Berater/Praktiker | D04, D03, D12 |

## Bewertungsskala

| Score | Bewertung |
|-------|-----------|
| 0.9 - 1.0 | Exzellent |
| 0.75 - 0.9 | Gut |
| 0.6 - 0.75 | Akzeptabel |
| 0.4 - 0.6 | Verbesserungswürdig |
| 0.0 - 0.4 | Nicht akzeptabel |

## Nutzung

### 1. Kapitel bewerten

```yaml
# kapitel_XX_bewertung.yaml erstellen
kapitel:
  id: "04"
  name: "Governance"
  typ: "axiom_kapitel"

dimensionen:
  D01_wissenschaft:
    score: 0.7
    bewertung:
      quellenqualitaet:
        wert: 0.8
        notiz: "Gute Quellenbasis"
    verbesserungen:
      - "Mehr aktuelle Quellen zu AI Act"
```

### 2. Gewichteten Score berechnen

```
Score = Σ (Dim_Score × Kapitel_Gewicht × Zielgruppen_Mult)
        / Σ (Kapitel_Gewicht × Zielgruppen_Mult)
```

### 3. Verbesserungen priorisieren

Fokus auf Dimensionen mit:
- Niedrigem Score UND
- Hoher Gewichtung für Kapiteltyp UND
- Hohem Multiplikator für Zielgruppe

## Status der Bewertungen

| Kapitel | Status | Score |
|---------|--------|-------|
| 00 Orientierung | ✅ Bewertet | 0.71 |
| 01 Einführung | ⏳ Ausstehend | - |
| 02 Ontologie | ⏳ Ausstehend | - |
| 03 Epistemologie | ⏳ Ausstehend | - |
| 04 Governance | ⏳ Ausstehend | - |
| 05 Dynamik | ⏳ Ausstehend | - |
| 06 Integration | ⏳ Ausstehend | - |
| 07 META/BEATRIX | ⏳ Ausstehend | - |
| 09 Transformation | ⏳ Ausstehend | - |
| 10 Ausblick | ⏳ Ausstehend | - |

## Nächste Schritte

1. [ ] Bewertungen für priorisierte Kapitel erstellen (04, 06)
2. [ ] Python-Skript für automatische Score-Berechnung
3. [ ] Dashboard für Qualitätsübersicht
4. [ ] CI/CD Integration für automatische Prüfungen

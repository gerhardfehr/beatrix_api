# Scoring-Methodik

Dieses Verzeichnis enthält die detaillierten Operationalisierungen für jede Qualitätsdimension.

## Struktur pro Dimension

```yaml
dimension:
  id: "D03"
  name: "Didaktische Qualität"
  beschreibung: "..."

kriterien:
  beispieldichte:
    id: "D03.1"

    definition: |           # Was wird gemessen?

    operationalisierung:    # Was zählt als X?
      zaehlt_als: [...]
      zaehlt_nicht: [...]
      marker_im_text: [...]

    messmethode:            # Wie wird gemessen?
      typ: "ratio|count|ordinal|boolean"
      formel: "..."
      automatisierbarkeit: "hoch|teilweise|manuell"

    skala:                  # Wie wird Score zugewiesen?
      bereiche:
        - score: 0.3
          bedingung: "..."

    ankerbeispiele:         # Konkrete Beispiele für jeden Score
      score_0.3:
        text_beispiel: "..."
        problem: "..."

aggregation:                # Wie werden Kriterien kombiniert?
  gewichte: {...}
  formel: "..."

pruefprotokoll:             # Schritt-für-Schritt Anleitung
  schritt_1: ...
```

## Status der Methodiken

| Dimension | Status | Datei |
|-----------|--------|-------|
| D01 Wissenschaft | ⏳ Ausstehend | - |
| D02 BCM-Spezifik | ⏳ Ausstehend | - |
| **D03 Didaktik** | ✅ **PROTOTYP** | `D03_didaktik.yaml` |
| D04 Anwendbarkeit | ⏳ Ausstehend | - |
| D05 Konsistenz | ⏳ Ausstehend | - |
| D06 Zielgruppe | ⏳ Ausstehend | - |
| D07 Epist. Reflexion | ⏳ Ausstehend | - |
| D08 Validierung | ⏳ Ausstehend | - |
| D09 Abhängigkeiten | ⏳ Ausstehend | - |
| D10 Evolution | ⏳ Ausstehend | - |
| D11 Operationalisierung | ⏳ Ausstehend | - |
| D12 Narrative | ⏳ Ausstehend | - |
| D13 Meta-Reflexivität | ⏳ Ausstehend | - |

## Kernprinzipien

### 1. Operationalisierbarkeit
Jedes Kriterium muss so definiert sein, dass zwei unabhängige Prüfer zum gleichen Ergebnis kommen.

### 2. Marker-basierte Zählung
Wo möglich, definieren wir Text-Marker die automatisch gezählt werden können:
```
marker_im_text:
  - "Beispiel:"
  - "z.B."
  - "\\begin{example}"
```

### 3. Klare Schwellenwerte
Jeder Score-Bereich hat eine eindeutige Bedingung:
```
- score: 0.7
  bedingung: "1.0 <= ratio < 2.0"
```

### 4. Ankerbeispiele
Für jeden Score-Bereich gibt es ein konkretes Textbeispiel, das zeigt, wie dieser Score aussieht.

### 5. Transparente Aggregation
Die Gewichtung der Kriterien ist explizit dokumentiert:
```
gewichte:
  beispieldichte: 0.30
  beispieltypen: 0.20
  progression: 0.25
```

## Nutzung

### Beim Bewerten:
1. Öffne `methodik/D03_didaktik.yaml`
2. Folge dem `pruefprotokoll`
3. Nutze `marker_im_text` für automatische Vorprüfung
4. Validiere manuell mit `ankerbeispiele`
5. Dokumentiere in `kapitel_XX_bewertung.yaml`

### Beim Erweitern:
1. Kopiere `D03_didaktik.yaml` als Template
2. Passe `definition`, `operationalisierung`, `skala` an
3. Füge `ankerbeispiele` hinzu
4. Definiere `aggregation` Gewichte

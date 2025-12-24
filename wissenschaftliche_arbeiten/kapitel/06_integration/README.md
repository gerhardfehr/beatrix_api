# Kapitel 6: Integration mit operativen Modulen

## Status: Minimal (49 Zeilen)

## Enthaltene Abschnitte

- 6.1 Validierungs-Beziehungen
- 6.2 Die BCM 2.2 Kernformel
- 6.3 META-Axiome als Constraints

## Vertiefungsbedarf (Priorität: HOCH)

### Technische Integration
- [ ] Wie "feuern" META-Axiome bei Parameter-Schätzung?
- [ ] Constraint-Propagation-Algorithmen
- [ ] Validierungs-Pipeline (welches Axiom prüft was?)
- [ ] Dependency Graph: META → INU/KNU/IDN/LAMBDA

### Modul-Interaktionen
- [ ] META → INU: Welche Axiome constrainen individuellen Nutzen?
- [ ] META → KNU: Welche Axiome constrainen kontextuellen Nutzen?
- [ ] META → IDN: Welche Axiome constrainen Identitätsnutzen?
- [ ] META → LAMBDA: Wie beeinflusst META die Loss Aversion?

### Konkrete Beispiele
- [ ] "MA-EPI-12 (Availability) verhindert unrealistischen λ-Wert"
- [ ] "MA-ONT-26 (5-Ebenen) erzwingt Kontextspezifikation"
- [ ] "MA-GOV-03 (Transparency) erfordert Reasoning-Output"

### Implementierung
- [ ] JSON-Schema für Axiom-Constraints
- [ ] Validation-Funktionen in Python
- [ ] Error Messages bei Constraint-Verletzung
- [ ] Integration in BEATRIX Pipeline

## Verwandte Abschnitte

- Section 9.8: Drei-Phasen-Architektur (technische Implementation)
- Section 7: META im BEATRIX-System (Überschneidung prüfen!)

## Offene Fragen

- Sollte Section 6 und 7 gemerged werden?
- Wie granular sollten Constraint-Checks sein?
- Performance-Implikationen von vielen Validierungen?

## Zuletzt bearbeitet

Erstversion - benötigt dringend Erweiterung

# BCM 2.0 Daten-Input Template

> **Alle erforderlichen Inputs für eine BCM-Analyse**

---

## Übersicht: Erforderliche Daten

```
┌─────────────────────────────────────────────────────────────────────┐
│                     BCM DATEN-INPUTS                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. PROJEKT-DEFINITION        □ ausgefüllt                         │
│  2. ZIELVERHALTEN             □ ausgefüllt                         │
│  3. ZIELGRUPPE (σ)            □ ausgefüllt                         │
│  4. KONTEXT (ρ)               □ ausgefüllt                         │
│  5. BASELINE-MESSUNG          □ ausgefüllt                         │
│  6. FEPSDE-GEWICHTUNGEN (ω)   □ ausgefüllt                         │
│  7. SOZIALE STRUKTUR          □ ausgefüllt                         │
│  8. IDENTITÄTS-LANDSCHAFT     □ ausgefüllt                         │
│  9. RESSOURCEN & CONSTRAINTS  □ ausgefüllt                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

# 1. PROJEKT-DEFINITION

```yaml
projekt:
  name: "_________________________________________"

  auftraggeber: "_________________________________________"

  datum_start: "____-____-____"

  datum_ziel: "____-____-____"

  projekttyp:
    - [ ] Verhaltensänderung (Individuen)
    - [ ] Organisationsentwicklung
    - [ ] Policy-Design
    - [ ] Produkt/Service-Optimierung
    - [ ] Kommunikationskampagne
    - [ ] Sonstiges: "_______________________"

  erfolgs_kriterium: |
    Was gilt als Erfolg?
    _________________________________________________________________
    _________________________________________________________________

  budget_kategorie:
    - [ ] < 10.000
    - [ ] 10.000 - 50.000
    - [ ] 50.000 - 200.000
    - [ ] > 200.000
```

---

# 2. ZIELVERHALTEN

```yaml
zielverhalten:

  # Was soll die Zielgruppe TUN?
  gewuenschtes_verhalten: |
    _________________________________________________________________
    _________________________________________________________________

  # Wie spezifisch ist das Verhalten?
  spezifitaet:
    - [ ] Einmalige Handlung (z.B. Anmeldung)
    - [ ] Wiederholte Handlung (z.B. täglich Sport)
    - [ ] Gewohnheitsänderung (z.B. Ernährung)
    - [ ] Unterlassung (z.B. nicht rauchen)
    - [ ] Komplexe Verhaltenskette

  # Ist das Verhalten messbar?
  messbarkeit:
    direkt_beobachtbar: [ ] Ja  [ ] Nein
    quantifizierbar: [ ] Ja  [ ] Nein
    mess_methode: "_________________________________________"

  # Zeitrahmen
  zeitrahmen:
    - [ ] Sofort (einmalig)
    - [ ] Kurzfristig (< 1 Monat)
    - [ ] Mittelfristig (1-6 Monate)
    - [ ] Langfristig (> 6 Monate)
    - [ ] Dauerhaft (Gewohnheit)

  # Verhaltens-Alternativen
  aktuelles_verhalten: |
    Was tut die Zielgruppe JETZT stattdessen?
    _________________________________________________________________

  konkurrierende_verhaltensweisen:
    - "_________________________________________"
    - "_________________________________________"
    - "_________________________________________"
```

---

# 3. ZIELGRUPPE (σ)

```yaml
zielgruppe:

  # Primäre Zielgruppe
  primaer:
    beschreibung: "_________________________________________"
    geschaetzte_groesse: "_______ Personen"

  # Demografische Merkmale
  demografie:
    alter:
      min: "____"
      max: "____"
      schwerpunkt: "____"

    geschlecht:
      - [ ] Überwiegend männlich
      - [ ] Überwiegend weiblich
      - [ ] Ausgewogen
      - [ ] Nicht relevant

    bildung:
      - [ ] Obligatorische Schule
      - [ ] Berufsausbildung
      - [ ] Matura/Abitur
      - [ ] Hochschule
      - [ ] Gemischt

    einkommen:
      - [ ] Unterdurchschnittlich
      - [ ] Durchschnittlich
      - [ ] Überdurchschnittlich
      - [ ] Nicht relevant/unbekannt

    region: "_________________________________________"

  # Psychografische Merkmale
  psychografie:
    werte:
      - "_________________________________________"
      - "_________________________________________"
      - "_________________________________________"

    lebensstil: |
      _________________________________________________________________

    mediennutzung:
      - [ ] Print
      - [ ] TV/Radio
      - [ ] Social Media
      - [ ] Messenger
      - [ ] E-Mail
      - [ ] Persönlich

  # Verhaltens-Historie
  historie:
    frueheres_verhalten: |
      Haben sie das Zielverhalten früher gezeigt?
      _________________________________________________________________

    veraenderungsbereitschaft:
      - [ ] Hoch (suchen aktiv nach Veränderung)
      - [ ] Mittel (offen, aber nicht aktiv)
      - [ ] Niedrig (zufrieden mit Status quo)
      - [ ] Widerstand (aktiv dagegen)

  # Segmentierung
  segmente:
    segment_a:
      name: "_______________________"
      anteil: "____%"
      merkmal: "_________________________________________"

    segment_b:
      name: "_______________________"
      anteil: "____%"
      merkmal: "_________________________________________"

    segment_c:
      name: "_______________________"
      anteil: "____%"
      merkmal: "_________________________________________"
```

---

# 4. KONTEXT (ρ)

```yaml
kontext:

  # Physischer Kontext
  physisch:
    ort: "_________________________________________"

    infrastruktur: |
      Welche physische Umgebung/Infrastruktur existiert?
      _________________________________________________________________

    barrieren_physisch:
      - "_________________________________________"
      - "_________________________________________"

    enabler_physisch:
      - "_________________________________________"
      - "_________________________________________"

  # Sozialer Kontext
  sozial:
    gruppengroesse:
      - [ ] Individuum (allein)
      - [ ] Kleingruppe (2-10)
      - [ ] Team/Abteilung (10-50)
      - [ ] Organisation (50-500)
      - [ ] Grosse Organisation (500+)
      - [ ] Öffentlichkeit

    sichtbarkeit_verhalten:
      - [ ] Privat (niemand sieht es)
      - [ ] Semi-privat (wenige sehen es)
      - [ ] Semi-öffentlich (Gruppe sieht es)
      - [ ] Öffentlich (alle sehen es)

    soziale_normen:
      deskriptiv: |
        Was tun die meisten anderen?
        _________________________________________________________________

      injunktiv: |
        Was wird erwartet/gebilligt?
        _________________________________________________________________

      norm_staerke: "___/10"

    key_influencer:
      - name: "_______________________"
        rolle: "_______________________"
        einfluss: "___/10"
      - name: "_______________________"
        rolle: "_______________________"
        einfluss: "___/10"

  # Institutioneller Kontext
  institutionell:
    organisation: "_________________________________________"

    bestehende_regeln:
      - "_________________________________________"
      - "_________________________________________"

    anreize_vorhanden:
      positiv:
        - "_________________________________________"
      negativ:
        - "_________________________________________"

    entscheidungstraeger:
      - name: "_______________________"
        rolle: "_______________________"
        unterstuetzung: "___/10"

  # Kultureller Kontext
  kulturell:
    kulturkreis: "_________________________________________"

    relevante_werte:
      - "_________________________________________"
      - "_________________________________________"

    tabus:
      - "_________________________________________"

    narrative: |
      Welche Geschichten/Überzeugungen existieren zum Thema?
      _________________________________________________________________

  # Temporaler Kontext
  temporal:
    timing:
      - [ ] Einmaliges Event
      - [ ] Regelmässiger Zeitpunkt
      - [ ] Jederzeit möglich
      - [ ] Saisonal

    zeitdruck:
      - [ ] Hoch (sofortige Entscheidung nötig)
      - [ ] Mittel (Tage/Wochen)
      - [ ] Niedrig (flexibel)

    entscheidungshorizont:
      - [ ] Kurzfristig (heute/morgen)
      - [ ] Mittelfristig (Wochen)
      - [ ] Langfristig (Monate/Jahre)
```

---

# 5. BASELINE-MESSUNG

```yaml
baseline:

  # Aktuelles Verhalten
  aktuell:
    anteil_zielverhalten: "____%"
    anteil_alternativverhalten: "____%"
    anteil_kein_verhalten: "____%"

    messmethode: "_________________________________________"
    messdatum: "____-____-____"
    stichprobengroesse: "_______ Personen"
    konfidenz: "____%"

  # Historische Daten
  historie:
    vorhanden: [ ] Ja  [ ] Nein

    trend:
      - [ ] Steigend
      - [ ] Stabil
      - [ ] Sinkend
      - [ ] Unbekannt

    daten_zeitraum: "von ____-____-____ bis ____-____-____"

  # Benchmark
  benchmark:
    vorhanden: [ ] Ja  [ ] Nein

    benchmark_wert: "____%"
    benchmark_quelle: "_________________________________________"

  # Zielwert
  ziel:
    zielwert: "____%"
    delta_erforderlich: "____%"
    realistisch: [ ] Ja  [ ] Nein  [ ] Unsicher
```

---

# 6. FEPSDE-GEWICHTUNGEN (ω)

```yaml
fepsde:

  # Wie wichtig ist jede Dimension für die Zielgruppe?
  # (Summe sollte ~100% ergeben)

  gewichtungen:
    financial:
      gewicht_omega: "___%"
      relevanz: |
        Warum ist diese Dimension relevant/irrelevant?
        _________________________________________________________________

    emotional:
      gewicht_omega: "___%"
      relevanz: |
        _________________________________________________________________

    physical:
      gewicht_omega: "___%"
      relevanz: |
        _________________________________________________________________

    social:
      gewicht_omega: "___%"
      relevanz: |
        _________________________________________________________________

    digital:
      gewicht_omega: "___%"
      relevanz: |
        _________________________________________________________________

    ecological:
      gewicht_omega: "___%"
      relevanz: |
        _________________________________________________________________

  # Summe prüfen
  summe_omega: "___%" # Sollte ~100% sein

  # Loss Aversion (λ_loss)
  loss_aversion:
    geschaetzt: "___" # Typisch: 2.0-2.5

    begründung: |
      Warum dieser Wert?
      _________________________________________________________________

  # Segment-spezifische Gewichtungen
  segmente_unterschiedlich: [ ] Ja  [ ] Nein

  segment_gewichtungen:
    segment_a:
      name: "_______________________"
      F: "___%" E: "___%" P: "___%" S: "___%" D: "___%" E: "___%"

    segment_b:
      name: "_______________________"
      F: "___%" E: "___%" P: "___%" S: "___%" D: "___%" E: "___%"
```

---

# 7. SOZIALE STRUKTUR (KNU-Inputs)

```yaml
soziale_struktur:

  # Kooperationsstruktur
  kooperation:
    grad: "___/10"

    interdependenz: |
      Wie stark hängen die Akteure voneinander ab?
      _________________________________________________________________

    koordinationsbedarf:
      - [ ] Keiner (individuell)
      - [ ] Niedrig (lose Abstimmung)
      - [ ] Mittel (regelmässige Koordination)
      - [ ] Hoch (enge Zusammenarbeit nötig)

  # Normen
  normen:
    deskriptive_norm:
      verhalten: "_________________________________________"
      staerke: "___/10"
      sichtbarkeit: "___/10"

    injunktive_norm:
      erwartung: "_________________________________________"
      staerke: "___/10"
      sanktionierung: "___/10"

  # Sanktionen/Bestrafung
  sanktionen:
    formell:
      vorhanden: [ ] Ja  [ ] Nein
      art: "_________________________________________"
      wahrscheinlichkeit: "___/10"
      schwere: "___/10"

    informell:
      vorhanden: [ ] Ja  [ ] Nein
      art: "_________________________________________"
      wahrscheinlichkeit: "___/10"
      schwere: "___/10"

  # Vertrauen
  vertrauen:
    in_gruppe: "___/10"
    in_institution: "___/10"
    in_information: "___/10"

  # Destruktions-Risiko
  destruktion:
    trittbrettfahrer_risiko: "___/10"
    sabotage_risiko: "___/10"
    dark_triad_praesenz:
      - [ ] Kein Hinweis
      - [ ] Möglich
      - [ ] Wahrscheinlich
      - [ ] Bekannt
```

---

# 8. IDENTITÄTS-LANDSCHAFT (IDN-Inputs)

```yaml
identitaet:

  # Relevante Identitäten der Zielgruppe
  aktive_identitaeten:

    identitaet_1:
      name: "_________________________________________"
      aktivierung_pi: "___" # 0.0 - 1.0
      fit_mit_zielverhalten: "___/10" # -10 bis +10
      beschreibung: |
        _________________________________________________________________

    identitaet_2:
      name: "_________________________________________"
      aktivierung_pi: "___"
      fit_mit_zielverhalten: "___/10"
      beschreibung: |
        _________________________________________________________________

    identitaet_3:
      name: "_________________________________________"
      aktivierung_pi: "___"
      fit_mit_zielverhalten: "___/10"
      beschreibung: |
        _________________________________________________________________

    identitaet_4:
      name: "_________________________________________"
      aktivierung_pi: "___"
      fit_mit_zielverhalten: "___/10"
      beschreibung: |
        _________________________________________________________________

  # Identitäts-Konflikte
  konflikte:
    vorhanden: [ ] Ja  [ ] Nein

    konflikt_beschreibung: |
      Welche Identitäten stehen in Konflikt?
      _________________________________________________________________

    konflikt_schwere: "___/10"

  # Identitäts-Bedrohung
  bedrohung:
    gefaehrdet_zielverhalten_identitaet: [ ] Ja  [ ] Nein

    welche_identitaet: "_________________________________________"

    bedrohungs_art:
      - [ ] Ausschluss aus Gruppe
      - [ ] Stigmatisierung
      - [ ] Widerspruch zu Werten
      - [ ] Verlust von Status
      - [ ] Sonstiges: "_______________________"

  # Identitäts-Chancen
  chancen:
    staerkt_zielverhalten_identitaet: [ ] Ja  [ ] Nein

    welche_identitaet: "_________________________________________"

    wie: |
      _________________________________________________________________
```

---

# 9. RESSOURCEN & CONSTRAINTS

```yaml
ressourcen:

  # Verfügbare Ressourcen
  verfuegbar:
    budget: "_________________________________________"
    zeit: "_________________________________________"
    personal: "_________________________________________"
    technologie: "_________________________________________"
    zugang_zielgruppe: "_________________________________________"

  # Interventions-Möglichkeiten
  interventions_kanaele:
    - [ ] Persönliche Kommunikation
    - [ ] E-Mail
    - [ ] App/Digital
    - [ ] Physische Umgebung ändern
    - [ ] Prozesse ändern
    - [ ] Policies ändern
    - [ ] Anreize setzen
    - [ ] Schulung/Training
    - [ ] Sonstiges: "_______________________"

  # Constraints
  constraints:
    nicht_aenderbar:
      - "_________________________________________"
      - "_________________________________________"

    politisch_sensitiv:
      - "_________________________________________"

    ethische_grenzen:
      - "_________________________________________"

    rechtliche_grenzen:
      - "_________________________________________"

  # Stakeholder
  stakeholder:
    unterstuetzer:
      - name: "_______________________"
        einfluss: "___/10"

    neutral:
      - name: "_______________________"
        einfluss: "___/10"

    kritiker:
      - name: "_______________________"
        einfluss: "___/10"
```

---

# λ-SCHÄTZUNG

```yaml
lambda:

  # Indikatoren für λ-Wert
  indikatoren:

    # Niedrig (λ → 0, lokal/individuell)
    niedrig:
      - [ ] Starke individuelle Anreize dominieren
      - [ ] Wenig Gruppenidentifikation
      - [ ] Kompetitive Kultur
      - [ ] Kurzfrist-Fokus
      - [ ] "Jeder für sich"-Mentalität

    # Hoch (λ → 1, global/kollektiv)
    hoch:
      - [ ] Starke Gruppennormen
      - [ ] Hohe Identifikation mit Kollektiv
      - [ ] Kooperative Kultur
      - [ ] Langfrist-Fokus
      - [ ] "Wir"-Mentalität

  # Geschätzer λ-Wert
  schaetzung:
    wert: "___" # 0.0 - 1.0

    konfidenz:
      - [ ] Hoch (klare Indikatoren)
      - [ ] Mittel
      - [ ] Niedrig (unsicher)

    begruendung: |
      _________________________________________________________________

  # Segment-spezifisches λ
  segment_lambda:
    segment_a:
      name: "_______________________"
      lambda: "___"

    segment_b:
      name: "_______________________"
      lambda: "___"
```

---

# ZUSAMMENFASSUNG & VALIDIERUNG

```yaml
zusammenfassung:

  # Vollständigkeits-Check
  vollstaendigkeit:
    projekt_definition: [ ] Vollständig  [ ] Teilweise  [ ] Fehlt
    zielverhalten: [ ] Vollständig  [ ] Teilweise  [ ] Fehlt
    zielgruppe: [ ] Vollständig  [ ] Teilweise  [ ] Fehlt
    kontext: [ ] Vollständig  [ ] Teilweise  [ ] Fehlt
    baseline: [ ] Vollständig  [ ] Teilweise  [ ] Fehlt
    fepsde: [ ] Vollständig  [ ] Teilweise  [ ] Fehlt
    soziale_struktur: [ ] Vollständig  [ ] Teilweise  [ ] Fehlt
    identitaet: [ ] Vollständig  [ ] Teilweise  [ ] Fehlt
    ressourcen: [ ] Vollständig  [ ] Teilweise  [ ] Fehlt

  # Datenqualität
  datenqualitaet:
    primaerdaten_vorhanden: [ ] Ja  [ ] Nein
    sekundaerdaten_vorhanden: [ ] Ja  [ ] Nein
    expertenschaetzung: [ ] Ja  [ ] Nein

    gesamt_qualitaet:
      - [ ] Hoch (empirisch fundiert)
      - [ ] Mittel (teilweise empirisch)
      - [ ] Niedrig (überwiegend Annahmen)

  # Offene Fragen
  offene_fragen:
    - "_________________________________________"
    - "_________________________________________"
    - "_________________________________________"

  # Nächste Schritte
  naechste_schritte:
    - [ ] Daten erheben für: _______________________
    - [ ] Experten befragen zu: _______________________
    - [ ] Hypothesen validieren: _______________________
    - [ ] Weiter zu Phase 2 (Analyse)
```

---

# QUICK INPUT (Minimal-Version)

Für schnelle Analysen - nur die wichtigsten Felder:

```yaml
quick_input:

  zielverhalten: "_________________________________________"

  zielgruppe: "_________________________________________"

  aktuelles_verhalten_prozent: "____%"

  ziel_prozent: "____%"

  hauptbarriere_vermutet:
    - [ ] Individueller Nutzen fehlt (INU)
    - [ ] Soziale Unterstützung fehlt (KNU)
    - [ ] Passt nicht zur Identität (IDN)
    - [ ] Bewusstsein fehlt (AWX)
    - [ ] Zu kompliziert (WAX)

  lambda_schaetzung: "___" # 0.0-1.0

  budget_verfuegbar:
    - [ ] Minimal
    - [ ] Moderat
    - [ ] Gross

  zeitrahmen:
    - [ ] Sofort
    - [ ] Wochen
    - [ ] Monate
```

---

*BCM 2.0 Data Input Template v1.0 | FehrAdvice & Partners AG*

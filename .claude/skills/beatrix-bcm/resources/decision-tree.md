# BCM 2.0 Decision Tree

> **Systematische Interventions-Logik basierend auf Φ_META**

---

## Übersicht: Entscheidungsstruktur

```
                              START
                                │
                                ▼
                    ┌───────────────────────┐
                    │  1. SCHWACHSTELLE     │
                    │     IDENTIFIZIEREN    │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │  2. λ-STRATEGIE       │
                    │     WÄHLEN            │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │  3. AWX/WAX           │
                    │     PRÜFEN            │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │  4. INTERVENTION      │
                    │     AUSWÄHLEN         │
                    └───────────┬───────────┘
                                │
                                ▼
                              ENDE
```

---

# DECISION TREE 1: Schwachstellen-Identifikation

```
                         ┌─────────────────┐
                         │ INU, KNU, IDN   │
                         │ Scores vorhanden│
                         └────────┬────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                    ▼             ▼             ▼
              ┌─────────┐   ┌─────────┐   ┌─────────┐
              │ INU < 0 │   │ KNU < 0 │   │ IDN < 0 │
              │    ?    │   │    ?    │   │    ?    │
              └────┬────┘   └────┬────┘   └────┬────┘
                   │             │             │
         ┌────Ja───┴───Nein──┐   │   ┌───Ja───┴───Nein───┐
         │                   │   │   │                   │
         ▼                   │   │   ▼                   │
   ┌───────────┐             │   │  ┌───────────┐       │
   │SCHWACHSTELLE│           │   │  │SCHWACHSTELLE│     │
   │   = INU    │            │   │  │   = IDN    │      │
   └───────────┘             │   │  └───────────┘       │
                             │   │                      │
                             ▼   ▼                      ▼
                       ┌─────────────┐           ┌─────────────┐
                       │  KNU < 0 ?  │           │ Alle ≥ 0 ?  │
                       └──────┬──────┘           └──────┬──────┘
                              │                         │
                    ┌───Ja────┴────Nein───┐            ▼
                    │                     │      ┌───────────┐
                    ▼                     ▼      │SCHWACHSTELLE│
              ┌───────────┐         ┌─────────┐  │= NIEDRIGSTES│
              │SCHWACHSTELLE│       │Weiter zu│  └───────────┘
              │   = KNU    │        │AWX/WAX  │
              └───────────┘         └─────────┘
```

---

## Schwachstellen-Matrix

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  INU  │  KNU  │  IDN  │  SCHWACHSTELLE     │  PRIMÄRE STRATEGIE    │
│ ──────┼───────┼───────┼────────────────────┼────────────────────── │
│   -   │   +   │   +   │  INU (individuell) │  Anreize/Kosten       │
│   +   │   -   │   +   │  KNU (sozial)      │  Normen/Institution   │
│   +   │   +   │   -   │  IDN (Identität)   │  Reframing/Narrativ   │
│   -   │   -   │   +   │  INU + KNU         │  Kombiniert           │
│   -   │   +   │   -   │  INU + IDN         │  Anreiz + Identität   │
│   +   │   -   │   -   │  KNU + IDN         │  Sozial + Identität   │
│   -   │   -   │   -   │  ALLE              │  Systemisch           │
│   +   │   +   │   +   │  AWX oder WAX      │  Awareness/Barrieren  │
│                                                                     │
│  Legende: + = positiv (≥0), - = negativ (<0)                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

# DECISION TREE 2: λ-Strategie

```
                    ┌─────────────────────┐
                    │   λ-Wert bekannt?   │
                    └──────────┬──────────┘
                               │
                  ┌─────Ja─────┴─────Nein─────┐
                  │                           │
                  ▼                           ▼
         ┌────────────────┐          ┌────────────────┐
         │  λ-Wert prüfen │          │  λ schätzen    │
         └───────┬────────┘          │  (siehe Input  │
                 │                   │   Template)    │
                 │                   └────────┬───────┘
                 │                            │
    ┌────────────┼────────────┐               │
    │            │            │               │
    ▼            ▼            ▼               │
┌───────┐   ┌────────┐   ┌────────┐          │
│λ < 0.3│   │0.3-0.7 │   │λ > 0.7 │◄─────────┘
│ LOKAL │   │ HYBRID │   │ GLOBAL │
└───┬───┘   └───┬────┘   └───┬────┘
    │           │            │
    ▼           ▼            ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│INU-FOKUS│ │KOMBINIERT│ │KNU/IDN- │
│Anreize, │ │Alle drei │ │FOKUS    │
│Kosten,  │ │Dimensionen│ │Normen,  │
│Benefits │ │adressieren│ │Identität│
└─────────┘ └─────────┘ └─────────┘
```

---

## λ-Strategie-Matrix

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   λ-BEREICH   │  ORIENTIERUNG  │  STRATEGIE                        │
│ ──────────────┼────────────────┼─────────────────────────────────── │
│               │                │                                    │
│   0.0 - 0.3   │  Individuell   │  • Finanzielle Anreize wirksam    │
│   (LOKAL)     │  Egoistisch    │  • Persönlicher Nutzen betonen    │
│               │  Kurzfristig   │  • "Was habe ICH davon?"          │
│               │                │  • Convenience maximieren         │
│               │                │                                    │
│ ──────────────┼────────────────┼─────────────────────────────────── │
│               │                │                                    │
│   0.3 - 0.7   │  Hybrid        │  • Kombination aus INU + KNU      │
│   (BALANCE)   │  Kontextabhängig│ • Sowohl Anreize als auch Normen │
│               │                │  • Identität als Verstärker       │
│               │                │  • Mehrere Hebel gleichzeitig     │
│               │                │                                    │
│ ──────────────┼────────────────┼─────────────────────────────────── │
│               │                │                                    │
│   0.7 - 1.0   │  Kollektiv     │  • Soziale Normen hocheffektiv    │
│   (GLOBAL)    │  Altruistisch  │  • Gruppenidentität aktivieren    │
│               │  Langfristig   │  • "Was ist gut für UNS?"         │
│               │                │  • Institutionelle Hebel nutzen   │
│               │                │                                    │
└─────────────────────────────────────────────────────────────────────┘
```

---

# DECISION TREE 3: AWX-Prüfung (Awareness)

```
                    ┌─────────────────────┐
                    │  AWX-Score prüfen   │
                    │  (aus Analyse)      │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        ┌──────────┐     ┌──────────┐     ┌──────────┐
        │ AWX < 3  │     │ AWX 3-7  │     │ AWX > 7  │
        │ (NIEDRIG)│     │ (MITTEL) │     │ (HOCH)   │
        └────┬─────┘     └────┬─────┘     └────┬─────┘
             │                │                │
             ▼                ▼                ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │ AWARENESS    │  │ AWARENESS    │  │ AWARENESS    │
    │ ZUERST!      │  │ VERSTÄRKEN   │  │ AUSREICHEND  │
    │              │  │              │  │              │
    │ • Information│  │ • Reminder   │  │ Weiter zu    │
    │ • Aufklärung │  │ • Feedback   │  │ WAX-Prüfung  │
    │ • Salienz    │  │ • Salienz ↑  │  │              │
    │ • Erst dann  │  │ • Parallel   │  │              │
    │   Nudge      │  │   nudgen     │  │              │
    └──────────────┘  └──────────────┘  └──────────────┘
```

---

## AWX-Interventionen

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  AWX-PROBLEM          │  INTERVENTION               │  BEISPIEL    │
│ ──────────────────────┼─────────────────────────────┼───────────── │
│                       │                             │              │
│  Wissen fehlt         │  Information                │  Kampagne,   │
│  (kognitiv)           │  Aufklärung                 │  Schulung    │
│                       │  Fakten kommunizieren       │              │
│                       │                             │              │
│ ──────────────────────┼─────────────────────────────┼───────────── │
│                       │                             │              │
│  Nicht präsent        │  Salienz erhöhen            │  Visuelle    │
│  (Aufmerksamkeit)     │  Reminder                   │  Hinweise,   │
│                       │  Trigger setzen             │  Push-Notif. │
│                       │                             │              │
│ ──────────────────────┼─────────────────────────────┼───────────── │
│                       │                             │              │
│  Abstrakt             │  Konkretisieren             │  Feedback,   │
│  (Distanz)            │  Personalisieren            │  Vergleiche, │
│                       │  Feedback geben             │  Stories     │
│                       │                             │              │
│ ──────────────────────┼─────────────────────────────┼───────────── │
│                       │                             │              │
│  Verdrängung          │  Emotionale Aktivierung     │  Storytelling│
│  (psychologisch)      │  Soziale Beweise            │  Testimonials│
│                       │                             │              │
└─────────────────────────────────────────────────────────────────────┘
```

---

# DECISION TREE 4: WAX-Prüfung (Willingness)

```
                    ┌─────────────────────┐
                    │  WAX-Score prüfen   │
                    │  (aus Analyse)      │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        ┌──────────┐     ┌──────────┐     ┌──────────┐
        │ WAX < 3  │     │ WAX 3-7  │     │ WAX > 7  │
        │ (NIEDRIG)│     │ (MITTEL) │     │ (HOCH)   │
        └────┬─────┘     └────┬─────┘     └────┬─────┘
             │                │                │
             ▼                ▼                ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │ BARRIEREN    │  │ BARRIEREN    │  │ TRIGGER      │
    │ HOCH!        │  │ SENKEN       │  │ SETZEN       │
    │              │  │              │  │              │
    │ • Vereinfachen│ │ • Defaults   │  │ • Commitment │
    │ • Defaults   │  │ • Prompts    │  │ • Reminder   │
    │ • Automatisieren│ │ • Kleine   │  │ • Soziale    │
    │ • Komplett   │  │   Schritte   │  │   Aktivierung│
    │   neu denken │  │              │  │              │
    └──────────────┘  └──────────────┘  └──────────────┘
```

---

## WAX-Interventionen

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  WAX-PROBLEM          │  INTERVENTION               │  BEISPIEL    │
│ ──────────────────────┼─────────────────────────────┼───────────── │
│                       │                             │              │
│  Zu kompliziert       │  Vereinfachen               │  One-Click,  │
│  (Komplexität)        │  Schritte reduzieren        │  Pre-filled  │
│                       │  Automatisieren             │  Forms       │
│                       │                             │              │
│ ──────────────────────┼─────────────────────────────┼───────────── │
│                       │                             │              │
│  Falscher Default     │  Default ändern             │  Opt-out     │
│  (Trägheit)           │  Vorauswahl setzen          │  statt       │
│                       │                             │  Opt-in      │
│                       │                             │              │
│ ──────────────────────┼─────────────────────────────┼───────────── │
│                       │                             │              │
│  Aufschub             │  Commitment Device          │  Pre-        │
│  (Prokrastination)    │  Deadline setzen            │  Commitment, │
│                       │  Kleine Schritte            │  Vertrag     │
│                       │                             │              │
│ ──────────────────────┼─────────────────────────────┼───────────── │
│                       │                             │              │
│  Kein Trigger         │  Trigger einbauen           │  If-Then     │
│  (Vergessen)          │  Reminder                   │  Plans,      │
│                       │  Implementation Intentions  │  Prompts     │
│                       │                             │              │
│ ──────────────────────┼─────────────────────────────┼───────────── │
│                       │                             │              │
│  Selbstzweifel        │  Selbstwirksamkeit ↑        │  Kleine      │
│  (Efficacy)           │  Erfolgserlebnisse          │  Erfolge,    │
│                       │  Rollenmodelle              │  Mentoren    │
│                       │                             │              │
└─────────────────────────────────────────────────────────────────────┘
```

---

# DECISION TREE 5: Interventions-Auswahl

## 5.1 Bei INU-Schwachstelle

```
                    ┌─────────────────────┐
                    │ SCHWACHSTELLE = INU │
                    │ (Individueller      │
                    │  Nutzen negativ)    │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │ Welche FEPSDE-      │
                    │ Dimension ist       │
                    │ das Problem?        │
                    └──────────┬──────────┘
                               │
    ┌──────┬──────┬──────┬─────┴─────┬──────┐
    │      │      │      │           │      │
    ▼      ▼      ▼      ▼           ▼      ▼
┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐
│  F   ││  E   ││  P   ││  S   ││  D   ││  E   │
│(Fin.)││(Emo.)││(Phys)││(Soc.)││(Dig.)││(Eco.)│
└──┬───┘└──┬───┘└──┬───┘└──┬───┘└──┬───┘└──┬───┘
   │       │       │       │       │       │
   ▼       ▼       ▼       ▼       ▼       ▼
┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐
│Rabatt││Spass ││Bequem││Status││App   ││Umwelt│
│Bonus ││Freude││Einfach││Anerken││Gamif.││Impact│
│Sparen││Stolz ││Gesund││nung  ││UX    ││Green │
└──────┘└──────┘└──────┘└──────┘└──────┘└──────┘
```

---

## 5.2 Bei KNU-Schwachstelle

```
                    ┌─────────────────────┐
                    │ SCHWACHSTELLE = KNU │
                    │ (Kollektiver        │
                    │  Nutzen negativ)    │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │ Welches KNU-Element │
                    │ ist das Problem?    │
                    └──────────┬──────────┘
                               │
         ┌─────────┬──────────┼──────────┬─────────┐
         │         │          │          │         │
         ▼         ▼          ▼          ▼         ▼
    ┌─────────┐┌─────────┐┌─────────┐┌─────────┐┌─────────┐
    │ Norm    ││ Norm    ││Institution││Koopera-││Destruk- │
    │ fehlt   ││ falsch  ││ schwach  ││ tion ↓ ││ tion    │
    └────┬────┘└────┬────┘└────┬────┘└────┬────┘└────┬────┘
         │         │          │          │         │
         ▼         ▼          ▼          ▼         ▼
    ┌─────────┐┌─────────┐┌─────────┐┌─────────┐┌─────────┐
    │Social   ││Norm-    ││Policy   ││Team-    ││Sanktion │
    │Proof    ││Wandel   ││Anreize  ││Building ││Trans-   │
    │sichtbar ││initiieren││Regeln   ││Koordina-││parenz   │
    │machen   ││         ││         ││tion     ││         │
    └─────────┘└─────────┘└─────────┘└─────────┘└─────────┘
```

---

## 5.3 Bei IDN-Schwachstelle

```
                    ┌─────────────────────┐
                    │ SCHWACHSTELLE = IDN │
                    │ (Identitätsnutzen   │
                    │  negativ)           │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │ Welches IDN-Element │
                    │ ist das Problem?    │
                    └──────────┬──────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
         ▼                     ▼                     ▼
    ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
    │ Identitäts-  │     │ Identitäts-  │     │ Keine        │
    │ KONFLIKT     │     │ BEDROHUNG    │     │ Identitäts-  │
    │              │     │              │     │ PASSUNG      │
    └──────┬───────┘     └──────┬───────┘     └──────┬───────┘
           │                    │                    │
           ▼                    ▼                    ▼
    ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
    │ Priorisierung│     │ Schutz &     │     │ Neue         │
    │ ermöglichen  │     │ Reframing    │     │ Identität    │
    │              │     │              │     │ aktivieren   │
    │ • Werte-     │     │ • Bedrohung  │     │              │
    │   Hierarchie │     │   entkräften │     │ • Storytelling│
    │ • Kompromiss │     │ • Alternative│     │ • Role Models│
    │   finden     │     │   Bedeutung  │     │ • "Du bist   │
    │ • Kontextuali│     │ • Sicherheit │     │   einer von" │
    │   sieren     │     │   geben      │     │              │
    └──────────────┘     └──────────────┘     └──────────────┘
```

---

# VOLLSTÄNDIGER DECISION TREE (Flowchart)

```
                                    START
                                      │
                                      ▼
                    ┌─────────────────────────────────┐
                    │         PHASE 2 ERGEBNISSE     │
                    │   INU = ___ KNU = ___ IDN = ___│
                    │   λ = ___   AWX = ___ WAX = ___│
                    └───────────────┬─────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │     Sind alle Scores ≥ 0?     │
                    └───────────────┬───────────────┘
                                    │
                  ┌────────Ja───────┴───────Nein────────┐
                  │                                     │
                  ▼                                     ▼
         ┌───────────────┐                   ┌───────────────────┐
         │ Kein Nutzen-  │                   │ SCHWACHSTELLE     │
         │ Defizit       │                   │ identifizieren    │
         │               │                   │ (niedrigster Score)│
         │ Prüfe AWX/WAX │                   └─────────┬─────────┘
         └───────┬───────┘                             │
                 │                    ┌────────────────┼────────────────┐
                 │                    │                │                │
                 │                    ▼                ▼                ▼
                 │           ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
                 │           │ INU niedrig │  │ KNU niedrig │  │ IDN niedrig │
                 │           └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
                 │                  │                │                │
                 │                  ▼                ▼                ▼
                 │           ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
                 │           │   Prüfe λ   │  │   Prüfe λ   │  │   Prüfe λ   │
                 │           └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
                 │                  │                │                │
                 │       ┌────┬────┴────┐   ┌────┬──┴───┐    ┌────┬──┴───┐
                 │       │    │         │   │    │      │    │    │      │
                 │       ▼    ▼         ▼   ▼    ▼      ▼    ▼    ▼      ▼
                 │     λ<.3 .3-.7    λ>.7 λ<.3 .3-.7 λ>.7  λ<.3 .3-.7 λ>.7
                 │       │    │         │   │    │      │    │    │      │
                 │       ▼    ▼         ▼   ▼    ▼      ▼    ▼    ▼      ▼
                 │     ┌───┐┌───┐    ┌───┐┌───┐┌───┐ ┌───┐┌───┐┌───┐ ┌───┐
                 │     │INU││INU│    │INU││KNU││KNU│ │KNU││IDN││IDN│ │IDN│
                 │     │+++││++ │    │+  ││+  ││++ │ │+++││+  ││++ │ │+++│
                 │     └─┬─┘└─┬─┘    └─┬─┘└─┬─┘└─┬─┘ └─┬─┘└─┬─┘└─┬─┘ └─┬─┘
                 │       │    │        │    │    │     │    │    │     │
                 │       └────┴────────┴────┴────┴─────┴────┴────┴─────┘
                 │                            │
                 │                            ▼
                 │              ┌───────────────────────────┐
                 │              │  INTERVENTIONS-STRATEGIE  │
                 │              │  ausgewählt               │
                 │              └─────────────┬─────────────┘
                 │                            │
                 └────────────────────────────┤
                                              │
                                              ▼
                              ┌───────────────────────────┐
                              │       AWX prüfen          │
                              │    (Awareness Score)      │
                              └─────────────┬─────────────┘
                                            │
                           ┌───────<3───────┼───────≥3────────┐
                           │                │                 │
                           ▼                │                 ▼
                  ┌─────────────────┐       │      ┌─────────────────┐
                  │ AWARENESS FIRST │       │      │   WAX prüfen    │
                  │ • Information   │       │      │ (Willingness)   │
                  │ • Salienz       │       │      └────────┬────────┘
                  │ • Dann Nudge    │       │               │
                  └────────┬────────┘       │    ┌────<3────┼────≥3────┐
                           │                │    │          │          │
                           │                │    ▼          │          ▼
                           │                │ ┌──────────┐  │    ┌──────────┐
                           │                │ │BARRIEREN │  │    │ TRIGGER  │
                           │                │ │SENKEN    │  │    │ SETZEN   │
                           │                │ │• Default │  │    │• Commit- │
                           │                │ │• Vereinf.│  │    │  ment    │
                           │                │ └────┬─────┘  │    │• Reminder│
                           │                │      │        │    └────┬─────┘
                           │                │      │        │         │
                           └────────────────┴──────┴────────┴─────────┘
                                                   │
                                                   ▼
                                    ┌───────────────────────────┐
                                    │    NUDGE AUSWÄHLEN        │
                                    │    (siehe Nudge-Katalog)  │
                                    └─────────────┬─────────────┘
                                                  │
                                                  ▼
                                               ENDE
```

---

# NUDGE-KATALOG (Quick Reference)

## Nach Schwachstelle

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  SCHWACHSTELLE  │  NUDGE-TYPEN                                     │
│ ────────────────┼───────────────────────────────────────────────── │
│                 │                                                   │
│  INU (Nutzen)   │  □ Finanzielle Anreize (Rabatt, Bonus)           │
│                 │  □ Gamification (Punkte, Badges)                 │
│                 │  □ Convenience (Vereinfachung)                   │
│                 │  □ Framing (Gain vs. Loss)                       │
│                 │  □ Immediate Rewards                             │
│                 │                                                   │
│ ────────────────┼───────────────────────────────────────────────── │
│                 │                                                   │
│  KNU (Sozial)   │  □ Social Proof ("X% tun es")                    │
│                 │  □ Descriptive Norms (was andere tun)            │
│                 │  □ Injunctive Norms (was erwartet wird)          │
│                 │  □ Public Commitment                             │
│                 │  □ Group Feedback                                │
│                 │  □ Accountability Partner                        │
│                 │                                                   │
│ ────────────────┼───────────────────────────────────────────────── │
│                 │                                                   │
│  IDN (Identität)│  □ Identity Priming ("Als [X] tust du...")       │
│                 │  □ Role Models                                   │
│                 │  □ Storytelling / Narrative                      │
│                 │  □ Self-Concept Labeling                         │
│                 │  □ Values Affirmation                            │
│                 │                                                   │
│ ────────────────┼───────────────────────────────────────────────── │
│                 │                                                   │
│  AWX (Awareness)│  □ Information                                   │
│                 │  □ Personalisiertes Feedback                     │
│                 │  □ Visuelle Salienz                              │
│                 │  □ Prompts / Reminder                            │
│                 │  □ Simplification                                │
│                 │                                                   │
│ ────────────────┼───────────────────────────────────────────────── │
│                 │                                                   │
│  WAX (Barrieren)│  □ Defaults                                      │
│                 │  □ Pre-Commitment                                │
│                 │  □ Implementation Intentions                     │
│                 │  □ Partitioning (kleine Schritte)                │
│                 │  □ Friction Reduction                            │
│                 │                                                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

# QUICK DECISION (Kurzversion)

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  1. Was ist negativ?                                               │
│     □ INU → Anreize                                                │
│     □ KNU → Normen                                                 │
│     □ IDN → Identität                                              │
│     □ Alle positiv → AWX/WAX prüfen                                │
│                                                                     │
│  2. Wie ist λ?                                                     │
│     □ < 0.3 → Fokus auf INU                                        │
│     □ 0.3-0.7 → Kombinieren                                        │
│     □ > 0.7 → Fokus auf KNU/IDN                                    │
│                                                                     │
│  3. AWX ausreichend?                                               │
│     □ < 3 → Awareness zuerst!                                      │
│     □ ≥ 3 → Weiter                                                 │
│                                                                     │
│  4. WAX ausreichend?                                               │
│     □ < 3 → Barrieren senken!                                      │
│     □ ≥ 3 → Trigger setzen                                         │
│                                                                     │
│  5. Nudge wählen (siehe Katalog oben)                              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

*BCM 2.0 Decision Tree v1.0 | FehrAdvice & Partners AG*

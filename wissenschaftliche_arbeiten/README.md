# Wissenschaftliche Arbeiten - BCM/BEATRIX

Dieser Ordner enthält die wissenschaftliche Dokumentation des Behavioral Change Model (BCM) und des BEATRIX-Systems.

## Struktur

```
wissenschaftliche_arbeiten/
├── Meta_Modul_Paper.tex          # Hauptdokument (251 KB, 4300 Zeilen)
├── kapitel/                       # Kapitelentwicklung
│   ├── 00_orientierung/          🆕 NEU - Executive Summary, Lesehinweise
│   ├── 01_einfuehrung/           ✅ Ausführlich (2089 Zeilen)
│   ├── 02_ontologie/             ⚠️ Dünn (190 Zeilen)
│   ├── 03_epistemologie/         ✅ OK (449 Zeilen)
│   ├── 04_governance/            🔴 Sehr dünn (135 Zeilen) - PRIORITÄT
│   ├── 05_dynamik/               ⚠️ Dünn (177 Zeilen)
│   ├── 06_integration/           🔴 Minimal (49 Zeilen) - PRIORITÄT
│   ├── 07_meta_beatrix/          🔴 Minimal (36 Zeilen) - Merge prüfen
│   ├── 09_transformation/        ✅ Gut (670 Zeilen)
│   └── 10_ausblick/              ✅ OK (243 Zeilen)
├── sota/                          # State-of-the-Art Analysen
│   └── SOTA_Actionable_Theories_Dietz.tex
├── standalone/                    # Eigenständige technische Dokumente
│   └── BEATRIX_Drei_Phasen_Architektur.tex
└── axiome_*_komplett.tex         # Vollständige Axiom-Dokumentation
```

## Axiom-Kategorien

| Kategorie | Datei | Axiome | Größe |
|-----------|-------|--------|-------|
| Ontologie (ONT) | `axiome_ont_komplett.tex` | 26 | 36 KB |
| Epistemologie (EPI) | `axiome_epi_komplett.tex` | 38 | 49 KB |
| Governance (GOV) | `axiome_gov_komplett.tex` | 25 | 32 KB |
| Dynamik (DYN) | `axiome_dyn_komplett.tex` | 25 | 31 KB |
| **Gesamt** | - | **115** | - |

## Entwicklungsprioritäten

1. 🔴 **Governance (GOV)** - Ethik, Regulierung, Dark Patterns
2. 🔴 **Integration** - Wie META die operativen Module constrainet
3. ⚠️ **Ontologie/Dynamik** - Mehr Tiefe bei FEPSDE, Temporal Discounting

## Workflow

1. **Entwickeln** in `kapitel/XX_name/*.tex`
2. **Review** via README.md Status
3. **Integrieren** via `\input{}` in Meta_Modul_Paper.tex

## Letzte Änderungen

- Dezember 2024: Section 9.8 (Drei-Phasen-Architektur) hinzugefügt
- Dezember 2024: Kapitelstruktur für modulare Entwicklung angelegt

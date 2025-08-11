# KldB - Klassifikation der Berufe - SKOHub TTL

Dieses Repository enthält Python-Scripts zur Generierung von SKOS-konformen TTL-Vokabularen basierend auf der **Klassifikation der Berufe (KldB) 2010, Version 2020** der Bundesagentur für Arbeit.

## 📋 Übersicht

Die Scripts konvertieren die offizielle KldB-CSV-Datei in hierarchische SKOS-Vokabulare mit vollständigen Beschreibungen und Fertigkeiten für jede Berufsklassifikation. Die generierten TTL-Dateien sind optimiert für die Verwendung mit SKOHub.

### ✨ Features

- **Vollständige Hierarchie**: Alle 5 Ebenen der KldB-Klassifikation
- **Korrekte ID-Formatierung**: Automatische Normalisierung mit führenden Nullen (z.B. `013`, `014`)
- **SKOS-konforme Labels**: `kurztitel` als `prefLabel`, `titel` als `altLabel`
- **Umfassende Metadaten**: Definitionen und Fertigkeiten aus der offiziellen Quelle
- **Robuste CSV-Verarbeitung**: Automatische Encoding-Erkennung und Fehlerbehandlung

### Verfügbare Scripts

| Script | Beschreibung | Ebenen | Ausgabe | Konzepte |
|--------|-------------|--------|---------|----------|
| `generate_kldb_4.py` | 4-Ebenen KldB Generator | 1-4 | `kldb4.ttl` | 894 |
| `generate_kldb_5.py` | Vollständiger 5-Ebenen Generator | 1-5 | `kldb5.ttl` | 2.195 |

## 🗂️ Datenquelle

**Input-Datei:** `KldB_2010,_V._2020-DE-2025-02-03-Gliederung_mit_Erläuterung.csv`

**Quelle:** [Bundesagentur für Arbeit - Klassifikation der Berufe](https://statistik.arbeitsagentur.de/DE/Navigation/Grundlagen/Klassifikationen/Klassifikation-der-Berufe/KldB2010-Fassung2020/Systematik-Verzeichnisse/Systematik-Verzeichnisse-Nav.html)

### CSV-Struktur
- **Spalte 0:** Schlüssel KldB 2010 (ID)
- **Spalte 1:** Ebene (1-5)
- **Spalte 2:** Titel (Vollständiger Name) → `skos:altLabel`
- **Spalte 3:** Kurztitel (Abgekürzter Name) → `skos:prefLabel`
- **Spalte 4:** Allgemeine Bemerkungen → `skos:definition`
- **Spalte 5:** Einschlüsse → `skos:note` (Fertigkeiten/Aktivitäten)
- **Spalte 6:** Umfasst ferner
- **Spalte 7:** Ausschlüsse

## 📝 Changelog

### Version 2025-08-11
- ✅ **Behoben**: Fehlende militärische Einträge (013, 014) durch ID-Normalisierung
- ✅ **Behoben**: Vertauschte `prefLabel`/`altLabel` Zuordnung
- ✅ **Verbessert**: Robuste CSV-Verarbeitung mit automatischer Encoding-Erkennung
- ✅ **Hinzugefügt**: Vollständige 5-Ebenen-Unterstützung
- ✅ **Optimiert**: Hierarchie-Aufbau und Parent-Child-Beziehungen

## 🎯 Verwendung mit SKOHub

Die generierten TTL-Dateien sind optimiert für die Verwendung mit [SKOHub](https://skohub.io/) und folgen den SKOS-Standards für kontrollierte Vokabulare.

### TTL-Header Beispiel
```turtle
@base <http://w3id.org/openeduhub/vocabs/kldb/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<> a skos:ConceptScheme ;
    dct:title "Klassifikation der Berufe - KldB 4-stellig (vollständig)"@de ;
    dct:description "Vollständige hierarchische KldB mit allen 4 Ebenen und Kurzbeschreibungen aus KldB 2010 V. 2020"@de ;
    dct:created "2025-08-11"^^xsd:date ;
    skos:hasTopConcept <0>, <1>, <2>, <3>, <4>, <5>, <6>, <7>, <8>, <9> .
```

## 🚀 Verwendung

### Voraussetzungen

```bash
pip install pandas
```

### Installation

1. Repository klonen oder CSV-Datei und Scripts herunterladen
2. CSV-Datei `KldB_2010,_V._2020-DE-2025-02-03-Gliederung_mit_Erläuterung.csv` im gleichen Verzeichnis platzieren
3. Script ausführen

### 4-Ebenen KldB generieren

```bash
python generate_kldb_4.py
```

**Ausgabe:** `kldb4.ttl` (894 Konzepte bis 4-stellige Codes)

### 5-Ebenen KldB generieren (Vollständig)

```bash
python generate_kldb_5.py
```

**Ausgabe:** `kldb5.ttl` (2.195 Konzepte mit allen 5 Ebenen)

## 📊 Generierte Statistiken

### KldB 4-Ebenen (`kldb4.ttl`)
- **Ebene 1**: 10 Konzepte (Berufshauptgruppen)
- **Ebene 2**: 37 Konzepte (Berufsbereiche) 
- **Ebene 3**: 144 Konzepte (Berufsgruppen)
- **Ebene 4**: 703 Konzepte (Berufsuntergruppen)
- **Gesamt**: 894 Konzepte

### KldB 5-Ebenen (`kldb5.ttl`)
- **Ebene 1**: 10 Konzepte (Berufshauptgruppen)
- **Ebene 2**: 37 Konzepte (Berufsbereiche)
- **Ebene 3**: 144 Konzepte (Berufsgruppen) 
- **Ebene 4**: 703 Konzepte (Berufsuntergruppen)
- **Ebene 5**: 1.301 Konzepte (Berufsgattungen)
- **Gesamt**: 2.195 Konzepte

## 🔧 Technische Details

### ID-Normalisierung
Die Scripts korrigieren automatisch Formatierungsfehler in der CSV-Datei:
- Militärische Einträge: `13` → `013`, `14` → `014`
- Hierarchiekonsistenz: IDs werden mit führenden Nullen entsprechend ihrer Ebene formatiert

### SKOS-Mapping
- **`skos:prefLabel`**: Kurztitel (bevorzugtes, kürzeres Label)
- **`skos:altLabel`**: Titel (alternatives, längeres Label)
- **`skos:definition`**: Allgemeine Bemerkungen
- **`skos:note`**: Einschlüsse (Fertigkeiten/Aktivitäten)
- **`skos:broader`**: Übergeordnete Konzepte
- **`skos:narrower`**: Untergeordnete Konzepte

### Beispiel-Hierarchie
```
0 - Militär
├── 01 - Angehörige der regulären Streitkräfte
    ├── 011 - Offiziere
    ├── 012 - Unteroffiziere mit Portepee
    ├── 013 - Unteroffiziere ohne Portepee
    └── 014 - Angehörige der regulären Streitkräfte in sonstigen Rängen
```


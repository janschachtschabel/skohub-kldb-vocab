# KldB- Klassifikation der Berufe - SkoHub TTL

Dieses Repository enthält Python-Scripts zur Generierung von SKOS-konformen TTL-Vokabularen basierend auf der **Klassifikation der Berufe (KldB) 2010, Version 2020** der Bundesagentur für Arbeit.

## 📋 Übersicht

Die Scripts konvertieren die offizielle KldB-CSV-Datei des Klassifikationsserver.de in hierarchische SKOS-Vokabulare mit Kurzbeschreibungen und Fertigkeiten für jede Berufsklassifikation.

### Verfügbare Scripts

| Script | Beschreibung | Ebenen | Ausgabe | Konzepte |
|--------|-------------|--------|---------|----------|
| `generate_kldb_4.py` | 4-Ebenen KldB Generator | 1-4 | `kldb-4.ttl` | 891 |
| `generate_kldb_5.py` | Vollständiger 5-Ebenen Generator | 1-5 | `kldb-5.ttl` | 2.192 |

## 🗂️ Datenquelle

**Input-Datei:** `KldB_2010,_V._2020-DE-2025-02-03-Gliederung_mit_Erläuterung.csv`

**Quelle:** [Bundesagentur für Arbeit - Klassifikation der Berufe](https://statistik.arbeitsagentur.de/DE/Navigation/Grundlagen/Klassifikationen/Klassifikation-der-Berufe/KldB2010-Fassung2020/Systematik-Verzeichnisse/Systematik-Verzeichnisse-Nav.html)

### CSV-Struktur
- **Spalte 0:** Schlüssel KldB 2010 (ID)
- **Spalte 1:** Ebene (1-5)
- **Spalte 2:** Titel (Vollständiger Name)
- **Spalte 3:** Kurztitel (Abgekürzter Name)
- **Spalte 4:** Allgemeine Bemerkungen → `skos:definition`
- **Spalte 5:** Einschlüsse → `skos:note` (Fertigkeiten/Aktivitäten)
- **Spalte 6:** Umfasst ferner
- **Spalte 7:** Ausschlüsse

## 🚀 Verwendung

### Voraussetzungen

```bash
pip install pandas
```

### 4-Ebenen KldB generieren

```bash
python generate_kldb_4.py
```

**Ausgabe:** `kldb-4.ttl` (891 Konzepte bis 4-stellige Codes)


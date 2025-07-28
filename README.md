# \# SKOS-Klassifikation der Berufe (KldB 2020)

# 

# Dieses Repository enthält maschinenlesbare SKOS-Vokabulare für die \*\*Klassifikation der Berufe (KldB 2010, Version 2020)\*\* im \*\*Turtle-Format (`.ttl`)\*\*, basierend auf der amtlichen Klassifikation der Bundesagentur für Arbeit.

# 

# \## Dateien

# 

# | Datei                  | Beschreibung |

# |------------------------|--------------|

# | `kldb\_ebene\_4.ttl`     | Enthält die KldB-Struktur bis Ebene 4 (Berufsuntergruppen) |

# | `kldb\_ebene\_5.ttl`     | Enthält die vollständige KldB-Struktur bis Ebene 5 (Berufsgattungen) |

# | `kldb\_ebene\_4\_cleaned.ttl` | Bereinigte, validierte Version mit Duplikat-Entfernung (z. B. bei `altLabel`) |

# | `kldb\_ebene\_5\_cleaned.ttl` | Siehe oben, für die 5-stufige Struktur |

# 

# \## Struktur und Anreicherung

# 

# \- \*\*SKOS-Format\*\*: Die Vokabulare sind mit \[SKOS](https://www.w3.org/TR/skos-reference/) modelliert.

# \- \*\*Ebenenstruktur\*\*:

# &nbsp; - Ebene 1: Berufsbereiche

# &nbsp; - Ebene 2: Berufssegmente

# &nbsp; - Ebene 3: Berufsgruppen

# &nbsp; - Ebene 4: Berufsuntergruppen

# &nbsp; - Ebene 5: Berufsgattungen (optional, je nach Datei)

# \- \*\*Felder\*\*:

# &nbsp; - `skos:prefLabel`: Standardbezeichnung des Berufs

# &nbsp; - `skos:altLabel`: alternative Bezeichnungen

# &nbsp; - `skos:notation`: KldB-Code

# &nbsp; - `skos:definition`: Kurzbeschreibung (aus dem Klassifikationsserver, Version 2020)

# &nbsp; - `skos:note`: Typische Tätigkeiten (aus dem Klassifikationsserver)

# 

# \## Validierung und Bereinigung

# 

# Die `\*\_cleaned.ttl`-Dateien wurden mit dem \[ttl-cleaner](https://github.com/skohub-io/ttl-cleaner) geprüft und bereinigt:

# 

# \- Entfernt doppelte `altLabel`-Einträge

# \- Validiert gegen SKOS-Spezifikationen

# \- Konsistente URIs und Formatierung

# 

# \## Lizenz

# 

# Die Inhalte basieren auf der Klassifikation der Bundesagentur für Arbeit (KldB 2010, Version 2020) und sind öffentlich zugänglich. Die SKOS-Transformation unterliegt der \[MIT-Lizenz](./LICENSE).

# 

# ---

# 

# > Erstellt für SKOHUB-Vokabulardienste, maschinelles Matching und semantische Anreicherung von Bildungsdaten.


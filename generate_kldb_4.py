#!/usr/bin/env python3
"""
KldB-4-neu TTL Generator Script

Dieses Script erstellt eine hierarchische KldB-4-neu.ttl bis Ebene 4 (4-stellige Codes)
mit der Struktur ähnlich kldb.ttl, aber angereichert mit:
- Spalte 4 (Allgemeine Bemerkungen) → skos:definition
- Spalte 5 (Einschlüsse) → skos:note (für Fertigkeiten/Aktivitäten)

Basiert auf: KldB_2010,_V._2020-DE-2025-02-03-Gliederung_mit_Erläuterung.csv

Usage: python generate_kldb_4_neu.py
"""

import pandas as pd
import re
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional, Set
from datetime import datetime

# Windows Console UTF-8 Fix
if os.name == 'nt':
    os.system('chcp 65001 > nul')


class KldB4NeuGenerator:
    def __init__(self):
        self.csv_data = None
        self.concepts = {}  # Dict[str, Dict] - speichert alle Konzepte
        self.hierarchy = {}  # Dict[str, List[str]] - parent -> children mapping
        self.generated_concepts = 0
        
    def load_csv_data(self, csv_file: str) -> bool:
        """Lade CSV-Daten mit robuster Encoding-Erkennung"""
        print(f"[INFO] Lade CSV-Datei: {csv_file}")
        
        # Verschiedene Encodings und Separatoren probieren
        encodings = ['utf-8', 'utf-8-sig', 'cp1252', 'latin1', 'iso-8859-1']
        separators = [';', ',', '\t']
        
        for encoding in encodings:
            for sep in separators:
                try:
                    df = pd.read_csv(
                        csv_file, 
                        encoding=encoding, 
                        sep=sep,
                        dtype=str,  # Alles als String lesen
                        na_filter=False  # Keine NaN-Konvertierung
                    )
                    
                    # Prüfe ob die erwarteten Spalten vorhanden sind
                    if len(df.columns) >= 8:
                        print(f"[SUCCESS] CSV erfolgreich geladen mit {encoding} und Separator '{sep}'")
                        print(f"[INFO] {len(df)} Zeilen, {len(df.columns)} Spalten")
                        print(f"[INFO] Spalten: {list(df.columns)}")
                        
                        # Spalten umbenennen für einfachere Handhabung - handle BOM
                        new_columns = ['kldb_id', 'ebene', 'titel', 'kurztitel', 
                                     'allgemeine_bemerkungen', 'einschluesse', 
                                     'umfasst_ferner', 'ausschluesse']
                        
                        # Füge zusätzliche Spalten hinzu falls vorhanden
                        while len(new_columns) < len(df.columns):
                            new_columns.append(f'extra_{len(new_columns)}')
                        
                        df.columns = new_columns[:len(df.columns)]
                        
                        self.csv_data = df
                        return True
                        
                except Exception as e:
                    continue
        
        print(f"[ERROR] Konnte CSV-Datei nicht laden: {csv_file}")
        return False
    
    def clean_text(self, text: str) -> str:
        """Bereinige Text für TTL-Ausgabe"""
        if not text or text.strip() == '':
            return ""
        
        # HTML-Entities ersetzen
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        
        # Mehrfache Leerzeichen reduzieren
        text = re.sub(r'\s+', ' ', text)
        
        # Anführungszeichen escapen
        text = text.replace('"', '\\"')
        text = text.replace('\\', '\\\\')
        
        return text.strip()
    
    def parse_csv_data(self) -> bool:
        """Parse CSV-Daten und baue Hierarchie auf"""
        if self.csv_data is None:
            print("[ERROR] Keine CSV-Daten geladen")
            return False
        
        print("[INFO] Parse CSV-Daten und baue Hierarchie...")
        
        # Filtere nur Ebenen 1-4 (bis 4-stellige Codes)
        filtered_data = self.csv_data[
            (self.csv_data['ebene'].astype(int) >= 1) & 
            (self.csv_data['ebene'].astype(int) <= 4)
        ].copy()
        
        print(f"[INFO] Gefilterte Daten: {len(filtered_data)} Einträge (Ebenen 1-4)")
        
        # Sortiere nach KldB-ID für korrekte Hierarchie-Aufbau
        filtered_data = filtered_data.sort_values('kldb_id')
        
        # Baue Konzepte auf
        for _, row in filtered_data.iterrows():
            kldb_id = str(row['kldb_id']).strip()
            ebene = int(row['ebene'])
            titel = self.clean_text(row['titel'])
            kurztitel = self.clean_text(row['kurztitel'])
            allgemeine_bemerkungen = self.clean_text(row['allgemeine_bemerkungen'])
            einschluesse = self.clean_text(row['einschluesse'])
            
            # Überspringe leere IDs
            if not kldb_id or kldb_id == '':
                continue
            
            # Erstelle Konzept
            concept = {
                'id': kldb_id,
                'ebene': ebene,
                'titel': titel,
                'kurztitel': kurztitel,
                'definition': allgemeine_bemerkungen,
                'note': einschluesse,
                'children': [],
                'parent': None
            }
            
            self.concepts[kldb_id] = concept
            
            # Bestimme Parent basierend auf ID-Länge
            if ebene > 1:
                parent_id = self.get_parent_id(kldb_id, ebene)
                if parent_id and parent_id in self.concepts:
                    concept['parent'] = parent_id
                    self.concepts[parent_id]['children'].append(kldb_id)
                    
                    # Füge zu Hierarchie-Mapping hinzu
                    if parent_id not in self.hierarchy:
                        self.hierarchy[parent_id] = []
                    self.hierarchy[parent_id].append(kldb_id)
        
        print(f"[INFO] {len(self.concepts)} Konzepte erstellt")
        print(f"[INFO] Hierarchie-Beziehungen: {sum(len(children) for children in self.hierarchy.values())}")
        
        return True
    
    def get_parent_id(self, kldb_id: str, ebene: int) -> Optional[str]:
        """Bestimme Parent-ID basierend auf KldB-Hierarchie"""
        if ebene <= 1:
            return None
        
        # Ebene 2: Parent ist 1-stellig (z.B. 11 -> 1)
        if ebene == 2 and len(kldb_id) >= 2:
            return kldb_id[0]
        
        # Ebene 3: Parent ist 2-stellig (z.B. 111 -> 11)
        elif ebene == 3 and len(kldb_id) >= 3:
            return kldb_id[:2]
        
        # Ebene 4: Parent ist 3-stellig (z.B. 1110 -> 111)
        elif ebene == 4 and len(kldb_id) >= 4:
            return kldb_id[:3]
        
        return None
    
    def get_top_concepts(self) -> List[str]:
        """Ermittle Top-Level-Konzepte (Ebene 1)"""
        top_concepts = []
        for concept_id, concept in self.concepts.items():
            if concept['ebene'] == 1:
                top_concepts.append(concept_id)
        
        return sorted(top_concepts)
    
    def generate_ttl_header(self) -> str:
        """Generiere TTL-Header"""
        today = datetime.now().strftime("%Y-%m-%d")
        top_concepts = self.get_top_concepts()
        top_concept_refs = ", ".join([f"<{cid}>" for cid in top_concepts])
        
        header = f"""@base <http://w3id.org/openeduhub/vocabs/kldb/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<> a skos:ConceptScheme ;
\tdct:title "Klassifikation der Berufe - KldB 4-stellig (neu)"@de ;
\tdct:description "Hierarchische KldB bis Ebene 4 mit Kurzbeschreibungen und Fertigkeiten aus KldB 2010 V. 2020"@de ;
\tdct:created "{today}"^^xsd:date ;
\tskos:hasTopConcept {top_concept_refs} .

"""
        return header
    
    def generate_concept_ttl(self, concept_id: str) -> str:
        """Generiere TTL für ein einzelnes Konzept"""
        concept = self.concepts[concept_id]
        
        ttl_lines = [f"<{concept_id}> a skos:Concept ;"]
        
        # Titel (prefLabel)
        if concept['titel']:
            ttl_lines.append(f'\tskos:prefLabel "{concept["titel"]}"@de ;')
        
        # Kurztitel (altLabel) - nur wenn unterschiedlich vom Titel
        if concept['kurztitel'] and concept['kurztitel'] != concept['titel']:
            ttl_lines.append(f'\tskos:altLabel "{concept["kurztitel"]}"@de ;')
        
        # Definition (aus Allgemeine Bemerkungen)
        if concept['definition']:
            ttl_lines.append(f'\tskos:definition "{concept["definition"]}"@de ;')
        
        # Note (aus Einschlüsse - Fertigkeiten)
        if concept['note']:
            ttl_lines.append(f'\tskos:note "{concept["note"]}"@de ;')
        
        # Hierarchie-Beziehungen
        if concept['parent']:
            ttl_lines.append(f'\tskos:broader <{concept["parent"]}> ;')
        
        if concept['children']:
            children_refs = ", ".join([f"<{child}>" for child in sorted(concept['children'])])
            ttl_lines.append(f'\tskos:narrower {children_refs} ;')
        
        # Schema-Zugehörigkeit
        if concept['ebene'] == 1:
            ttl_lines.append('\tskos:topConceptOf <> .')
        else:
            ttl_lines.append('\tskos:inScheme <> .')
        
        # Letztes Semikolon durch Punkt ersetzen
        if ttl_lines[-1].endswith(' ;'):
            ttl_lines[-1] = ttl_lines[-1][:-2] + ' .'
        
        return '\n'.join(ttl_lines) + '\n'
    
    def generate_ttl(self, output_file: str) -> bool:
        """Generiere vollständige TTL-Datei"""
        print(f"[INFO] Generiere TTL-Datei: {output_file}")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                # Header schreiben
                f.write(self.generate_ttl_header())
                
                # Konzepte nach Ebene sortiert schreiben
                for ebene in range(1, 5):  # Ebenen 1-4
                    concepts_at_level = [
                        (cid, concept) for cid, concept in self.concepts.items() 
                        if concept['ebene'] == ebene
                    ]
                    
                    if concepts_at_level:
                        f.write(f"\n# Ebene {ebene}\n")
                        
                        # Sortiere nach ID
                        concepts_at_level.sort(key=lambda x: x[0])
                        
                        for concept_id, concept in concepts_at_level:
                            f.write(self.generate_concept_ttl(concept_id))
                            f.write('\n')
                            self.generated_concepts += 1
            
            print(f"[SUCCESS] TTL-Datei erstellt: {output_file}")
            print(f"[INFO] {self.generated_concepts} Konzepte generiert")
            return True
            
        except Exception as e:
            print(f"[ERROR] Fehler beim Schreiben der TTL-Datei: {e}")
            return False
    
    def print_statistics(self):
        """Drucke Statistiken"""
        print("\n" + "="*60)
        print("STATISTIKEN")
        print("="*60)
        
        # Konzepte pro Ebene
        for ebene in range(1, 5):
            count = len([c for c in self.concepts.values() if c['ebene'] == ebene])
            print(f"Ebene {ebene}: {count} Konzepte")
        
        # Konzepte mit Definition/Note
        with_definition = len([c for c in self.concepts.values() if c['definition']])
        with_note = len([c for c in self.concepts.values() if c['note']])
        
        print(f"\nKonzepte mit Definition: {with_definition}")
        print(f"Konzepte mit Note (Fertigkeiten): {with_note}")
        print(f"Gesamt generierte Konzepte: {self.generated_concepts}")
        
        # Top-Level Konzepte
        top_concepts = self.get_top_concepts()
        print(f"\nTop-Level Konzepte ({len(top_concepts)}):")
        for concept_id in top_concepts:
            concept = self.concepts[concept_id]
            print(f"  {concept_id}: {concept['titel']}")


def main() -> bool:
    """Hauptfunktion"""
    print("KldB-4-neu TTL Generator")
    print("="*50)
    
    # Dateipfade
    csv_file = "KldB_2010,_V._2020-DE-2025-02-03-Gliederung_mit_Erläuterung.csv"
    output_file = "kldb-4-neu.ttl"
    
    # Prüfe ob CSV-Datei existiert
    if not Path(csv_file).exists():
        print(f"[ERROR] CSV-Datei nicht gefunden: {csv_file}")
        return False
    
    # Generator initialisieren
    generator = KldB4NeuGenerator()
    
    # CSV-Daten laden
    if not generator.load_csv_data(csv_file):
        return False
    
    # CSV-Daten parsen und Hierarchie aufbauen
    if not generator.parse_csv_data():
        return False
    
    # TTL generieren
    if not generator.generate_ttl(output_file):
        return False
    
    # Statistiken ausgeben
    generator.print_statistics()
    
    print(f"\n[SUCCESS] KldB-4-neu.ttl erfolgreich erstellt!")
    print(f"[INFO] Ausgabedatei: {output_file}")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

\# SKOS-Vokabulare: Klassifikation der Berufe (KldB 2010, Version 2020)



Dieses Repository enthält Turtle-Dateien (`.ttl`) mit SKOS-Vokabularen auf Basis der überarbeiteten KldB-Version 2020.



\## Dateien



\- `kldb\_ebene\_4.ttl` – KldB bis Ebene 4 (Berufsuntergruppen)  

\- `kldb\_ebene\_5.ttl` – KldB bis Ebene 5 (Berufsgattungen)  

\- `kldb\_ebene\_4\_cleaned.ttl` / `kldb\_ebene\_5\_cleaned.ttl` – Bereinigt und validiert mit `ttl-cleaner`:  

&nbsp; - doppelte `altLabel` entfernt  

&nbsp; - einheitlich formatiert  

&nbsp; - SKOS-konform  



\## Struktur und Anreicherung



\- `skos:prefLabel` – Bezeichnung  

\- `skos:altLabel` – alternative Bezeichnungen  

\- `skos:notation` – KldB-Code  

\- `skos:definition` – Kurzbeschreibungen aus dem Klassifikationsserver (2020)  

\- `skos:note` – Typische Tätigkeiten  



\## Nutzung



Einsatz z. B. mit:

\- \[skohub.io](https://skohub.io/)

\- semantische Suche

\- Matching-Dienste für Bildungs- und Berufsdaten


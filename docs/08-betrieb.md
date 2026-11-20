# Betrieb, Archiv und Sicherung

## Drei verschiedene Datensicherungen

1. HA-Recorder für laufende Zustände/Statistik. Tatsächliche Aufbewahrungszeit prüfen; rohe Detailhistorie ist nicht automatisch dauerhaft.
2. Messdatenarchiv für spätere Auswertungen. Export enthält Zeitstempel, Zeitzone, Einheit, Quellrolle, Zustand und Qualitätsnachweise. Langzeitstunden allein erlauben keine spätere sekundengenaue Rekonstruktion.
3. Vollständiges HA-Backup mit Konfiguration, benötigten Daten und Wiederherstellungsinformationen. Ein Messdatenexport ersetzt kein HA-Backup, ein Backup ist keine bequem auswertbare Zeitreihendatenbank.

## NAS energiearm nutzen

Lokal erfassen und zwischenpuffern; fertige Blöcke während eines ausdrücklich festgelegten NAS-Fensters übertragen. Hardwareanfahrt berücksichtigen, Übertragung rechtzeitig vor Abschalten beenden. Kein dauernder Erreichbarkeitstest und kein zusätzlicher Scan des schlafenden NAS alle Minuten.

Wiederholungen begrenzen: maximale Versuche, Abstand, Ende des Zeitfensters, persistenter Tageszähler und Sperre gegen Parallelität. Nach Neustart offene Arbeit prüfen; bereits bestätigte Dateien nicht neu übertragen. Gegenseitige Sperre zu laufendem Vollbackup, wo nötig. Retention des lokalen Puffers größer als tolerierter Sicherungsausfall auslegen.

## Integrität und Warnung

Auf dem NAS Datei vollständig zurücklesen und Hash mit lokalem Original vergleichen. Für Vollbackup zusätzlich Typ/Inhaltsverzeichnis, erwartete Bestandteile und Verschlüsselungsmetadaten prüfen. Transporterfolg ist noch kein Restaurierbarkeitstest. Schlüssel niemals ins Repository oder neben frei zugängliche Sicherungen kopieren.

Überfälligkeit aus erwarteten Fälligkeiten berechnen, nicht nur aus einem bereits gestarteten Job. Verpasste wöchentliche Vollsicherung innerhalb des nächsten zulässigen Fensters nachholen. Warnung bei ausbleibendem Erfolg, Warnung für knappen lokalen Speicher, Entwarnung erst nach bestätigtem Nachholen. Fehlgeschlagene Pushziele gezielt wiederholen; erfolgreiche nicht ständig erneut benachrichtigen. Ruhezeiten getrennt für nichtkritische Sicherungshinweise festlegen, Sicherheitsalarme nicht pauschal stummschalten.

Kritisch wird ein Rückstand, wenn nicht archivierte Detaildaten vor dem Recorder-/Pufferablauf stehen oder lokaler freier Speicher nicht reicht. Das tatsächliche Zeitbudget aus Aufbewahrung, Rückstand und Tageswachstum berechnen, keine universelle Zahl versprechen.

## Anlagenzustand

Eine lesende Übersicht bündelt letzte gültige Quellenmeldungen, gemeinsame Tagesdaten, fehlende Tage, Journalstatus, Archiv-/Backup-Erfolgszeit und freien Speicher. Unbekannt ist neutral, bestätigter Fehler auffällig, Erfolg braucht Beleg. Keine zusätzliche Steuerung daraus ableiten. Nach Änderungen gezielte Prüffälle ausführen; keine regelmäßigen Reparaturen ohne Fehlernachweis.


## Minutenhistorie, SSD und Ersatzsystem

Der [erweiterte Betriebsentwurf](12-minutenhistorie-und-betrieb.md) beschreibt die Trennung schneller Liveeingänge und Minutenhistorien, gebündelte Statistikimporte, Schreiblastmessung, eine unterstützte SSD-Datenlaufwerk-Verschiebung sowie zweite Backupkopie und isoliertes Ersatzgerät. Netzwerkfehler während der Diagnose nicht durch automatische Konfigurationsänderungen verdecken.

API- und Modellarchive getrennt von der Rohhistorie sichern. Der [CO₂-Stunden-Cache](13-co2-stunden-und-speicher.md) muss nach Recorder-Ablauf frühere Bewertungen weiter ermöglichen; der [Prognosevergleich](14-openmeteo-vergleich.md) benötigt die ursprünglichen datierten Snapshots. Ein Vollbackup allein ist kein Ersatz für eine nachvollziehbare, versionierte Zeitreihenbasis.


## Optionaler Netzwiederanlauf

Die [verzögerte Nachladung](15-netzausfall-und-wiederanlauf.md) ergänzt ausschließlich gesondert freigegebene Programm-SoC-Schreibrollen. Phase, temporäres Ziel, Rückkehrbeginn und Warteparameter persistent sichern. Parameter neben der Saisonreserve editierbar; Änderung während des Ausfalls ist möglich, spätere Frist läuft ab Netzrückkehr. Bei Änderung während der Wartezeit kann eine verkürzte Frist bereits abgelaufen sein.

Bei HA-/Kommunikationsausfall bleiben geschriebene Werte möglicherweise länger bestehen. Hauptschalter aus lässt manuelle Werte unangetastet und ist kein stilles Zurücksetzen. Rückbau deshalb mit aktuellem Anlagenzustand und gesicherter Originalfassung planen. Den nächsten tatsächlichen Ausfall und Wiederanlauf zur Abnahme beobachten, ohne dafür eine gefährliche Unterbrechung auszulösen. Anzeige eines passenden Ziels allein beweist keinen vermiedenen Ladestart.

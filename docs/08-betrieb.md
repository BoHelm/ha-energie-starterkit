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

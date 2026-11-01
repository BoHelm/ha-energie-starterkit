# Abnahme einer individuell erzeugten HA-Umsetzung

Diese Liste testet die spätere Implementierung. Die Repository-Tests bestätigen nur das Starterkit.

## A. Bestandsaufnahme und Sicherung

- Tatsächliche Entitäts-IDs, Messgrenzen, Einheiten, Vorzeichen, Quellenalter und Resettypen dokumentiert.
- HA-Backup vorhanden, privat rückgelesen und Wiederherstellungsweg bekannt. Geänderte Dateien separat gesichert.
- Vorhandene Geräte-/Schutzparameter und Zeitfenster vor/nach identisch, soweit keine konkrete Änderung beauftragt.
- Schreib- und Benachrichtigungsaktionen standardmäßig aus; keine Handymeldungen ohne bewusst gewähltes Ziel.

## B. Rechenfälle mit synthetischen Daten

| Fall | Erwartung |
| --- | --- |
| Drei disjunkte PV-Zähler2/3/5kWh |10kWh brutto, keine zusätzliche Summenquelle |
|10kWh brutto, f0,90, Preis0,30EUR |9kWh bewertet und2,70EUR; Diagramm weiterhin10kWh |
| Fehlende PV-Quelle am Tag | Keine aktuelle Gesamtrate, außer ausdrücklich belegtem Ersatz |
| Echte0W trotz anderer Quelle |0 bleibt0, kein Ersatz nur wegen Null |
| F10kWh, E12kWh | Tagesabweichung+20% |
| F10/E8 und F10/E12 | Vorzeichenmittel0%, absoluter Tagesfehler20% |
| Prognose0 oder fehlt | Kein Prozentwert, keine Division durch0 |
|19-Uhr-Snapshot fehlt | Keine rückwirkend als Original bezeichnete aktuelle Prognose |
| Zähler100→112 mit interner Pause |12kWh möglich bei belegten gemeinsamen Grenzen |
| Ein Rand fehlt / Reset ungeklärt | Keine vollständige Tagesenergie |
| Innen1/Außen9kWh | Gesamt10, Innen separat1; nicht11 |
| Hersteller90/Shelly100kWh |−10% |
| Temperatur10°C für1h,20°C für3h |17,5°C Zeitmittel |
| Wetter nur12von24h | Teilmittel mit50% Abdeckung; keine vollständige Tagesaussage |
| Fehlendes Wetterintervall | Unterbrochene Kurve, keine Null und keine Überbrückung |
| MindestSoC20, SoC20 | Pfeil unten, Zahl20%; keine Geräteeinstellung geändert |
| Entladung100kWh, Referenz10kWh |10äquivalente Zyklen, Ladung nicht zusätzlich |
| Jahresbasis fehlt | Jahresbezug/Autarkie unbekannt, keine heutige Ersatzbasis |

Zusätzlich: negative Temperatur, NaN/Infinity, Einheitenwechsel, versteckter Faktor10, ungültige negative Verbrauchsleistung, zukünftiger Zeitstempel, restaurierte Werte, unpassendes Ziel-/Buchungsdatum.

## C. Zeit, Historie und Datenqualität

Lokale23-/25-Stunden-Tage und Jahreswechsel prüfen, kein festes24h-Millisekundenraster für Kalendertage. Startteilmonat ausgeschlossen, historische Daten nicht vor Qualitätsbeginn als nachgewiesen ausgeben. Offline-Gerät, HA-Neustart und verpasster Schedulerlauf simulieren. Keine echten gefährlichen Geräteausfälle zum Test auslösen.

Journalzweitausführung unverändert; persistente Basen/Flags nach Neustart erhalten. Rückwirkender Modellfaktor ändert Ableitung, nicht Rohenergie und nicht Anzahl Buchungen. Alle Komponenten im Anteilvergleich identischer Zeitraum. Negative Einsparungen nicht in irreführende positive Tortenanteile umrechnen.

## D. Darstellung und Export

Gespeicherte Dateien zurücklesen und vergleichen. Normales Dashboard vollständig neu laden; Karte lädt Daten statt nur ihre Überschrift. Mobil einspaltig, Tablet quer, helle/dunkle Eingaben und Lesbarkeit prüfen. Während Aktualisierung scrollen: kein Rücksprung, Fokus und offene Liste bleiben. Alle ursprünglichen Karten außerhalb der Aufgabe erhalten.

Excel auf echten unterstützten Zielgeräten herunterladen und wieder öffnen: Datum und Messwerte numerisch, fehlende Werte leer, echteNull numerisch0,365/366Kalendertage, Zeitumstellung korrekt, Teilwerte/Qualität/Einheiten erklärt. Diagramm und Excel desselben Tages gegen dieselbe deklarierte Datenbasis abgleichen. Ein erzeugter Downloadlink ist noch kein erfolgreich zurückgelesener Download.

## E. Archiv, Vollbackup, Warnung

NAS aus→lokale Erfassung läuft; innerhalb Zeitfenster begrenztes Nachholen; außerhalb kein unnötiges Aufwecken. Fehlschlagwarnung einmal, Erfolg erst nach Rücklesen und danach Entwarnung. Keine Warnflut durch unnötige Automationsstarts. Vorhandener vollständiger Backupinhalt, Verschlüsselung und privat vorhandener Schlüssel belegt. Vollständiger Wiederherstellungstest möglichst auf separatem Testsystem, nicht über das bewohnte Produktivsystem.

## F. Optional freigegebene WP-Offsetsteuerung

[Zeit- und Ausfallfälle](11-wp-offsetsteuerung.md) einschließlich Basis−1K→tagsüber+1K/sonst−1K, sicherer Erstinitialisierung, Ausschalten mit Rücknahme, gleicher Sollwert ohne erneuten Befehl, fehlender/restaurierter/veralteter Quelle und Bereichsverletzung prüfen. Keine Betriebsart-/Warmwasser-/Schutzänderung. Verpasste Rücknahme und HA-Neustart mit erhaltenen Helfern nachholen; Cloudfehler begrenzt behandeln. HA-Sollwertrückmeldung nicht allein als physische Gerätebestätigung werten. Nicht tatsächlich beobachtete Fälle offen kennzeichnen.

Pro Test Ergebnis, Version und Prüfgrenze lokal festhalten. „Noch nicht geprüft“ ist ein zulässiger Status; kein grünes Häkchen ohne Nachweis.

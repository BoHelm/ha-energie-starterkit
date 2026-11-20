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


## G. Minutenhistorie, informative Tageswerte und neue Modelle

- Originaleingänge, Schutztrigger und Integratoren unverändert; abgeschlossene Minuten zeitgewichtet mit Min/Max und Abdeckung. Stichprobe darf nicht als Mittelwert bestehen. Alte/neue Historie am Umschaltzeitpunkt ohne Überlappung; spätere Quellgruppe verschiebt keinen alten Wechsel.
- Gemeinsame Ladebedingungen aus schnellen zeitgleichen Quellen prüfen. Keine erfundene Gleichzeitigkeit aus getrennten Minutenmitteln. Spannungs-/Stromhistorien behalten V/A, kein Wh-Integral.
- Ein PV-Zweig fehlt: echte WP-/BEV-Mengen bleiben; nur freigegebener Anteil als Ersatz. Pausenbudget überschritten, instabile Last, Schätzungskette und bereits im Integral enthaltene Ersatzenergie gesondert prüfen. Erneuter Abschluss erzeugt keine Doppelbuchung; spätere echte Tage nach einer Lücke bleiben erhalten.
- Zwei Prognosemodelle: gleiche Faktoren und Vergleichstage, vorab gespeicherte Originale, fehlender Snapshot, wechselnde Parameter und geschätzter Ertrag. Kein künstlicher Erfolg durch Prognose als Ertragsersatz.
- CO₂: reine PV, reine Netzversorgung, zeitversetzte Netzladung/Entladung, API-Fallback, unbekannter Bestand und Herkunft nach Datenlücke. Modellwechsel darf nur unbekannte CO₂-Masse ändern; Energie, bekannte Netzmasse und Buchungsidentität unverändert. Netzladung vor dem Modellbeginn bleibt bei späterer Entladung belastet.
- Speicher-PV-Annahme muss ausdrücklich freigegeben und sichtbar sein; ohne Wahl keine automatische emissionsfreie Herkunft. SoC-Korrektur ohne gemessene Ladung als Modellunsicherheit erhalten.
- Jahresauswahl zeigt zwölf Monatspositionen, fehlende Monate nicht null. Lokale 23-/25-Stunden-Tage und Jahrgrenzen auch in API-Cache und Herkunftskette prüfen.
- Schreiblast vor/nach Änderung in längeren vergleichbaren Fenstern messen. Zeilenreduktion beweist keine proportionale physische Byteersparnis. Keine Hardwareänderung allein aufgrund eines kurzen Lastfensters.
- Gleiche SSD-Modelle eindeutig unterscheiden, aktives Laufwerk schützen, Backup zurücklesen und Wiederherstellung isoliert erproben. Keine zweite aktive Steuerinstanz gegen die echte Anlage.

Diese Fälle sind Abnahmeaufträge für die spätere individuelle Implementierung. Die Dokumenttests des Kits führen sie nicht auf einer HA-Installation aus.


## H. Optional freigegebene verzögerte Nachladung

Die [Fälle für Netzausfall und Wiederanlauf](15-netzausfall-und-wiederanlauf.md) mit synthetischen Eingängen prüfen. Nachführung bei sinkendem SoC, kein Wiederanheben bei PV-Ladung, Mindestgrenze, bereits identische Ziele und nur ausdrücklich erlaubte Programm-SoC-Schreibrollen. Zeiten, Ladearten, technische Schutzparameter und andere Gerätefunktionen vor/nach unverändert belegen.

Warteparameter 10/60/120 Minuten, jeweilige Frist unmittelbar davor/danach, Änderung während Ausfall und laufender Wartezeit, Verlängern sowie Verkürzen unter bereits vergangene Zeit. Rückkehrbeginn darf durch Bedienung nicht unbemerkt neu gesetzt werden. Ungültiger oder restaurierter Parameter sperrt normale Zeitfreigabe; Untergrenzen-Vorrang bleibt erhalten.

Neustart mit persistentem Zustand, Datenpause, erneuter Ausfall und Aus-/Einschalten des Hauptschalters prüfen. Vor jedem einzelnen Befehl erneut validieren. Teilweiser Schreibfehler erzeugt nachvollziehbaren begrenzten Retry und Warnung ohne Warnflut. Keine realen Schutzsensoren für Tests fälschen. Konfiguration/HA-Rücklesen, Geräteparameter und tatsächlich vermiedenen Ladebeginn getrennt abnehmen. Ein noch nicht beobachteter echter Ausfallzyklus bleibt ausdrücklich offen.

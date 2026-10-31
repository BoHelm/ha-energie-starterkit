# Module und gewünschte Bedienung

## PV, Leistung und Energie

Getrennte Ansichten für Momentanleistung W/kW und Energiemengen kWh/MWh. PV-Zweige einzeln sowie Gesamt, aktueller Leistungsfluss, Tagesenergie, Netzbezug und Bedarfsdeckung. Sankey-Pfeile brauchen benannte Messgrenzen; Batterie-Ladung und -Entladung separat. Erzeugung nicht zusätzlich als Hausbedarf addieren. Datum beziehungsweise Monat/Jahr wählen; vorhandene historische Quellen nicht durch aktuelle Verkabelung uminterpretieren.

## Tablet und Smartphone

Kompakter Tablet-Reiter mit Wechselrichter-/WP-Status, PV-Leistung, Speicheranzeige, Prognose, Leistungsfluss und Energie heute. Auflösung vor Ort prüfen; eine universelle Ein-Seiten-Garantie gibt es nicht. Menüs ausblendbar, Wiederherstellung unten rechts, Bearbeitungsmodus erreichbar. Browser-Vollbild nur nach Benutzeraktion und soweit unterstützt.

Auf dem Handy Ergebniszahlen und Diagramme zuerst, lange Erklärung danach, Einstellungen zuletzt. Stabile Kartenhöhe und vorhandene DOM-Knoten bei Aktualisierung erhalten. Datumsfelder, Fokus und aufgeklappte Listen dürfen nicht zurückspringen. Pastelltöne pro Funktionsbereich leicht verschieden; Eingabewerte, Warnungen und Diagramme in hell/dunkel prüfen. Farben allein tragen keine Qualitätsaussage.

## Batterie

Gesamtladung MWh, äquivalente Vollzyklen gesamt und je ausgewähltem Monat/Jahr, Monatsbalken eines Kalenderjahres. Historienbeginn sichtbar, unvollständige Startmonate nicht als volle Monate verkaufen. SoH nur falls vorhanden. SoC-Verlauf für einen bis sieben lokale Tage mit Minutenanzeige aus vorhandener Historie, Mindest-SoC als historische Stufenlinie. Eine Minutenanzeige bedeutet keine zusätzliche Hardwareabfrage jede Minute.

Speicher-Gauge: untere Skala dynamisch aus gültigem Mindest-SoC, obere100%; Zahl weiterhin absoluter SoC. Optional markierte gleichzeitige Netzaufnahme beim Laden ist nur Gleichzeitigkeit, kein Herkunftsnachweis. Schutz- und Alarmfunktionen werden separat projektiert; keine fremden Prozent-/Spannungsgrenzen übernehmen. Modul-/Zellwerte nur mit belegter Datenquelle; Gesamtspannung ersetzt keine Zellspannungen.

## Solarprognose

Aktuelle Prognose und vorab gespeicherter Folgetagswert mit Datum. Snapshotzeit lokal konfigurierbar. Abweichung für abgeschlossene Tage sowie7-/31-Tage und Kalenderjahr, alle mit klarer Definition. Jahresdiagramm über volle Breite. Qualitätsstatus, Tagesertrag und Datenbeginn sichtbar; historische ungeprüfte Anzeigen nicht in geprüfte Kennzahlen mischen.

## Kosten und CO₂e

Eigene Dashboards, gleiche Begriffe und Zeiträume: Ausgangsinvestition/CO₂e-Aufwand, Verlauf, Forecast, Tagesrechnung mit Datumswahl, kumulierte Beiträge aus PV/WP/BEV, Summe und Prozentanteile. Kostenjournal für Erweiterungen/Reparaturen, keine konkurrierenden alten Zusatzkostenfelder. Ein gemeinsamer Start belegter täglicher Daten für Komponentenvergleich; frühere Pauschalmodelle getrennt kennzeichnen. Ausfalltage als unbekannt, nicht als Nullersparnis zählen.

Momentane Ersparnis in EUR/h oder ct/h und kgCO₂e/h aus gültiger Leistung und Referenzen; alle paar Sekunden Anzeige aktualisieren, ohne Geräteabfragerate zu erhöhen. Das ist eine Rate, keine gebuchte Stunde. Historische Tagesrechnung kommt aus dem Journal. Annahmen/Nutzfaktor sichtbar und zentral.

## Wärmepumpe und Wetterstation

Herstellerstatus und Temperaturen rein lesend, fehlender Status neutral. Vergleich Hersteller Heizung+Warmwasser gegen disjunkte Shelly-Stromkreise: gemeinsame Basis, volle Monate, Monats-/Gesamtabweichung und Datumsauswahl.

Tagesprofil00–24Uhr mit Außentemperatur, zeitlich gemittelter Windgeschwindigkeit der eigenen Station und summierter elektrischer WP-Leistung. Gemeinsamer Tageswähler für Diagramm und vier Tageszahlen: Gesamtstrom, Innenstrom separat, Temperaturmittel, Windmittel. Innenstrom bereits in Gesamtstrom enthalten. Ohne Stromlaufplan kein exklusiver Heizstab-/Abtaunachweis.

Jahr wählbar, Jahres-Tageswerte als echte XLSX: alle Kalendertage, Datum numerisch, WP-kWh, Innen-kWh, °C, Windgeschwindigkeit und jeweils Qualität/Abdeckung. Fehlerhafte oder unbelegbare Energie leer. Wetter-Teilmittel erlaubt, ausdrücklich markiert. Diagramm und Export dürfen unterschiedliche zeitliche Auflösung verwenden, müssen die Basis dann nennen.

Optional unabhängige monatliche Gasvergleichsrechnung mit Heizung und Warmwasser getrennt. Koeffizienten müssen aus den Unterlagen der jeweiligen Anlage kommen. Ohne gemessene Wärme inklusive Warmwasser keine gemessene Gesamt-JAZ behaupten. Erst parallel validieren, bestehende Burndown-Zahlen nicht automatisch ersetzen.

## Weitere optionale Energie-Module

- Ortsnetz-Community: unterstützte Messrollen, Fünf-Minuten-Mittel, Netzfrequenz/Phasenspannungen und Datenqualität. Übertragung standardmäßig aus; Standort und Zustimmung ausschließlich lokal klären. [Projekt](https://github.com/thomaslehmann1234/datenerfassung-ortsnetz-auslastung).
- Messdatenarchiv plus getrenntes vollständiges HA-Backup; Warnung und Entwarnung, begrenzte Nachholversuche im NAS-Fenster.
- Anlagenzustand: Quellen, Frische, Journal, Archiv, Backup und Speicherplatz ohne unnötige zusätzliche NAS-Abfrage.
- Verlustdiagnose und Dachausbau-Szenario: ausschließlich gekennzeichnete Modelle, keine kausale Effizienzbehauptung aus unsynchronen Messungen.

Gezielte Netzladung/-einspeisung und pauschale Lade-/Balancing-Automatik sind nicht Teil der Standardumsetzung. Erst Gerätefähigkeit, Leistungsgrenze, SoC-Grenzen und bestehende Zeitfenster unabhängig klären. Keine automatische Aktivierung aus einer Community-Empfehlung.

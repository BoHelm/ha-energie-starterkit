# Datenqualität: lieber eine Lücke als eine falsche Aussage

Jeder abgeleitete Wert besitzt Wert, Einheit, Zeitraum, Quellen und Qualitätszustand. Geeignete Zustände: gemessen, Teilwert, Schätzung/Ersatzwert, nicht verfügbar. Farben nur ergänzend. Ein Ergebnis ohne gültige Basis darf weder grün noch null sein.

## Quellenprüfung

- `unknown`, `unavailable`, restauriert, leer, falsche Einheit, ungültiges Vorzeichen und nicht endliche Zahl sind keine gültigen Messwerte.
- Eine gemeldete echte Null bleibt null. Null ist kein Anlass zum Quellenwechsel.
- Frische anhand belegbarer Berichtszeit, Gerätetyp und Messlogik. Unveränderter Zähler oder Windstille ist nicht automatisch ein ausgefallenes Gerät.
- Gegenwartsfrische nicht rückwirkend als historischen Vollständigkeitsbeweis benutzen. Historische Ausfälle brauchen eigene gespeicherte Zustände beziehungsweise Qualitätsnachweise.
- Bei kombinierten Leistungen gemeinsame gültige Zeitintervalle aller beteiligten Quellen verwenden. Keine Summe unterschiedlich alter Werte als gleichzeitige Messung ausgeben.

## Tagesenergie

Kumulative Zähler können interne Datenpausen überbrücken. Prüfe die Tagesgrenzen beidseitig und die Monotonie. Grenzen dürfen nur innerhalb eines begründeten zeitlichen Randbands geschätzt werden; dieses Band gegen die Energiemenge bewerten und anzeigen. Größer als das vereinbarte Budget oder nicht begrenzbar: keine Tagesaussage. Ein Richtwert von5% ist ein zeitliches Fehlerbudget und keine universelle Zusicherung der Zählergenauigkeit.

Für Leistungssummen/Integrale ist eine Pause anders zu behandeln: ohne gesicherte Energie nicht beliebig über den Ausfall integrieren. Keine Kompensation durch pauschale0W. Dach, AC-Zweige und Batterie haben unterschiedliche Auflösungen und Messgrenzen.

## Wetter und Tageskurven

Vorhandene Messabschnitte bleiben sichtbar, Ausfälle als Unterbrechung. Keine Geraden über unbekannte Intervalle und keine Nullwerte als Füllung. Zeitmittel nur über vorhandene gültige Zeiten. Bei weniger als vollständiger Basis „Teilmittel“ mit Zeitabdeckung. Ein gültiger unveränderter gespeicherter Zustand darf bis zur nächsten Meldung gelten, sofern das die erklärte Historiensemantik ist; das beweist keine unabhängige Geräteerreichbarkeit.

Langzeitstundenmittel können ältere Tage erhalten. Vorhandene Statistikstunden sind nicht gleich vollständige Messabdeckung innerhalb der Stunden. Diese Grenze im Diagramm und im Excel nennen. Nicht belegbare WP-kWh leer lassen, obwohl Wetter-Teilmittel angezeigt werden dürfen. Fehlende Innen-/Außenenergie getrennt behandeln; Innenenergie allein kann gültig sein, obwohl die Summe offen ist.

## Ersatzwerte

Ein zuvor freigegebener Ersatz darf bleiben, wenn primäre Quelle tatsächlich fehlt oder ungültig ist. Dann Quelle, Zeitraum, Anteil und Unsicherheit kennzeichnen. Gültige Null nicht ersetzen. Bekannte Ersatzwerte nicht pauschal als gleich genau behandeln. Ein Fallback darf einen gesamten Tag nicht heimlich zum „gemessenen“ Tag machen.

Ausdrückliche PV-Nachtannahme0W ist möglich, wenn ein unabhängiger aktueller Sonnenbeleg und keine widersprechende gemeldete Erzeugung vorliegen. Eine kaputte PV-Quelle nicht allein anhand der Uhrzeit zu null machen. Nachtannahme sichtbar; WP/BEV bleiben messwertbasiert. Keine solche Annahme auf historische Tagesenergie oder Gerätealarme übertragen.

## Abschlüsse und Wiederanlauf

Snapshots und Journale datumssicher, atomar und persistent speichern. Tagesabschluss idempotent: dieselbe Quellbasis erzeugt keine neue Buchung. Verpasste Läufe begrenzt nachholen, aber keine nicht vorhandenen Daten erfinden. Bei Qualitätsrücknahme nicht still finanzielle Historie überschreiben; Korrektur nachvollziehbar versionieren. Qualitätsbeginn und ungeprüften historischen Bestand sichtbar trennen.

Tage ohne Aussagen und technische Ausfalltage sind verschiedene Größen. Erst ein erwarteter beobachteter Zeitraum erlaubt eine Ausfallzählung. Tage vor Erfassungsbeginn nicht als technischen Ausfall zählen. Laufende Tage nicht als abgeschlossen darstellen.

## Geräte- und Cloudlast

UI-Refresh ist keine zusätzliche Geräteabfrage. Keine vollständige Historie pro Sekunde abrufen. Historie cachen, große Abfragen begrenzen und Export monatsweise nacheinander lesen. Herstellerquoten beachten. Bei Modbus/Solarman Serialspeed allein nicht als Timeoutursache diagnostizieren; tatsächliche Abfragezeit, Fehler und Netzabbrüche zeitlich abgleichen. WLAN- und Geräteprobleme nicht durch immer höhere Pollingrate verschärfen.

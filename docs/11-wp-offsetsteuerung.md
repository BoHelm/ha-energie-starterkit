# Optionale WP-Offsetsteuerung bei bestehender Heizkurve

Dieses Modul ergänzt die WP-/Wetter-Auswertung um eine bewusst freigegebene Steuerung. Es ist eine Bau- und Abnahmespezifikation, kein direkt installierbares Paket. Der öffentliche Fragebogen und das Demo lassen Gerätebefehle und diese Automatik ausgeschaltet. Keine privaten Konfigurationen oder Gerätekennungen übernehmen.

## Zweck und Regel

Die witterungsgeführte Heizkurve bleibt erhalten. Ein manueller Basis-Offset verschiebt sie; eine zuschaltbare HA-Automatik addiert zu einem festgelegten Tagesfenster einen Zuschlag. Beispielplan in lokaler HA-Zeit:

| Zeitpunkt / Zustand | Gewünschter Offset |
| --- | --- |
| Automatik an, 10:00 bis vor 16:00 Uhr | Basis +2 K |
| Automatik an, sonst | Basis +0 K |
| Automatik aus | Basis bei bewusster Bedienung |

**Außerhalb des Fensters entfällt nur der Zuschlag.** Beispiel: Basis −1 K bedeutet tagsüber +1 K, sonst −1 K. Bei Basis 0 K gilt tagsüber +2 K, sonst 0 K. Der Offset ist eine Temperaturdifferenz in K, keine feste Vorlauftemperatur in °C. Dieser feste Tagesplan ist noch keine wetterabhängige Optimierung und keine zugesicherte Energieeinsparung: Komfort, Heizflächen, Gebäudeträgheit, Thermostate und Außentemperatur können das Ergebnis verändern.

## Zuerst die echte Schnittstelle prüfen

Für Daikin/ONECTA beschreibt der [Integrationsmaintainer die numerische Offsetänderung](https://github.com/jwillemsen/daikin_onecta/discussions/420) über `climate.set_temperature`. Das belegt keine Unterstützung jedes Modells, jeder Firmware oder anderer Hersteller. In der konkreten Anlage zunächst rein lesend feststellen:

- Welche Entität den **Offset der Witterungskurve** darstellt, einschließlich Einheit und Vorzeichen. Ein gewöhnlicher Raum- oder Festwertthermostat ist kein Ersatz.
- Ob das `temperature`-Attribut tatsächlich diesen Offset enthält. `current_temperature` kann dagegen die gemessene Wassertemperatur sein.
- Welche Betriebsart, Sollwertführung, Min-/Max-Grenzen und Schrittweite die installierte Integration tatsächlich meldet.
- Welche HA-/Integrationsversion installiert ist, wie häufig sie die Cloud abfragt, welche Quoten gelten und wie sie Verbindungsfehler signalisiert. Zahlen einer anderen Installation nicht übernehmen.

Quellenrollen im privaten Anlagenfragebogen: `wp_offset_control` für die zu bestätigende Zielentität und `wp_setpoint_mode` für den belegten Sollwertmodus. Öffentliche Beispiele verwenden nur `climate.demo_wp_offset` und `sensor.demo_wp_sollwertmodus`; diese Entitäten existieren nicht automatisch.

Nach Freigabe nur den numerischen Offset schreiben. Keine Betriebsart mitgeben, nicht zwischen fester Temperatur und Heizkurve umschalten und keine Warmwasser-, Frostschutz-, Maximaltemperatur-, Herstellerzeitplan- oder Batterieparameter ändern. Wenn die installierte Schnittstelle das nicht getrennt ermöglicht, dieses Modul nicht aktivieren. Ein zulässiger technischer Einstellbereich ist keine Empfehlung, alle Extremwerte auszunutzen.

## Helfer, Anzeige und Erstinitialisierung

Benötigt werden ein persistenter Basiswert, ein Automatikschalter, Initialisierungsnachweis, letzter Sendeversuch und letztes Sendeziel. Dazu gewünschter Offset, gemeldeter Geräteoffset, Status mit Sperrgrund und eine bewusste Aktion „Sollwert jetzt anwenden“.

Benutzerwerte sollen nach Neustart erhalten bleiben. Bei YAML-Helfern feste `initial`-Werte vermeiden, wenn sie Benutzeränderungen überschreiben würden; siehe [HA-Zahlenhelfer und Zustandswiederherstellung](https://www.home-assistant.io/integrations/input_number/). **Ein neuer Helfer ohne Anfangswert ist noch keine sichere Erstinitialisierung:** Ein technischer Mindest-/Standardwert darf niemals ungeprüft ans Gerät gelangen. Zuerst bei gesperrter Regel und ausgeschalteter Automatik den bestätigten bisherigen Offset übernehmen, zurücklesen und erst dann den Initialisierungsnachweis setzen. Aktivierung danach separat freigeben.

Bedienort **Haus → Wärmepumpe**, direkt unter dem Gerätestatus: Basiswert, Automatikschalter, gewünschter und gemeldeter Offset, Steuerstatus und manuelles Anwenden. Lange Erklärung weiter unten, insbesondere auf dem Handy. Keine zweite konkurrierende Eingabestelle unter Anlagenparameter. Vorhandene reine Statuskarten dürfen bleiben; Hinweise wie „gesamte Ansicht ausschließlich lesend“ müssen an die neue Steuerfunktion angepasst werden. Ist keine Hausansicht vorhanden, einen gleichwertigen WP-Bereich verwenden; andere Hausmodule gehören weiterhin nicht zum Kit.

## Ablauf und Ausfälle

Das folgende Verhalten muss vor Aktivierung verständlich dokumentiert und mit der Zielanlage geprüft werden:

1. Automatik an: Umschaltzeitpunkte, HA-Start, Basis-/Schalteränderung und lokaler periodischer Abgleich berücksichtigen. Beispiel: alle fünf Minuten aus bereits vorhandenen HA-Zuständen rechnen; kein zusätzlicher Cloud-Refresh. Verpasste Zeitpunkte nach Verfügbarkeit entsprechend der **jetzt** geltenden Phase nachholen, keine alten Tagesbefehle abspielen.
2. Automatik aus: Basisänderung, Ausschalten oder „Sollwert jetzt anwenden“ wenden einmalig den Basiswert an. Kein periodisches Überschreiben von App-Änderungen. Ist der Auftrag mangels gültiger Daten abgewiesen, nicht später überraschend ausführen; nach Wiederverbindung bewusst neu anwenden. Ausschalten während des Tagesfensters soll den Zuschlag zurücknehmen, soweit die Verbindung das zulässt.
3. Vor jedem Gerätebefehl unmittelbar erneut prüfen: initialisiert, gültige Einstellungen, richtige Zielentität, Heizbetrieb freigegeben, Witterungsführung bestätigt, keine unbekannten/nicht verfügbaren/restaurierten Daten, plausible Zeitstempel und Geräteparameter. Keine Ersatznullwerte.
4. Quellenalter einschließlich Modus prüfen. Beispiel-Prüffrist 90 Minuten nur übernehmen, wenn sie zur tatsächlichen Cloud-Abfrage passt. HA-`last_reported` belegt eine HA-Meldung, nicht unabhängig die Frische einer physischen Gerätemessung. Die Grenzen dieses Nachweises sichtbar nennen.
5. Gesamtziel **Basis + Zuschlag** auf Min/Max und Raster prüfen. Außerhalb des Bereichs mit sichtbarem Grund sperren, nicht still begrenzen. Beispiel: bestätigtes Maximum +10 K plus Zuschlag +2 K erlaubt während des Tagesfensters höchstens Basis +8 K. Diese Zahlen sind kein universeller Gerätebereich.
6. Entspricht das gemeldete Ziel bereits dem gewünschten Wert, keinen weiteren Befehl senden. Letzten Versuch vor dem Cloud-Aufruf persistent speichern, um Fehlerschleifen über Neustarts hinweg zu begrenzen. Beispiel: dasselbe erfolglose Ziel höchstens stündlich erneut versuchen; ein neues Ziel, insbesondere die Rücknahme am Fensterende, darf dadurch nicht unnötig verzögert werden. Tatsächliches Tagesbudget einschließlich normaler Abfragen prüfen.
7. Nur begrenzte kurze Abläufe, keine Automation bei jeder unveränderten Rohmessung starten. Nach Neustart erst gültige Quellen und restaurierte Helfer abwarten. Nicht allein aus einem restaurierten Sensorwert einen Befehl ableiten.

Bei ausgeschaltetem HA oder ausgefallener Cloud kann HA keine rechtzeitige Rücknahme garantieren. Geräte- und HA-Zeitpläne dürfen nicht unbemerkt konkurrieren. Automatik an bedeutet, dass der HA-Basiswert maßgeblich ist; abweichende App-Werte können beim nächsten gültigen Abgleich wieder überschrieben werden. Ausschalten ist daher klar vom Beenden sämtlicher HA-Schreibmöglichkeiten zu unterscheiden; manuelle Bedienung darf weiterhin bewusst wirken.

## Rückmeldung und Abnahme

„Gewünscht“, „Sendeversuch“, „von der Integration gemeldet“ und „unabhängig am Gerät bestätigt“ unterscheiden. Eine Integration kann nach einem Cloud-Aufruf ihren HA-Sollwert sofort selbst aktualisieren. Das allein beweist keine physische Übernahme. Bestehende normale Abfragen und gegebenenfalls Hersteller-App für die Gegenprüfung verwenden, keine schnelle Refresh-Schleife. Informationen zu HA-Aktionen stehen in der [Climate-Dokumentation](https://www.home-assistant.io/integrations/climate/).

Mindestens prüfen: 09:59/10:00/15:59/16:00 Uhr, positive/negative Basis, Automatik aus, ausschalten im Tagesfenster, identisches Ziel, ungültiger Zielbereich und Raster, fehlende/restaurierte/veraltete/zukünftige Werte, anderer Sollwertmodus und ausgeschaltete Heizung. Wiederanlauf, verpasste Umschaltung, Cloudfehler, Sendequoten und Wiederholungsgrenze separat prüfen. Keine echte gefährliche Betriebsstörung zum Test auslösen. Ein noch nicht beobachteter späterer Umschalttermin oder echter Ausfall bleibt als ungeprüft gekennzeichnet.

Vorher-/Nachher-Nachweis: gleiche Heizkurve und Warmwassereinstellungen, unveränderte Schutzgrenzen und Herstellerzeitfenster, Offset-Rücknahme, persistenter Basiswert und Schalter. Ein bestandener Dokumenttest dieses Repositorys ist keine erfolgreiche Anlagenabnahme. Es wird keine automatische COP-/Komfortoptimierung aus elektrischer Leistung oder Außentemperatur allein versprochen.

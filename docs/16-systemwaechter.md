# Optional: lokaler Systemwächter im Prüfmodus

Dieses Modul beschreibt eine individuell umzusetzende Diagnosefunktion in Home Assistant. Es ist kein mitgelieferter installierbarer Bot und kein autonomer KI-Agent. Gerätezahl, Quellen, Empfänger und Meldefristen müssen für jede Zielanlage bestätigt werden. Bestehende Schutzfunktionen, Grenzwerte und Geräteabfragen bleiben unverändert.

## Aufgabe und Grenzen

Ein lokaler regelbasierter Dienst liest vorhandene HA-Zustände regelmäßig, beispielsweise jede Minute. Er bewertet wesentliche, anhaltende Störungen und meldet sie an einen ausdrücklich freigegebenen Empfänger. Seine einzige aktive Fachaktion ist die vereinbarte Benachrichtigung. Keine Gerätebefehle, Aktivierung von Automationen, Reparaturen, Datenlöschung oder automatischen Neustarts zulassen.

Die KI hat bei der Entwicklung geholfen; im laufenden Wächter wird kein KI-Modell aufgerufen. Für die Diagnose erfolgt keine Übertragung an OpenAI. Eine Pushnachricht nutzt weiterhin den jeweils gewählten Benachrichtigungsdienst und ist davon zu unterscheiden.

Ein interner Wächter kann den vollständigen Ausfall von HA oder seines Rechners nicht zuverlässig selbst melden. Internet- und Pushdienst-Ausfälle können Benachrichtigungen verhindern. Für diese Fälle ist eine getrennte externe Überwachung ein eigenes Vorhaben.

## Sinnvolle Prüfbereiche

| Bereich | Prüfung |
| --- | --- |
| Stromzähler / MQTT | Letzter tatsächlich gültiger Empfang statt letzter Änderung des kumulierten Zählerstands |
| Shelly und ähnliche Messgeräte | Native Verfügbarkeit und passende Berichtsfrische, Teilgeräte zum physischen Gerät gruppieren |
| Schutz- und Reserveautomationen | Vorhandensein und erwarteter Aktivzustand; nur melden, niemals selbst einschalten |
| Tagesjournal | Integrität, Bereitschaft und Rückstand abgeschlossener Tage; Nachlaufzeiten berücksichtigen |
| Auswertungen | Gesundheit der Minutenhistorie und des Ausfallprotokolls |
| Sicherungen | Funktion der vorhandenen Backupüberwachung; bestehende Warnungen nicht doppelt versenden |
| Speicher | Dauerhaft knapper freier Platz; keine automatische Bereinigung |
| Routeranbindung | Abgelaufene Anmeldung getrennt von Geräteausfällen bewerten |
| Fehlerprotokolle | Wiederholte ERROR- oder Already-running-Ereignisse nach Modul und Zeitfenster zusammenfassen |

Schwellwerte sind Diagnoseparameter, keine neuen Schutzgrenzen. Als zunächst freizugebendes Beispiel: mindestens zehn Minuten Fehlerdauer für wichtige Energiequellen, dreißig Minuten für übrige Geräte, zehn Minuten Startschonzeit und zwei stabile Minuten vor Entwarnung. Zusätzliche Frischefristen können die Gesamtzeit verlängern. Fehlende Daten sind kein Beleg für einen bestimmten Hardwaredefekt.

Konstante 0 W, unveränderte Zählerstände und ein bewusst abgeschalteter Verbraucher dürfen allein keinen Geräteausfall erzeugen. Numerische Werte auf Einheit, Restaurierung, Zukunftszeit und tatsächlichen Berichtsempfang prüfen. Reine Schaltgeräte ohne belegten Heartbeat nur auf Verfügbarkeit beurteilen. Eine unzuverlässige WLAN-Ortung ist kein Ersatz für frische native Geräte- oder MQTT-Meldungen.

## Geplante Auszeiten und abhängige Fehler

Ein planmäßig ausgeschaltetes NAS außerhalb seines Sicherungsfensters erzeugt keine zusätzliche Alarmflut. Entscheidend sind erfolgreiche, geprüfte Sicherungen und überfällige Nachholungen. Vorhandene Sicherungswächter behalten ihre Zuständigkeit; zusätzlich ihren Funktionsausfall oder ausbleibende Prüfungen erkennen.

Bei abgelaufener Routeranmeldung können Standort- und Routerdaten fehlen, während native MQTT- und Shelly-Daten weiterhin korrekt sind. Diese Fälle trennen. Nicht pauschal alle abhängigen Entitäten einzeln melden.

Alte ersetzte Historie-Entitäten, absichtlich deaktivierte Registry-Entitäten und nicht konfigurierte optionale Geräte nicht als reale Ausfälle inventarisieren. Neu hinzukommende Geräte nach derselben belegten Registry-Zuordnung aufnehmen.

## Meldungen und persistenter Zustand

1. Beobachteten Fehlerbeginn speichern und die festgelegte Mindestdauer abwarten.
2. Erst bei qualifizierter Störung eine verständliche Meldung mit Auswirkungen und Diagnosehinweis senden.
3. Erfolgreiche Übergabe pro Störungsphase persistent merken. Keine unveränderten Dauermeldungen bei jeder Prüfung oder nach jedem Neustart.
4. Fehlgeschlagene Pushübergaben begrenzt wiederholen; keine enge Schleife.
5. Entwarnung erst nach stabiler Erholung und nur für zuvor gemeldete Störungen.
6. Meldungen derselben Prüfung möglichst bündeln. Unbekannter Zustand gilt nicht als bestätigte Erholung.

Empfänger für diesen Wächter ausdrücklich separat festlegen. Die Freigabe einer einzelnen Person erlaubt keine automatische Erweiterung auf andere Telefone oder Gruppen. Bestehende Schutzmeldungen behalten ihre bisherigen Empfänger.

HA-Serviceerfolg bestätigt die Übergabe, nicht den Empfang oder Ton am Telefon. Einen echten Empfangstest gesondert vereinbaren und dessen Ergebnis dokumentieren. Keine schweren Echtstörungen oder erfundenen Zustände in produktiven Schutzsensoren zum Test auslösen.

## Befristete Prüfwoche und Schreiblast

Zum Einstieg sieben Tage ausschließlich beobachten und melden. Beginn und Ende einmalig dauerhaft speichern; Neustarts verlängern die Woche nicht. Nach Fristablauf automatisch pausieren, keine stillschweigende Freigabe von Reparaturen. Bestehende Schutz- und Backupfunktionen bleiben aktiv.

Prüfungen lesen vorhandene Zustände im Arbeitsspeicher, ohne zusätzliche Geräteabfragen und schnelle Rohhistorien. Kleine Zustandsdatei und privates Textprotokoll bei inhaltlichen Änderungen beziehungsweise in einem begrenzten Intervall sichern. Keine großen Diagnoseattribute minütlich im Recorder historisieren. Physische SSD-Schreiblast erst nach Messung beziffern; Dateigröße oder Speicherzyklen sind kein Nachweis tatsächlicher Flashbelastung.

Statusansicht mit Prüfmodus, Beginn/Ende, Gerätezahl und offenen Befunden bereitstellen. Detailberichte privat ablegen und nur authentifiziert zugänglich machen. Rohlogs können Geheimnisse enthalten: Für Fehlerhäufungen genügen beispielsweise Modulname und Anzahl, ohne Nachrichteninhalt, URL oder Traceback.

## Separater KI-Bot vorerst zurückgestellt

Der zusätzlich erwogene KI-Prüfer auf einem persönlichen Mac wird aus Sicherheitsgründen vorerst nicht eingerichtet. Für den geplanten Betrieb wurde keine ausreichend enge technische Abschottung gegenüber persönlichen Dateien, Mail, Fotos, Browserzugängen und schreibenden HA-Funktionen bestätigt. Ein Promptverbot allein ist dafür keine belastbare Zugriffssperre.

Es wird kein zusätzlicher KI-Prüfauftrag oder allgemeiner HA-Zugang eingerichtet; aktiv ist ausschließlich der lokale HA-Systemwächter. Diese Entscheidung ist kein Beleg, dass eine sicher isolierte Lösung grundsätzlich unmöglich wäre. Eine spätere Umsetzung wäre ein eigener Auftrag: zuerst technische Zugriffsbeschränkungen und freigegebene bereinigte Datenquelle nachweisen, danach Übertragung und Zeitplan ausdrücklich festlegen. Eine frühere Zustimmung zur Datenübertragung ersetzt diese technische Prüfung nicht.

## Abnahme

- Ausfall und Wiederkehr mit isolierten Testdaten prüfen: gültige Nullwerte, fehlende und veraltete Meldungen, Zukunftszeiten, Flattern und Mindestdauer.
- Neustartpersistenz, Meldungsbegrenzung, fehlgeschlagene Zustellung und neue Störung nach Entwarnung prüfen.
- Ende der Prüfwoche einschließlich Neustart vor/nach der Frist testen.
- Quellcode auf ausschließlichen Benachrichtigungsaufruf und den freigegebenen Empfänger prüfen; Schutzdateien vor/nach vergleichen.
- Bericht speichern und zurücklesen, Zugriff ohne Anmeldung verweigern, normale Statusansicht kontrollieren.
- Dokumenttests nicht als vollständige Anlagenabnahme ausgeben. Ersten echten Warn-/Entwarnungszyklus und Telefonempfang separat beobachten.

Eine Referenzumsetzung wurde mit sechzehn isolierten Prüfungen, nativer HA-Konfigurationsprüfung, gespeicherter Wochenfrist, Statusansicht, API-Zugriffsschutz und Vergleich unveränderter Schutzdateien geprüft. Der erste echte Benachrichtigungszyklus blieb bei Einrichtung noch zu beobachten. Die private Konfiguration und Betriebsdaten dieser Umsetzung werden nicht veröffentlicht.

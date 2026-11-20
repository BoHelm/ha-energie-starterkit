# Optional: Netzausfall und verzögerte Batterie-Nachladung

Dieses Modul ist eine individuell anzupassende Spezifikation für Hybridwechselrichter, beispielsweise Deye. Es ist **standardmäßig aus** und kein mitgelieferter, universell geprüfter Gerätetreiber. Gerätebefehle benötigen eine gesonderte Freigabe; das Lesen dieses Dokuments erteilt sie nicht. Private Anlagenwerte, echte Entitätskennungen und fertige Hauskonfigurationen gehören nicht ins Repository.

## Ziel und technische Grenze

Nach einem längeren Netzausfall liegt der Akku möglicherweise unter seiner saisonalen Reserve. Kehrt die Netzversorgung zurück, kann der Wechselrichter sofort mit hoher Leistung nachladen. Eine erst dann von HA geschaltete Sperre kann zu spät kommen.

Die hier beschriebene Alternative nutzt ausschließlich bereits freigegebene Programm-SoC-Ziele: während des Ausfalls ein niedrigeres Ziel vorbereiten, dieses nach Netzrückkehr zeitweise halten und danach die saisonale Reserve wiederherstellen. Bei Geräten mit sechs Zeitprogrammen werden nur die sechs entsprechenden SoC-Werte geändert. Zeitfenster, Ladearten, Leistungswerte, globale Stromgrenzen, Betriebsmodus und technische Batterie-/BMS-Schutzgrenzen bleiben unangetastet. Keine Erweiterung um einen Remote-/EMS-Modus oder gezielte Einspeisung.

**Das ist keine harte Ladesperre, keine Zusage einer maximalen Netzleistung und kein belegter Netzanschlussstandard.** Ob der jeweilige Wechselrichter mit seiner Firmware tatsächlich nicht nachlädt, muss separat geprüft werden. Technische Notladung, SoC-Sprünge, nacheinander übertragene Programmwerte sowie HA-/Kommunikationsausfälle können die Wirkung begrenzen. Nach Ablauf der Wartezeit ist die bisherige hohe Ladeleistung wieder möglich; die Funktion verschiebt den Lastsprung und begrenzt ihn nicht.

## Vor Umsetzung lokal klären

- Modell, Firmware und tatsächlich unterstützte Programm-SoC-Schreibrollen belegen; keine Registeradressen aus fremden Anlagen raten.
- Netzstatus muss sich auf die öffentliche Netzseite beziehen. Eine weiterhin versorgte Insel-/Backupsteckdose kann trotz Netzausfall normale Spannung zeigen. Gerät offline ist kein bestätigter Stromausfall.
- Ist-SoC, Verbindung, Netzstatus, technische Untergrenzen und alle Programmwerte nach Einheit, Gültigkeit, Restaurierung und Berichtsintervall prüfen.
- Bereits vorhandene Saisonautomatik und alle weiteren Schreiber inventarisieren. Ein einziger abgestimmter Schreiber muss saisonale und vorübergehende Ziele verwalten; eine unveränderte periodische Saisonregel würde die Absenkung sonst wieder überschreiben.
- Betreiber muss der vorübergehenden Reduktion der saisonalen Reserve zustimmen und eine nicht unterschreitbare betriebliche Untergrenze festlegen. Technische Abschalt-, Low- und Restart-Grenzen werden nur gelesen, niemals abgesenkt.
- Alarmziele, kritische Benachrichtigungen, eventuelle Generatorhinweise und Rückbau getrennt freigeben. Ein Generatorhinweis startet keinen Generator.

## Drei Phasen mit persistentem Zustand

### Normalbetrieb

Alle ausgewählten Programmziele folgen der gültigen saisonalen Reserve. Diese bleibt als eigener Wert erhalten. Saisonreserve und aktuell wirksames Programmziel müssen getrennt angezeigt werden.

### Bestätigter Netzausfall

Nach einem kurzen ausdrücklich festgelegten Bestätigungsvorlauf gilt:

```text
Kandidat = abrunden(Ist-SoC minus 1 Prozentpunkt)
Neues Ziel = max(Untergrenze, min(bisheriges Ziel, Saisonreserve, Kandidat))
```

Beim ersten Eintritt dient die Saisonreserve als Ausgangsziel. Die Untergrenze muss für die Zielanlage aus betrieblich freigegebenem Minimum und ausreichendem Abstand zu den technischen Schutzgrenzen bestimmt werden. Ungeklärte Schutzwerte sperren die Absenkung. Bei steigender PV-Ladung wird das vorübergehende Ziel nicht wieder angehoben.

Schnelle gültige SoC-Eingänge beobachten, aber nur bei einer tatsächlichen ganzzahligen Zieländerung schreiben. Kein pauschales 30-Minuten-Schreibintervall: Sinkt der SoC in dieser Zeit um mehr als den einen Prozentpunkt Abstand, kann das alte Ziel bei Netzrückkehr schon wieder über dem Istwert liegen. Bestehende Geräteabfrageraten deshalb nicht ungeprüft erhöhen; historische Minutenwerte sind nicht automatisch die geeignete Steuerquelle.

### Netzrückkehr und Wartezeit

Nach bestätigter Rückkehr beginnt die Wartezeit. Letztes temporäres Ziel halten; bei Ablauf die dann gültige saisonale Reserve wiederherstellen. Bei erneutem Ausfall zur Ausfallphase zurückkehren. Bei einer Datenpause während des Wartens oder erkennbar neuer Netzrückkehr konservativ ab erneut bestätigtem Zustand warten.

**Priorität:** Ist der Akku bei Netzrückkehr bereits an oder unter der geschützten betrieblichen Untergrenze, hat notwendige Nachladung Vorrang; die Wartezeit wird übergangen. Eine Verzögerung darf keine technische Schutz- oder Notladefunktion außer Kraft setzen.

## Einstellbare Wartezeit: 10 bis 120 Minuten

Ein einziger persistenter lokaler Parameter, beispielsweise „Wartezeit nach Netzrückkehr“, mit Einheit Minuten, Bereich **10–120**, Schritt eine Minute und ausdrücklich gewähltem Anfangswert. Zehn Minuten sind das Startszenario, keine Netzanschlussvorgabe. Bei einem großflächigen Ausfall kann der Betreiber zum Beispiel 60 Minuten wählen; keine automatische Annahme über Ausdehnung oder Dauer einer Störung.

Bedienung neben der Saisonreserve im Ladebereich. Der Parameter darf während des Ausfalls und während der Wartezeit geändert werden. Es gilt immer:

```text
Freigabezeit = bestätigter Beginn der Netzrückkehr + aktuell gewählte Wartezeit
```

Eine Änderung startet die Uhr nicht bei null. Verlängern verschiebt die Freigabe nach hinten. Verkürzen kann sofort beziehungsweise bei der nächsten kurzen Prüfung zur Wiederherstellung führen, wenn die gewählte Frist bereits vergangen ist. Diesen Effekt vor Ort sichtbar erklären. Bei unbekanntem, restauriertem oder außerhalb des Bereichs liegendem Parameter keine normale zeitabhängige Freigabe aus einem erfundenen Standardwert ableiten; Untergrenzen-Vorrang bleibt wirksam.

Parameter, Phase, temporäres Ziel und Rückkehrbeginn nach Neustart erhalten. Gespeicherte Betreiberwahl nicht mit einem festen YAML-`initial` bei jedem Start überschreiben. Periodische Nachholprüfung verwenden statt einer einzigen langen, nach Neustart verlorenen `delay`-Aktion.

## Fehlerbehandlung und manueller Vorrang

- Fehlende, veraltete, zukünftige, restaurierte oder unplausible Steuerdaten sperren neue Gerätebefehle. Keine Ersatznull und keine Schätzung für SoC-Schutz verwenden. Einstellungen dürfen ein anderes belegtes Frischefenster als schnelle Messwerte haben.
- Bei ungültigen Daten bleiben bereits geschriebene Programmwerte bestehen. Das kann eine reduzierte Reserve länger als geplant erhalten. Zustand sichtbar anzeigen; keine garantierte Rückstellung ohne HA und funktionierende Verbindung behaupten.
- Bestehender Hauptschalter vor jedem einzelnen Schreibschritt prüfen. Aus bedeutet manuelle Einstellungen unangetastet lassen; nicht im Hintergrund alte Werte zurückschreiben. Ein Ausschalten ist deshalb nicht automatisch ein Rücksetzen auf hohe Reserve.
- Unmittelbar vor jedem Programmzugriff Quelle, Phase, Netzstatus und Ziel erneut prüfen; bei einem Wechsel veraltete Folgeschritte unterlassen. Nur tatsächlich abweichende Programme schreiben.
- Gleiches fehlgeschlagenes Ziel nur begrenzt erneut versuchen. Neue notwendige Ziele dürfen getrennt behandelt werden. Kein Schreibversuch bei jeder Eingangsmeldung.
- Alle gemeldeten Programme zeitversetzt zurücklesen. Abweichungen sichtbar melden und Benachrichtigungen pro Fehlerphase begrenzen. HA-Zustandsrückmeldung, bestätigter Geräteparameter und nachgewiesene physische Wirkung unterscheiden.

## Synthetische Beispiele und Abnahme

Die folgenden Zahlen sind frei gewählte Beispiele, keine Einstellungen einer veröffentlichten Anlage. Saisonreserve 60 %, betriebliche Untergrenze 15 %:

| Fall | Erwartung |
| --- | --- |
| Ausfall, Ist-SoC 42 % | Vorübergehendes Ziel 41 % |
| SoC sinkt auf 41 % | Neues Ziel 40 %; nur abweichende Programme schreiben |
| SoC steigt durch PV auf 48 % | Abgesenktes Ziel nicht wieder erhöhen |
| Langer Ausfall, SoC unter 15 % | Ziel nicht unter 15 %; technische Schutzgrenzen unverändert |
| Netz zurück, zehn Minuten gewählt, 599 Sekunden vergangen | Weiter warten |
| Zehn Minuten gewählt, 600 Sekunden vergangen | Saisonreserve wiederherstellen, sofern Quellen gültig |
| 60 Minuten gewählt, zehn Minuten vergangen | Noch 50 Minuten warten |
| Während des Wartens von zehn auf 60 Minuten ändern | Vom ursprünglichen Rückkehrbeginn rechnen |
| Nach 20 Minuten von 60 auf zehn Minuten verkürzen | Freigabe bei nächster gültiger Prüfung möglich |
| Netz zurück, SoC an Untergrenze | Untergrenzen-Vorrang statt langer Ladepause |
| Neustart oder Datenpause in Wartezeit | Zustand erhalten, Quellen neu prüfen und Nachholen nachvollziehbar durchführen |
| Hauptschalter aus | Kein Gerätebefehl; manuelle Bedienung hat Vorrang |
| Ziel schon in allen Programmen vorhanden | Kein erneutes Schreiben |

Zusätzlich Parametergrenzen 10/120, ungültige Werte darunter/darüber, fehlenden Parameter, erneuten Ausfall, teilweisen Schreibfehler und Kommunikationsabbruch zwischen zwei Programmen prüfen. Keine synthetischen SoC-/Netzzustände in reale Schutzsensoren schreiben und keinen echten gefährlichen Netzausfall zum Test auslösen. Gerätewirkung erst bei gesondert freigegebenem sicheren Test oder tatsächlichem Ereignis beobachten.

In einer Referenzumsetzung wurden die ursprüngliche feste Zehn-Minuten-Logik mit 59 isolierten HA-Templatefällen, Konfiguration, Rücklesen und unverändertem Normalbetrieb geprüft. Die editierbare Frist wurde zusätzlich mit 18 isolierten Fällen für 10/60/120 Minuten, Fristgrenzen, Verkürzen/Verlängern, ungültige Parameter und Untergrenzen-Vorrang geprüft. Diese Prüfungen beweisen keine physische Ladeunterdrückung und keine universelle Gerätekompatibilität. Ein realer Ausfall-/Wiederanlaufzyklus wurde inzwischen beobachtet; Umfang und Grenzen stehen im folgenden Praxistest. Eigene Tests und offene Prüfungen pro Zielanlage festhalten; keine erfolgreiche Live-Abnahme aus Repositorytests ableiten.

## Beobachteter Praxistest am 20.11.2026

In einer Referenzumsetzung wurde ein vom Betreiber durchgeführter Ausfall-/Wiederanlaufzyklus erfolgreich beobachtet. Dokumentiert werden hier nur das Verhalten und gerundete Zeitabstände, keine privaten Anlagenkennungen oder Originalmessdateien.

- Die Netzausfallmeldung kam auf dem Betreibertelefon an. Eine laufende Fahrzeugladung wurde einmal automatisch gestoppt; der Betreiber bestätigte den Stillstand und konnte sie anschließend bewusst manuell wieder starten, ohne erneuten Stopp durch dieselbe Ausfallregel. Diese ergänzende Fahrzeugfunktion benötigt eine eigene sichere Fahrzeugzuordnung und Freigabe; sie ist keine harte Wallboxabschaltung.
- Die sechs Programm-SoC-Ziele folgten dem fallenden Ist-SoC mit einem Prozentpunkt Abstand. Die abgesenkten Werte wurden am Gerät zurückgelesen.
- Bei der Netzrückkehr gab es eine Datenpause der Deye-Werte. HA bestätigte die Rückkehr deshalb erst ungefähr zwei Minuten nach der vom Betreiber gemeldeten mechanischen Zuschaltung. Die Ursache der Datenpause ist durch diesen Test nicht abschließend geklärt.
- **Die eingestellten zehn Minuten begannen erst mit dieser bestätigten HA-Erkennung.** Die tatsächliche Zeit ab mechanischer Zuschaltung war entsprechend länger. Eine Datenpause darf nicht rückwirkend als sicher bekannte Netzverfügbarkeit behandelt werden.
- Während des Wartens blieben alle sechs Ziele abgesenkt. Die Versorgung des Hauses aus dem Netz war erwünscht und ist von der Batterienachladung zu unterscheiden. Zuletzt war die Batterieleistung praktisch null; ein kurzer Ladewert in einer Übergangsminute wurde beobachtet. Eine vollständig ladungsfreie Übergangsphase wird daher nicht behauptet.
- Gut zehn Minuten nach bestätigter Erkennung gab HA die saisonale Reserve frei. Die sechs Programme wurden nacheinander zurückgestellt und vollständig zurückgelesen. Anschließend begann die deutliche Batterienachladung; der Betreiber bestätigte sie.

Damit sind diese Abläufe für diesen einzelnen Test praktisch belegt. Nicht separat getestet wurden unter anderem die wiederholte Ausfallmeldung nach 30 Minuten, der Generatorhinweis bei niedrigem SoC und der Empfang auf jedem weiteren Telefon. Keine allgemeine Firmwarekompatibilität, harte Ladesperre oder Verfügbarkeit bei beliebigen HA-, Internet- und Geräteausfällen daraus ableiten. Schutzgrenzen blieben unverändert.

## Optional: Notstromstatus an eine Community-Plattform

Nur nach konkreter Freigabe für Empfänger und Daten. Aktuelle Plattformspezifikation und tatsächlich ausgerolltes API-Schema lesen. [Ortsnetz-Auslastung](https://www.ortsnetz-auslastung.de/methodik#notstrom-und-netzausfallmeldungen) beschreibt eine ausdrückliche Clientmeldung „Notstrom aktiv“, keine unabhängige Bestätigung einer regionalen Störung.

Unterstützt die konkrete API `emergency_power_active`, dieses Signal ausdrücklich setzen und nach Netzrückkehr ausdrücklich beenden. Wenn echte 0 V abgelehnt werden, darf ein vom Betreiber freigegebenes technisches Sendesignal wie 0,1 V nur klar gekennzeichnet zusammen mit dem unterstützten Notstromstatus verwendet werden. Keine normale Unterspannungsmessung vortäuschen; echte HA-Messwerte bleiben unverändert. Fehlende Geräteverbindung niemals als 0 V oder als Notstrommeldung ausgeben. Bestätigung der Serverannahme, Kartenaktualisierung und tatsächlichen Ausfall unterscheiden. Quellen: [API-Schema](https://www.ortsnetz-auslastung.de/openapi.json), [Datenerfassungsprojekt](https://github.com/thomaslehmann1234/datenerfassung-ortsnetz-auslastung).

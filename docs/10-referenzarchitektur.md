# Referenzarchitektur für einen funktionalen Nachbau

Diese ergänzende Spezifikation beschreibt Bausteine, Datenverträge, Abläufe und sichtbare Ergebnisse. Sie ersetzt keinen lauffertigen Quellcode. Konkrete Herstelleradapter, HA-Versionen und Installationsdateien müssen für die Zielanlage implementiert und abgenommen werden. Eine optisch oder intern identische Kopie wird nicht zugesichert.

## 1. Abhängigkeiten und Bausteine

| Baustein | Liest | Liefert | Darf nicht |
| --- | --- | --- | --- |
| Quellenadapter | Tatsächliche Integrationsentitäten | Kanonische Einheiten, Vorzeichen, Quellenzeit und Status | Schutzparameter schreiben, fehlend zu0 machen |
| Qualitätsprüfung | Kanonische Zustände/Historie | Gemeinsame gültige Zeitfenster, Randband, Lücken | Gegenwartsfrische rückwirkend behaupten |
| Tagesabschluss | Zählergrenzen, Originalprognose, Qualitätsnachweis | Persistente datierte Energie-/Prognosefakten | Vorhersage nachträglich als Original erfinden |
| Bewertung | Fakten, datierte Preise, Modellversion | Kosten-/CO₂e-Komponenten und Salden | Rohenergie überschreiben, Nutzfaktor doppeln |
| Forecast | Gemeinsame abgeschlossene Basis und Annahmen | Szenario bis zu gewähltem Horizont | Fehlende Tage heimlich hochrechnen |
| Historienansichten | Fakten/Historie, ausgewählter Zeitraum | Diagramme, Teilwerte und Qualität | Hardware-Polling beschleunigen |
| WP/Wetter | Disjunkte elektrische Zähler und Stationsdaten | Tagesprofil, Monatsvergleich, Jahres-Excel | Innenenergie nochmals addieren, Heizstab behaupten |
| Archiv-/Backupwächter | Lokaler Rückstand, Fälligkeit, geprüfte Erfolge | Nachholauftrag, Warnung, Entwarnung | Schlafendes NAS ständig testen |
| Optionale Steuerung | Gesonderte Freigabe, frische Messwerte, bestätigte Grenzen | Begrenzte bestätigte Aktion | Aus einer Anzeige selbständig Gerätebefehle ableiten |

Gerätezugriff, Faktenerfassung, Geld-/CO₂e-Bewertung und Darstellung bleiben getrennt. Eine Dashboardkarte darf nicht nebenbei Tagesbuchungen auslösen. Vorhandene native HA-Energiedaten nicht für einen neuen Chart löschen.

## 2. Privates Quellenregister

Jede Rolle bekommt einen Eintrag mit:

- tatsächlicher Entität, physischem Stromkreis und Verhältnis zu anderen Summenquellen;
- Roh-/Zieleinheit und genau einer Skalierungs-/Vorzeichenregel;
- Erzeugung/Bezug/Ladung als ausdrücklich definierter Richtung;
- `state_class`, kumulativem oder periodischem Zählertyp und dokumentiertem Reset;
- belegbarer Berichtszeit, typischem Intervall und begründeter Frischegrenze;
- bekanntem Qualitätsbeginn und verfügbarem Historienzeithorizont;
- erlaubtem Ersatzpfad einschließlich Kennzeichnung und Unsicherheitsannahme.

Diese Zuordnung ist privat. Die öffentliche Vorlage enthält nur Rollen. Ein neuer Gerätename darf niemals still die alte kumulative Basis übernehmen. Gemeinsame Eingänge eines Wechselrichters und bereits darin enthaltene AC-Erzeuger als Überlappung markieren.

## 3. Datenverträge

Die folgenden Feldnamen sind ein Architekturvorschlag, keine bereits vorhandenen API-Endpunkte. Zu jedem Feld sind Typ und Einheit vor Implementierung verbindlich festzulegen.

### Messwert

`value`: Zahl oder null; `unit`: kanonische Einheit; `observed_at`: tatsächliche Quellzeit soweit vorhanden; `received_at`: Empfangszeit; `source_role`: neutrale Rolle; `quality`: gemessen/Teilwert/Ersatz/unbekannt; `reason`: maschinenlesbarer Grund. Keine erfundene Quellzeit, wenn nur die Empfangszeit verfügbar ist.

### Tagesfakt

`day`: lokaler Kalendertag; `timezone`: konfigurierte Zeitzone; `interval_start` und `interval_end`: eindeutige Zeitpunkte; `source_revision`: nachvollziehbare Quellenrevision; `algorithm_version`: verwendete Methode. Energiemengen pro disjunkter Rolle in kWh, ursprünglicher Prognosewert mit Zieltag und Snapshotzeit. Fehlende Mengen null statt numerisch0.

Qualität getrennt speichern: gültige/fehlende Zeit, verwendete Ersatzanteile, Randunsicherheit in kWh, Nachweisart und Freigabegrund. Ein durch kumulative Grenzen geretteter Energietag kann trotzdem eine Kommunikationspause enthalten. Eine pauschale Prozentabdeckung allein bildet diese Unterscheidung nicht ab.

### Bewertungsdatensatz

Verweist auf Tagesfakt und Modell-/Preisversion. Enthält PV-/WP-/BEV-Komponenten in EUR und kgCO₂e, ihre Summe, angewandte Referenzen und die bereits bewertete PV-Energie. Ein Prüffeld dokumentiert, an welcher einzigen Stelle der Nutzfaktor eingesetzt wurde. Brutto und bewertet als getrennte Felder, nicht als mehrdeutiges `energy`.

Eine rückwirkende Modelländerung erzeugt neue Ableitungen derselben Fakten. Historische Rohdaten und ursprüngliche Buchungsidentität bleiben erhalten. Eine Modellversion ist keine zusätzliche Investition und keine zweite Tagesersparnis.

## 4. Persistenz und Wiederanlauf

Mindestens Faktenspeicher, Preis-/Kostenjournal, Modellparameter und Zustandsautomaten dauerhaft speichern. Geeignete HA-Persistenz oder atomare Dateiablage mit Schema-/Versionskennung wählen. Nicht nur Templateattribute oder Browservariablen als Langzeitjournal verwenden.

Schreiben: validieren → temporär schreiben → konsistent ersetzen. Bei konkurrierenden Aufrufen eine Sperre; nach Neustart letzter konsistenter Stand. Eine Integritätskette kann Änderungen erkennbar machen, ist aber kein Ersatz für Backup oder fachliche Prüfung. Migrationen müssen wiederholbar sein und eine Sicherung des alten Schemas erhalten.

Idempotenzschlüssel beispielsweise aus Tag, Faktenrevision und Bewertungsrevision. Doppelte Timer-/Startaufrufe dürfen nicht doppelt buchen. Korrekturen nachvollziehbar mit Vorversion und Grund speichern, nicht still eine historische Summe verändern. Browser-Neuladen darf keine Buchungsaktion auslösen.

## 5. Prognose- und Tagesabschluss als Zustandsautomat

Zustände: `snapshot_fehlt`, `snapshot_vorhanden`, `tag_laeuft`, `abschluss_ausstehend`, `abgeschlossen`, `unbelegbar`. Fachlicher Status und technischer Fehler getrennt halten.

1. Vor Zieltag an konfigurierter lokaler Uhrzeit Folgetagsprognose atomar mit Zieltag ablegen. Bereits vorhandenen Original-Snapshot nicht mit späteren Updates überschreiben.
2. Während des Tages erforderliche Nachweise sammeln, soweit nicht bereits in vertrauenswürdiger Historie enthalten. Keine ungespeicherte Historienquelle rückwirkend unterstellen.
3. Nach Tagesende und begründetem Nachlauf reale gemeinsame Energiegrenzen prüfen. Abregelungs-/Ersatz-/Lückenstatus getrennt ermitteln.
4. Nur bei ausreichend belegtem Ertrag und passendem Snapshot Prozentfehler berechnen. Fehlender Snapshot bedeutet nicht fehlende reale Energie: die Energie kann unabhängig gültig sein.
5. Bei HA-Start und regelmäßiger Kontrolle begrenzt fehlende Abschlüsse nachholen. Keine unbeschränkte Rückwärtsschleife oder automatische Reparatur fremder Statistik.
6. Tag ohne belegbare Grenzen bleibt unbelegbar; bekannte spätere Zusatzdaten dürfen eine versionierte Neubewertung ermöglichen.

Sieben-/31-Tage-Auswertung verwendet jeweils das tatsächliche Fenster und dieselbe Qualitätsauswahl für Prognose und Ertrag. Den letzten abgeschlossenen Tag als klaren Standard wählen. Historisch ungeprüfte Vergleichswerte optisch und rechnerisch von geprüften Tagen trennen.

## 6. Kosten-/CO₂e-Modell konkretisieren

Vor Umsetzung ein einziges konsistentes Referenzszenario definieren: Welcher Netzstrom, Gasverbrauch und Kraftstoff wären ohne die Maßnahmen angefallen? Welche Investitionen, verbleibenden Gebühren und Erlöse gehören dazu? Szenarien und echte Rechnungen trennen.

### Eine mögliche additive Zuordnung

Bei einem ausdrücklich vereinfachten Modell werden WP-/BEV-Stromkosten zunächst vollständig zum selben Referenz-Strompreis belastet. Ein separat zugeordneter PV-Vorteil kompensiert gegebenenfalls darin enthaltenen Solarstrom. Dieser Anteil darf dann nicht zusätzlich als kostenloser WP-/BEV-Strom abgezogen werden.

- WP-Beitrag = Gasreferenzmenge × Gaspreis − WP-Strom × Strompreis.
- BEV-Beitrag = ersetzte Modell-Liter × Dieselpreis − BEV-Strom × Strompreis.
- PV-Beitrag = dokumentierter Wert der einmal bewerteten PV-Mengen nach gewählter Preis-/Nutzungsregel.
- Gesamtersparnis = Summe dieser drei Beiträge; zusätzliche tatsächliche Kosten separat datieren.

Alternativ eine vollständige Gegenfaktualbilanz aus Netzbezug, Einspeisung und Referenzverbrauch verwenden. Beide Modelle dürfen nicht unbemerkt gemischt werden. Insbesondere darf nicht derselbe Eigenverbrauch in zwei Komponenten als vermiedener Netzbezug erscheinen. PV-Erzeugung zum vollen Bezugspreis zu bewerten ist eine Vereinfachung und braucht eine sichtbare Begründung; Einspeisung hat gegebenenfalls eine andere Bewertung. Bei bereits gemessenen Nettomengen nicht nochmals dieselben Verluste abziehen.

CO₂e analog mit derselben Energiebilanz, jedoch eigenen Faktoren/Systemgrenzen. Eine kWh elektrischer Verbrauch ist keine kWh Gas. Wasser-/Heizwärme, elektrische Energie und Brennstoffenergie nicht gleichsetzen.

### Historie, Saldo und Forecast

Historische Pauschalphase und spätere tägliche Messphase mit Übergangsdatum und gesicherter Basis trennen. Keine Überlappung, kein neuer Nullstart aus Bequemlichkeit. Komponentenvergleich startet erst am gemeinsamen belegten Beginn der täglichen Methode. Die finanzielle Gesamtrechnung darf einen älteren separat gekennzeichneten Modellbeginn besitzen.

Kostenjournal: eindeutige ID, Datum, Betrag, Kategorie, Text und Vorzeichen. Alte Zusatzkostenmasken nicht als zweite aktive Buchungsquelle weiterführen. Preisjournal: Datum plus vollständige Preiskombination oder eindeutig definierte Feldänderungsregel. Neuester gültiger Preis bis zum nächsten Wechsel; unbekannte Zukunft nur als Szenario.

Falls ein Preis aus einer API kommt: gültiger frischer API-Preis → jüngster zulässiger Journalpreis → bewusst gesetzter manueller Ersatz. Herkunft/Alter anzeigen; gültigeNull nicht automatisch als Ausfall behandeln, sofern sie fachlich zulässig ist. Keine unvalidierten Extrempreise übernehmen.

Offener Saldo, Zinsbasis und Buchungsreihenfolge präzise definieren. Zinsen nicht gleichzeitig als eigener Kostenposten und erneut im Saldo berechnen. Für eine aktuelle Rate nur gemeinsame vollständige Tage verwenden; Fenster, Anzahl und enthaltene Schätzungen nennen. Fehlende Tage sind weder Nullersparnis noch automatisch ein Nennerbeitrag. Forecast bis zum gewählten Zieljahr mit datierten Energie-/Preis-/Strommixannahmen; kein positives Amortisationsdatum erzwingen, wenn die Rate nicht ausreicht.

Prozentanteile: gleiche Zeitgrenze für alle Komponenten. Bei nichtpositiver Summe oder negativen Komponenten eine Tabelle oder signierte Balken statt einer mathematisch irreführenden positiven Torte zeigen.

## 7. Konkrete Ansichten und Karten

| Ansicht | Zahlen zuerst | Diagramme / Bedienung | Erläuterung unten |
| --- | --- | --- | --- |
| Leistung | PV-Zweige, Haus/Netz/Batterie, WP-Status | Leistungsfluss und datierter Tagesverlauf | Messgrenzen, Frische, Vorzeichen |
| Energie | Tages-/Periodenmengen und Batterieübersicht | Energie-Sankey, Bedarfsdeckung, SoC1–7Tage, Monats-/Jahreswahl | Datenbeginn, Ersatzquellen, Teilmengen |
| Solarprognose | Aktuelle und Originalprognose, geprüfter Ertrag |7/31Tage und volle Kalenderjahrbreite | Fehlerdefinition, Anzahl gültiger Tage, Abregelung |
| Anlagenparameter | Globaler Nutzfaktor und gemeinsame Größen | Editierbare Parameter, datierte Journale | Quelle, Wirkung und Rückwirkung |
| Tablet | Status, PV, Speicher, Prognose | Leistungsfluss und Energie heute | Kompaktmenü mit Rückweg |
| Kosten-Burndown | Saldo, Amortisationsszenario, momentane Rate | Verlauf, Tageswahl, Komponenten und Kostenjournal | Preis-/Zins-/Verlustannahmen |
| CO₂e-Burndown | Saldo, Modellhorizont, momentane Rate | Verlauf, Tageswahl, Komponenten | Faktoren, Vorkette und Szenariogrenzen |
| Wärmepumpe | Status, optional freigegebene Offset-Bedienung, Gesamt-/Innenstrom und Wetter | Tagesprofil, Monatsvergleich, Jahres-Excel | Messgrenzen, Teilmittel, keine Heizstabbehauptung |
| Anlagenzustand | Quellen- und Abschlussstatus | Journal-/Archiv-/Backupnachweis | Letzter Erfolg und konkrete fehlende Nachweise |
| Ortsnetz optional | Frequenz und drei Spannungen | Unterstützte Empfehlungen und Übertragungsstatus | Mittelung, Zustimmung, keine automatische Netzsteuerung |

Die Tabelle beschreibt Funktionen, keine Pflicht zu denselben URLs oder einer bestimmten Kartenbibliothek. Bestehende benutzerdefinierte Karten nur nach Versions-/Lizenzprüfung einsetzen. Statische Texte dürfen auf dem Handy die Ergebnisbereiche nicht nach unten verdrängen. Timer aktualisieren vorhandene DOM-Strukturen und reservierte Ladeflächen; keine springenden Listen.

## 8. WP-/Wetter-Auswertung im Detail

Tagesgrenzen aus gewählter lokaler Zeitzone, nicht durch Addition fester24Stunden bilden. Elektrische Gesamtenergie und Innenenergie unabhängig prüfen; Innen gültig/Außen fehlend darf einen Innenwert bei leerer Summe ergeben. Keine Energie aus einem bloß unvollständigen Leistungsverlauf als volle Tagesenergie ausgeben.

Minutenkurven aus vorhandenen Zustandsintervallen zeitgewichten. Bereits bereinigte Teilphasen nicht erneut betragsbilden oder mit Totband versehen. Temperatur und Wind nur über ihre gültigen Zeiten mitteln; fehlende Quelle zerstört nicht automatisch die andere Kurve. Explizite Ausfälle als Lücke. Ein gehaltener gültiger Recorderzustand ist als gespeicherte Zustandszeit zu beschreiben, kein unabhängiger Geräte-Heartbeat.

Bei fehlender älterer Detailhistorie geeignete Langzeitstunden verwenden und Auflösung/Abdeckung nennen. Keine unkenntliche Mischung grober und feiner Daten im selben Ergebnis. XLSX-Methode darf stündlich sein, auch wenn Tagesdetailkurve minutengenau ist; dann Unterschiede erklären.

Export mindestens: Datum, Gesamt-kWh, Gesamtqualität, Innen-kWh, Innenqualität, Temperaturmittel, Temperaturabdeckung, Temperaturqualität, Windmittel, Windabdeckung, Windqualität und tatsächliche Tageslänge. Methodenblatt mit Einheit, Zeitzone, Quellenrollen und Unvollständigkeitsregeln. Fehler oder Abbruch einer Jahresabfrage darf keine scheinbar vollständige Datei liefern. Große Historie monatsweise nacheinander lesen. Download speichern, zurücklesen und auf dem Zielbrowser öffnen.

Herstellervergleich erst nach gemeinsam belegter Basis und vollständigem Monat. Jahressummenreset des Herstellers kann einen Grenzmonat sperren. Keine automatische Reparatur unbekannter Altdaten. Gasvergleich parallel und unabhängig; eigener Heizbedarf statt zirkulär aus demselben WP-Strom abgeleitetem „Beweis“.

Optionale Offsetsteuerung: [eigene Bau- und Abnahmespezifikation](11-wp-offsetsteuerung.md). Basiswert, Automatikschalter, Initialisierungsnachweis, Ziel, gemeldeter Offset, Sperrgrund und letzter Sendeversuch bilden eine getrennte Steuerschicht. Die WP-Auswertung bleibt davon unabhängig; keine Anwendung des PV-Nutzfaktors auf Offset oder WP-Strom. Bedienelemente im WP-Bereich, ausführliche Erläuterung dahinter.

## 9. Optionale Überwachung und Steuerung

Allgemeine Gerätestatusanzeige nur aus bestätigten Zuständen, nicht „Wechselrichter OK bedeutet sicher Netz vorhanden“. Netzverfügbarkeit braucht geeignete eigene Signale. Kommunikationsausfall ist nicht automatisch niedriger SoC, und restaurierte Werte sind kein neuer Notfall.

Wenn eine gesondert freigegebene Hausakku-Schutzfunktion umgesetzt wird: kritische gültige SoC-Unterschreitung, Wiederanlauf und gegebenenfalls erneut beginnende Heimladung prüfen. Nur ausdrücklich erlaubtes Fahrzeug-/Wallbox-Laden stoppen, Erfolg bestätigen; andere hohe Hauslasten nur melden, sofern so beauftragt. Fehlgeschlagene Befehle/Pushziele gezielt und begrenzt wiederholen. Hysterese und Rückkehrzustand benennen. Nicht bei jeder unveränderten Messmeldung eine lange Automation erneut starten.

Saisonreserve, technische Abschalt-/Wiederanlaufgrenzen und alle vorhandenen Zeitfenster erfassen, nicht aus einem fremden Beispielsatz übernehmen. Eine Community-Ladeempfehlung ist kein Schaltauftrag. Kalibrierung, Balancing und CAN-Zellauslesung bleiben separate herstellerabhängige Themen.

Archiv und Vollbackup haben getrennte Fälligkeit und Erfolgsnachweise. Retry-Zähler und Warnzustand über Neustart behalten. Entwarnung nach bestätigtem Nachholen, nicht nach bloßer Erreichbarkeit des NAS. Ein gültiger Hash bestätigt Dateitransport, nicht eine vollständige Rücksicherung des Systems.

## 10. Umsetzungsphasen und Liefernachweis

1. Privates Inventar, Messstellenplan und offene Zuordnungen; keine Geräteänderung.
2. Adapter-/Qualitätsschicht mit synthetischen und echten plausiblen Gegenproben.
3. Rein lesende Leistungs-/Energie-/Batterieansichten, mobile und Tablet-Abnahme.
4. Persistente Originalprognose und idempotente Tagesfakten mit Fehlerfällen.
5. Kosten-/CO₂e-Bewertung, Journale, Rückwirkung und belegbarer Forecast.
6. WP-/Wetter-Tagesprofil, voller Monatsvergleich soweit zeitlich möglich und tatsächlich geöffneter Jahres-Excel.
7. Ausgewählte Archive/Community/Überwachung nach ausdrücklicher eigener Einrichtung.
8. Regression, gesicherter Wiederanlauf, private Dokumentation und sichtbare Prüfgrenzen.

Jede Phase liefert Dateien, Konfigurationsweg, getestete Beispiele und normale UI-Nachweise. Eine später stattfindende erste Wochen-/Jahresausführung bleibt bis dahin unbeobachtet. Lokale und öffentliche Dokumentation nicht verwechseln.

## 11. Funktionsmatrix statt unzutreffender Kopiergarantie

Für jedes Modul festhalten: ausgewählt, Daten vorhanden, implementiert, fachlich getestet, live geprüft, offene Grenze. „Gleichartig“ ist erst erreicht, wenn die vereinbarten Bedien- und Rechenfälle mit anderen Entitätszuordnungen dieselben erwarteten Ergebnisse liefern. Eine exakt gleiche Grafik oder derselbe interne Programmcode ist dafür keine notwendige Bedingung und mit einem Prompt allein nicht garantierbar.

Eine spätere Veröffentlichung lauffähiger Referenzmodule benötigt zusätzliche Portierung, Parametrisierung, Lizenz-/Datenschutzprüfung und Tests auf mindestens einer zweiten Anlagenkonfiguration. Das ist ein weiterer Entwicklungsschritt, kein bereits ausgelieferter Bestandteil dieses Dokuments.

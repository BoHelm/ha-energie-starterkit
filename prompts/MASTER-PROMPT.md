# Master-Prompt: eigene Home-Assistant-Energieauswertung aufbauen

Diesen Text zusammen mit der ausgefüllten **privaten** Anlagenbeschreibung in einem eigenen lokalen KI-Projekt verwenden. Eckige Platzhalter und ungeklärte `null`-Werte sind Rückfragen, keine gültigen Messdaten. Du kannst Hersteller, Wechselrichter, Batteriegröße, Messgeräte, WP und Wetterstation in der Anlagenbeschreibung austauschen. Das Kit selbst enthält keine persönlichen Werte.

**Wichtig für den Nachbau:** Der Prompt ist der Einstieg in ein mehrteiliges Pflichtenheft. Lade das vollständige Repository herunter und stelle der KI den gesamten Ordner bereit. Nur diesen Text ohne die verlinkten Fachdateien einzufügen reicht für den spezifizierten Nachbau nicht aus. Die [Referenzarchitektur](../docs/10-referenzarchitektur.md) legt Bausteine, Datenverträge, Zustandsautomaten, Karten und Abnahmen fest. Das Ergebnis soll funktional gleichartig und an die Zielanlage angepasst sein; identischer Quellcode oder identische Darstellung werden nicht zugesichert.

---

Du unterstützt mich beim Aufbau einer zuverlässigen, verständlichen Home-Assistant-Energieauswertung. Arbeite auf Deutsch. Lies zuerst `AGENTS.md`, meine private Anlagenbeschreibung und alle zehn Fachdateien im Ordner `docs`, insbesondere `docs/03-module.md`, `docs/04-berechnungen.md`, `docs/05-datenqualitaet.md`, `docs/06-abnahme.md` und `docs/10-referenzarchitektur.md`. Prüfe vor Beginn, ob du diese Dateien tatsächlich lesen konntest. Wenn sie nicht bereitgestellt sind, nenne die fehlenden Dateien und beschaffe sie aus dem freigegebenen Repository; ersetze fehlende Spezifikation nicht durch frei erfundene Details. Erhalte bestehende Konfiguration und ergänze gezielt. Das Ziel ist eine an meine Anlage angepasste Implementierung, keine wörtliche Installation einer fremden Hauskonfiguration.

## 1. Arbeitsauftrag und Ergebnis

Erstelle gemeinsam mit mir PV-/Leistungs-/Energieansichten, Batterieauswertung, Solarprognose und Prognoseabweichung, Kosten- und CO₂e-Burndown, eine kompakte Tabletansicht sowie WP-/Wetter-Tagesanalyse. Optionale Module ausschließlich aus meiner Auswahl: Ortsnetz-Community, Archiv/Vollbackup, Anlagenzustand, Verlustdiagnose und Dachausbau-Szenario. Andere Hausfunktionen wie Anwesenheit, Kochgeräte, Teich, Kameras und allgemeine Raumsteuerung gehören nicht zum Auftrag.

Liefere Konfiguration/Code, verständliche Dokumentation und tatsächlich überprüfte Anzeigen. Ein Vorschlag oder ein gespeichertes YAML allein ist kein Fertigstellungsnachweis. Dokumentiere offene Grenzen und noch nicht beobachtbare automatische Abläufe ehrlich. Wenn Zugang oder Gerätequelle fehlt, erledige unabhängige Arbeit und nenne den konkreten fehlenden Schritt.

## 2. Zuerst Bestand aufnehmen, noch nichts verändern

Prüfe meine HA-Version, Integrationen und verfügbare Werkzeuge. MCP bedeutet nicht automatisch Zugriff auf sämtliche Konfigurationsdateien. Prüfe die tatsächlich angebotenen Fähigkeiten; keine Entitäten, Dienste oder Registeradressen raten. Bestimme einen nachvollziehbaren lesenden Zugang und einen bewusst freigegebenen Konfigurationsweg. Keine zusätzlichen Vollzugriffsserver allein aus Bequemlichkeit installieren.

Erfasse reale Entitätsrollen aus `docs/02-sensoren-und-parameter.md`: PV-Zweige mit Leistung und fortlaufender Energie; Netzbezug/-einspeisung und saldierte Leistung; Hauslast; Batterie; WP-Innen/Außen; eigene Wetterstation; Prognose; optional Wallbox und Herstellerzähler. Verifiziere Einheiten und `state_class` anhand der echten Zustände und Historie. Sensorname allein ist kein Nachweis der Richtung.

Erstelle eine Zuordnungstabelle mit Rolle, echter Entität, Einheit, Vorzeichen, physischer Messposition, typischem Berichtsintervall, verfügbarer Historie, Resetverhalten und Qualitätsgrenze. Erkenne, ob ein Total bereits einzelne Zweige enthält. Prüfe Quellenbrüche, Zählerwechsel und geänderte Verdrahtung. Frage nur die tatsächlich fehlenden kritischen Angaben ab; keine bestätigten Werte immer wieder erfragen.

Gib eine kurze priorisierte Bestandsanalyse. Noch keine Geräte-/BMS-/Netz-/WP-Sollwerte, Zeitfenster oder Schutzfunktionen verändern. Für Wechselrichter-/Batterieprofile offizielle modell- und firmwarepassende Unterlagen prüfen; fremde YAML-Dateien nur als unbestätigte Quelle behandeln.

## 3. Sicherheit, Datenschutz und Bestandsschutz

Zugangsdaten bleiben in lokalen Secrets beziehungsweise vorgesehenem Anmeldedialog. Keine Token, privaten URLs, Hostnamen, Serien-/MAC-Nummern, Wohnorte, GPS-Daten oder Originaldaten in öffentliche Dateien, Screenshots, Issues oder Commits. Auch Entitäts-IDs können Kennungen enthalten. Lokale private Dokumentation und öffentliche Vorlagen strikt getrennt führen. Keine Messdaten an Drittanbieter übertragen, solange Empfänger, konkrete Daten und Zustimmung nicht geklärt sind.

Vor wesentlichen Konfigurationsänderungen aktuelles HA-Backup prüfen beziehungsweise anlegen. Betroffene Dateien separat sichern. Tatsächliche Konfiguration ist maßgeblich, eine alte lokale Kopie kann veraltet sein. Kleinste passende Änderung vorbereiten, Syntax prüfen, speichern, zurücklesen und vergleichen. Vor nötigem Neustart native HA-Konfigurationsprüfung. Frontend-Neuladen und HA-Neustart unterscheiden. Nicht betroffene Karten/Automationen erhalten.

Alle vorhandenen Schutzfunktionen und Grenzwerte beibehalten. Technische Fähigkeit zu schreiben ist keine Beauftragung zu schreiben. Benachrichtigungsziele und Ruhezeiten erst bewusst wählen. Steuerung grundsätzlich aus; keine Netzladung/-einspeisung, Kalibrierung, Balancing-Haltezeit oder Abschaltung anderer Verbraucher aus Annahmen aktivieren. Bei später gesondert beauftragten Automationen Start/Stop-Bestätigung, Eigentümerflag, manuellen Vorrang, Frischeprüfung, Wiederanlauf und begrenzte Wiederholung vorsehen.

## 4. Gemeinsame Quellen- und Qualitätsschicht

Normalisiere jede Quelle genau einmal. Keine doppelte Faktor10-Korrektur, Betragsbildung oder Leerlaufbereinigung. Negative saldierte Netzleistung ist nicht automatisch falsch. Verwende echte Null und unbekannt als verschiedene Zustände; kein pauschales `float(0)` für unlesbare Daten.

Prüfe numerische Endlichkeit, Einheit, Richtung, restaurierte Werte, Quellenalter und gemeinsame Zeitfenster. Ein unveränderter Wert ist keine ausbleibende Meldung. Gegenwartszeitstempel nicht als historischen Nachweis verwenden. Bei kombinierten Leistungen nur gemeinsame gültige Abschnitte summieren. Fehlerhafte oder fehlende Quellen nicht durch größere Abfrageraten kaschieren. Geräte-/Cloudquoten und Modbus-Abfragezeit beobachten, bestehende Intervalle zunächst erhalten.

Für Energie kumulative Zählerdifferenzen an gemeinsamen Grenzen bevorzugen. Eine Übertragungspause ist nicht automatisch Energieverlust. Tagesgrenzen, Zählerreset und zeitliche Unsicherheit prüfen. Fehlende Leistung nicht beliebig integrieren. Ein ungefähr5%-Zeitfehlerbudget ist ein Richtwert, keine Garantie für gesamte Modell-/Messgenauigkeit. Bekannte freigegebene Ersatzwerte dürfen bleiben, mit Quelle, Dauer, Anteil und Unsicherheit. Echte Null nicht ersetzen.

Rechenergebnisse liefern neben Wert und Einheit immer Zeitraum und Qualität: gemessen, Teilwert, Schätzung oder unbekannt. Lieber keine Aussage als grob falsch. Fehlergrenzen nicht blind so streng wählen, dass belastbare Zählerbilanzen wegen kurzer Kommunikationspausen verschwinden.

## 5. Zentrale Anlagenparameter

Baue einen eigenen Reiter für global genutzte Parameter und Annahmen. Jeder Eintrag erklärt Bedeutung, Einheit, Herkunft, Gültigkeit und betroffene Rechnungen. Persönliche Tarifdaten bleiben lokal. Historische Preise als datierte Intervalle, Modellannahmen klar getrennt. Gegebenenfalls historische Investition, Betriebskosten, Energieträgerreferenzen, CO₂e-Systemgrenzen und Zinsszenario dokumentieren.

Ein editierbarer globaler PV-Nutzfaktor darf auf Wunsch rückwirkend die abgeleiteten Kosten-/CO₂e-Ergebnisse neu bewerten. Rohmessungen und ursprüngliche Tagesenergien bleiben unverändert. Bewertungsmenge klar benennen: brutto, bewertet/netto, gemessen oder geschätzt. Den Faktor ausschließlich einmal je definierter Bewertungsmenge anwenden. Keine Korrektur auf bereits netto gemessene Energie, WP-Strom, Batteriezyklen oder Prognose-Bruttovergleich. Verschiedene notwendige Wirkungsgrade nicht still als denselben Verlust ausgeben.

Keine fremden historischen Referenzverbräuche, Anlagenkapazitäten, Jahresbasen oder Brennstofffaktoren als meine Tatsachen übernehmen. Ungeklärte Parameter bleiben leer; Demo-Werte nie als Produktivwerte initialisieren. Editierbare historische Werte nicht durch YAML-`initial` bei Neustart überschreiben.

## 6. PV, Energie, Batterie und Tablet

Erstelle übersichtliche getrennte Leistungs- und Energieansichten. PV-Zweige getrennt und zusammen, Hauslast, Netz, Batterie und optionale Wallbox. Keine doppelte Summierung von Teilzweigen und Gesamtquellen. Sankey und Bedarfsdeckung mit expliziten Messgrenzen; Leistungsdiagramme inW/kW, Energiemengen inkWh/MWh. Historische Quellen und Messgrenzen erhalten.

Batterie: geladenMWh, äquivalente Vollzyklen aus passender Entladeenergie, Gesamt und Monat/Jahr, Monatsdiagramm mit Jahreswahl, SoH nur falls wirklich vorhanden. Inbetriebnahme, Gesamtzählerbasis und Historienbeginn unterscheiden. Startteilmonate nicht nachträglich voll machen. SoC für1–7lokale Tage mit Minutenauflösung aus vorhandener Historie, historische Mindestlinie. Gauge nutzt gültigen dynamischen MindestSoC als unteren Rand, Zahl bleibt absolut. Keine Geräteparameter verändern.

Baue die Tabletseite kompakt mit Status, PV, Speicher, Prognose, Leistungsfluss und Energie heute. Menüs ausblendbar und über sichtbaren Einstieg wiederherstellbar. Handy einspaltig: Zahlen/Diagramme oben, Erklärungen danach, Einstellungen unten. Pastellfarben pro Bereich, kontrastreiche Eingaben. Keine Scrollsprünge durch kompletten DOM-Neuaufbau bei jeder Meldung. Fokus, Auswahl, offene Listen und sinnvolle Kartenhöhe erhalten. Zielauflösungen wirklich testen.

## 7. Solarprognose und Abweichungen

Tagesvorhersage vor dem Zieltag zu konfigurierter Uhrzeit mit Datum/Quellzeit/Version unveränderlich festschreiben. Persistenter atomarer Snapshot. Neustart darf ihn nicht löschen oder eine spätere Prognose als Original deklarieren. Nur belegbare verpasste Abschlüsse begrenzt nachholen.

Vergleiche abgeschlossenen geprüften Brutto-PV-Ertrag mit dem Original für genau diesen Tag. Prozentformel und Vorzeichen aus `docs/04-berechnungen.md`. Bei Prognose0 keine Prozentzahl. Rollierende7/31Tage und Kalenderjahr über gemeinsame gültige Datensätze; absolute Tagesfehler, vorzeichenbehaftetes Mittel und energiegewichtete Periodenabweichung sauber benennen. Anzahl gültiger Tage und Lücken nennen. Abregelung separat, kein vermeintlicher Modellfehler aus absichtlicher Abschaltung.

Historische ungeprüfte Werte nur ausdrücklich getrennt anzeigen, nicht in geprüfte Mittelwerte mischen. Jahresgrafik volle Breite. Fehlende Tage als Lücke, nicht−100% wegen erfundener0Erzeugung. Keine nachträgliche Vollständigkeit behaupten, die damals nicht gespeichert wurde.

## 8. Kosten- und CO₂e-Burndown

Baue persistente idempotente Tagesjournale aus derselben bestätigten Energiegrundlage. Eigene Ansichten mit Saldo, Forecast, Tagesrechnung per Datumswahl, KomponentenPV/WP/BEV, kumulierter Summe und Anteilgrafik. Für Komponentenvergleich gemeinsamer Beginn belegter täglicher Daten; frühere Pauschalmodelle getrennt. Technische Ausfalltage separat zählen, Startvorlauf nicht als Ausfall. Unvollständiger Tag bleibt offen.

Kostenjournal für Reparaturen/Erweiterungen, keine parallelen alten Zusatzkostenmasken. Datierte Preisintervalle und tatsächliche Kosten berücksichtigen. Gasgrundgebühr nicht doppelt gutschreiben; noch gezahlte Gebühr gegebenenfalls gegensätzlich verbuchen. PV, WP und BEV brauchen konsistente Energiezuordnung, damit derselbe PV-Strom keine doppelte Einsparung erzeugt. Referenzfahrzeug aus BEV-kWh ist Modell, keine echte Fahrleistung.

CO₂e in passenden Einheiten und gleicher Gegenfaktualität. Vorkette, Gas-Brennwertbasis, Stromjahrfaktoren und zukünftige Szenarien sichtbar. Keine zweite Vorkette. Finanzielle/CO₂e-Amortisation nur bei definierter Investitions-/Herstellungsgrenze und gültiger Rate. Negative oder null Rate liefert keine erfundene Amortisationszeit.

Aktuelle RatenEUR/h beziehungsweisekgCO₂e/h aus aktuellen gültigen Leistungswerten. Anzeige alle paar Sekunden möglich, ohne Geräte zusätzlich abzufragen. Rate ist keine gebuchte Stundenenergie. Eine unabhängig belegte und ausdrücklich markierte PV-Nachtannahme0W ist optional; WP/BEV nicht fiktiv null setzen. Komponentenanteile bei negativen Beiträgen nicht als unpassende positive Torte ausgeben.

## 9. Wärmepumpe, eigene Wetterstation und Excel

Nutze die tatsächlich vorhandenen disjunkten Stromkreise. Gesamtenergie aus Innen+Außen, Innenenergie separat bereits darin enthalten. Ohne bestätigte Verdrahtung nicht „nur Heizstab“ nennen. Abtauvorgänge nicht aus Innenstrom allein beweisen. Herstellerwerte nicht ungeprüft anstelle der Stromzähler verwenden.

Herstellervergleich: Heizung+Warmwasser gegen elektrische Referenz im selben Zeitraum. Gemeinsame persistente Basis, Startteilmonat aus Monatsvergleich ausschließen, Rücksprünge/Jahresreset prüfen. Monatsabweichung und Gesamtabweichung aus Energiesummen derselben freigegebenen Monate. Keine Mittelung verschiedener Prozentbasen. Keine zusätzlichen Cloud-Refresh-Schleifen.

Erstelle einen Tageswähler und00–24Uhr-Diagramm mit Außentemperatur, zeitgewichteter Windgeschwindigkeit der eigenen Station und WP-Gesamtleistung. Keine Böen als Durchschnitt. Summen nur aus gültigen passenden Teilquellen. Tage mit23/25Stunden und lokale Zeit berücksichtigen. Temperatur, Wind und Leistung mit richtigen Achsen/Einheiten; keine unsichtbar abgeschnittene24-Uhr-Achse.

Darunter beziehungsweise darüber vier Tageszahlen: WP-Gesamtstrom, Innenstrom separat, mittlere Temperatur und mittlerer Wind. Alle verwenden denselben ausgewählten Tag. Vorhandene Kurvenabschnitte sichtbar lassen, unbekannte Abschnitte unterbrechen, keine erfundenen Nullen oder Verbindungen über Ausfälle. Wetter-Teilmittel mit Abdeckung zulassen und klar kennzeichnen. Unbelegbare WP-Tagesenergie leer lassen. Aktueller Tag nur Teilwert bis belegtem Zeitpunkt, nicht vollständiger Tag.

Jahresauswahl und Export der Tageswerte in echteXLSX. Alle Kalendertage, echte Excel-Daten und Zahlen, leere Zellen bei Unbekannt, numerische0bei echterNull. Energie/Temperatur/Wind/Innenstrom plus getrennte Qualitäts-/Abdeckungsfelder, Methodenblatt und Zeitzone. Stündliche Langzeitstatistik ist als solche auszuweisen, kein unabhängiger Beweis lückenloser Gerätekommunikation. Diagramm- und Exportbasis erklären und den tatsächlichen Download auf dem Zielgerät durch Öffnen/Zurücklesen prüfen.

Optional monatliches unabhängiges Gasvergleichsmodell parallel, Heizung und Warmwasser getrennt, lokale Messunterlagen/Koeffizienten. Keine fremde Heizgerade einsetzen. Nur Heizwärmemessung ohne Warmwasser nicht als Gesamt-JAZ ausgeben. Fenstereffekt ohne Messnachweis klar als Szenario. Bestehende Burndown-Rechnung nicht automatisch austauschen.

## 10. Archiv, Zustandsübersicht und optionale Community

Wenn ausgewählt: lokale Messdatenerfassung mit Aufbewahrung, tägliche Blockübertragung aufsNAS im zulässigen Fenster und separate wöchentliche HA-Vollsicherung. Keine Dauerabfragen des schlafenden NAS. Begrenzte persistente Retry-Versuche, Parallelitätssperre, Fehlwarnung bei Überfälligkeit/knappem Speicher und Entwarnung erst nach rückgelesenem Erfolg. Zeitfenster, lokale Reserve, Verschlüsselung und Wiederherstellungsschlüssel privat festlegen. Verpasste geplante Backups erkennen, selbst wenn kein Job gestartet war.

Anlagenzustand kompakt, ausschließlich lesend: Quelle/Frische, Tagesqualität, Journal, Archiv, Vollbackup und Speicher. Grün nur bei belegtem Erfolg. Keine unnötige Warnflut oder bei jeder Wertmeldung neu startende langlaufende Automation.

Ortsnetz nur nach eigener ausdrücklicher Auswahl und Zustimmung. Aktuelle Plattformspezifikation lesen, erlaubte Datenrollen bestätigen, Fünf-Minuten-Werte zeitgewichtet mitteln, Abdeckung und Quellenalter prüfen. Koordinaten/Registrierung ausschließlich lokal, nichts davon veröffentlichen. Lade-/Einspeiseempfehlung zunächst nur anzeigen; keine automatische3kW-Steuerung ohne gesondert bestätigte Gerätefähigkeit und Schutzkonzept.

## 11. Verluste, Simulationen und Modellgrenzen

Für Verlustdiagnose zuerst Zähler gegeneinander abgleichen. Gemeinsame Stunden-/Tagesenergiebilanzen, Batterieänderung, AC/DC-Grenzen, Skalierung und Zeitband prüfen. Signierter Rest bleibt Diagnose. Negative Reste nicht betragsbilden, positive Beschneidung erzeugt Bias. Ersatzwerte sichtbar. Keine kausale Effizienzaussage unterschiedlicher Schaltungen aus unsynchronen Leistungen oder nicht vergleichbaren Monaten. Dachausbau nur als klar abgegrenzte Simulation mit eigenen Annahmen, keine fehlenden Jahresdaten hochrechnen.

## 12. Prüf- und Abschlussverfahren

Arbeite in überprüfbaren Modulen, nicht als großer unkontrollierter Austausch. Implementiere zuerst Quellen-/Qualitätsbasis, dann Darstellung, dann Abschlüsse, Modelle und optionale Aktionen. Nach jedem Modul speichern, zurücklesen, Syntax/gezielte Tests und normale UI prüfen. Keine Tests, die nur die eigene Implementierung nacherzählen; teste fachliche Gegenbeispiele und Ausfälle.

Verwende den gesamten Katalog `docs/06-abnahme.md`: Datenlücke, echteNull, veralteter/restaurierter Wert, Einheiten-/Faktorwechsel, Zählerrücksprung, fehlende Tagesgrenze, Neustart, verpasster Lauf, Sommerzeit, Jahreswechsel, Startteilmonat, Doppelausführung und doppelter Verlustfaktor. Bestehende Schutzfunktionen unverändert nachweisen. Für Sicherungen Rücklesen und später unabhängige Restoreprobe unterscheiden.

Pflege private Projektdateien mit Datum, Zweck, Dateien, Entitätsrollen, Formel, Einheit, Annahme, Datenbeginn und Prüfergebnis. Öffentliche Dokumentation ausschließlich neutral. Am Ende: was funktioniert live, welche Dateien geändert wurden, welche Tests bestanden und was noch unbestätigt ist. Keine Erfolgsmeldung allein aufgrund einer Absicht, eines Klicks, einer gespeicherten Datei oder eines grünen Symbols.

## 13. Verbindlicher Umsetzungsplan und Schnittstellen

Erstelle zuerst eine Funktionsmatrix nach der Referenzarchitektur: je Modul Auswahl, Quellnachweis, Implementierung, Fachtest, Liveprüfung und offene Grenzen. Ein Häkchen bei „Datei gespeichert“ ist kein Häkchen bei „funktioniert“. Ohne echte gemeinsame vollständige Monatsdaten bleibt eine Monatsauswertung bis zum ersten vollen Monat leer, obwohl ihre Software bereits implementiert sein kann.

Trenne Quellenadapter, Qualitätsprüfung, persistente Tagesfakten, Geld-/CO₂e-Bewertung, Forecast und Darstellung in überprüfbare Bausteine. Ein Chart darf nicht nebenbei Tagesdaten buchen. Erzeuge keine zweite Gesamt-PV-Quelle, wenn die vorhandene Summe dieselben Zweige enthält. Erhalte Quellzeit und Empfangszeit getrennt; unbekannte Quellzeit nicht erfinden.

Plane für jede Messrolle Wert/Zahl-oder-null, Einheit, Zeit, Richtung und Qualitätsgrund. Tagesfakten enthalten lokalen Tag, eindeutige Grenzen, Energien je disjunkter Quelle, Originalprognose und Qualitätsnachweis. Bewertungen referenzieren Fakten und Modellversion. Zeige in einer Methodenansicht, welche Menge brutto und welche bereits einmal mit dem Nutzfaktor bewertet ist.

Entwirf atomare Persistenz mit Schema-/Versionskennung, Sperre gegen Parallelaufrufe und wiederholbarem Tagesabschluss. Nach Neustart dieselbe Datenbasis und keine doppelten Kosten. Eine Parameteränderung darf dieselben Rohfakten neu bewerten, aber weder neue Tagesenergie erfinden noch eine zweite Buchung verursachen. Korrekturen mit Vorversion/Grund dokumentieren. Ungeprüfte Altwerte bleiben als Altbestand erkennbar.

## 14. Präzise Bedien- und Rechenfälle

Liefere die Ansichten aus der Referenzarchitektur: Leistung, Energie, Solarprognose, Anlagenparameter, Tablet, Kosten-/CO₂e-Burndown und Wärmepumpe; Anlagenzustand und Ortsnetz nach Auswahl. Übernimm Funktionen und Bedienfälle, nicht private Original-URLs oder Gerätekennungen. Ergebnisse stehen auf dem Handy vor Erläuterungen; Datum/Jahr bleiben während Aktualisierung erhalten. Ein-/ausblendbare Tabletmenüs haben einen funktionierenden Rückweg.

Prognoseablauf: fehlender Snapshot, gespeicherter Original-Snapshot, laufender Tag, Abschluss ausstehend, abgeschlossen oder unbelegbar. Ein tatsächlich gültiger Energietag kann ohne Originalprognose dennoch gültige Energie haben; sperre dann den Prozentvergleich und nicht die unabhängige Energieanzeige.7-/31-Tage-Mittel haben getrennte Fenster und gemeinsame gültige Vergleichstage. Prozentzahl mit F0 bleibt leer; absolute Tagesabweichung darf sich nicht durch Vorzeichen aufheben.

Löse die Doppelzählung im Kosten-/CO₂e-Modell durch ein ausdrückliches Referenzszenario. Wenn WP-/BEV-Strom zunächst voll zum gleichen Referenz-Strompreis belastet wird, darf der zugeordnete Solarstrom nicht zusätzlich innerhalb der WP-/BEV-Komponente kostenlos gemacht und zugleich als volle PV-Ersparnis gutgeschrieben werden. Vor Umsetzung anhand eines gemeinsamen synthetischen Tages alle Teilbeiträge zur Portfolio-Gesamtersparnis abstimmen. Eine andere Gegenfaktualbilanz ist zulässig, muss aber konsistent umgesetzt und erklärt sein.

Ordne Preisquellen bei optionaler API zu: gültige frische API, gültiges datiertes Journal, bewusster manueller Ersatz. Herkunft und Alter anzeigen. Historische Perioden nicht rückwirkend zum heutigen Preis rechnen. Historische Pauschalphase und tägliche Messphase ohne Überlappung verbinden; der Komponentenvergleich verwendet nur den gemeinsamen täglich belegten Beginn. Signierte oder negative Beiträge nicht in irreführende positive Tortenanteile verwandeln.

WP/Wetter: Summe und Innenenergie getrennt validieren. Innen1kWh/Außen9kWh ergeben Gesamt10kWh und Innen1kWh; Innen allein kann bei fehlendem Außenwert sichtbar bleiben, die Summe bleibt dann offen. XLSX muss Innenenergie sowie getrennte Abdeckungs-/Qualitätsspalten enthalten. Explizite Ausfälle unterbrechen Kurven, Wetter-Teilmittel bleiben klar markiert. Zeitzone und tatsächliche Tageslänge gehören in die Auswertung.

## 15. Abschluss ohne übertriebene Nachbauzusage

Erzeuge einen ausführbaren Installations-/Migrationsweg für die konkrete Zielanlage, keine bloße Textbeschreibung. Nenne erforderliche Integrationen und Ressourcen, sichere vorhandene Stände und liefere einen gezielten Rückbau. Erzeuge ein privates Betriebsdokument mit Quellen, Formeln, Annahmen, Datenbeginn, Fehlerbehandlung und noch unbeobachteten geplanten Läufen.

Prüfe jeden ausgewählten Bedienfall mit der Funktionsmatrix und den fachlichen Gegenbeispielen. Wenn ein Modul wegen fehlender Sensoren oder Historie nur teilweise möglich ist, nenne die Einschränkung statt ein Ersatzresultat als exakt gleich auszugeben. Keine Behauptung einer pixelgleichen oder intern identischen Kopie aus einem Prompt. Ziel ist eine fachlich überprüfte gleichartige Energieanwendung mit den tatsächlich vorhandenen Geräten.

Beginne jetzt mit der **rein lesenden Bestandsaufnahme** meiner Anlage und den wichtigsten fehlenden Zuordnungen. Führe anschließend die freigegebenen Arbeiten eigenständig bis zur geprüften Umsetzung fort.

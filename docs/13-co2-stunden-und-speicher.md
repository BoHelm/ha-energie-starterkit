# CO₂-Stundenfaktoren und Vergleich von Netz und Haus

Optionale Erweiterung zur individuellen Umsetzung. Eine finanzielle Burndown-Rechnung, eine CO₂-Amortisationsrechnung und eine CO₂-Intensitätskurve beantworten unterschiedliche Fragen und dürfen nicht still dieselbe Bilanz ersetzen.

## API, Cache und Jahresmix

Für WP und BEV kann ein zeitlich passender Stromfaktor anstelle eines pauschalen Jahresfaktors verwendet werden. Als zu prüfender Anbieter dient [EnergieTakt mit API-Dokumentation](https://api.energietakt.de/); [Methodik und Systemgrenzen](https://www.energietakt.de/methodik-der-energietakt-karte/) vor Einsatz lesen. Verbrauchs- und Erzeugungsmix unterscheiden. Vorkette, Braun-/Steinkohle, Importmodell, Einheit und Zeitauflösung anhand der tatsächlich gewählten Datenreihe bestätigen. Keinen zweiten Vorkettenzuschlag auf einen vollständigen Faktor aufschlagen.

Ein gemeinsamer stündlicher Hintergrundabruf speichert abgeschlossene API-Stunden dauerhaft lokal. Dashboard, Tagesauswertung und Vergleichskurve lesen denselben Cache; sie lösen keine zusätzlichen Anbieterabfragen aus. Fehlerbehandlung, TLS-Prüfung, Quoten und zulässige historische Zeitspanne explizit prüfen. Lokale Daten beim fehlgeschlagenen Abruf nicht löschen. Ein Serverfehler darf keine neuen Nullfaktoren erzeugen.

Je Stunde benötigen wir Zeitraum, gültigen Faktor, Einheit, Status, Abrufzeit und Herkunft. Prognose-, Fehl- oder unplausible API-Werte sind kein bestätigter Istwert. Für jede fehlende oder ungültige Stunde gilt der konfigurierte Jahresmix genau dieses Jahres als gekennzeichneter Fallback. Auch dieser muss gültig sein, sonst bleibt die Aussage offen. Neue API-Korrekturen dürfen gespeicherte Ableitungen nachvollziehbar neu bewerten.

Ein letzter abgeschlossener Faktor ist nicht automatisch der aktuelle Faktor einer laufenden Stunde. Livekarten zeigen deshalb Zeitintervall und Alter des letzten API-Istwerts sowie separat den tatsächlich verwendeten Livefaktor. Veraltete Werte kennzeichnen.

## WP und BEV zeitgerecht bewerten

Emissionen = Summe(Stundenenergie × passender Stundenfaktor). Einheiten zuerst vereinheitlichen. Die Periodenintensität ergibt sich aus Emissionssumme / zugehöriger Energiesumme; nicht ungewichtet Stundenprozente oder Faktoren mitteln.

Ist nur eine Tagesenergie nachgewiesen, darf sie nicht ohne Kennzeichnung in beliebige Stunden aufgeteilt werden. Für eine solche Menge Jahresmix beziehungsweise ein ausdrücklich freigegebenes Zeitmodell verwenden und dessen Anteil anzeigen. Geschätzte Tagesenergie ist keine belegte stündliche Lastverteilung.

PV-Gutschrift und Zukunftsszenario der bestehenden CO₂-Amortisation separat beschreiben. Die Umstellung von WP/BEV auf Stundenwerte ändert nicht automatisch den dort gewählten Jahresmix für PV oder die Zukunft. Verlust-/Nutzfaktor nur einmal an seiner definierten Bewertungsstelle anwenden.

## Separate Ansicht „Netz & Haus“

Zeitraum Woche, Monat oder Kalenderjahr über Datum und Vor/Zurück wählen. Woche/Monat enthalten Tagespunkte, Jahr zwölf Monatspositionen. Künftige oder nicht belegte Bereiche bleiben leer. Für denselben gültigen Zeitraum anzeigen:

- Netzintensität und Hausintensität in g CO₂e/kWh mit deutlich verschiedenen Farben und eindeutiger Legende;
- Hausenergie und Emissionen, gültige/erwartete Stunden und Lücken;
- API-/Jahresmix-Anteil und separat angenommene Speicherherkunft;
- prozentuale Reduktion und eine ausklappbare Tages-/Monatstabelle mit Gründen.

Beide Kurven werden mit derselben Hausenergie auf denselben gültigen Stunden gewichtet. Die Netzkurve beschreibt die Emissionen bei vollständiger Versorgung dieses Hausverbrauchs aus dem jeweiligen Netzstundenmix. Sie ist kein ungewichteter Tagesdurchschnitt des Netzes.

Reduktion[%] = 100 × (Netzvergleich_kg − Hausmodell_kg) / Netzvergleich_kg. Nur bei positiver gültiger Vergleichsmenge berechnen. Negative Ergebnisse nicht auf null begrenzen. Bei Datenlücken gilt der Prozentwert nur für den gemeinsamen erfassten Anteil.

Die Bewertung eigener PV muss ausdrücklich gewählt werden: z.B. reine Betriebsbilanz mit 0 g oder ein begründeter Lebenszyklusfaktor. PV mit 0 g Betrieb gegenüber Netz inklusive Vorkette ist keine vollständige Lebenszyklusbilanz der eigenen Anlage. Herstellung und Ersatz von PV/Batterie dadurch nicht als berücksichtigt ausgeben.

## Herkunft der Batterie erhalten

Benötigt werden passende Energiegrenzen für Netz hinein/hinaus, Haus, disjunkte PV-Zweige, Batterieladung/-entladung sowie ein plausibler Speicherenergieanker. AC-/DC-Grenzen, Verluste und gleichzeitige Quellen erklären. Ein SoC-Stundenmittel ist kein genauer Energieinhalt am Stundenanfang. Stündliche Saldierung kann Lastwechsel und gegenläufige Flüsse verdecken.

Ein mögliches informatives Modell führt getrennt gespeicherte Energie und CO₂-Masse aus belegter Netzladung mit API-Faktor, Netzladung mit Jahresmix-Fallback sowie ungeklärter Herkunft. Ladung speichert die zugeordnete CO₂-Masse; Entladung gibt sie proportional weiter. Physikalisch nicht belegte Direktwege nicht als gemessen bezeichnen. Ein später sauberer Netzfaktor darf alte Netzladung nicht nachträglich sauber machen.

Bei einem gemeinsamen stündlichen Mischungsmodell lassen sich die Emissionen der Eingänge proportional auf Haus, Ladung und Export verteilen. Umwandlungsreste nur einmal berücksichtigen. Die resultierende Rechnung bleibt ein Modell und ersetzt keinen geeichten Verlustnachweis. Einen globalen pauschalen PV-Nutzfaktor nicht zusätzlich über die bereits bilanzierte Netz-/Hausenergie legen.

## Wahlpflicht: ungeklärter Speicherbestand

Unbekannter Anfangsbestand, Datenlücken oder positive SoC-Ankerkorrekturen beweisen keine Netzladung. Umgekehrt beweist ein hoher PV-Anteil nicht die Herkunft jeder Ladestunde. Vor Aktivierung eine lokale Betreiberentscheidung erfassen:

| Regel | Behandlung | Kennzeichnung |
| --- | --- | --- |
| Keine Herkunftsannahme freigegeben | Herkunftsabhängige Gesamtwerte offen lassen oder nur nachgewiesenen Teil ausweisen | Unbekannt / Teilwert |
| Jahresmix als konservativer Ersatz | Nur ungeklärten Anteil mit Jahresmix bewerten | Herkunftsmodell, kein API-Ausfall |
| PV-Annahme ausdrücklich freigegeben | Nur ungeklärten Anteil mit 0 g bewerten | Angenommene PV-kWh, kein Messnachweis |

Die PV-Annahme ist eine verfügbare Modellentscheidung und kein ungefragt übertragbarer Standard für andere Anlagen. Geltungsbeginn, Faktor, Grund und Modellversion zentral dokumentieren. API-Fallback für nachgewiesene Netzladung ist davon unabhängig.

Bei rückwirkender Änderung die ganze erforderliche Herkunftskette aus erhaltenen Stundenfakten erneut durchrechnen. Zum Geltungsbeginn nur die CO₂-Kategorie „ungeklärt“ neu bewerten. Bekannte Netz- und API-Fallback-Masse im Speicher unbedingt erhalten, auch wenn die Ladung vor dem Änderungsdatum lag. Nicht pauschal sämtliche Batterieemissionen löschen. Frühere Zeiträume nach der gewählten Geltungsregel unverändert lassen. Keine Energiewerte, Rohzähler oder Finanzjournalbuchungen verändern.

Ungeklärte Energie weiterhin als eigene kWh-Kategorie zeigen, auch wenn ihr angenommener CO₂-Faktor null ist. Solche Mengen nicht als gemessene PV-Ladung umbenennen. SoC-Ankerabweichungen können selbst zusätzliche ungeklärte Mengen erzeugen; Größe und Einfluss beobachten, statt jede Differenz als reale Netzladung zu behandeln.

## Speicherung, Lücken und Abnahme

Stundenfakten lokal dauerhaft halten, unabhängig von der Recorder-Aufbewahrung; nach Schreiben neu laden und vergleichen. Keine fehlenden alten Stunden aus Jahresmengen erfinden. Interne Ausfälle, ungültige Bilanz oder fehlende Pflichtquelle bleiben Lücken; spätere echte Stunden weiterverwenden. Vollständige Statistikstunden sind kein Nachweis lückenloser Unterstundenmessung.

Mit synthetischen Fällen prüfen: nur PV, nur Netz, gemischte Ladung, Netzladung bei hohem Faktor mit späterer Entladung bei niedrigem Faktor, fehlende API bei belegter Netzladung, Anfangsbestand, Herkunftsverlust nach Lücke, SoC-Korrektur ohne Ladeenergie, Kapazitätswechsel und ungültige Bilanz. Eine rückwirkende PV-Annahme darf ausschließlich die unbekannte CO₂-Kategorie ändern. Gemessene Energie, bekannte Netzanteile, Gültigkeit und Buchungsanzahl bleiben gleich. Sommerzeit und Jahreswechsel zusätzlich prüfen.

Siehe [Rechenregeln](04-berechnungen.md), [Datenqualität](05-datenqualitaet.md) und [Abnahme](06-abnahme.md).

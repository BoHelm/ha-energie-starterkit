# Verbindliche Rechenregeln

Alle Formeln benötigen benannte, zeitlich passende Messgrenzen. Einheit und Datenqualität gehören zum Ergebnis. Modellbeispiele sind keine geräte- oder lieferantenspezifischen Garantien.

## 1. Normalisierung und Energie

W→kW durch1000; Wh→kWh durch1000. Eine profilabhängige Skalierung erfolgt genau einmal im Quellenadapter, niemals später im Diagramm. Falsches Vorzeichen physisch klären; den Betrag nicht pauschal auf saldierte Netz-/Batterieflüsse anwenden. Ein für einen Verbrauchskreis begründetes Leerlauf-Totband gehört zentral in genau einen Adapter und nicht zusätzlich in jede Anzeige.

Für einen fortlaufenden Zähler: E=Stand(Ende)−Stand(Start). Nur valide gemeinsame Grenzen und nachvollziehbares Reset-/Zählerwechselverhalten. Ein interner Kommunikationsausfall kann durch fortlaufende Zähler überbrückt werden; fehlende Randstände nicht durch spätere aktuelle Stände ersetzen. Statistik-`sum`, Roh-`state` und `change` unterscheiden. In HA kann `sum` Resets normalisieren; bei einem Tag ohne gültige Grenzen dennoch keine Tagesenergie erfinden. [Offizielle Statistiksemantik](https://developers.home-assistant.io/docs/core/entity/sensor/#long-term-statistics).

Leistungsintegration: zeitgewichtete Fläche, Einheit korrekt, gültige Intervalle und Alter prüfen. Große Datenlücken nicht mit letzter Leistung überbrücken. Bei asynchronen Geräten gemeinsame Zeitfenster statt Summe verschiedener Zeitpunkte.

## 2. Prognosevergleich

Vorhersage F für TagD wird vorD zu einer konfigurierten Uhrzeit atomar mit Zieltag, Quellzeit und Modellversion gespeichert. Fehlender Snapshot bleibt fehlend; die inzwischen aktualisierte Prognose ist kein Original. Nach Neustart nur durch einen tatsächlich erhaltenen passenden Snapshot nachholen.

Tagesfehler[%]=100×(E_brutto−F)/F, nur beiF>0 und zulässigem Ertrag. Positiv=mehr Ertrag. F=0 oder fehlend ergibt keine Prozentzahl. Abregelung und Teilbeobachtung separat anzeigen.

Mittlere vorzeichenbehaftete Tagesabweichung=Summe Tagesfehler/n. Mittlerer absoluter Tagesfehler=Summe abs(Tagesfehler)/n, gegenläufige Fehler heben sich dabei nicht auf. Energiegewichtete Periodenabweichung=100×(SummeE−SummeF)/SummeF über dieselben gültigen Tage. Diese drei Größen unterscheiden und n sowie Zeitraum nennen. Nicht denselben Wert versehentlich für7 und31Tage referenzieren.

## 3. PV-Nutzfaktor genau einmal

Gemessene Bruttoenergie bleibt E_brutto. Bewertete Energie E_bewertet=f×E_brutto,0≤f≤1. Der Nutzfaktor ist eine Modellannahme für einen definierten Verlustanteil, kein Umbau des Messzählers. Bei einem bereits an der Nutzungsgrenze gemessenen Nettowert denselben Verlust nicht erneut abziehen.

PV-Messdiagramm, Prognosevergleich, Zählerbilanz, WP-Strom und Batteriezyklen verwenden keinen zusätzlichen Nutzfaktor. Kosten- und CO₂e-Bewertung verwenden die jeweils definierte bewertete PV-Menge einmal. Für rückwirkende editierbare Neubewertung Rohdaten unveränderlich erhalten, Ableitungen versionieren und neu berechnen; niemals dieselbe Tagesenergie doppelt buchen.

Synthetischer Test:10kWh brutto, f=0,90 →9kWh bewertet. Bei0,30EUR/kWh sind das2,70EUR, nicht2,43EUR. Eine aus einem Sankey bereits korrigierte Quelle darf nicht nochmals mitf multipliziert werden.

## 4. Kosten und Referenzen

PV-Wert aus dokumentierter Verwendung und Preisregel: vermiedener Bezug beziehungsweise Einspeiseerlös je passender Energiemenge. PV-Erzeugung ist nicht automatisch vollständig vermiedener Netzbezug. Bei Wechsel zu einer vereinfachten pauschalen Bewertung deren Grenze nennen. Netzbezug für Batterie-/BEV-Ladung oder WP nicht mehrfach berücksichtigen.

WP-Ersparnis in einem einfachen Referenzmodell: vermiedene Gas-kWh×Gasreferenzpreis−WP-Strom-kWh×Stromreferenzpreis. Ein fixes Gas/WP-Verhältnis ist ein Jahresmodell; täglicher temperaturabhängiger COP wird dadurch nicht bewiesen. Strom aus PV nicht zugleich als volle separate Einsparung und kostenloser WP-/BEV-Strom buchen. Gemeinsame Bilanz und explizite Zuordnungsregel erforderlich.

BEV: elektrische kWh→modellierte Fahrkilometer mit dokumentiertem Verbrauch→ersetzte Liter mit Referenzfahrzeug. Das sind Kilometeräquivalente, keine tatsächlich gemessenen Fahrkilometer; externes Laden und andere Ladeverluste beachten.

Gaspreis auf Brennwertbasis aus Rechnungen konsistent halten. Grundgebühr je Referenzjahr entweder inEUR/kWh umlegen oder separat führen. Noch tatsächlich bezahlte Anschlussgebühr ist nicht vermieden. Datierte Zusatzkosten nur einmal im Kostenjournal berücksichtigen.

Zins-/Opportunitätskostenmodell mit Basis, Vorzeichen, Intervall und ggf. Zinseszins dokumentieren. Finanzielle Amortisation bei nichtpositiver Rate oder zu kurzer Basis nicht erzwingen. Forecast verwendet erklärte Szenarien, keine Zusage.

## 5. CO₂e

Einheit kgCO₂e statt stiller Mischung mitg. Gas- und Dieselfaktoren mit Vorkette oder ohne, Brennwert/Heizwert und Herkunft dokumentieren. Keine zweite Vorkette auf einen bereits vollständigen Faktor aufschlagen. Stromfaktor zeitlich versioniert; zukünftige jährliche Reduktion ausdrücklich Szenario.

PV-/WP-/BEV-Komponenten müssen dieselbe Gegenfaktualität wie das Kostenmodell verwenden und dürfen dieselbe vermiedene Netzenergie nicht doppelt gutschreiben. Investitions-/Herstellungsemissionen separat; keine Lebenszyklusamortisation ohne entsprechende Systemgrenze behaupten.

## 6. Batterie und Netzbezug

Äquivalente Vollzyklen=Entladeenergie/passende nutzbare Referenzkapazität. Ladung nicht zusätzlich zählen. Monatszyklen aus Monatsenergie, nicht aus dem Sprung eines später importierten Lebensdauerzählers. Fehlende Monate bleiben unbekannt. Änderungen der Kapazität datieren.

Gaugewinkel=clamp((SoC−MindestSoC)/(100−MindestSoC),0,1), sofern gültigerMindestSoC<100. Angezeigte Zahl bleibt absoluterSoC. Fehlende Mindestgrenze sperrt dynamische Skalierung. Das verändert keine Batterieeinstellung.

Jahresbezug=amtlicher Jahresend-/Aktuellstand−bestätigte Basis desselben Jahres. Jahreszahl und Basis atomar speichern. Verpassten Jahreswechsel nur aus belegbaren historischen Grenzen nachholen; heutiger Stand ist keine Januar-Basis. Ein gekennzeichneter Gerätefallback braucht einen gültigen gleichjährigen Abgleich, Frische und begrenzte Unsicherheit.

## 7. Wärmepumpe und Wetter

Elektrische WP-Leistung=Summe disjunkter gültiger Stromkreise. Innenenergie ist Teil der Gesamtenergie. Herstellervergleich[%]=100×(HerstellerHeizung+HerstellerWW−ShellyGesamt)/ShellyGesamt, nur bei positiver Referenz und gemeinsamem vollständigem Zeitraum. Gesamtabweichung aus Energiesummen derselben gültigen Monate, nicht Mittelwert der Monatsprozente.

Zeitmittel=Summe(x_i×gültigeDauer_i)/Summe(gültigeDauer_i). Windgeschwindigkeit mitteln, nicht Böenmaxima oder Richtungen. Tageslänge aus lokaler Zeitzone, einschließlich Sommerzeit. Tagesmittel mit fehlenden Zeiten ist Teilmittel; Wetter-Teilmittel beweist keine Tagesenergie.

Eine Gas-Parallelrechnung muss unabhängige Wärmebedarfsannahmen verwenden. Heizung als lokal kalibriertes Temperaturmodell und Warmwasser separat. Gemessene Heizung ohne gemessenes Warmwasser erlaubt keine Gesamt-JAZ. Fenstereffekt ohne separate Messung nur Szenario, nicht nachträglich als gemessene Verbesserung einsetzen.

## 8. Verlustdiagnose

Signierter Bilanzrest=Zufuhr−Abfuhr in derselben Messgrenze und im gemeinsamen Zeitfenster. Gemeinsame Stunden-/Tages-Zählerbilanzen sind oft robuster als asynchrone Momentanleistung. AC/DC-Grenzen und Batterie-Energieänderung müssen passen. Bei Speicherung über Fenstergrenzen kann ein Rest auch Speicheränderung enthalten.

Negative Reste sind Diagnosen, keine negativen technischen Verluste. Permanentes max(Rest,0) erzeugt positiven Clipping-Bias. Ersatzwerte samt Energiebeitrag und Zeit kennzeichnen. Keine kausale Aussage „SchaltungA ist effizienter“ ohne vergleichbare Betriebsbedingungen, Meterabgleich, Standby-/Wandlungsgrenzen und Unsicherheitsband. AC-Durchleitung ist keine automatisch belegte Doppelwandlung.

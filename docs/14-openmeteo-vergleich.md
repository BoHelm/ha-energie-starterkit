# Zweites PV-Prognosemodell und fairer Vergleich

Optionale Spezifikation: den vorhandenen Prognosereiter als eigene Ansicht mit gleicher Bedienung ergänzen. Das bestehende Modell bleibt erhalten, bis ein belastbarer Vergleich eine Entscheidung erlaubt. Dieses Repository liefert keine fertig installierte Open-Meteo-Integration.

## Anlage in Teilflächen modellieren

Für jede physisch unterschiedliche Fläche getrennt erfassen: installierte kWp, Neigung, Azimut samt Winkelkonvention, Wechselrichterzuordnung, Leistungsgrenzen und bekannte Verschattung. Unterschiedliche Garagendächer nicht in eine einzige mittlere Neigung zwingen. Nennleistung und tatsächlich gemessene Spitzenleistung unterscheiden; eine beschattete Fläche verliert dadurch nicht ihre installierte kWp-Angabe.

Wetter-/Strahlungsdaten etwa über [Open-Meteo](https://open-meteo.com/en/docs) beziehen und mit einem geeigneten PV-Flächenmodell in Energie umrechnen. Strahlungsgrößen, Bezugsfläche, Zeitstempel, Temperatur-/Wandlungsmodell und Grenzen der Wetterauflösung dokumentieren. Niemals horizontale Strahlung ungeprüft als Strahlung auf einen senkrechten Zaun behandeln. Passende Nutzungsbedingungen, Quoten und Datenverfügbarkeit vor Einsatz prüfen; keine pauschale Zusage kostenloser oder genauerer Prognosen.

Nur die ausdrücklich freigegebene räumliche Genauigkeit an den Wetteranbieter übertragen. Gerundete Koordinaten sind weiterhin Standortdaten und gehören nicht ins öffentliche Repository. Die Rundung und ihre räumliche Unschärfe lokal erklären. Keine eigenen Verbrauchszeitreihen an einen Wetteranbieter senden.

## Korrekturfaktor und Verschattung

Beide Modelle erhalten zunächst denselben numerischen Prognose-Korrekturfaktor. In der Oberfläche denselben Faktor oder klar synchronisierte Eingaben zeigen; keine verdeckten voneinander abweichenden Startwerte. Dieser Prognosefaktor ist nicht automatisch der wirtschaftliche PV-Nutzfaktor. Faktoren mit unterschiedlichen Aufgaben getrennt benennen und jeden genau einmal anwenden.

Morgen-/Abendverschattung kann als editierbares Sonnenstands- beziehungsweise Horizontprofil modelliert werden. Ein an einem Beobachtungstag gesehenes Uhrzeitfenster in Sonnenhöhe/-azimut einordnen; kein ganzjährig starres Sommer-Zeitfenster verwenden. Nur belegte Verschattungsgrenzen übernehmen. Ein einfacher Schwellenwinkel ist keine vollständige dreidimensionale Schattenberechnung.

Diffusstrahlung nicht ohne Begründung vollständig streichen, wenn direkte Sonne abgeschattet ist. Wechselnder Blattschatten, Schnee und zeitvariable Hindernisse bleiben zunächst Unsicherheit oder benötigen zusätzliche Kalibrierung. Verschattungsprofil, Flächenparameter und Modellversion im Snapshot mitführen; keine rückwirkend angepasste Vorhersage als damaliges Original ausgeben.

## Unabhängige Vorhersagen festschreiben

Je Modell für denselben Zieltag einen vor dem Tag erstellten Snapshot speichern: Prognoseenergie, Erstellungs-/Quellzeit, Zieltag, Faktor, Modellversion und Parameterrevision. Bei einem Abruffehler den anderen Snapshot nicht als den fehlenden ausgeben. Nachträglich verfügbare Wetter-Istwerte sind keine damalige Day-ahead-Prognose.

Die Auswertung beginnt mit tatsächlich gespeicherten Vorhersagen. Fehlende alte Prognosen nicht aus dem aktuellen Modell oder gemessenem Ertrag rekonstruieren. Eine leere Anfangsperiode nach Einrichtung ist sachlich korrekt; Anzeige nennt den ersten erwarteten und ersten belegten Vergleichstag.

## Vergleich und Bedienung

Beide Modelle gegen denselben gültigen gemessenen Bruttoertrag vergleichen. Nur die Schnittmenge gültiger Originalprognosen und Ertragstage für eine Rangfolge verwenden. Einzelmodell-Zeiträume dürfen zusätzlich gezeigt werden, aber nicht als fairer direkter Vergleich mit unterschiedlichen Tagen.

Anzeigen: Originalprognose, Ertrag, Tagesfehler in Prozent, mittlerer absoluter Tagesfehler, energiegewichtete Periodenabweichung und Anzahl gemeinsamer Tage. Definitionen aus den [Rechenregeln](04-berechnungen.md) verwenden. Ein Medianverhältnis nahe eins kann trotz großer Tagesfehler entstehen und beweist allein keine hohe Prognosegüte.

Streudiagramm optional: X ursprüngliche Tagesprognose, Y gemessener Ertrag, 1:1-Linie, Zeitraum und Anzahl Punkte. Bei wenigen Tagen oder nur einer Saison noch kein allgemeines Sieger-Modell behaupten. Trainings-/Kalibriertage von einer unabhängigen Bewertung trennen.

Die neue Ansicht behält Datumswahl, 7-/31-Tage-Fenster und Kalenderjahrvergleich des bestehenden Reiters. Breite Diagramme sinnvoll über mehrere Spalten, mobil untereinander. Lange Texte unten; Eingabewerte in hellem und dunklem Theme lesbar. Automatische lokale Aktualisierung darf Fokus, Scrollposition und geöffnete Listen nicht zurücksetzen.

## Getrennte Qualitätsregeln

Informativ geschätzter Burndown-Ertrag ist kein gültiger Messbeleg für die Prognosegüte. Abregelung, fehlende Teilflächen, geschätzte Energie und unbekannte Messgrenzen getrennt ausweisen. Ein fehlerhafter Ertragssensor darf weder minus hundert Prozent erzeugen noch beide Modelle unbegründet gleich bewerten. Vorhandene echte historische Vergleichstage erhalten.

Abnahme: gemischte Neigungen, Winkelkonvention, Nacht, Sonnenfenster über Jahreszeiten, fehlende API, fehlender Snapshot, Ertragsausfall, Schätzanteile, gleiche Faktoren, identische Vergleichstage und 23-/25-Stunden-Tage prüfen. Ein Wechsel des kostenpflichtigen Anbieters wird erst nach einer gesonderten Entscheidung vorgenommen.

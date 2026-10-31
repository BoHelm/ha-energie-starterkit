# Sensorzuordnung und zentrale Parameter

## Private Anlagenbeschreibung

`config/anlage.vorlage.json` ist ein Fragebogen mit maschinenlesbarer Struktur. `null` bedeutet unbekannt oder noch nicht zugeordnet. Die Datei ist kein HA-Paket. In einer privaten Kopie lassen sich Hersteller, Integration, Batteriegröße und Messgeräte austauschen, ohne den Master-Prompt umzuschreiben.

Für jede Quelle sind zu erfassen: tatsächliche Entitäts-ID, Einheit, `state_class`, Vorzeichenkonvention, typische Berichtszeit, zulässiges Alter und physische Messgrenze. Der Zeitpunkt einer Wertänderung ist kein zuverlässiger Nachweis der letzten Gerätemeldung. `last_reported` nur verwenden, wenn die konkrete HA-Schnittstelle ihn tatsächlich liefert; eine historische Heartbeat-Reihe nicht aus dem aktuellen Zustand erfinden.

## Benötigte Rollen

| Rolle | Bedeutung / Prüfung |
| --- | --- |
| `pv_power[]` | Getrennte PV-Zweige in W, Erzeugung positiv nach einmaliger Normalisierung |
| `pv_energy[]` | Dieselben disjunkten Zweige als fortlaufende kWh; keine Summenquelle zusätzlich addieren |
| `grid_import_energy` | Bezugsregister des Netz-/Abrechnungszählers; Einspeisung separat |
| `grid_export_energy` | Einspeiseregister; keine automatische Vorzeichenannahme aus Namen |
| `grid_power` | Saldierte Netzleistung mit dokumentierter Bezugsrichtung |
| `house_power` | Last innerhalb bestätigter Messgrenze; bei wechselnder Verdrahtung Grenzen datieren |
| `battery_soc` / `battery_min_soc` | Tatsächlicher SoC und gültiger betrieblicher Mindestwert in % |
| `battery_charge_energy` / `battery_discharge_energy` | Getrennte kumulative Zähler; keine doppelte Zykluszählung |
| `battery_power`, `battery_soh` | Richtung / gemeldeter SoH prüfen; fehlender SoH bleibt leer |
| `wp_power[]` | Disjunkte Innen-/Außenphasen oder disjunkte Gesamtsensoren, niemals beides addieren |
| `wp_outdoor_energy` / `wp_indoor_energy` | Beide Stromkreise einzeln in kWh, keine Einspeiseregister |
| `wp_vendor_heating_energy` / `wp_vendor_hot_water_energy` | Herstellerwerte mit Zeitraum und Resetverhalten |
| `outside_temperature` / `wind_speed` | Eigene Wetterstation, °C und km/h oder einmal konvertierbare Einheiten; keine Böen als Mittelwind |
| `forecast_tomorrow` | Ertragsprognose in kWh und eindeutiger Zieltag |
| `bev_power[]` / `bev_energy` | Optional Wallbox, elektrische Energie ohne Annahme realer Fahrkilometer |

Die Größen der Arrays richten sich nach der wirklichen Anlage. Sechs WP-Phasen sind ein mögliches Beispiel, keine Vorgabe für jeden Hersteller. Ein vorhandener einzelner korrekt abgegrenzter Gesamtzähler ist vorzuziehen, wenn er dieselbe Größe verlässlich liefert.

## Zentrale Parameter

Ein gemeinsamer Reiter „Anlagenparameter“ enthält Kapazitäten, PV-Größen, Energieträgerreferenzen, Preiszeiträume und Modellannahmen. Bei jedem Wert: Einheit, Quelle/Begründung, Gültigkeitszeitraum und Wirkung. Historische Preisänderung und bewusst globale Modellneubewertung unterscheiden.

- `pv_usable_fraction`: Anteil zwischen0 und1, keine Prozentpunkte. Bei Verlustannahme L gilt f=1−L. Ein zentraler Wert, keine zweite versteckte Korrektur.
- Preise in EUR/kWh beziehungsweise EUR/L. Historische Preise als datierte Intervalle, heutiger Preis nicht rückwirkend einsetzen.
- Strom-/Gas-/Dieselfaktoren in kgCO₂e je passender Einheit, Systemgrenze und Brennwert/Heizwert dokumentieren. Keine persönlichen Rechnungswerte in diesem Kit.
- Gasgrundgebühr entweder als Teil des vermiedenen Referenzpreises oder separat modellieren; tatsächlich noch gezahlte Gebühren gegebenenfalls als datierte Kosten berücksichtigen. Doppelte Entlastung verhindern.
- Batterie-Kapazität: Nenn- und nutzbare Energie trennen; Zyklusdefinition konsistent mit dem Entladezähler.
- Frischegrenzen und zeitliche Unsicherheitsbudgets aus realen Aktualisierungen ableiten; ein willkürlich enger Grenzwert kann funktionierende Anzeigen sperren.
- Saisonreserve und Schutzschwellen gehören zur bestehenden Anlage. Sie werden erhoben, aber nicht aus diesem Kit übernommen oder geändert.

Tarife, persönliche Journale und Messreihen bleiben lokal. Die Demo ist frei erfunden und keine Empfehlung für Geräteschutz oder Wirtschaftlichkeit.

# Home Assistant Energie-Starterkit

Eine ausführliche Bauanleitung und ein anpassbarer KI-Arbeitsauftrag für eine eigene Energieauswertung in Home Assistant.

**Dies ist eine Spezifikation zur individuellen Umsetzung, keine fertige Integration und kein direkt installierbares Dashboard.** Geräte, Sensoren, Messgrenzen und verfügbare Historie werden pro Anlage geprüft. Das Kit enthält keine Konfiguration eines bewohnten Hauses und keine echten Messdaten.

## Was entstehen soll

- PV-Leistung und Energieflüsse, Autarkie und Netzbezug mit nachvollziehbaren Messgrenzen.
- Batterie: SoC, dynamische Mindestskala, Energie, äquivalente Vollzyklen und SoH, soweit nachgewiesen.
- Solarprognose: vorab gespeicherte Prognose, Tagesvergleich und sichtbare Datenqualität.
- Kosten- und CO₂e-Burndown: Tagesjournal, Komponenten, Preiszeiträume und editierbare Modellannahmen.
- Kompakte Tabletansicht, mobile Darstellung und einheitliche Pastellfarben.
- Wärmepumpe: Innen-/Außenenergie, optional Herstellervergleich, Heizung/Warmwasser als getrenntes Modell.
- Eigene Wetterstation: Außentemperatur und Wind im WP-Tagesvergleich, Tageswerte und Jahres-Excel.
- Optional: Ortsnetz-Community, Messdatenarchiv, HA-Vollbackup und Zustandsübersicht.

Andere Hausfunktionen wie Anwesenheit, Kochgeräte, Teich, Kameras oder Raumsteuerung sind nicht Bestandteil dieses Kits.

## Einstieg

1. [Einrichtung und Voraussetzungen](docs/01-einrichtung.md) lesen.
2. `config/anlage.vorlage.json` nach `config/anlage.private.json` kopieren und **nur lokal** ausfüllen. `null` bedeutet ungeklärt, niemals automatisch null Verbrauch.
3. [Messquellen zuordnen](docs/02-sensoren-und-parameter.md). `config/demo.json` zeigt ausschließlich frei erfundene Beispiele.
4. Den [ausführlichen Master-Prompt](prompts/MASTER-PROMPT.md) zusammen mit der privaten Anlagenbeschreibung im eigenen KI-Projekt verwenden. Private Dateien nicht in öffentliche Chats oder Issues kopieren.
5. Das vollständige Repository bereitstellen; die KI muss auch die [Referenzarchitektur](docs/10-referenzarchitektur.md) und Fachdateien lesen. Der Prompt allein genügt nicht.
6. Module einzeln umsetzen und mit dem [Abnahmekatalog](docs/06-abnahme.md) prüfen.

Der Prompt startet mit einer Bestandsaufnahme. Er darf fehlende Sensoren nicht erfinden und allein über MCP keine beliebige Konfigurations-Schreibfähigkeit annehmen.

## Orientierung

| Datei | Zweck |
| --- | --- |
| [Referenzarchitektur](docs/10-referenzarchitektur.md) | Bausteine, Datenverträge, Abläufe und konkrete Ansichten |
| [Module](docs/03-module.md) | Funktionsumfang und optionale Erweiterungen |
| [Rechenregeln](docs/04-berechnungen.md) | Energie, Prognosefehler, Geld, CO₂e, WP und Verluste |
| [Datenqualität](docs/05-datenqualitaet.md) | Fehlende/veraltete Daten, Teilwerte, Ersatzwerte |
| [Betrieb](docs/08-betrieb.md) | Archiv, Backups, Warnung und Wiederherstellung |
| [Datenschutz](docs/07-datenschutz.md) | Dateien und Git-Metadaten vor Veröffentlichung prüfen |
| [Grenzen](docs/09-status-und-grenzen.md) | Was dieses Repository tatsächlich liefert |

## Lokale Prüfung des Kits

Python 3 genügt, ohne Zusatzpakete:

```sh
python3 scripts/check_release.py
python3 -m unittest discover -s tests -v
```

Die Prüfung untersucht Dateien, Struktur, Links und typische sensible Muster. Sie ersetzt keine menschliche Prüfung und bestätigt keine Funktion einer später daraus erzeugten HA-Installation.

## Mitarbeit und Fehlerberichte

Nur synthetische Beispiele einstellen. Keine vollständigen HA-Diagnosen, Datenbanken, Backups, Konfigurationen, Original-Screenshots oder Messdaten veröffentlichen. [Beitragsregeln](CONTRIBUTING.md) und [Datenschutz](docs/07-datenschutz.md) beachten.

Lizenz der neu verfassten Texte und Vorlagen: [MIT](LICENSE). Externe Integrationen, Karten und Herstellerunterlagen behalten ihre eigenen Lizenzen; sie werden nicht mitgeliefert.

# Status, Lieferumfang und Grenzen

## Was vorhanden ist

Das Repository enthält eine detaillierte neutrale Funktionsspezifikation, einen ausführlichen Master-Prompt, einen Anlagenfragebogen, ein frei erfundenes Beispiel, Abnahmeregeln und lokale Prüfwerkzeuge. Es enthält keine komplette Home-Assistant-Integration, keine lauffertigen Lovelace-Dashboards und keine Beispiel-Geheimnisse. Es führt beim Download nichts auf der eigenen Anlage aus.

Die Spezifikation beruht auf praktischen Entwicklungs- und Prüfmethoden, ihre allgemeine Übertragbarkeit auf andere Hardware ist dennoch nicht automatisch nachgewiesen. Ein bestandener Repositorytest bestätigt weder ein fremdes Modbusprofil noch eine WP-Verdrahtung noch die Wiederherstellbarkeit eines NAS-Backups.

## Was „Nachbauen“ hier bedeutet

Der Master-Prompt muss gemeinsam mit allen zehn Fachdateien und der eigenen privaten Anlagenbeschreibung verwendet werden. Die Referenzarchitektur konkretisiert Datenverträge, Abschlüsse, Komponenten und Bedienfälle. Damit ist ein funktional gleichartiger individueller Nachbau spezifiziert. Eine exakt gleiche fertige Installation oder reproduzierbar identischer Quellcode wird mit diesem Kit weiterhin nicht ausgeliefert. Die KI muss die Software erst entwickeln und mit der Zielanlage abnehmen.

## Bewusste offene Grenzen

- Die richtige Skalierung, Frische und Messgrenze muss pro Gerät vor Ort geprüft werden.
- Eine jahresbezogene Gas/WP-Referenz ist kein Tages-COP. Eine temperaturbasierte Parallelrechnung benötigt eigene Kalibrierung und bleibt bis zur Validierung ein Modell.
- Signierte Bilanzreste sind keine belastbaren technischen Verluste ohne Zeitabgleich und gemeinsame Energiebilanzen. Ersatzquellen müssen erkennbar bleiben.
- Erfasste Statistikstunden beweisen keine vollständige Messung innerhalb jeder Stunde.
- Unbeobachtete alte Tage, fehlende Snapshots, Zellwerte und historische Monatsanteile sind nicht nachträglich erfindbar.
- XLSX-Dateien müssen nach individueller Umsetzung tatsächlich auf den Zielbrowsern heruntergeladen und geöffnet werden. Ein Link oder korrekter ZIP-Aufbau genügt nicht als End-to-End-Abnahme.
- Gezielt3kW Netzladung/-einspeisung, CAN-Zellauslesung und feste Balancing-Ladepläne sind keine zugesagten Standardfunktionen dieses Kits.
- Wetterdaten ersetzen keine Wärmemengenmessung. Innenstrom ist ohne Schaltplan kein reiner Heizstabverbrauch.
- Datenschutzprüfung ist regelbasiert plus manuell. Keine mathematische Garantie völliger Anonymität und keine Anonymisierung des GitHub-Profils.

## Weiterentwicklung

Erst je Anlage verlässliche Quellenbasis, dann Darstellung und Tagesabschlüsse, anschließend Modelle. Steuerungen benötigen einen eigenen Auftrag mit klaren Grenzen. Probleme reproduzierbar mit synthetischen Daten und ohne private Diagnosepakete beschreiben. Erkenntnisse zu einer konkreten Anlage bleiben in deren privater Dokumentation.

# Veröffentlichung ohne persönliche Anlageninformationen

## Inhalt des Starterkits

Nur neu verfasste neutrale Dokumente, Vorlagen, Prüfscripte und synthetische Beispieldaten sind vorgesehen. Keine reale HA-Konfiguration, Screenshots, Messreihen, Excel-Arbeitsmappen, Supportmails, Datenbanken, Logs oder Backups. Hersteller-/Produktkategorien sind austauschbare technische Angaben, keine Gerätekennungen.

## Was niemals ins öffentliche Repository gehört

Namen/Benutzerzuordnungen, E-Mail-Adressen, Straßen-/Postadressen, Telefonnummern, Koordinaten, Standortdateien, Kartenlinks oder Standortparameter. Ebenso interne/externe HA- und NAS-Adressen, private Hostnamen, MAC-/Seriennummern, Logger-IDs, OAuth-URLs, Kontokennungen, Pushziele, Tokens, Schlüssel und Passwörter. Verbrauchs-/Anwesenheitsverläufe können selbst ohne Namen private Informationen verraten.

Auch gerätespezifische Entitäts-IDs können Hardwarekennungen enthalten. Öffentliche Beispiele verwenden ausschließlich neutral benannte `sensor.demo_…` und `number.demo_…`. Echte Zuordnungen werden ausschließlich in ignorierten privaten Dateien gepflegt. Gegebenenfalls für eine Prognose oder Community benötigte Standortparameter nur lokal konfigurieren; keine realen oder gerundeten Hauskoordinaten mitliefern. Die Community-Übertragung bleibt bis zur eigenen Einwilligung ausgeschaltet.

## Technische Grenzen

`.gitignore` verhindert kein manuelles Hochladen, bereits getrackte Dateien werden dadurch nicht entfernt. Die automatische Prüfung erkennt typische Muster, keine beliebige personenbezogene Prosa oder in Zahlen versteckte Koordinaten. Deshalb zusätzlich jede freigegebene Datei lesen und eine explizite Dateiliste verwenden. Keine Verzeichnisse mit alten Arbeitsnachweisen pauschal übernehmen.

Dateiinhalte, Dateinamen, Dateimetadaten, Git-Autoren/E-Mails, Committexte, Branch-Namen und vorherige Commits prüfen. Ein neues Repository mit frischer neutraler Historie verwenden; alte Projektgeschichte nicht importieren. GitHub-Konto, Eigentümername, Profil und Aktivität sind unabhängig vom anonymen Dateiinhalt sichtbar, sobald das Repository öffentlich wird. Dieses Kit anonymisiert kein GitHub-Konto.

## Vorgehen für eine neue Veröffentlichung

1. Ausschließlich dieses frisch geprüfte Paket auswählen; keine privaten Quellen beimischen.
2. `python3 scripts/check_release.py` und Tests lokal ausführen.
3. Inhalt, Pfade, synthetische Herkunft und Links manuell kontrollieren.
4. Git-Autor neutral setzen, persönlichen Absender nicht aus globaler Git-Konfiguration übernehmen. Danach `git log --format=fuller` lokal prüfen; persönliche Ausgaben nicht als Prüfbericht hochladen.
5. Zunächst privat hochladen, Dateien und Historie auf GitHub zurücklesen und vergleichen.
6. Erst nach kompletter Prüfung bewusst veröffentlichen. Repositoryzugang ersetzt keine Einwilligung zu zusätzlich gefundenen persönlichen Daten.

Vorlagen bleiben im öffentlichen Bestand unverändert; ausgefüllte Anlagenbeschreibung wird nicht später eingecheckt. Für Beiträge dieselben Regeln anwenden. Wenn ein Geheimnis bereits veröffentlicht wurde, reicht Löschen im letzten Commit nicht: Zugriff sperren/Geheimnis rotieren und Historie angemessen bereinigen.

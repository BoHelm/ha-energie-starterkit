# Einrichtung und Voraussetzungen

## 1. Home Assistant bereitstellen

Home Assistant Green ist ein möglicher Einstieg mit vorinstalliertem Home Assistant OS. Strom und Netzwerk anschließen und dem aktuellen offiziellen Onboarding folgen. Ein funktionierendes vorhandenes HA-System kann ebenso verwendet werden; ein Neukauf ist dann unnötig. [Offizielle Green-Einrichtung](https://www.home-assistant.io/installation/green/).

Geräte zunächst mit ihren vorgesehenen Integrationen einbinden: Wechselrichter, Batterie, Energiezähler und optional Wärmepumpe und Wetterstation. Herstellerbezeichnung allein genügt nicht: Firmware, Registerprofil, physische Messposition und Einheiten müssen zur Anlage passen. Keine fremde Solarman-YAML blind aktivieren. [HA-Integrationsverzeichnis](https://www.home-assistant.io/integrations/).

Vor Konfigurationsänderungen vollständiges HA-Backup anlegen, Speicherort und Wiederherstellungsweg prüfen. Wiederherstellungsschlüssel privat sichern. Native Energieauswertung und kumulative Zähler zuerst plausibilisieren; erst dann eigene Modelle.

## 2. Codex beziehungsweise geeigneten KI-Arbeitsplatz einrichten

Die aktuelle offizielle Download-/Einrichtungsseite verwenden, anmelden und die im eigenen Konto verfügbaren Funktionen prüfen. Produktnamen, Oberflächen, Tarife und Zugriff können sich ändern; das Kit verlangt keinen fest benannten Tarif und verspricht keinen unbegrenzten Zugang. Keine API-Schlüssel allein zum Lesen dieses Kits anlegen. [Offizielle App-Dokumentation](https://developers.openai.com/codex/app).

Einen eigenen lokalen Projektordner für die Umsetzung anlegen. Dieses Repository hineinlegen beziehungsweise klonen. Private Anlagenbeschreibung getrennt von öffentlichen Vorlagen führen. Für eine individuelle Implementierung zuerst `prompts/MASTER-PROMPT.md` und die ausgewählten Module lesen lassen.

## 3. HA-MCP verbinden

MCP ist eine Verbindung zwischen KI-Werkzeugen und HA. Welche Aktionen tatsächlich verfügbar sind, hängt von Version, gewählter API und freigegebenen Entitäten ab. Vor Nutzung die angebotenen Werkzeuge prüfen. Ein erfolgreicher Lesezugriff beweist keinen Zugriff auf YAML-Dateien oder Lovelace-Raw-Konfiguration.

Die HA-Integration heißt **Model Context Protocol Server**. Gemäß eigener HA-Version über Einstellungen aktivieren, die dort angebotene Serveradresse privat kopieren und im lokalen KI-Client verbinden. Authentifizierung im eigenen Browser durchführen, Zugangsdaten niemals in den Prompt setzen. [Offizielle HA-MCP-Anleitung mit Codex-Beispiel](https://www.home-assistant.io/integrations/mcp_server/).

Für eine installierte Codex-CLI zeigt die offizielle Anleitung diese Form; der Platzhalter wird ausschließlich lokal ersetzt:

```sh
codex mcp add homeassistant --url '<DEINE_LOKALE_MCP_SERVER_URL>'
codex mcp list
```

Falls OAuth nicht automatisch startet, laut aktueller Clientanleitung `codex mcp login homeassistant` verwenden. Die exakte Callback-Adresse aus dem Client übernehmen, keine fremde Callback-Konfiguration kopieren. [Offizielle MCP-Clientdokumentation](https://learn.chatgpt.com/docs/extend/mcp).

Eine lokal erreichbare HA-Instanz nicht allein für dieses Kit öffentlich freigeben. Ein Cloud-Client benötigt gegebenenfalls einen anderen Erreichbarkeitsweg; das ist eine separate, bewusst zu planende Einrichtung. Lesezugriff für die erste Bestandsaufnahme bevorzugen. Geräte-Schreibrechte sind kein notwendiger Bestandteil dieser Dokumentationsvorlage.

## 4. Einen geprüften Konfigurationsweg bestimmen

Wenn MCP die benötigten Konfigurationsaktionen nicht bietet, vorhandenen HA-File-Editor oder den Raw-Editor bewusst verwenden. Nicht aus fehlenden Fähigkeiten heraus einen unkontrollierten Zusatzserver mit Vollzugriff installieren. Änderungen vorbereiten, relevante Originaldateien sichern, exakt speichern und zurücklesen. HA-Konfiguration prüfen, bevor ein dafür nötiger Neustart erfolgt. Frontend-Ressourcen benötigen häufig nur einen vollständigen Browser-Neuladevorgang.

## 5. In kleinen Schritten beginnen

Zuerst Bestandsaufnahme und rein lesende Anzeigen, dann Tageshistorie, anschließend Prognose und Modelle. Erst zum Schluss bewusst freigegebene Benachrichtigungen oder Steuerung. Pro Modul einen fehlenden und einen gültigen Datensatz testen. Details im Abnahmekatalog.

Stand der verlinkten Anleitungen für dieses Kit geprüft: 31.10.2026. Bei abweichender Oberfläche erneut die aktuellen offiziellen Seiten verwenden.

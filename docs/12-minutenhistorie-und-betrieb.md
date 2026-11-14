# Schnelle Livewerte, Minutenhistorie und robuster Betrieb

Erweiterung der Spezifikation. Diese Datei beschreibt einen umzusetzenden Entwurf; sie installiert keine Integration und enthält keine privaten Gerätewerte.

## Drei getrennte Datenwege

| Weg | Aufgabe | Speicherung |
| --- | --- | --- |
| Schnelle Originalzustände | Schutz, Geräteautomationen, aktuelle Leistungsanzeige | Nur benötigte Ereignisse und Quellen historisieren |
| Abgeschlossene Minuten | Leistungs-, Spannungs- und Stromverläufe, gemeinsame Auswertungen | Zeitgewichtete Werte samt Qualitätsnachweis |
| Energie und Ereignisse | Fortlaufende kWh, SoC, Alarme, Verbindungswechsel | Nach eigener Semantik; nicht pauschal drosseln |

Das Ausschließen einer Entität aus dem Recorder verlangsamt ihre Integration nicht. Eine Anzeigeaktualisierung ist keine neue Geräteabfrage. Schutztrigger niemals auf Minutenmittel umstellen. Auch ein negativer Batteriestrom oder eine echte Null bleibt erhalten. Ein zentraler Live-Schalter ist für diese Trennung nicht erforderlich.

Vor Änderungen alle Verbraucher einer Rohhistorie inventarisieren: eigene Karten, Tagesqualität, Ladeherkunft, WP/Wetter, Integratoren, native Energieansicht, Statistiken und Exporte. Originalhistorie erst ausschließen, wenn alle benötigten Verbraucher die neue Historie nachweislich lesen. Bestehende kWh-Integratoren nicht ungeprüft auf gemittelte Quellen umhängen.

## Vertrag einer abgeschlossenen Minute

Mindestens erfassen: Quellrolle, eindeutigen Intervallbeginn und -abschluss, Einheit, zeitgewichtetes Mittel, Minimum, Maximum, gültige Sekunden und ungültige Teilintervalle. Eine Stichprobe alle sechzig Sekunden ist ausdrücklich kein Minutenmittel.

Das Mittel lautet Summe(Wert × gültige Dauer) / gültige Dauer. Nur bei vollständiger zulässiger Abdeckung ist es ein vollständiges Minutenmittel; sonst separat bezeichnetes Teilmittel oder unbekannt. Überalterte, restaurierte und nicht verfügbare Werte niemals als Null integrieren. Reale unveränderte Meldungen nach ihrer nachgewiesenen Berichtssemantik behandeln. Eine Veröffentlichungszeit kurz nach Minutenende darf nicht als Messbeginn verwendet werden.

Bei W kann das zeitgewichtete Integral als Wh gespeichert werden. V/A-Werte erhalten kein irreführendes Energieintegral in Wh. Min/Max stammen aus den beobachteten schnellen Eingängen; sehr kurze ungemessene Spitzen sind damit nicht garantiert erfasst.

Gemeinsame Bedingungen wie „Batterie lädt und zugleich Netzbezug oberhalb einer Schwelle“ zuerst aus zeitlich passenden schnellen Eingängen bestimmen. Getrennte Minutenmittel können falsche Gleichzeitigkeit vortäuschen. Event- und Schutzgrenzen bleiben unabhängig davon unverändert.

## Historienwechsel ohne Datenverlust

- Pro Quellgruppe einen persistenten Umschaltzeitpunkt speichern. Später hinzukommende Spannungsquellen dürfen den früheren Leistungswechsel nicht verschieben.
- Ein zentraler Historienadapter verbindet alte Rohdaten vor dem Wechsel mit Minuten danach. Keine Überlappung oder Doppelzählung; bestehende Altdaten nicht löschen.
- Fehlende Minuten bleiben fehlend. Energiestatistiken nur aus geeigneten vollständigen Intervallen erzeugen; Summen, Zeitgewichtung und Einheiten nachrechnen.
- Statistikimporte je gemeinsamem Zeitfenster bündeln. Fortschritt erst nach bestätigtem Speichern fortschreiben; Neustart und begrenztes Nachholen vorsehen.
- Nur entbehrliche Diagnoseattribute aus der Historie nehmen. Abdeckung, Min/Max, Quellwechsel und Fehlerzustände für spätere Auswertungen erhalten. Liveattribute dürfen weiter vollständig vorliegen.

Neue Quellen müssen immer gemeinsam in Sammlung, Recorder-Regeln und Verbrauchern geprüft werden. Die maßgebliche HA-Statistik-Schnittstelle hängt von der installierten Version ab; keine interne Schnittstelle ohne Versions-/Parameterprüfung voraussetzen.

## Informative Tagesberichte trotz Ausfällen

Die folgenden Regeln gelten optional für informative Kosten-/CO₂-Tagesberichte. Strenge Prognosegüte, Schutzfunktionen und Rohdaten werden dadurch nicht gelockert.

1. Echte gültige Zählerdifferenzen bevorzugen. Ein Kommunikationsloch zwischen nachweislich passenden Randständen bedeutet nicht automatisch fehlende Energie.
2. Jede Komponente getrennt bewerten. Gültige WP-/BEV-Mengen behalten, auch wenn ein PV-Zweig unvollständig ist.
3. Nur den fehlenden Anteil nach einer vorab freigegebenen Regel ergänzen. Mögliche Stufen: begrenzte Fortschreibung letzter Leistung, datierte Prognose, geeigneter ungeschätzter Vergleichstag, zentrales Saison-/Jahresmodell.
4. Pro Stufe maximale Einzelpause, gesamte Tagespause, zulässige Randstände, Alter und Unsicherheitskennzeichnung festlegen. Keine universelle Zwei-Stunden- oder Fünf-Prozent-Garantie. Stark wechselnde Leistung benötigt eine andere Bewertung als stabile Nachtlast.
5. Keine Schätzungsketten. Kein unbegrenztes Warten auf Daten, die nicht mehr eintreffen werden. Zu große Lücken entweder leer lassen oder als ausdrücklich grobe Modellmenge führen, abhängig vom vorher vereinbarten Zweck.
6. Bereits in einer Integralenergie enthaltene Fortschreibung nicht noch einmal addieren. Gemessene, geschätzte und modellierte Anteile getrennt speichern und anzeigen.
7. Tagesabschluss idempotent und versioniert. Einzeltagfehler darf Folgetage nicht blockieren; alte Lücken vor dem aktuellen Cursor begrenzt erneut prüfen. Nach einer Lücke wieder echte Tageswerte verwenden.

Ein aus einer Prognose geschätzter Ertrag darf nicht dieselbe Prognose bestätigen. Rekonstruierte Tage aus dem unabhängigen Gütevergleich ausschließen oder getrennt ausweisen. Fehlende stündliche Geräteenergie lässt sich durch einen plausiblen Tageswert nicht in echte Stundenmessung verwandeln.

## SSD, Zweitsicherung und Ersatzgerät

Vor einer HA-Datenlaufwerk-Verschiebung die tatsächlich angeschlossenen Laufwerke eindeutig unterscheiden: physische Zuordnung, Größe, Serien-/Datenträgerkennung und aktiver Mount. Gleiches Modell oder eine identische Herstellerkennung reicht nicht. Formatierung und Datenverlust separat freigeben lassen. Unterstützten HA-OS-Migrationsweg der installierten Version verwenden, vollständiges Backup und Schlüssel vorhalten, während Migration nicht ausschalten.

Das Datenlaufwerk kann Recorder, Konfiguration, Apps und deren Schreiblast vom internen Datenspeicher verlagern. Boot-/Systemzugriffe und mögliche Restschreibvorgänge im internen Speicher verschwinden nicht automatisch. Tatsächliche Mounts und Schreibzähler prüfen, keine völlige Entlastung oder bestimmte Lebensdauer versprechen.

Eine zweite angeschlossene SSD ist kein automatischer RAID-Spiegel und kein bootfertiger Ersatz. Unterstützten Übertragungsweg gesondert bestimmen; täglich bestätigte vollständige Backups mit Aufbewahrung sind oft sinnvoller als eine laufende Blockkopie des aktiven Laufwerks. Dateien zurücklesen und Integrität prüfen. Eine dauerhaft angeschlossene Kopie schützt nicht gegen alle gemeinsamen Fehler; NAS oder getrennte Kopie ergänzen.

Für ein Ersatzgerät den Wiederherstellungsweg dokumentieren und auf einem isolierten Testsystem erproben. Keine zweite aktive Instanz derselben Steuerautomationen gegen die reale Anlage betreiben. Ein Backup auf zweiter SSD ist erst nach Prüfung der enthaltenen Konfiguration, Daten, Schlüssel und Wiederherstellung als Notfallweg nutzbar.

## Schreiblast und Netzwerkfehler prüfen

Physische Schreibzähler über längere vergleichbare Betriebsfenster messen, inklusive normaler Statistikläufe. Startphase, Backup, Datenbankbereinigung und Export separat notieren. Recorder-Zeilen, Attributvolumen und physische SSD-Bytes sind verschiedene Größen. WAL-/Checkpoint-Schreibvorgänge berücksichtigen. Nur gemessene Unterschiede berichten; keine Tageslast aus wenigen Sekunden hochrechnen.

Bei Ausfällen Router-/Repeater-Ereignisse, Geräteverbindung, gültige Minuten und HA-Neustarts zeitlich abgleichen. Gleichzeitige `unavailable`-Tracker können eine ausgefallene Routerintegration widerspiegeln, während direkte Shelly-Messungen weiterlaufen. Roamingmeldungen sind keine unabhängigen vollständigen Ausfälle. Regelmäßige Abstände begründen eine Hypothese, keinen bewiesenen Watchdog- oder Firmwarefehler. Logger-, Wechselrichter- und Repeaterfirmware getrennt identifizieren. Kein Reset, Update oder Pollingwechsel während einer ausdrücklich lesenden Prüfung.

Siehe [Betrieb und Sicherung](08-betrieb.md), [Datenqualität](05-datenqualitaet.md) und [Abnahme](06-abnahme.md).

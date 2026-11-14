# Änderungen der Spezifikation

## 2026-11-14

Diese Fassung erweitert die Bauanleitung; sie enthält weiterhin keine direkt installierbare Integration und keine private HA-Konfiguration.

- [Minutenhistorie und Betrieb](docs/12-minutenhistorie-und-betrieb.md): schnelle Live-/Schutzwerte von zeitgewichteten Minutenhistorien trennen, historische Verbraucher migrieren, Statistikimporte bündeln und Schreiblast belastbar messen.
- Informative Tagesberichte komponentenweise robuster gestalten: echte Mengen erhalten, nur fehlende Anteile nach ausdrücklich gewählter Regel schätzen, Schätzungsketten und doppelte Energie vermeiden. Strenge Prognosegüte bleibt getrennt.
- [CO₂-Stunden und Speicher](docs/13-co2-stunden-und-speicher.md): gemeinsamer stündlicher API-Cache, zeitgerechte WP-/BEV-Bewertung, Jahresmix-Fallback sowie separate Netz-/Hauskurven mit Prozentvergleich und nachvollziehbarer Batterieherkunft.
- Ungeklärte Batterieherkunft als explizite Wahlpflicht: eine freigegebene PV-Annahme darf rückwirkend gelten, ohne bekannte Netzladungen, Messdaten oder Finanzjournal zu verändern.
- [Zweites Prognosemodell](docs/14-openmeteo-vergleich.md): Flächenmodell, datenschutzbewusster Wetterabruf, Sonnenstandsverschattung und unabhängiger Vergleich zweier vorab gespeicherter Prognosen.
- SSD-Migration, zweite Backupkopie und isolierter Ersatzgerätetest als Betriebsanforderungen ergänzt. Regelmäßige Netzunterbrechungen anhand tatsächlicher Ereignisse prüfen; keine unbelegten Firmwarediagnosen übernehmen.
- WP-Tageszuschlag editierbar spezifiziert, zentrale Parameter/Annahmen und Auswahl eines Kalenderjahres mit zwölf Monatsbalken präzisiert.
- Master-Prompt, Verweise und Abnahmekatalog an die neuen Fachdateien angepasst. Veröffentlichungen bleiben auf neutrale Texte und synthetische Beispiele beschränkt.

## 2026-11-01

Optionale WP-Heizkurven-Offsetsteuerung mit manuellem Basiswert, Tagesfenster, ausdrücklicher Freigabe und Ausfallprüfung ergänzt.

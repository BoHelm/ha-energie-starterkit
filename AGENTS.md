# Arbeitsregeln für dieses Starterkit

- Arbeite auf Deutsch; erkläre Berechnungen verständlich.
- Dieses Repository ist eine Spezifikation, kein laufendes HA-System. Behaupte keine erfolgreiche Installation aus bestandenen Dokumenttests.
- Öffentliche Dateien enthalten nur neutrale Texte und synthetische Beispiele. Keine privaten Anlagen-, Personen-, Standort-, Netzwerk-, Geräte- oder Zugangsdaten übernehmen, auch nicht in Dateinamen, Git-Autoren, Logs oder Bildern.
- Private Anlagenbeschreibungen bleiben in ignorierten Dateien. Keine privaten Quellen als automatisch freigegeben behandeln.
- Bei Umsetzung zuerst tatsächliche Sensoren, Messgrenzen, Vorzeichen, Einheiten, Frische und Historie prüfen. Ungeklärt bleibt ungeklärt.
- Gerätebefehle, Schutzschwellen, Batterieparameter und Zeitfenster sind standardmäßig gesperrt. Auch vorhandener technischer Zugriff ist keine Freigabe.
- Fehlende Werte niemals still zu null machen. Bekannte Ersatzwerte als solche ausweisen. Qualitätsnachweis und Genauigkeitszusage unterscheiden.
- Verlust-/Nutzfaktor je Bewertungsmenge genau einmal; niemals auf rohe Messanzeigen oder WP-Strom anwenden.
- Vor jedem Upload `python3 scripts/check_release.py` und Tests ausführen; zusätzlich Inhalt und Commit-Metadaten prüfen.
- Nur explizit freigegebene Dateien übernehmen; niemals einen ganzen alten Arbeitsordner oder seine Git-Historie kopieren.

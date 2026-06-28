# Erfahrungsbericht: README fuer Programmdoku von Regenbogen

Zeitpunkt: 2026-06-20
Bezug auf Plan: `docs/plans/2026-06-20-readme-programmdoku.md`

## Kontext

Der erste Test nach Planfreigabe war kein Codeausbau, sondern die Erstellung
einer kanonischen Programmdoku fuer `Regenbogen`. Ziel war bewusst nicht das
Agenten-Metasystem, sondern das Beispielprogramm selbst.

## Beobachtungen

1. Der Programmkern ist klein genug, um ihn aus wenigen Dateien stabil zu
   rekonstruieren:
   - CLI / GUI
   - Use Case
   - Domain-Berechnung
   - Wetterport und Standortport

2. Der Glossarabgleich war fuer diese Doku hilfreich. Die wichtigsten Begriffe
   waren bereits explizit vorhanden:
   - `Wetterzustand`
   - `RegenbogenWahrscheinlichkeit`
   - `Sonnenstand`
   - `RegenbogenSichtbarkeit`
   - `WetterErgebnis`

3. Fuer Programmdoku reicht das Glossar in seiner aktuellen Form aus, obwohl
   einzelne Eintraege knapper sind als das formale Wunschschema der
   Glossardokumente.

4. Bestehende Projektdokumente sind inhaltlich verteilt:
   - `INSTALLATION.md` enthaelt nur Laufzeitvoraussetzungen
   - `regentropfen-und-wetterdaten.md` enthaelt eine kleine fachliche Notiz
   - `tutorial.md` ist Meta-Dokumentation der Agenten-Box

   Ohne `README.md` fehlte ein kanonischer Einstieg fuer Menschen, die nur das
   Beispielprogramm verstehen wollen.

## Was gut funktioniert hat

- Der Planschnitt war sauber. Programmdoku liess sich erstellen, ohne Produkt-
  code oder geschuetzte Agentendokumente zu aendern.
- Der Glossarabgleich hat verhindert, dass die README neue freie Begriffe
  einfuehrt.
- Die vorhandene Trennung zwischen `domain`, `system` und `infrastructure`
  hilft nicht nur Agenten, sondern auch menschlicher Programmdoku.

## Reibungspunkte

- Die Systemglossare enthalten mehr Formschema als die tatsaechlichen Eintraege
  derzeit voll ausfuellen. Fuer diesen Schnitt war das tolerierbar, aber bei
  strengeren Dokuaufgaben koennte daraus SP7-Druck entstehen.
- Ein Teil der Fehlersemantik ist allgemeiner als der aktuelle Demo-Stand:
  `OrtNichtGefunden` ist im System vorgesehen, waehrend die Demo-Standortquelle
  faktisch vor allem `PostleitzahlUnbekannt` liefert. Programmdoku muss diese
  Asymmetrie sauber formulieren.

## Lernwert fuer das Priming

Dieser Schnitt war ein guter erster Test, weil er zwei Dinge sichtbar gemacht
hat:

- Das System eignet sich nicht nur fuer Codeaenderungen, sondern auch fuer
  kontrollierte, semantikgebundene Dokumentation.
- Glossare sind bereits bei Dokuarbeit nuetzlich, wenn die Aufgabe an der
  Programmbedeutung haengt und nicht nur an Formulierung.

## Naechste Folgerung

Fuer kommende Iterationen lohnt sich eine bewusste Trennung zwischen:

- Programmdoku des Beispiels `Regenbogen`
- Agenten- und Priming-Doku der Box

Diese Trennung war vorher im Repo nicht stark genug sichtbar. Das neue
`README.md` schliesst genau diese Luecke.

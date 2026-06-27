# Sprechakt: Sekundärbogen — Fachbegriffe und Datenmodell

Aufgabe:          Sekundärbogen-Prognose (PLAN-2026-06-27-sekundaerbogen)
Zeitpunkt:        2026-06-27
Sprechakt-Klasse: SP1 — Neuer Fachbegriff würde entstehen
Betroffener Begriff / Grenze: Sekundaerbogen, SonnenstandsFaktorSekundaerbogen,
                               SekundaerbogenDaempfung, SekundaerbogenWahrscheinlichkeit
Status: festgelegt
Folgeartefakte: glossar-domain.md
Ersetzt:
Ersetzt durch:
Widerruft:
Freigabequelle: Dieter Haag, 2026-06-27 ("1. Option A / 2. Option A / 3. Abschwächungsfaktor")

## Was festgelegt wurde

```text
Begriff 1: Sekundaerbogen
  Kanonischer Fachbegriff für den äußeren zweiten Regenbogen.
  (Option A gewählt)

Begriff 2: SonnenstandsFaktorSekundaerbogen
  Geometrischer Faktor für den Sekundärbogen, Cutoff 51 Grad.
  Analog zu SonnenstandsFaktor (42 Grad) für den Primärbogen.

Begriff 3: SekundaerbogenDaempfung
  Physikalischer Abschwächungsfaktor: 0.57 (Sekundärbogen ist ca. 43 % schwächer).
  Wird auf die SekundaerbogenWahrscheinlichkeit multipliziert.

Begriff 4: SekundaerbogenWahrscheinlichkeit
  Neues Feld in PrognoseStunde (Option A gewählt).
  Typ: int, Wertebereich [0, 100], Default: 0.
  Berechnung: basis * SonnenstandsFaktorSekundaerbogen * SekundaerbogenDaempfung.
```

## Was der Agent danach tut

glossar-domain.md mit allen vier Begriffen ergänzen.
Plan PLAN-2026-06-27-sekundaerbogen auf in-arbeit / aktiv setzen.
Ausführung starten (Phase 2: Geometriefunktion).

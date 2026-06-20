# Erfahrungsbericht: MODELL-README und Framing fuer Modellarbeit

Zeitpunkt: 2026-06-20
Bezug auf Plan: `docs/plans/2026-06-20-modell-readme-und-framing.md`

## Kontext

In diesem Schnitt wurde ein neues `MODELL-README.md` eingefuehrt und per SP2
als Pflichtprojektion fuer kuenftige Modellarbeit in das Agenten-Framing
aufgenommen.

## Beobachtungen

1. Das Beispielprojekt hatte bereits genug fachliche Substanz fuer eine echte
   Modellbeschreibung. Die Begriffe lagen aber verteilt in:
   - Domain-Code
   - System-Ableitungen
   - Wetterport-DTOs
   - Tests

2. Die Trennung zwischen:
   - technischem Wetterfeld
   - systemischer Ableitung
   - fachlichem Modellbegriff

   war fuer diesen Schnitt entscheidend. Ohne diese Trennung waere das
   Modell-README leicht zu einer zweiten losen Begriffswelt geworden.

3. Die neue Regel musste so eingefuehrt werden, dass `MODELL-README.md`
   wichtig ist, aber nicht in Konkurrenz zu Glossar und Code tritt.

## Was gut funktioniert hat

- SP2 war der richtige Mechanismus. Es ging nicht um neuen Fachinhalt,
  sondern um eine neue verbindliche Arbeitsregel fuer Modellpflege.
- Das Framing liess sich mit kleiner Reichweite nachziehen:
  `AGENTS.md`, `AGENTS-COMPACT.md`, `preflight-checkliste.md`.
- Das Modell-README schafft einen neuen, klaren Lesepunkt fuer kuenftige
  Modelliterationen.

## Reibungspunkte

- Mehrere optische Unterbegriffe existieren bereits in Code und Sprechakten,
  aber nicht in gleich starker Form im Glossar. Fuer diesen Schnitt war das
  noch beherrschbar, weil das Modell-README diese Faktoren beschreibend und
  nicht als neue kanonische Einzelbegriffe eingefuehrt hat.
- Die Nummerierung der Preflight-Schritte musste angepasst werden. Das ist
  klein, aber ein gutes Beispiel dafuer, dass Framing-Aenderungen sofort
  mehrere gekoppelte Dokumente beruehren.

## Lernwert fuer das Priming

Dieser Schnitt zeigt einen wichtigen Unterschied:

- `README.md` erklaert das Programm
- `MODELL-README.md` erklaert das implementierte Modell

Diese Trennung ist fuer agentische Arbeit nuetzlich, weil Modellarbeit oft
nicht deckungsgleich mit Programmbenutzung ist.

## Folgerung

Fuer kuenftige Modellschritte sollte frueh geprueft werden:

- aendert sich nur Code?
- oder aendert sich das Modell?

Wenn sich das Modell aendert, ist `MODELL-README.md` jetzt ein verpflichtender
Bestandteil des Schnitts. Das ist eine gute Schaerfung gegen semantische Drift.

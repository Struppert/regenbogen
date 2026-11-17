# Erfahrungsbericht: Priming-Verbesserungen aus Systemanalyse (Abschlussdokument)

Datum: 2026-11-16 (nachträglich verfasst; Plan vom 2026-06-20)
Learning-Matrix-Kandidat: nein
  (ja wenn: HARD-Abbruch verursacht, oder ≥2 Sessions gleiches Muster,
   oder Mensch markiert als systemic — siehe learning-matrix.md §1a)
Vorgeschlagene Musterkennung: keine
Session-Typ:  Abschlussdokument bei der Bestandsverdichtung
Aufgabe:      Sieben Schwächen des Priming-Systems schließen (Plan `2026-06-20-priming-verbesserungen`)
Ergebnis:     Sechs von sieben Verbesserungen sind umgesetzt, eine ist überholt (V7)

---

## Hinweis zur Herkunft

Dieser Bericht ersetzt den fehlenden Erfahrungsbericht der Aufgabe. Er wurde bei der Verdichtung
der Pläne aus dem Plan, dem heutigen Repository-Stand und dem Template-Changelog verfasst. Was in
der damaligen Sitzung erlebt wurde, ist nicht rekonstruiert.

---

## Stand der sieben Verbesserungen (geprüft am 2026-11-16)

| Nr | Inhalt | Stand heute | Beleg |
|---|---|---|---|
| V1 | Bridge-Diff-Prüfverfahren, Warnblock | umgesetzt | `migration-bridges.md`: aktive Diff-Prüffragen, Warnblock "ACHTUNG FÜR AGENTEN". Bridge-Verletzung ist heute H3 (das Template ersetzte H2 durch H3 in v0.2.7) |
| V2 | Fast-Path für SICHER-Aufgaben | umgesetzt | `preflight-checkliste.md`, Abschnitt Risikoklassen-Weiche. Das Template führte später die 8-Punkte-Positivliste ein (v0.3.9) |
| V3 | Eintragstiefe im Glossarformat | umgesetzt | `glossar-domain.md`, `glossar-system.md` tragen das Feld Eintragstiefe. Im Template seit v0.2.7 |
| V4 | Metabegriffe in eigene Datei | umgesetzt | `glossar-meta.md` existiert, `glossar-system.md` enthält nur Produktbegriffe. Im Template vorhanden |
| V5 | H10-Erkennungsregeln | umgesetzt, verlagert | Im Template seit v0.2.7 präzisiert. Im Template v0.3.11 steht nur noch die Zeile "H10"; lokal stehen die vier Erkennungsregeln in `REGELN-UND-TOOLS.md`, Abschnitt H10-Erkennungsregeln |
| V6 | Muster-Schwelle der Learning-Matrix | umgesetzt | `learning-matrix.md`, Abschnitt 1a |
| V7 | Platzhalter-Block in `AGENTS-COMPACT.md` | überholt | `AGENTS-COMPACT.md` wurde mit der Migration auf v0.3.0 entfernt (Commit e4794c8) |

Die Abschlusskriterien des Plans sind damit bis auf V7 erfüllt. V7 entfiel, weil die Datei nicht mehr
existiert.

---

## Rückfluss

V3, V4, V5 (H10) und die Muster-Schwelle (V6) stehen im Template-Changelog v0.2.7. Sie sind dort
übernommen. V2 wurde im Template weiterentwickelt.

---

## Offene Fragen aus dem Plan

Der Plan fragte, ob V3 und V4 einen Sprechakt SP2 brauchen. In diesem Projekt liegt dazu kein
Sprechakt vor. Das Template hat beide Änderungen übernommen. Die Frage ist damit erledigt, ohne dass
ein Sprechakt entstand.

---

## Nicht-Ziel dieses Dokuments

Dieser Bericht ist kein Änderungsauftrag.

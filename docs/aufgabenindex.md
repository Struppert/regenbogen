# Aufgabenindex

> Ebene: REPOSITORY
> Rolle: dauerhafte Spur abgeschlossener Aufgaben, nachdem ihre Plaene und Checkpoints verdichtet wurden
> Geltung: dieses Projekt
> Autoritative Frage: Welche Aufgaben wurden abgeschlossen und wo steht ihr Ergebnis?
> Nicht zustaendig fuer: Plaene, Checkpoints, Begriffsbedeutungen

> Eine Zeile je Aufgabe. Die Zeile bleibt, wenn die Datei des Plans vor dem Merge entfernt wird
> (`aufgaben-lebenszyklus-protokoll.md`, Abschnitt Aufgabenindex). Das Abschlussdokument ist ein
> eigenes Dokument, dessen Form die Aufgabe bestimmt. Rückfluss-Status: LOCAL-ONLY,
> ERFAHRUNGSBERICHT, TEMPLATE-CANDIDATE, TOOLING-CANDIDATE, UNKNOWN, NO-RETURN.

| Plan-ID | Datum | Ziel | Ergebnis | Abschlussdokument | Rückfluss-Status |
|---|---|---|---|---|---|
| 2026-06-12-gui-einstiegspunkt | 2026-06-12 | Tkinter-GUI als zweiter Einstiegspunkt | GUI unter cli eingeordnet, Tkinter als optionale Plattformfaehigkeit dokumentiert | `.agent-box/evidence/erfahrungsberichte/2026-06-12-EB-gui-session.md` | UNKNOWN |
| 2026-06-13-sonnenstand-winkelmodell | 2026-06-13 | Regenbogen-Wahrscheinlichkeit um Sonnenstand erweitern | PLZ/Ort -> Koordinaten, Uhrzeit -> Sonnenstand, Sonnenstand -> Geometriefaktor | `.agent-box/evidence/erfahrungsberichte/2026-06-13-EB-sonnenstand-winkelmodell.md` | UNKNOWN |
| 2026-06-14-tropfenqualitaet-sichtbarkeitsmodell | 2026-06-14 | Optische Bedingungen und Sichtbarkeits-Score integrieren | Fachnotiz, neue Optikfaktoren, neue Tests | `.agent-box/evidence/erfahrungsberichte/2026-06-14-EB-tropfenqualitaet.md` | UNKNOWN |
| 2026-06-20-blickrichtung | 2026-06-20 | Das Programm soll sagen, in welche Himmelsrichtung man schauen muss. | abgeschlossen (Ergebnis im Abschlussdokument) | `.agent-box/evidence/erfahrungsberichte/2026-06-20-EB-blickrichtung.md` | UNKNOWN |
| 2026-06-20-echte-plz-bestimmung | 2026-06-20 | Die bisherige Demo-Standorttabelle soll durch eine echte PLZ-Bestimmung erweitert werden. | abgeschlossen (Ergebnis im Abschlussdokument) | `.agent-box/evidence/erfahrungsberichte/2026-06-20-EB-plz-bestimmung.md` | UNKNOWN |
| 2026-06-20-modell-readme-und-framing | 2026-06-20 | Ein neues `MODELL-README.md` im Projektroot einführen, das das aktuell implementierte Regenbogen-Modell erklärt: | abgeschlossen (Ergebnis im Abschlussdokument) | `.agent-box/evidence/erfahrungsberichte/2026-06-20-EB-modell-readme-und-framing.md` | UNKNOWN |
| 2026-06-20-priming-verbesserungen | 2026-06-20 | Sieben Schwächen des Agenten-Priming-Systems schliessen, die in `analysen/priming-analyse.md` identifiziert wurden. | sechs von sieben Verbesserungen umgesetzt, V7 überholt | `.agent-box/evidence/erfahrungsberichte/2026-11-16-EB-priming-verbesserungen.md` | ERFAHRUNGSBERICHT |
| 2026-06-20-readme-programmdoku | 2026-06-20 | Ein kanonisches `README.md` fuer das Beispielprojekt `Regenbogen` erstellen. | abgeschlossen (Ergebnis im Abschlussdokument) | `.agent-box/evidence/erfahrungsberichte/2026-06-20-EB-readme-programmdoku.md` | UNKNOWN |
| 2026-06-20-sonnenscheinanteil-begriffsklaerung | 2026-06-20 | Die aktuelle Ausgabe `Sonnenschein (25 %)` wird leicht als Sonnenscheinwahrscheinlichkeit verstanden. | abgeschlossen (Ergebnis im Abschlussdokument) | `.agent-box/evidence/erfahrungsberichte/2026-06-20-EB-sonnenscheinanteil.md` | UNKNOWN |
| 2026-06-20-tagesprognose | 2026-06-20 | Das Programm soll nicht nur die aktuelle Stunde bewerten, sondern alle Stunden des aktuellen Tages. | abgeschlossen (Ergebnis im Abschlussdokument) | `.agent-box/evidence/erfahrungsberichte/2026-06-20-EB-tagesprognose.md` | UNKNOWN |
| 2026-06-20-uv-projektkonfiguration | 2026-06-20 | `uv` fuer das Projekt einrichten. | abgeschlossen (Ergebnis im Abschlussdokument) | `.agent-box/evidence/erfahrungsberichte/2026-06-20-EB-uv-projektkonfiguration.md` | UNKNOWN |
| 2026-06-21-brownfield-migration-v0.2.3-to-v0.2.7 | 2026-06-21 | Die Agenten-Box dieses Projekts wurde am 2026-06-20 mit box-python v0.2.3 instanziiert. | abgeschlossen: Box auf v0.2.7 | `.agent-box/migrations/2026-06-21-v0.2.3-to-v0.2.7-migration.md` | ERFAHRUNGSBERICHT |
| 2026-06-21-glossar-domain-regenbogenwahrscheinlichkeit-vollstaendig | 2026-06-21 | Den Glossar-Eintrag `RegenbogenWahrscheinlichkeit` in `glossar-domain.md` von `Eintragstiefe: minimal` auf `Eintragstiefe: vollständig` upgr | Änderung durchgeführt, alle 7 Checks identisch grün wie Migrations-Baseline. | `.agent-box/evidence/erfahrungsberichte/2026-06-21-EB-glossar-regenbogenwahrscheinlichkeit-vollstaendig.md` | UNKNOWN |
| PLAN-2026-06-27-brownfield-v0.2.7-to-v0.3.0 | 2026-06-27 | Brownfield-Migration Fall B: Box-Versionsmigration von v0.2.7 auf v0.3.0. | abgeschlossen: Box auf v0.3.0 | `.agent-box/migrations/2026-06-27-v0.2.7-to-v0.3.0-evidence.md` | ERFAHRUNGSBERICHT |
| PLAN-2026-06-28-format-altbestand-bereinigung | 2026-06-28 | Den durch `ruff format --check . --exclude tmp` bestätigten Format-Altbestand in genau fünf unveränderten Bestandsdateien separat bereinigen | Format-Altbestand in fünf Dateien bereinigt (Commit 99f4e3a) | `.agent-box/evidence/erfahrungsberichte/2026-06-20-ABBRUCH-globaler-format-check.md` | UNKNOWN |
| PLAN-2026-11-16-dokumentstruktur-und-index | 2026-11-16 | Dokumentstruktur neu ordnen und Begriffsindex einführen (Plan A) | verworfen: Template v0.3.11 wurde Basis, die eigene AGENTS.md-Struktur entfiel; behalten wurden Begriffsindex, `check_begriffsindex`, Entwurfstool und `PROJEKT.md` (Migration Phase 7); der Sprechakt beschreibt die AGENTS.md-Aufteilung noch im alten Stand | `docs/sprechakte/2026-11-16-dokumentstruktur-und-begriffsindex.md` | LOCAL-ONLY |
| PLAN-2026-11-16-migration-v0.3.11 | 2026-11-16 | Box von v0.3.10 auf v0.3.11 migrieren | abgeschlossen: Box auf v0.3.11 (Phase 7 im Nachtrag) | `.agent-box/migrations/2026-11-16-v0.3.10-to-v0.3.11-evidence.md` | ERFAHRUNGSBERICHT |
| PLAN-2026-11-16-task-dokument-und-lebenszyklus | 2026-11-16 | Kurzform, Merge-Gate, Abschlussdokument und Aufgabenindex für Aufgaben-Artefakte einführen (Plan B) | abgeschlossen, Modellreview bestätigt 2026-11-17; Verdichtung der Pläne steht aus | `.agent-box/evidence/erfahrungsberichte/2026-11-16-EB-task-dokument-und-lebenszyklus.md` | TEMPLATE-CANDIDATE |
| PLAN-2026-11-16-kurz-bestandsverdichtung | 2026-11-16 | 15 abgeschlossene Altpläne verdichten (erste Anwendung der Kurzform) | 15 Pläne verdichtet, docs/plans von 22 auf 6 Dateien | `.agent-box/evidence/erfahrungsberichte/2026-11-16-EB-bestandsverdichtung.md` | TEMPLATE-CANDIDATE |

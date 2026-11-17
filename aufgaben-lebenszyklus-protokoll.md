# aufgaben-lebenszyklus-protokoll.md — Lebenszyklus der Aufgaben-Artefakte

> Ebene: PLAN/RUN
> Rolle: lokaler Pilot: Plan-Form, Run-Ende, Merge-Gate, Abschlussdokument, Aufgabenindex
> Geltung: dieses Projekt
> Autoritative Frage: Wie werden Pläne und Checkpoints geführt, abgeschlossen und vor dem Merge verdichtet?
> Nicht zustaendig fuer: Mandatsregeln, Checkpoint-Format, Sprechakte, Produktsemantik

> Lokale Ergänzung, kein Template-Dokument. Festgelegt im Sprechakt
> `docs/sprechakte/2026-11-16-lebenszyklus-aufgaben-artefakte.md` (L1 bis L5). Plan:
> `docs/plans/2026-11-16-task-dokument-und-lebenszyklus.md`. Rückfluss-Kandidat für das Template.
> Bei Widerspruch zu `AGENTS.md`, `ausfuehrungsmandat-protokoll.md` oder
> `docs/runs/checkpoint-template.md` gilt der Template-Text. Der Widerspruch ist Abbruch H3.

---

## 1. Problem und Geltung

Pläne und Checkpoints wachsen mit jeder Aufgabe. Das Template kennt keinen Abschluss und
keine Bereinigung dafür. Dieses Protokoll regelt, wie sie abgeschlossen werden und was vor dem
Merge in den Hauptzweig mit ihnen geschieht.

Voraussetzungen dieses Protokolls (Entscheidungen des Menschen):

```text
- Entwickelt wird in Feature-Branches. Der Punkt vor dem Merge ist die Stelle der Bereinigung.
- Gemerged wird mit Squash. Pläne und Checkpoints des Branches sind danach nicht mehr erreichbar.
  Es gibt keinen Archiv-Verweis und keinen Tag (L5).
- Pläne, Checkpoints und Run-Verzeichnisse sind branch-lokal. Sie dienen der Arbeit im Branch.
```

---

## 2. Plan-Form

Ein Plan hat die Form Kurz oder Voll. Das Feld `Plan-Form: Kurz` steht in der Kurzform.
Ohne das Feld ist es ein Vollplan.

Der **Vollplan** ist Pflicht, wenn mindestens eines zutrifft (L2):

```text
- Arbeitsprofil brownfield-migration oder governance-migration
- Interaktionsprofil autonom oder Recovery-Profil overnight
- eine geschützte Datei liegt im Scope
- ein neuer Begriff, Status oder eine neue Fehlerbedeutung braucht einen Sprechakt
- Schema-, API-, Dependency- oder Bridge-Änderung
- mehr als ein semantischer Schnitt (Task-Schnitt T2 oder T3)
```

Sonst genügt die **Kurzform**: `docs/plans/task-kurz-template.md`. Sie ist natürliche Sprache,
höchstens eine Seite und vom Menschen bestätigt. Sie führt Mandatsfelder, Scope,
Korrespondenzsatz oder `nicht anwendbar`, Testpflicht, Abbruchkriterien und das Feld
`Abschlussdokument`.

Abgrenzung:

```text
Direktauftrag:  kleine, vollständig bestimmte Fast-Path-Arbeit ohne Planartefakt. Nicht
                wiederaufnehmbar (ausfuehrungsmandat-protokoll.md). Bleibt unverändert.
Kurzform:       wiederaufnehmbare, kleine Arbeit, die die Fast-Path-Grenze verfehlt.
Vollplan:       alles, was ein Kriterium oben erfüllt.
```

Die Wahl der Form ist semantisch. Dateizahl und Zeilenzahl sind kein Kriterium.

---

## 3. Lebenszyklus

```text
Plan:        entwurf -> angenommen -> aktiv -> abgeschlossen -> verdichtet
Checkpoint:  draft -> sealed -> verdichtet
```

Der Zustand `verdichtet` bedeutet: Die Datei ist vor dem Merge aus dem Branch entfernt worden.
Es gibt ihn nur als Wirkung des Merge-Gates (Abschnitt 5). Der Plan-Status im Dokument bleibt
auf einem Wert des Plan-Templates (`angenommen`, `verworfen`), solange das Dokument existiert.

---

## 4. Run-Ende (Stufe 1)

Letzte Phase jedes Laufs mit Checkpoints:

```text
1. Der letzte Checkpoint hat Run-Status COMPLETED und Checkpoint-Status sealed.
2. Die Zwischen-Checkpoints dieses Laufs können entfernt werden. Der letzte bleibt bis
   zum Merge-Gate.
3. Was vom Lauf bleiben soll, steht im Abschlussdokument der Aufgabe (Abschnitt 6).
```

Entfernen versiegelter Checkpoints ist eine eigene Wirkung. Sie braucht ein Mandat mit der
genauen Dateiliste. Sie überschreibt keine Evidence. Die Checkpoint-Regel des Templates
bleibt unverändert (L3). Der Plan schneidet nur Phasen mit eigener Wiederaufnahmegrenze.
Interne Arbeitsschritte sind keine Phasen.

---

## 5. Merge-Gate (Stufe 2)

Das Merge-Gate ist eine Review-Checkliste (L1). Der Mensch geht sie vor dem Merge durch,
entscheidet und führt den Merge aus. Kein Checker in CI oder Branch-Schutz erzwingt sie.

```text
[ ] Alle Läufe des Branches sind COMPLETED oder gültig abgebrochen.
[ ] Keine Pläne mit Status entwurf, angenommen oder aktiv für offene Arbeit, keine aktiven Mandate.
[ ] Jede Aufgabe des Branches hat ihr Abschlussdokument (im Task-Dokument benannt) und es ist nicht leer.
[ ] Erkenntnisse sind gesichert: Erfahrungsbericht, Learning-Matrix-Kandidaten, Rückfluss-Status.
[ ] Sprechakte der Aufgabe liegen vor (append-only, bleiben erhalten).
[ ] Für jede Aufgabe ist eine Zeile im Aufgabenindex eingetragen.
[ ] Pläne, Zwischen-Checkpoints und Run-Verzeichnisse des Branches sind entfernt
    (Verdichtungs-Commit vor dem Merge, mit Mandat und Dateiliste).
[ ] Konsistenzcheck, Import-Check und Selbstcheck sind grün.
```

Die Verdichtung läuft nach dem Abschluss des Plans. Sie ist kein Teil des Plans, der entfernt
wird. Das Werkzeug `tools/verdichte_aufgaben.py` erzeugt dafür einen Entwurf nach `tmp/`
(Kandidatenliste, Indexzeilen). Es entfernt nichts.

**Verweise auf entfernte Pläne.** Versiegelte Dokumente (Sprechakte, Erfahrungsberichte,
Migrationsevidence) nennen Pläne per Pfad. Nach dem Entfernen bleiben diese Verweise stehen, denn
versiegelte Dokumente werden nicht geändert. Die Plan-ID im Aufgabenindex löst sie auf. Der Pfad
enthält Datum und Name der Plan-ID. Das Entwurfstool zählt die betroffenen Verweise.

**Squash.** Mit Squash gehen die entfernten Pläne und Checkpoints bewusst verloren. Der
Abschlussbericht und der Aufgabenindex müssen ohne sie verständlich sein.

---

## 6. Abschlussdokument

Für jede Aufgabe entsteht ein eigenes Abschlussdokument. Das Template schreibt weder Name,
Ort, Inhalt noch Form vor. Die Aufgabe bestimmt sie. Das Task-Dokument benennt es im Feld
`Abschlussdokument` (Pfad, Zweck, Form).

Prüfung: Existenz und Nichtleere. Der Inhalt wird nicht bewertet. Der Checker meldet ein
fehlendes oder leeres Abschlussdokument nur als Hinweis.

---

## 7. Aufgabenindex

`docs/aufgabenindex.md` führt je Aufgabe eine Zeile:

```text
Plan-ID | Datum | Ziel in einer Zeile | Ergebnis | Abschlussdokument | Rückfluss-Status
```

Die Zeile bleibt, wenn die Datei des Plans entfernt wird. Sie ist die einzige dauerhafte Spur
des Plans im Hauptzweig neben dem Abschlussdokument. Rückfluss-Status:
`LOCAL-ONLY | ERFAHRUNGSBERICHT | TEMPLATE-CANDIDATE | TOOLING-CANDIDATE | UNKNOWN | NO-RETURN`.

---

## 8. Nie entfernt

```text
- Sprechakte (append-only, klein)
- Erfahrungsberichte und Migrationsevidence
- offene oder aktive Pläne und deren Checkpoints, solange der Feature-Branch lebt
- abgebrochene Läufe ohne abgeschlossenen Wiedereinstieg
- Mandate bis zum Abschluss
```

---

## 9. Verhältnis zu anderen Dokumenten

```text
ausfuehrungsmandat-protokoll.md   Mandat, Direktauftrag, Arbeitsmodus. Unverändert.
docs/plans/template.md            Vollplan. Unverändert.
docs/plans/task-kurz-template.md  Kurzform (lokal, neu).
docs/runs/checkpoint-template.md  Checkpoint-Lebenszyklus. Unverändert (L3).
korrespondenz-protokoll.md        Korrespondenzsätze gelten auch in der Kurzform.
regelmatrix.md                    Schreibrechte; Entfernen versiegelter Checkpoints braucht Mandat.
sprechakt-protokoll.md            Sprechakte bleiben append-only und werden nicht verdichtet.
```

---

## 10. Schlussregel

Pläne und Checkpoints sind Arbeitsmittel des Branches, keine Projektwahrheit. Was bleiben soll,
steht im Abschlussdokument, im Aufgabenindex, in Sprechakten und in Erfahrungsberichten.

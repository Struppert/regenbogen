# Erfahrungsbericht: Brownfield-Migration v0.3.10 -> v0.3.11

Datum: 2026-11-16
Learning-Matrix-Kandidat: ja
  (ja wenn: HARD-Abbruch verursacht, oder ≥2 Sessions gleiches Muster,
   oder Mensch markiert als systemic — siehe learning-matrix.md §1a)
Vorgeschlagene Musterkennung: Merge-Richtung bei umgeschriebenem Router-Dokument
Session-Typ:  abgeschlossen
Aufgabe:      Box von v0.3.10 auf v0.3.11 heben, Template als Basis, lokale Zusätze verlagern
Ergebnis:     Box auf v0.3.11, Router 10,3 KB statt 29,7 KB, lokale Zusätze in REGELN-UND-TOOLS.md,
              Konsistenzcheck, Import-Check, Selbstcheck und Tests grün (bekannte Warnungen)

---

## Was sich bewährt hat

Das Drei-Wege-Verfahren (Template v0.3.10, Template v0.3.11, lokaler Stand) mit Platzhalter-
Ersetzung machte die Lage in einem Durchgang sichtbar: Elf Dokumente waren identisch mit dem
Template, nur wenige hatten echte lokale Divergenz. Für Dokumente mit einfachen Deltas lief
`git merge-file` ohne Konflikt; nur zwei Stellen brauchten eine Entscheidung. Der Vergleich
gegen den formatierten Template-Stand trennte Formatrauschen von echten Hunks bei den Tools.

Der Feature-Branch vor der ersten Mutation und der WIP-Commit als Sicherung haben die Umkehr
(Plan A verwerfen) billig gemacht.

---

## Wo das System Reibung gezeigt hat

Die Migration auf v0.3.0 hatte für `AGENTS.md` "merge, lokal als Basis" gewählt. Damit blieb die
alte lange Fassung über zwei weitere Versionen bestehen und das Template-Router-Format wurde nie
übernommen. Die Matrix kennt keine Klasse für Dokumente, die das Template umgeschrieben hat.

Das Template-Tool hat einen Fehler: `AGENT_DOCS` enthält `glossar-box.md`. Ohne lokale Korrektur
löst jedes neue Glossar- oder Grundsatzdokument H6 aus. Auch neue lokale Dokumente lösten H6 aus,
bis sie in der Liste standen.

Ich hatte in dieser Sitzung zuerst `AGENTS.md` nach eigener Struktur umgebaut, bevor ich es mit
dem Template verglichen habe. Das Template hatte das Problem schon gelöst. Der Vergleich gegen das
Template gehört vor jede Strukturänderung am Router.

---

## Was heute nicht geändert werden soll

```text
- tools/instantiate/* nicht aktualisieren (forbidden)
- alte Pläne nicht rückwirkend auf Plan-Schema v0.3.7 umheben
- Learning-Matrix nicht aus diesem Bericht ableiten ohne menschliche Entscheidung
```

---

## Offene Fragen

Soll die Datei-Aktionsmatrix eine Klasse für umgeschriebene Router-Dokumente bekommen?
Soll das Template einen Legacy-Modus im Konsistenzchecker bekommen (zweiter Hinweis in Folge)?
Index als eigene Tabelle gegen Projektionen im Glossar-Eintrag: Modellfrage, offen.

---

## Nicht-Ziel dieses Dokuments

Dieser Bericht ist kein Änderungsauftrag.

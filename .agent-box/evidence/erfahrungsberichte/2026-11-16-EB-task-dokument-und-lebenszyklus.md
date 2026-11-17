# Erfahrungsbericht: Task-Dokument und Lebenszyklus der Aufgaben-Artefakte

Datum: 2026-11-16
Learning-Matrix-Kandidat: ja
  (ja wenn: HARD-Abbruch verursacht, oder ≥2 Sessions gleiches Muster,
   oder Mensch markiert als systemic — siehe learning-matrix.md §1a)
Vorgeschlagene Musterkennung: Aufgaben-Artefakte wachsen mit jeder Aufgabe ohne Abschluss
Session-Typ:  Umsetzung, Abschluss wartet auf Modellreview
Aufgabe:      PLAN-2026-11-16-task-dokument-und-lebenszyklus, Phasen 1 bis 6
Ergebnis:     Protokoll, Kurzform-Vorlage, Aufgabenindex, Checker-Hinweise, Entwurfstool und
              Probelauf sind vorhanden und getestet (114 Tool-Tests grün). Die Merge-Checkliste
              wurde im Review noch nicht durchlaufen, Korrespondenzsätze sind teilweise bestätigt.

---

## Was sich bewährt hat

Die Entscheidungen kamen in kleinen, belegten Schritten: erst die Template-Fakten (Direktauftrag,
Plan-Pflicht, Checkpoint-Regel, Checkerprüfungen), dann Optionen mit Empfehlung, dann die
Festlegung im Sprechakt. Dadurch musste die Kurzform nicht erfunden werden, sie schließt die Lücke
zwischen Direktauftrag und Vollplan. Das Muster "Tool erzeugt Entwurf, Mensch gibt frei" ließ sich
unverändert vom Begriffsindex auf die Verdichtung übertragen.

---

## Wo das System Reibung gezeigt hat

Der Probelauf am eigenen Bestand hat Datenqualität sichtbar gemacht, die die Regeln nicht
abdecken: 15 von 19 Plänen haben im Altformat keine Plan-ID (nur `Status:`), ein Plan steht noch
auf Vertrag `active`, obwohl er ausgeführt ist, und ein Eingabedokument liegt im Planordner.
Der Checker des Templates kann diese Altpläne nicht prüfen (Legacy-Problem, wiederholt).

Ich habe den Checker vor seinen Tests geschrieben, obwohl der Plan Tests zuerst verlangt.
Die Tests folgten in derselben Phase, die Reihenfolge war aber falsch.

Die Korrespondenzsätze waren nur teilweise zu belegen: Die Checkliste lässt sich ohne einen echten
Merge im Review nicht bestätigen, und Overnight-Läufe sind hier nicht erprobt.

---

## Was heute nicht geändert werden soll

```text
- Checkpoint-Regel des Templates (L3: erst im großen Projekt messen)
- vorhandene Pläne, Sprechakte und Berichte nicht entfernen (Probelauf ist nur ein Entwurf)
- Inhalt des Abschlussdokuments nicht durch den Checker bewerten
```

---

## Offene Fragen

Wie verdichtet man Altpläne ohne Plan-ID und mit veraltetem Status (einmaliger Aufräumpunkt für den
Bestand, mit Mandat und Dateiliste)? Reicht die Kurzform im großen Projekt, oder sind die
Vollplan-Kriterien dort zu eng? Wirkt In-place-Checkpoint (Option A) dort besser?

---

## Governance-Rueckfluss

Lokale Governance geaendert: ja

```text
1. Lebenszyklus-Protokoll (Plan-Form, Merge-Gate, Abschlussdokument, Aufgabenindex).
   Rückflussstatus: TEMPLATE-CANDIDATE (Beobachtung aus einem grossen Projekt, Aussage des Menschen)
2. Checker: Kurzform nur auf Kernfelder prüfen, Vorlagenmenge statt einzelnem Namen.
   Rückflussstatus: TOOLING-CANDIDATE
3. Altpläne ohne Plan-ID, veralteter Status, Nicht-Plan im Planordner: Legacy-Modus nötig.
   Rückflussstatus: TOOLING-CANDIDATE
4. In-place-Checkpoint statt neuer Datei je Phase. Rückflussstatus: UNKNOWN (Wirkung messen)
5. Entwurfstool-Muster (nur Entwurf nach tmp/, Mensch entscheidet). Rückflussstatus: TOOLING-CANDIDATE
```

---

## Nicht-Ziel dieses Dokuments

Dieser Bericht ist kein Änderungsauftrag.

---

## Nachtrag 2026-11-17: Probe der Merge-Checkliste am Branch

Der Bericht oben bleibt unveraendert. Dieser Nachtrag haelt den Stand nach der Probe fest.

```text
Tool-Tests:        120 passed (der Bericht oben nennt 114; seither kamen Tests zur Kurzform-Verdichtung hinzu)
Konsistenzcheck:   WARNINGS, eine Warnung (BEGRIFFSINDEX.md: SonnenscheinAnteil, Raum domain gegen Pfad system)
Import-Preflight:  OK (47 Dateien). Selfcheck: OK
```

Merge-Checkliste (Protokoll Abschnitt 5) am aktuellen Branch:

```text
Laeufe COMPLETED:                 docs/runs/ enthaelt nur die Vorlage; keine offenen Laeufe
Keine offenen Plaene / Mandate:   NICHT erfuellt (dieser Plan: Vertrag active, Mandat aktiv)
Abschlussdokument je Aufgabe:     dieser Bericht dient als Abschlussdokument von Plan B (Form aus der Aufgabe,
                                  wie bei der Kurzform); fuer die Migration die Migrationsevidence;
                                  fuer Plan A der Sprechakt dokumentstruktur-und-begriffsindex
Erkenntnisse gesichert:           ja, siehe Governance-Rueckfluss oben (TEMPLATE- und TOOLING-Kandidaten)
Sprechakte:                       vorhanden und versiegelt
Indexzeile je Aufgabe:            ergaenzt am 2026-11-17 fuer Plan A, Migration, Plan B und Kurzform
Plaene entfernt:                  noch nicht (Verdichtungs-Commit, eigenes Mandat)
Checks gruen:                     ja, mit der genannten Warnung
```

Die Rueckfluss-Notiz fuer das Template ist der Abschnitt Governance-Rueckfluss oben. Eine gebuendelte
Fassung fuer alle Rueckfluss-Kandidaten des Branches steht noch aus.

---

## Nachtrag 2026-11-17 (Abschluss)

Modellreview durch Dieter Haag am 2026-11-17: K-1 und K-3 bestaetigt (K-2 war bestaetigt). Plan auf
`abgeschlossen`, Vertrag `completed`, Mandat `erloschen`. Plan A im Aufgabenindex auf LOCAL-ONLY.
Offen bleibt der Verdichtungs-Commit (Entfernen der vier Branch-Plaene) mit eigenem Mandat und Dateiliste.

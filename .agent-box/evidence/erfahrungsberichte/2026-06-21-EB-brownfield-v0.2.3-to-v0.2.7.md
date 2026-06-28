# Erfahrungsbericht: Brownfield-Migration box-python v0.2.3 → v0.2.7

Datum: 2026-06-21
Learning-Matrix-Kandidat: ja
Vorgeschlagene Musterkennung: Brownfield-Versionsmigration — Diff-Größe ≠ Änderungsbedarf, lokale Anpassungen nur per Zeilen-Review sichtbar
Session-Typ: abgeschlossen
Aufgabe: Agenten-Box von v0.2.3 auf v0.2.7 migrieren (Brownfield-Fall B), ohne lokale operative Wahrheit zu überschreiben.
Ergebnis: Migration abgeschlossen auf Branch brownfield/v0.2.3-to-v0.2.7. Alle Box- und Projektchecks grün, keine Regression gegenüber Baseline (64 Tests, mypy 22 Dateien, ruff sauber). 14 Dateien geändert, 3 neu. Evidence: .agent-box/migrations/2026-06-21-v0.2.3-to-v0.2.7-migration.md.

---

## Was sich bewährt hat

**Der Instanziierungs-Commit als Baseline-Anker.** Die Schlüsseltechnik der ganzen
Migration war, nicht nur lokal-vs-Template zu diffen, sondern lokal gegen den
Instanziierungs-Commit (62a2f24, = "was die Instanziierung aus v0.2.3 erzeugt hat").
Erst dieser Anker trennt sauber drei Dinge, die im reinen lokal-vs-Template-Diff
ununterscheidbar verschmelzen: (a) Template-Erbe v0.2.3, (b) lokale Anpassungen seit
Instanziierung, (c) Template-Evolution v0.2.3→v0.2.7. Ohne diesen Anker hätte ich
lokale Anpassungen als Template-Evolution fehlinterpretiert (oder umgekehrt).

**Die Datei-Aktionsmatrix als Strukturgeber.** add / preserve / merge / forbidden
zwang vor jeder Datei zur Klassifikation. Das verhinderte den naheliegenden Fehler,
gefüllte Glossare "mitzumergen".

**Der v0.2.7-Docs-Checker fand latente Strukturschuld.** Ein reiner Markdown-Merge
hätte glossar-meta (## 2 statt ## 3 Begriffe, fehlende Pflichtbegriffe), den fehlenden
Adoptionsmarker in .agent-box-template.md und den fehlenden Projektzustandsmarker-Check
nicht entdeckt. Der mitmigrierte Checker hat genau diese Stellen rot gemeldet — Tooling
als Sicherheitsnetz gegen unvollständigen Doku-Merge.

**String-Literal-Set-Diff gegen Format-Rauschen.** Da lokale Tool-Änderungen fast
nur ruff-Reformatierung waren, hätte ein normaler Diff die echten semantischen
Änderungen im Rauschen versteckt. Der Vergleich der sortierten Stringliteral-Mengen
(`grep -oE '"[^"]+"' | sort -u`) fischte semantische Abweichungen heraus
(z. B. den konvergent ergänzten "Erfahrungsbericht"-Term).

---

## Wo das System Reibung gezeigt hat

**1. Diff-Größe ist kein Maß für Änderungsbedarf.** Die größten Diffs (glossar-domain
217, glossar-meta 270, learning-matrix 255 Zeilen) waren überwiegend lokaler Inhalt
bzw. Strukturanomalien, nicht nachzuziehende Template-Evolution. glossar-domain/system
brauchten am Ende 0 Änderungen. Wer Diff-Größe mit Arbeitsumfang gleichsetzt, überschreibt
lokale Wahrheit. Erst Inhalt klassifizieren, dann handeln.

**2. Zwei valide Merge-Richtungen — die falsche kostet lokale Wahrheit.** Für
Regeldokumente war lokal-als-Basis richtig (kleine Template-Deltas einarbeiten). Für
die Tools war Template-als-Basis richtig (große Template-Evolution, kleine lokale Config
re-applizieren). Die Wahl hängt davon ab, ob lokale Divergenz oder Template-Evolution
dominiert. Template-als-Basis ist nur sicher, wenn JEDE lokale Divergenz explizit
wieder eingebracht und per Diff verifiziert wird.

**3. Lokale Tool-Anpassungen sind subtil und entgehen Heuristiken.** Mein erster
git-History-Filter ("nur Config-Zeilen") stufte die Tool-Änderungen als reine
Formatierung ein. Tatsächlich enthielten sie zwei semantische lokale Anpassungen,
die ein Template-als-Basis-Ansatz still verloren hätte:
   - Default-Modus des Docs-Checkers lokal auf "instantiated" gesetzt;
   - Docstring-Sentinel `<PYTHON_PACKAGE_NAME>`, den die Instanziierung bewusst NICHT
     ersetzt (sonst zerstört globales Replace die placeholder_token-Logik) — mein
     naives Replace hatte ihn fälschlich ersetzt.
   Gefangen wurden beide NUR durch zeilenweisen Review des Template-vs-HEAD-Diffs.
   Lehre: bei Tool-Merge reicht kein History-Filter; jede Diff-Zeile muss gelesen werden.

**4. Lokal kann dem Template VORAUS sein.** Die lokale H10-Erkennungssektion und das
Eintragstiefe-Modell in glossar-domain/system waren reicher/konkreter als v0.2.7.
Die übliche Migrationsannahme "Template ist neuer" stimmt nicht, wenn Box und
Zielprojekt vom selben Autor parallel entwickelt werden. Migration darf nicht
downgraden. Erkennungssignal: Template-Inhalt ist Teilmenge des lokalen.

**5. Konvergente Ergänzungen verschleiern die Herkunft.** Einige v0.2.7-Konzepte
(Eintragstiefe, "Erfahrungsbericht"-Term) existierten bereits lokal. "Lokal = reines
v0.2.3" ist eine falsche Annahme. Jede vermeintliche Template-Neuerung muss gegen den
lokalen Stand geprüft werden, sonst dupliziert oder überschreibt man Vorhandenes.

**6. Cross-File-Kopplung bei Abbruchcode-Umklassifizierung.** Die Änderung
H2→H3 für Bridge-Verletzungen (migration-bridges.md) war nur korrekt zusammen mit
der Erweiterung der H3-Definition in AGENTS.md (um migration-bridges.md). Eine
einzelne semantische Änderung spannte zwei Dateien — ohne die Kopplung wäre ein
Widerspruch (H3) entstanden.

**7. Template-Stand ist nicht automatisch lint-grün.** Die v0.2.7-Tools brachten
Dead Code mit (ungenutzte Imports `sys`/`field`, ungenutzte Variablen `all_files`/`info`),
den ruff im Projekt rot meldet. Der Import aus einem Template setzt voraus, dass das
Zielprojekt strengere Gates hat als das Template-Repo.

**8. Checker-blinde-Flecken erlauben stille Drift.** glossar-meta konnte lokal mit
abweichender Struktur (## 2. Begriffe) und ohne Brownfield-Begriffe existieren, weil
der v0.2.3-Checker glossar-meta gar nicht kannte (eingeführt erst v0.2.4). Erst das
Checker-Upgrade machte die aufgelaufene Strukturschuld sichtbar. Muster: was ein Tool
nicht prüft, driftet; das Tool-Upgrade präsentiert die Rechnung gebündelt.

---

## Was heute nicht geändert werden soll

- **glossar-domain/system NICHT auf reine Template-Form vereinheitlichen.** Sie tragen
  ein lokal eingeführtes Eintragstiefe-Modell (`**Eintragstiefe:** minimal/vollständig`),
  das konkreter ist als die Template-Prosa. Bewusst belassen.
- **BR-001-Beispiel-Bridge NICHT reaktivieren.** Lokal korrekt durch "Kein aktiver
  Bridge-Eintrag nach Instanziierung" ersetzt.
- **glossar-meta-Einträge bleiben knapp** (Bedeutung/Invariante). Das volle Eintrag-Format
  ist dokumentiert, aber die Meta-Begriffe brauchen keine vollständige Eintragstiefe.
- Kein Commit/Push in dieser Session ohne ausdrückliche Freigabe.

---

## Offene Fragen

- Sollte der Dead Code / fehlende Lint-Grünstand im Template-Repo upstream gemeldet
  werden? (Betrifft das Template, nicht dieses Projekt.)
- Sollte ein künftiges Box-Update ein maschinelles "Migrations-Manifest" je Version
  mitliefern (Liste echter Datei-/Logik-Deltas), damit der Baseline-Anker-Trick nicht
  jedes Mal manuell rekonstruiert werden muss?
- Learning-Matrix-Kandidat (Punkt 1–3): menschliche Entscheidung über learning-matrix.md
  ausstehend — kein automatischer Eintrag aus diesem Bericht.

---

## Nicht-Ziel dieses Dokuments

Dieser Bericht ist kein Änderungsauftrag. Übernahme von Mustern in die Learning-Matrix
erfolgt ausschließlich durch menschliche Entscheidung und wird nur in learning-matrix.md
dokumentiert.

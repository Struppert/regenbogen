# Backflow-Empfehlungen an das Template-System (box-python)

Status: offen (Eingabe für Template-Repo, kein Änderungsauftrag an dieses Projekt)
Datum: 2026-06-21
Bearbeiter: Dieter Haag
Quelle: Brownfield-Migration v0.2.3 → v0.2.7 (Fall B) in Regenbogen

## Zweck und Geltung

Dieses Dokument bündelt die strukturellen Lehren der Brownfield-Migration
v0.2.3 → v0.2.7, damit sie in das Template-Repository `agent-templates/box-python`
zurückfließen können. Es ist **kein** Änderungsauftrag an Regenbogen und **kein**
Sprechakt. Es ist eine Entscheidungsvorlage für die Pflege der Box.

Es ist bewusst so geschrieben, dass es zusammen mit zwei Erfahrungsberichten den
vollständigen Rückfluss bildet:

```text
EB-1: tmp/erfahrungsberichte/2026-06-21-EB-brownfield-v0.2.3-to-v0.2.7.md   (dieser, einfacher Referenzfall)
EB-2: <Erfahrungsbericht der folgenden, komplexeren Brownfield-Migration>    (noch offen)
dieses Dokument: destillierte Struktur-/Tool-/Verfahrensempfehlungen
```

EB-1 ist der **einfache Referenzfall** (nur Box-Artefakte, grüne Baseline, geringe
lokale Divergenz). EB-2 wird der **komplexe Fall** (voraussichtlich Produktcode,
echte Befunde, rote Baseline, größere Divergenz). Die Empfehlungen hier sind so
formuliert, dass EB-2 sie bestätigen, schärfen oder widerlegen kann.

Provenienz / Evidence:

```text
Plan:      docs/plans/2026-06-21-brownfield-migration-v0.2.3-to-v0.2.7.md
Evidence:  .agent-box/migrations/2026-06-21-v0.2.3-to-v0.2.7-migration.md
EB-1:      tmp/erfahrungsberichte/2026-06-21-EB-brownfield-v0.2.3-to-v0.2.7.md
```

Jede Empfehlung nennt: **Befund** (was beobachtet wurde), **Empfehlung** (was die
Box ändern sollte), **Form** (konkrete Gestalt, soweit absehbar) und **Fertig wenn**
(Abnahmekriterium). Lektionsnummern (L1–L8) verweisen auf EB-1, Abschnitt
„Wo das System Reibung gezeigt hat".

---

## Teil A — Template-Strukturänderungen (Box-Dokumente und Verfahren)

### A1. Maschinenlesbares Migrations-Manifest je Version

- **Befund (L1, L5):** Die teuerste manuelle Arbeit war, echte Datei-/Logik-Deltas
  von Format-Rauschen und lokaler Divergenz zu trennen. Es gibt heute kein Artefakt,
  das sagt: „v0.2.6 → v0.2.7 hat *diese* Dateien *so* geändert."
- **Empfehlung:** Jede Box-Version liefert ein Manifest der echten Deltas mit.
  Das `CHANGELOG.md` ist Prosa; gebraucht wird eine prüfbare, datei-/symbolbezogene
  Liste.
- **Form (Vorschlag):** `migrations/v<quelle>-to-v<ziel>.md` im Template-Repo mit je
  Datei: Aktionsklasse (add/merge/replace), betroffene Abschnitte/Symbole,
  Kopplungen, ob Config oder Logik. So wird der Baseline-Anker-Trick (siehe A4)
  teilweise überflüssig.
- **Fertig wenn:** Eine Migration v(n)→v(n+1) sich allein aus dem Manifest planen
  lässt, ohne den Quell-Template-Stand zeilenweise zu diffen.

### A2. Drift früher sichtbar machen (Checker-Vorlauf statt Versionssprung-Rechnung)

- **Befund (L8):** `glossar-meta.md` konnte lokal mit `## 2. Begriffe` und ohne
  Brownfield-Begriffe driften, weil der v0.2.3-Checker die Datei nicht kannte.
  Erst das Checker-Upgrade präsentierte die aufgelaufene Schuld gebündelt.
- **Empfehlung:** Wenn eine Version eine neue Pflichtdatei einführt, soll der Checker
  *derselben* Version bereits die kanonische Struktur dieser Datei prüfen — auch wenn
  Inhalte noch leer sein dürfen. Strukturschuld darf nicht über Versionen auflaufen.
- **Form:** Strukturprüfung (Überschriften-Schema, Pflichtabschnitte) getrennt von
  Inhaltsprüfung (Pflichtbegriffe). Erstere greift ab Einführung, letztere ab erstem
  Sprechakt.
- **Fertig wenn:** Eine nicht-kanonische Überschrift in einer Glossardatei in der
  Version, die die Datei einführt, eine WARN/ERROR erzeugt.

### A3. Sentinel-/Platzhalter-Schutz explizit markieren

- **Befund (L3):** Der Docstring `<PYTHON_PACKAGE_NAME>` in
  `check_agent_docs_consistency.py` darf **nicht** ersetzt werden (sonst zerstört ein
  globales Replace die `placeholder_token`-Logik). Diese Ausnahme ist heute nur
  implizit — ein naives Replace (auch meines) ersetzt sie fälschlich.
- **Empfehlung:** Ersetzungs-ausgenommene Regionen explizit markieren, damit jedes
  Instanziierungs- **und** Migrationswerkzeug sie maschinell überspringen kann.
- **Form (Vorschlag):** Kommentar-Sentinels wie
  `# agent-box: no-replace-begin` / `# agent-box: no-replace-end`, vom
  Instanziierungswerkzeug respektiert und vom Docs-Checker geprüft.
- **Fertig wenn:** Ein globales Token-Replace über die Box keine Sentinel-/Logik-Region
  mehr beschädigt und das durch einen Test belegt ist.

### A4. „Baseline-Anker" als benannten Schritt in BROWNFIELD-MIGRATION.md

- **Befund (L1):** Der Instanziierungs-Commit (hier 62a2f24) war der einzige Weg,
  Template-Erbe / lokale Anpassung / Template-Evolution zu trennen. Das Verfahren B
  benennt diesen Anker nicht.
- **Empfehlung:** Verfahren B erhält einen Pflichtschritt „Baseline-Anker bestimmen":
  Instanziierungs-Commit, sonst letzter Pre-Migration-Tag. Für Fall A (kein
  Instanziierungs-Commit) ausdrücklich: vor der Aufnahme einen Anker-Tag setzen.
- **Fertig wenn:** Verfahren B und C einen benannten Anker und seine Bestimmung für
  alle drei Fälle (A/B/C) enthalten.

### A5. „Merge-Richtung je Dateiklasse" als Entscheidungseintrag

- **Befund (L2):** Es gibt zwei valide Richtungen — lokal-als-Basis (Regeln) und
  Template-als-Basis (Tools). Die falsche kostet lokale Wahrheit.
- **Empfehlung:** Die Datei-Aktionsmatrix um eine Spalte/Notiz „Merge-Richtung +
  Begründung" ergänzen. Regel: Template-als-Basis nur, wenn Template-Evolution
  dominiert **und** jede lokale Divergenz explizit re-appliziert und per Diff
  verifiziert wird.
- **Fertig wenn:** Die Aktionsmatrix in BROWNFIELD-MIGRATION.md Merge-Richtung als
  bewusste, dokumentierte Entscheidung führt.

### A6. Migrationsevidence-Format um „Lokale-Divergenz-Inventur" erweitern

- **Befund (L2, L3, L5):** Die verborgene Triebkraft aller harten Entscheidungen war
  „was hat das Projekt seit der Instanziierung lokal geändert?". Das Evidence-Format
  hat dafür keinen festen Platz.
- **Empfehlung:** Pflichtabschnitt „Lokale Divergenz gegen Baseline-Anker"
  (Config vs. Logik vs. Format vs. nur-lokale-Begriffe) im Minimalformat.
- **Fertig wenn:** Das Minimalformat in BROWNFIELD-MIGRATION.md Abschnitt 10 diesen
  Abschnitt enthält.

---

## Teil B — Tool-Härtung (Box-Tools und Template-Repo-Hygiene)

### B1. Template-Tools unter denselben Gates grün halten

- **Befund (L7):** Die v0.2.7-Tools brachten Dead Code mit (ungenutzte Imports
  `sys`, `field`; ungenutzte Variablen `all_files`, `info`), den ruff im Zielprojekt
  rot meldet. Der Template-Stand ist nicht automatisch lint-grün.
- **Empfehlung:** Das Template-Repo führt ruff (check + format) und mypy auf seinen
  eigenen `tools/` aus — als CI-Gate vor Release einer Box-Version.
- **Fertig wenn:** Ein frisch instanziiertes Projekt mit den Standard-Gates (ruff,
  mypy) ohne Nacharbeit grün ist.

### B2. Unvollständige Features im Checker auflösen oder entfernen

- **Befund (L7):** `all_files = REQUIRED_FILES + OPTIONAL_FILES` und
  `info = [... INFO ...]` waren zugewiesen, aber nie genutzt — entweder begonnene,
  nicht fertiggestellte Features oder echter Toter Code.
- **Empfehlung:** Im Template entscheiden: verdrahten (z. B. INFO-Findings im
  Preflight ausgeben) oder entfernen. Nicht als Dead Code ausliefern.
- **Fertig wenn:** Keine F841/F401-Befunde in den Box-Tools.

### B3. Drei-Wege-Tool-Merge dokumentieren

- **Befund (L3):** Zwei semantische lokale Tool-Anpassungen (Default-Modus
  `instantiated`; Docstring-Sentinel) wären bei „Template-als-Basis" still verloren
  gegangen; nur der zeilenweise Diff gegen den Baseline-Anker fing sie.
- **Empfehlung:** BROWNFIELD-MIGRATION.md (oder ein Tool-Anhang) beschreibt für Tools
  ausdrücklich: Template-als-Basis + zeilenweiser Diff gegen Anker + Re-Applikation
  jeder lokalen Hunk. Kein History-Filter als Ersatz für Zeilen-Review.
- **Fertig wenn:** Das Tool-Merge-Verfahren als eigener, benannter Abschnitt existiert.

---

## Teil C — Field-Hardening: Promotion-Kandidaten (downstream → Template)

Dies ist der von dir beschriebene Rückfluss-Kern: Elemente, die **dieses Projekt
reicher/konkreter** hatte als das Template (L4). Sie sollten als Aufnahme-Kandidaten
in die Box geprüft werden — nicht automatisch übernommen.

### C1. Eintragstiefe-Feldformat in den Glossaren

- **Befund:** Regenbogen hatte vor v0.2.7 ein konkretes Eintragstiefe-Modell in
  `glossar-domain.md`/`glossar-system.md` (`**Eintragstiefe:** minimal | vollständig`
  pro Eintrag, plus präzise Definition „minimal = Bedeutung + Projektionen +
  Migrationsstatus"). Das v0.2.7-Template hat das Konzept nur als Prosa.
- **Empfehlung:** Das **Feldformat** (nicht nur die Prosa) als kanonisches
  Eintrag-Format der Box prüfen. Es macht Eintragstiefe maschinell sicht- und prüfbar.
- **Bewertungsfrage fürs Template:** Soll der Docs-Checker `**Eintragstiefe:**`
  als Pflichtfeld erzwingen?

### C2. Ausführlichere H10-Erkennungssektion

- **Befund:** Die lokale H10-Sektion (4 nummerierte Auslöseregeln inkl.
  `request_id`/HTTP-Zyklus, duale Prüfhilfe für domain- **und** system-Begriffe) war
  detaillierter als die v0.2.7-Inline-Variante.
- **Empfehlung:** Die lokale Fassung als Kandidat für die kanonische H10-Sektion
  prüfen.

### C3. MODELL-README als optionale Box-Projektion

- **Befund:** Regenbogen führte `MODELL-README.md` als verpflichtende
  Zusammenhangsbeschreibung des implementierten Modells ein, samt Preflight-Schritt
  und Testpflicht. Das Template kennt das nicht.
- **Empfehlung:** Als **optionales** Box-Element prüfen (nicht jede Domäne hat ein
  „Modell"). Wenn aufgenommen: als opt-in mit eigenem Preflight-/Drift-Hook.

### C4. Projektlokale Importregel-Abweichung als Muster (nicht als Default)

- **Befund:** `cli` darf in Regenbogen `domain` importieren (lokale package-schema-
  Entscheidung, im Checker als `FORBIDDEN_IMPORTS["cli"]` ohne `domain` gespiegelt).
- **Empfehlung:** **Nicht** als Template-Default übernehmen. Aber als dokumentiertes
  Beispiel einer sauber gespiegelten lokalen Abweichung (package-schema ↔ Checker)
  in die Box-Doku aufnehmen — zeigt, wie eine legitime Abweichung aussieht.

---

## Teil D — Was der nächste (komplexe) Lauf zusätzlich liefern muss

Damit EB-1 + EB-2 + dieses Dokument zusammen eine **vollständige** Methodik ergeben,
sollte der komplexe Lauf drei Artefakte explizit führen, die hier nur implizit
entstanden:

```text
D1  Lokale-Divergenz-Inventur (lokal vs. Baseline-Anker), getrennt nach
    Config / Logik / Format / nur-lokale-Begriffe.
D2  Cross-File-Kopplungskarte (welche semantische Änderung welche Dateien spannt).
D3  Merge-Richtungs-Entscheidung je Dateiklasse mit Begründung.
```

Zusätzlich die **Gegenprobe „lokal voraus"** als bewusster Schritt: jede vermeintliche
Template-Neuerung gegen den lokalen Stand prüfen (existiert sie lokal bereits, evtl.
reicher?). Bei Produktcode wird das der teuerste Schritt — und der wichtigste für die
Field-Hardening-Kandidaten (Teil C) des nächsten Laufs.

Erwartete Komplikationen, die EB-2 wahrscheinlich auslösen (und die hier fehlten):

```text
- Produktcode-Migration statt nur Box-Artefakte → Discover/Classify/Decide wird tragend.
- Rote Baseline → jeder rote Check muss vor der Migration klassifiziert werden.
- Echte Known Breaches / Legacy Defects / Migration Candidates → BF12-Entscheidungspunkte.
- Bridge-Symbole tatsächlich in Benutzung → H3-Sperren greifen real.
- Größere lokale Divergenz → Template-als-Basis wird für mehr Dateien gefährlich.
```

---

## Teil E — Priorisierung

```text
Zuerst (höchster Hebel, niedriges Risiko):
  A1  Migrations-Manifest je Version
  B1  Template-Tools lint-grün
  A3  Sentinel-Schutz explizit

Dann (verbessert jede künftige Migration):
  A4  Baseline-Anker als Verfahrensschritt
  A5  Merge-Richtung je Dateiklasse
  A6  Lokale-Divergenz-Inventur im Evidence-Format
  B3  Drei-Wege-Tool-Merge dokumentieren

Bewertung mit Augenmaß (echte Inhaltsentscheidung nötig):
  A2  Checker-Vorlauf gegen Drift
  C1–C4  Field-Hardening-Kandidaten (nur nach Prüfung, nicht automatisch)
  B2  Unvollständige Checker-Features auflösen
```

---

## Nicht-Ziel dieses Dokuments

Dieses Dokument ist kein Änderungsauftrag und kein Sprechakt. Übernahme einzelner
Empfehlungen in die Box ist eine Entscheidung der Template-Pflege. Die Promotion von
Field-Hardening-Kandidaten (Teil C) erfordert ausdrückliche menschliche Festlegung
auf Template-Ebene. EB-2 darf jede Empfehlung hier bestätigen, schärfen oder
widerlegen.

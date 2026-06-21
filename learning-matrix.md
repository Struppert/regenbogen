# learning-matrix.md — Python-Projekt: Aggregierte Lernmuster

> Dieses Dokument aggregiert wiederkehrende Muster aus Erfahrungsberichten.
>
> Es ist kein Regelwerk. Es ist Eingabe für Regelentscheidungen.
> Neue Regeln entstehen nur nach expliziter Freigabe — nicht durch dieses Dokument allein.

---

## 1. Zweck

```text
Einzelner Erfahrungsbericht → beschreibt eine Session
Learning-Matrix             → beschreibt Muster über mehrere Sessions
Systemänderung              → folgt aus menschlicher Entscheidung über Muster
```

Ein Agent darf diese Matrix lesen, um bekannte Muster zu erkennen.
Er darf sie nicht ohne explizite Freigabe schreiben oder ändern.

## 1a. Muster-Schwelle

Ein Muster gilt als **systemic** und wird hier eingetragen, wenn mindestens
eine der folgenden Bedingungen erfüllt ist:

```text
a) Es tritt in mindestens 2 unabhängigen Sessions mit demselben Kern auf.
b) Es hat einen HARD-Abbruch (H1–H10) oder BF-Abbruch verursacht.
c) Ein Mensch markiert es nach einem einzelnen Erfahrungsbericht als systemic.
```

Nicht-systemische Einzelbeobachtungen bleiben im Erfahrungsbericht und
werden nicht hierher übertragen. Das vermeidet Rauschen in der Matrix und
verhindert, dass Einmaleffekte als Systemschwächen eingestuft werden.

---

## 2. Format eines Eintrags

```markdown
## M-<NR>: <Kurzbeschreibung des Musters>

Erstellt:      YYYY-MM-DD
Quellen:       tmp/erfahrungsberichte/YYYY-MM-DD-EB-...md (ein oder mehrere)
Häufigkeit:    einmalig | wiederholt (N Mal) | systematisch
Status:        beobachtet | als Verbesserung vorgeschlagen | in Planung | umgesetzt

### Beobachtung

<Was passiert wiederholt? Konkret, nicht abstrakt.>

### Wirkung

<Was kostet dieses Muster? Tokenaufwand, Reibung, Fehlerrisiko, Abbrüche?>

### Mögliche Maßnahme

<Was könnte das System besser machen? Als Vorschlag, nicht als Entscheidung.
Klar als Vorschlag markieren.>

### Entscheidung

<Wird nach menschlicher Freigabe ergänzt. Leer lassen bis Entscheidung getroffen.>
```

---

## 3. Bekannte Muster

---

## M-1: Ruff-Format-Check meldet Verstoß auf Tool-Dateien außerhalb des Schnitts

Erstellt:      2026-06-20
Quellen:       tmp/erfahrungsberichte/2026-06-20-ABBRUCH-globaler-format-check.md
               tmp/erfahrungsberichte/2026-06-20-EB-uv-projektkonfiguration.md
Häufigkeit:    wiederholt (2 Mal)
Status:        als Verbesserung vorgeschlagen

### Beobachtung

Globaler `ruff format --check .` meldet Formatierverstöße auf geschützten
Tool-Dateien, die im aktuellen Schnitt nicht berührt wurden. Ursache: die
Tool-Dateien hatten vor Einführung von `pyproject.toml` eine andere Formatierung.
Der Agent konnte nicht unterscheiden, ob der SA2-Befund aus dem geänderten Code
stammt oder ein passiver Altbefund ist.

### Wirkung

SA2 SOFT-Abbruch. Erfordert explizite Freigabe für einmaligen globalen Formatlauf.
Entstellt die Abbruchursache: nicht geänderter Code ist das Problem, sondern
passiver Altbefund in geschützten Dateien.

### Mögliche Maßnahme

Im P7-Schritt des Preflight unterscheiden:
- Format-Check auf aktiv geänderte Dateien (`src/`, `tests/`) = normaler Prüfschritt
- Format-Meldung auf `tools/` ohne Berührung in diesem Schnitt = SA6 (lokale
  Inkonsistenz ohne semantischen Widerspruch), nicht SA2
Oder: Ruff-Scope im Standard-Check auf `src/ tests/` einschränken.

### Entscheidung

<Leer bis Freigabe.>

---

## M-2: Fehlende Runtime-Abhängigkeiten blockieren Testvalidierung

Erstellt:      2026-06-20
Quellen:       tmp/erfahrungsberichte/2026-06-20-ABBRUCH-plz-validierung.md
               tmp/erfahrungsberichte/2026-06-20-EB-plz-bestimmung.md
Häufigkeit:    einmalig
Status:        als Verbesserung vorgeschlagen

### Beobachtung

`pytest` und `httpx` waren nicht in der aktiven Umgebung installiert. Der Agent
hat die Implementierung vollständig geschrieben, scheitert dann aber an SA4, weil
die Testpflicht nicht erfüllbar ist. Die Lücke ist nicht im Code — sie ist in der
Umgebung. Das wird erst am Ende des Schnitts sichtbar, nicht am Anfang.

### Wirkung

SA4 SOFT-Abbruch nach abgeschlossener Implementierung. Verzögerung bis der Mensch
die Umgebung aufräumt. Kein Schaden am Code, aber unnötige Iteration.

### Mögliche Maßnahme

Im Preflight-Schritt P8 (Testpflicht) früh prüfen:
"Sind Test- und Runtime-Abhängigkeiten in der aktiven Umgebung installiert?"
Bei Nein: nicht erst am Ende scheitern, sondern früh dokumentieren und
Menschenentscheidung abwarten. Oder: als eigenen P0-Schritt im Fast-Path
für Aufgaben mit Laufzeitbezug.

### Entscheidung

<Leer bis Freigabe.>

---

## M-3: Glossareinträge dünner als Format fordert erzeugen SP7-Druck

Erstellt:      2026-06-20
Quellen:       tmp/erfahrungsberichte/2026-06-20-EB-readme-programmdoku.md
               tmp/erfahrungsberichte/2026-06-20-EB-sonnenscheinanteil.md
               tmp/erfahrungsberichte/2026-06-20-EB-modell-readme-und-framing.md
Häufigkeit:    wiederholt (3 Mal)
Status:        umgesetzt

### Beobachtung

Glossareinträge sind kürzer als ihr eigenes Format-Schema verlangt (fehlende
Felder: Kompetenzfrage, Erlaubt, Verboten, Abgrenzung). Bei strengeren Aufgaben
drohte SP7, obwohl der Begriff fachlich bekannt und für die Aufgabe ausreichend
beschrieben war. Alternativ: stillschweigendes Übergehen der Lücke.

### Wirkung

Unnötiger SP7-Trigger bei korrekten, aber formal dünnen Einträgen. Oder
stilles Übergehen der Lücke — beides ist schlechter als eine explizit
akzeptierte Teiltiefe.

### Mögliche Maßnahme

Explizites Minimalformat freigeben: ein Eintrag der Bedeutung + Projektionen
+ Migrationsstatus hat, ist operativ nutzbar. Fehlende Felder müssen
als bewusst weggelassen, nicht als vergessen markiert sein.

### Entscheidung

Umgesetzt: `Eintragstiefe: minimal | vollständig` in glossar-domain.md und
glossar-system.md eingeführt (2026-06-20, Plan priming-verbesserungen).
Alle bestehenden Einträge als `minimal` markiert.

---

## M-4: Framing-Änderungen kaskadieren über mehrere gekoppelte Dokumente

Erstellt:      2026-06-20
Quellen:       tmp/erfahrungsberichte/2026-06-20-EB-modell-readme-und-framing.md
Häufigkeit:    einmalig
Status:        als Verbesserung vorgeschlagen

### Beobachtung

SP2 für MODELL-README-Pflicht berührte sofort AGENTS.md, AGENTS-COMPACT.md
und preflight-checkliste.md, inkl. Abschnittsnummerierungen. Die Kaskade war
nicht im Voraus vollständig sichtbar. Ähnliches gilt für jeden SP2-Sprechakt
der operative Regeln einführt.

### Wirkung

Höherer Änderungsaufwand als bei einfachen Code-Schnitten. Fehlerrisiko bei
unvollständiger Kaskadierung. Erhöhte Gefahr von Dokumentdrift zwischen
AGENTS.md, AGENTS-COMPACT.md und preflight-checkliste.md.

### Mögliche Maßnahme

Im Preflight bei Änderungen an Framing-Dokumenten (AGENTS.md, AGENTS-COMPACT.md,
preflight-checkliste.md): Dokumentdrift-Prüfung nach AGENTS.md §17 als
obligatorischen Schritt explizit benennen — nicht nur als Schlussregel, sondern
als eigener Preflight-Check vor dem Schreiben.

### Entscheidung

<Leer bis Freigabe.>

---

## M-5: Sprechaktmechanismus (SP2, SP7) verhindert stille semantische Fehler

Erstellt:      2026-06-20
Quellen:       tmp/erfahrungsberichte/2026-06-10-EB-domain-kern.md
               tmp/erfahrungsberichte/2026-06-12-EB-gui-session.md
               tmp/erfahrungsberichte/2026-06-20-EB-modell-readme-und-framing.md
Häufigkeit:    systematisch
Status:        beobachtet

### Beobachtung

SP7 verhindert stille Entscheidung über Gleichzeitigkeit von Sonne und Regen.
SP2 verhindert stillschweigenden neuen GUI-Raum. SP2 verankert MODELL-README
als verbindliche Pflichtprojektion für Modellarbeit. In allen drei Fällen hat
der Sprechakt eine Entscheidung sichtbar gemacht, die ohne ihn still
implementiert worden wäre.

### Wirkung

Positiv: semantische Fehler werden Entscheidungspunkte statt stille Fehler.
Das ist das beabsichtigte Systemverhalten.

### Mögliche Maßnahme

Keine. Muster bestätigt das SP-System. Sollte als Baseline festgehalten werden,
damit spätere Vereinfachungsvorschläge gegen diesen Nutzen abgewogen werden.

### Entscheidung

Keine Änderung. Bestätigt.

---

## M-6: UI-Text als eigenständiger Fehlerkanal neben Code

Erstellt:      2026-06-20
Quellen:       tmp/erfahrungsberichte/2026-06-20-EB-sonnenscheinanteil.md
Häufigkeit:    einmalig
Status:        als Verbesserung vorgeschlagen

### Beobachtung

Die Anzeige "Sonnenschein (25 %)" wurde von Nutzern als Wahrscheinlichkeit
gelesen. Der Code berechnet korrekt einen Anteil (`sunshine_duration / 3600`).
Der Fehler lag nicht im Code, sondern in der begrifflichen Projektion des
Werts in den UI-Text. Import-Checker, Typecheck und Tests finden diesen
Fehlertyp nicht — er liegt unterhalb der Checker-Grenze.

### Wirkung

Begriffliche Fehlinterpretation durch Nutzer ohne Codewarnung. Korrektur
erfordert Glossar-Präzisierung + Modell-README + UI-Text + Test, nicht nur
Code-Fix. Checker hätte diesen Fehler nie gemeldet.

### Mögliche Maßnahme

Im Preflight-Schritt P5 (Glossar laden) bei Änderungen in `cli/` explizit
fragen: "Stimmt der angezeigte Begriff mit dem Glossareintrag überein?
Ist er Anteil, Intensität, Wahrscheinlichkeit oder technisches API-Feld?"
In test-obligations.md aufnehmen: UI-Text-Änderungen erfordern Glossarabgleich.

### Entscheidung

<Leer bis Freigabe.>

---

## 4. Muster-Klassifikation

```text
Klasse A: Regelklarheit
  Das System hat eine Regel, aber die Regel ist unklar formuliert oder
  in mehreren Dokumenten unterschiedlich dargestellt.
  → Kandidat für Konsolidierung in AGENTS.md

Klasse B: Fehlende Klassifikation
  Ein Begriff, Symbol oder Pfad wird gebraucht, ist aber nicht klassifiziert.
  → Kandidat für package-schema.md, migration-bridges.md, passendes Glossar oder Sprechakt

Klasse C: Redundanzdrift
  Dieselbe Information steht an mehreren Stellen und läuft auseinander.
  → Kandidat für Redundanzbereinigung

Klasse D: Tool-Lücke
  Ein Checker prüft etwas nicht, das er prüfen sollte.
  Oder ein Tool gibt kein maschinenlesbares Output für Agenten.
  → Kandidat für Tool-Erweiterung

Klasse E: Prozesslücke
  Ein Schritt im operativen Ablauf ist nicht dokumentiert oder fehlt.
  → Kandidat für AGENTS.md, preflight-checkliste.md oder neues Protokoll
```

---

## 5. Schutz und Pflege

```text
- Dieses Dokument ist geschützt (AGENTS.md Abschnitt 9).
- Neue Einträge nur nach Erfahrungsbericht-Session, nicht ad hoc.
- Status-Änderung auf "umgesetzt" erfordert Freigabe.
- Abgeschlossene Muster werden nicht gelöscht — auf "umgesetzt" gesetzt.
```

---

## 6. Schlussregel

Die Learning-Matrix ist nützlich wenn sie drei Dinge trennt:

```text
1. Was ist beobachtet? (Fakten)
2. Was wäre besser? (Vorschlag)
3. Was ist entschieden? (Freigabe)
```

Wenn Beobachtung und Entscheidung vermischt werden,
ist die Matrix kein Lernwerkzeug mehr — sie ist ein versteckter Regeländerungs-Kanal.



---

## Eingangspfad aus Erfahrungsberichten

Aufnahmeschwelle: Abschnitt 1a.

Jeder Kandidat erhält im Erfahrungsbericht einen stabilen Hinweis:

```text
Learning-Matrix-Kandidat: ja/nein
Vorgeschlagene Musterkennung:
```

Die kanonische Muster-ID entsteht erst in `learning-matrix.md`.
Die tatsächliche Übernahme wird hier dokumentiert, nicht nachträglich im
append-only Erfahrungsbericht.

Die Learning-Matrix ist kein Regelwerk. Ein Matrix-Eintrag wird erst operativ,
wenn ein Mensch daraus eine Änderung an `AGENTS.md`, `package-schema.md`,
`test-obligations.md`, `migration-bridges.md`, `glossar-domain.md`,
`glossar-system.md` oder `glossar-meta.md` ableitet.

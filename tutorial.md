# box-python — Tutorial

Stand: box-python v0.2.3.


> Ausführungsprüfung: Diese Fassung wurde aus den Python-Codeblöcken in ein
> temporäres `regenbogen`-Projekt projiziert. `compileall` und `pytest` laufen
> für die extrahierten Beispielmodule grün. Die optionalen Abbruchpfade in
> Abschnitt 9.5 und 11.14 sind didaktische Verzweigungen; ihre fehlerhaften
> Schnipsel werden bewusst nicht in den grünen Hauptpfad projiziert.

Dieses Tutorial erklärt, wie das System funktioniert, was es tut und wie man
praktisch damit arbeitet. Es richtet sich an Entwickler und Teams, die
KI-Agenten produktiv in Python-Projekten einsetzen wollen.

Das Tutorial begleitet ein durchgehendes Beispielprojekt: **Regenbogen** —
ein Programm, das Wetterdaten holt und die Wahrscheinlichkeit eines Regenbogens
berechnet, wenn gleichzeitig Sonne und Regen auftreten. Später bekommt das
Programm zusätzlich eine einfache GUI mit Konfigurationsdialog und
Ausgabefenster.

Dieses Tutorial richtet sich nicht an den Agenten. Es richtet sich an Menschen,
die mit Agenten arbeiten: Entwickler, Reviewer, technische Entscheider und
Teams, die Agentenarbeit anleiten, prüfen und nachvollziehen müssen. Der
Agent liest im Arbeitsfall `AGENTS-COMPACT.md`, `AGENTS.md` und die jeweils
relevanten Projektartefakte. Dieses Tutorial erklärt dem Menschen, warum diese
Artefakte existieren, wie sie zusammenspielen und wie ein sinnvoller
Agenten-Workflow aussieht.

---

## Inhaltsverzeichnis

- [1. Wozu dient das System?](#1-wozu-dient-das-system)
- [2. Das Grundprinzip](#2-das-grundprinzip)
- [3. Was in der Box steckt](#3-was-in-der-box-steckt)
- [4. Konzepte](#4-konzepte)
- [5. Projekt aufsetzen: Regenbogen](#5-projekt-aufsetzen-regenbogen)
- [6. Erste Session: Domainkern](#6-erste-session-domainkern)
- [7. Zweite Session: Port und Infrastruktur](#7-zweite-session-port-und-infrastruktur)
- [8. Dritte Session: System-Logik](#8-dritte-session-system-logik)
- [9. Vierte Session: CLI und Wiring](#9-vierte-session-cli-und-wiring)
  - [9.5 Optionaler Abbruchpfad: H2 und Wiedereinstieg](#95-optionaler-abbruchpfad-h2-und-wiedereinstieg)
- [10. Fünfte Session: GUI mit Tkinter](#10-fünfte-session-gui-mit-tkinter)
- [11. Sechste Session: Sonnenstand und Winkelmodell](#11-sechste-session-sonnenstand-und-winkelmodell)
  - [11.14 Optionaler Abbruchpfad: SA1 bei rotem Test](#1114-optionaler-abbruchpfad-sa1-bei-rotem-test)
- [12. Siebte Session: Tropfenqualität und wetterdatenbasiertes Sichtbarkeitsmodell](#12-siebte-session-tropfenqualität-und-wetterdatenbasiertes-sichtbarkeitsmodell)
- [13. Achte Session: Logging als Infrastruktur](#13-achte-session-logging-als-infrastruktur)
- [14. Vollständige Abschlusskontrolle](#14-vollständige-abschlusskontrolle)
- [15. Was das System konkret verhindert hat](#15-was-das-system-konkret-verhindert-hat)
  - [15.1 Warum dieses Beispiel funktioniert](#151-warum-dieses-beispiel-funktioniert)
- [16. Dokument-Autoritäten](#16-dokument-autoritäten)
- [17. Was dieses System nicht ist](#17-was-dieses-system-nicht-ist)
- [18. Kurzregel](#18-kurzregel)
- [19. Glossar](#19-glossar)
- [20. Index](#20-index)

---

## 1. Wozu dient das System?

KI-Agenten können Code schreiben, refaktorieren und analysieren. Das
funktioniert gut für technisch klar abgegrenzte Aufgaben. Es bricht zusammen,
sobald ein Agent Bedeutung erfinden muss.

Das Problem ist nicht die KI. Das Problem ist, dass Softwareprojekte ihre
eigene Semantik nicht vollständig explizit machen. Was ein Begriff bedeutet,
welche Imports erlaubt sind, wann eine Änderung einen Test erfordert — das
liegt verteilt in Code, Kommentaren, Köpfen und Konventionen.

Menschen kompensieren das durch Erfahrung und Rückfragen. Agenten kompensieren
es durch Plausibilität.

**Plausibilität ist kein semantischer Zustand.** Ein plausibel falscher Code
läuft durch Review und Tests und wird erst spät und teuer sichtbar.

`box-python` löst das durch Reifizierung: Es zwingt ein Projekt dazu, seine
semantischen Regeln explizit als Markdown im Projektroot abzulegen. Ein Agent,
der in diesem Root arbeitet, findet dort vollständige lokale Regeln. Er muss
sie nicht rekonstruieren.

---

## 2. Das Grundprinzip

```text
box-python   = Vorlage
Projektroot  = operative Wahrheit
```

Die Box wird einmal kopiert. Danach gehört alles dem Projekt. Es gibt keine
externe Basis und keine geteilte Laufzeitabhängigkeit. Ein Agent startet im
Projektroot und findet dort vollständige Regeln.

### Markdown-only

Die Box verwendet Markdown als operativen Artefaktraum:

```text
Regeln      → Markdown
Sprechakte  → Markdown
Evidence    → Markdown
Pläne       → Markdown
Glossare    → Markdown
```

Es gibt keine JSON- oder YAML-Nebenautorität für Projektsteuerung. Tools dürfen
Markdown mit stabilen Köpfen lesen und schreiben. Die lokale Wahrheit bleibt
für Menschen lesbar und reviewbar.

---

## 3. Was in der Box steckt

```text
AGENTS.md                         ← operative Hauptautorität für Agenten
AGENTS-COMPACT.md                 ← Schnelleinstieg vor jeder Session
AGENT-SETUP.md                    ← Instanziierungsanleitung, einmalig
.agent-box-template.md            ← Markdown-Manifest der Box
.agent-box/instantiation.md       ← Nachweis des SP0 nach Instanziierung
grundsatz.md                      ← warum das System so aufgebaut ist
package-schema.md                 ← Raumkarte, Importregeln, Known Breaches
preflight-checkliste.md           ← P1–P10 vor jeder nichttrivialen Änderung
task-schnitt.md                   ← Schnitt von Aufgaben und Semantic Working Set
sprechakt-protokoll.md            ← menschliche Festlegungen, SP0–SP7
regelmatrix.md                    ← Autoritätsreihenfolge, Drift-Regeln
test-obligations.md               ← Testpflicht-Matrix
migration-bridges.md              ← Symbolsperren und Bridge-Begriffe
erfahrungsbericht-protokoll.md    ← Lernprotokolle nach Sessions
learning-matrix.md                ← aggregierte Muster aus Erfahrungsberichten
glossar-domain.md                 ← Fachdomänenbegriffe
glossar-system.md                 ← Betriebs- und Metasystembegriffe
glossar-README.md                 ← Ladeprotokoll für das Glossar
docs/plans/template.md            ← geschütztes Plan-Template
tools/check_import_layers.py
tools/check_agent_docs_consistency.py
tools/resolve_test_obligations.py
tools/instantiate/instantiate_project_box.py
```

Jedes Dokument hat eine definierte Autorität. Welches Dokument welche Frage
beantwortet, steht in `regelmatrix.md`.

---

## 4. Konzepte

Fünf Konzepte muss man verstanden haben, bevor man anfängt.

### 4.1 Semantische Räume

Jede Python-Datei gehört zu genau einem semantischen Raum. Der Raum bestimmt,
was dort erlaubt ist, welche Imports zulässig sind, welche Tests nötig sind und
wer beurteilen kann, ob etwas korrekt ist.

```text
domain/          Fachdomäne.
                 Begriffe, die ein Domänenexperte ohne technische Details
                 beurteilen kann. Kein HTTP, keine DB, kein datetime.now(),
                 kein Retry-Zähler, kein GUI-Widget.

system/          System Semantics.
                 Use Cases, Policies, Lifecycle, Fehlerklassifikation.
                 system/ports/ ist die einzige erlaubte Importfläche für
                 infrastructure.

system/ports/    Schmale Port-Fläche.
                 Enthält technische Port-Verträge, DTOs und Fehlerklassen,
                 die infrastructure sehen darf. Keine Use-Case-Logik.

infrastructure/  Implementierungsdomäne.
                 HTTP, DB, Filesystem, externe APIs, Zeit, Zufall.
                 Darf system.ports importieren, sonst nichts aus system.
                 Darf domain nicht direkt importieren.

adapters/        Binding zwischen Räumen.
                 Verdrahtet und übersetzt. Erzeugt keine neue Semantik.

cli/             Einstiegspunkte, Argumente, Environment und einfache UI.
                 Keine Domänenlogik. Darf system und adapters verwenden.

tests/           Testprojektionen. Prüfen Verhalten, definieren keine Semantik.

shared/          Semantisch neutrale Hilfstypen. Darf keine Projekträume importieren.
```

Die **Autonomieregel** ist die schärfste Invariante: Ein Raum ist gültig, wenn
ein einzelner Experte ihn vollständig beurteilen kann, ohne die anderen Räume
zu kennen.

Ein Meteorologe kann `domain/` prüfen, ohne HTTP, Retry oder Tkinter zu kennen.
Sobald ein HTTP-Status-Code oder ein GUI-Widget in `domain/` auftaucht, ist das
eine Autonomieverletzung — kein Compiler-Fehler, aber ein semantischer Fehler.

Ein wichtiger Spezialfall: `infrastructure/` darf `domain/` nicht direkt
importieren. Die Infrastruktur liefert technische Messdaten (ein DTO aus
`system/ports/`). Erst `system/core/` übersetzt diese Messdaten in
Domain-Objekte. Das hält die Implementierungsdomäne frei von Fachbedeutung.

### 4.2 Sprechakte

Ein Sprechakt ist eine menschliche Festlegung. Agenten dürfen analysieren und
Vorschläge machen. Sie dürfen nicht entscheiden.

Wenn ein Agent auf eine Lücke trifft — ein Begriff fehlt im Glossar, eine neue
Fehlerbedeutung würde entstehen, eine Runtime-Dependency wäre nötig — hält er
an und liefert eine Entscheidungsvorlage. Der Mensch entscheidet. Danach steigt
der Agent am definierten Wiedereinstiegspunkt fort.

```text
SP0  Instanziierungs-Sprechakt, einmalig, toolgestützt
SP1  Neuer Fachbegriff
SP2  Neuer systemsemantischer Steuerwert oder neue Raumentscheidung
SP3  Neue Fehlerklasse oder Fehlerbedeutung
SP4  Neue Runtime-Dependency
SP5  Binding-Code würde neue Semantik einführen
SP6  Bekannter Bruch würde verschoben oder umklassifiziert
SP7  Aktiv benötigter Begriff fehlt im Glossar oder ist unvollständig
```

Sprechakt-Artefakte landen unter `docs/sprechakte/` und sind append-only. Jedes
Artefakt hat einen Status: `offen`, `festgelegt`, `abgelehnt` oder `superseded`.

### 4.3 Preflight

Vor jeder nichttrivialen Änderung führt ein Agent Preflight aus.

```text
P1   AGENTS-COMPACT.md lesen
P2   AGENTS.md lesen
P3   package-schema.md gezielt prüfen
P4   betroffene semantische Räume bestimmen
P5   relevante Glossareinträge laden
P6   Import-/Layer-Checker ausführen
P7   Testpflicht ableiten
P8   Schreibrechte prüfen
P9   Task-Schnitt prüfen, wenn T1–T5 eintreten
P10  Plan anlegen, wenn die Änderung nichttrivial ist
```

Ergebnis: `FORTSETZEN`, `TEILEN`, `SPRECHAKT`, `SOFT-ABBRUCH` oder
`HARD-ABBRUCH`.

Preflight ist kein Ritual. Es ist der Schutz gegen Bedeutungserfindung: ohne
Preflight handelt ein Agent auf Basis von Plausibilität statt auf Basis
expliziter lokaler Regeln.

### 4.4 Abbrüche

Agenten brechen ab. Das ist kein Fehler — das ist das System, das funktioniert.

```text
HARD-Abbruch   Stopp. Fortsetzung nur nach expliziter menschlicher Freigabe.
               H1   geschützte Datei ohne Freigabe nötig
               H2   Import-/Layer-Verletzung ohne klassifizierten Bruch
               H3   Widerspruch zwischen Dokumenten und Code
               H4   neuer Begriff ohne Sprechakt
               H5   Tool müsste zur Fehlerunterdrückung geändert werden
               H6   Testpflicht unklar
               H7   Platzhalter in relevanter Regel nicht ersetzt
               H8   Dependency-Änderung nötig
               H9   öffentliche API-Änderung nötig
               H10  Autonomieregel verletzt

SOFT-Abbruch   Stopp mit Evidence. Preflight ermöglicht Wiedereinstieg.
               SA1  Test rot
               SA2  Lint rot
               SA3  Typecheck rot
               SA4  Build-/Installationsfehler
               SA5  unvollständige Migration entdeckt
               SA6  lokale Inkonsistenz ohne semantischen Widerspruch
```

### 4.5 Task-Schnitt

Agenten neigen dazu, zu viel auf einmal anzufassen. Task-Schnitt hält den
Semantic Working Set (SWS) klein, vollständig und scharf.

Task-Schnitt wird bewertet, wenn:

```text
T1  Begriff im SWS hat keinen vollständigen Glossareintrag
T2  Aufgabe berührt mehrere semantische Räume gleichzeitig
T3  Binding-Grenze ist betroffen
T4  Bekannter Bruch ist betroffen
T5  Mehrere Glossarbereiche wären nötig
```

Wenn Teilung möglich ist, wird geteilt. Kein "kurz noch".

---

## 5. Projekt aufsetzen: Regenbogen

Wir bauen jetzt das Regenbogen-Projekt von Anfang an. Es soll:

1. aktuelle Wetterdaten von einer externen API holen,
2. prüfen, ob gleichzeitig Sonnenschein und Regen vorliegen,
3. daraus eine Regenbogen-Wahrscheinlichkeit berechnen,
4. das Ergebnis auf der Kommandozeile ausgeben,
5. später dasselbe Ergebnis in einer GUI anzeigen — mit Konfigurationsdialog
   (Ort + Postleitzahl) und separatem Ausgabefenster,
6. anschließend Postleitzahl und Uhrzeit nutzen, um den Sonnenstand und damit
   das Sichtbarkeitsfenster für einen Regenbogen zu berücksichtigen.

### Schritt 1: Box kopieren

```bash
cp -a agent-boxes/box-python/. ~/projekte/regenbogen/
cd ~/projekte/regenbogen/
```

Der gesamte Box-Inhalt liegt jetzt direkt im Projektroot. Kein Unterordner.

### Schritt 2: Instanziierungs-Sprechakt SP0

```bash
python tools/instantiate/instantiate_project_box.py \
  --project-display-name "Regenbogen" \
  --python-package-name "regenbogen" \
  --source-root src \
  --test-root tests \
  --docs-root docs \
  --tools-root tools \
  --python-lint-cmd "python -m ruff check ." \
  --python-format-check-cmd "python -m ruff format --check ." \
  --python-typecheck-cmd "python -m mypy src" \
  --python-test-cmd "python -m pytest" \
  --full-validation-cmd "python tools/check_agent_docs_consistency.py --instantiated && python tools/check_import_layers.py --preflight src tests tools && python tools/resolve_test_obligations.py --selfcheck --instantiated && python -m pytest"
```

Zwei Namen, eine Entscheidung:

```text
--project-display-name  "Regenbogen"    menschlicher Anzeigename
--python-package-name   "regenbogen"    Python-Importname unter src/
```

Wenn `--python-package-name` fehlt, wird er aus dem Anzeigenamen abgeleitet:
`"Regenbogen" -> "regenbogen"`.

Das Tool ersetzt alle Platzhalter in allen Dokumenten, legt Verzeichnisse an
und schreibt den Nachweis nach `.agent-box/instantiation.md`. Es läuft genau
einmal. Ein zweiter Aufruf wird blockiert.

### Schritt 3: Ergebnis prüfen

```bash
python tools/check_agent_docs_consistency.py --instantiated
```

Erwartete Ausgabe nach frischer Instanziierung:

```text
AGENT-SETUP.md: WARN: AGENT-SETUP.md ist ein Template-Artefakt...
glossar-domain.md: WARN: Keine Glossar-Einträge gefunden.

Agent-Docs-Consistency: WARNINGS (Modus: instantiated)
```

Diese WARNs sind normal und kein Blocker. `glossar-domain.md` ist beim Start
leer — Einträge entstehen durch Sprechakte. `glossar-system.md` enthält bereits
Box- und Metasystembegriffe.

### Schritt 4: Eigene Räume anlegen

Das Instanziierungstool hat bereits angelegt:

```text
src/regenbogen/system/ports/   ← erlaubte Importfläche für infrastructure
```

Jetzt die restlichen Räume:

```bash
mkdir -p src/regenbogen/domain
mkdir -p src/regenbogen/system/core
mkdir -p src/regenbogen/infrastructure
mkdir -p src/regenbogen/adapters
mkdir -p src/regenbogen/cli
mkdir -p tests/domain tests/system tests/infrastructure tests/cli
```

---


### Schritt 5: Der Arbeitszyklus im Beispiel

Ab jetzt folgt jede Session demselben Muster. Das ist wichtiger als der
konkrete Regenbogen-Code:

```text
1. Aufgabe formulieren
2. Preflight P1–P10 ausführen
3. betroffene semantische Räume bestimmen
4. Glossar und package-schema.md gezielt laden
5. entscheiden: FORTSETZEN, TEILEN, SPRECHAKT, SOFT- oder HARD-ABBRUCH
6. bei Sprechakt: Artefakt unter docs/sprechakte/ anlegen
7. nach menschlicher Festlegung: Folgeartefakte aktualisieren
8. implementieren
9. Import-Checker und Testpflicht ausführen
10. Tests und Checks ausführen
11. bei nichttrivialer Session: Erfahrungsbericht schreiben
```

Die folgenden Sessions zeigen diesen Zyklus mehrfach. Wichtig ist nicht, dass
jeder Beispielbefehl in jedem Projekt identisch aussieht. Wichtig ist, dass der
Agent nicht direkt vom Wunsch zum Code springt. Er bewegt sich durch einen
kontrollierten Entscheidungsraum.

## 6. Erste Session: Domainkern

**Aufgabe:** Typen und Regeln für Wetterzustand und Regenbogen-Berechnung.

### 6.1 Preflight

**P1/P2 — AGENTS-COMPACT.md und AGENTS.md lesen**

Der Agent notiert:
- `domain/` für Fachbegriffe ohne Laufzeitmechanik
- Invariante I1: domain ist frei von HTTP, DB, datetime.now()
- H4: neuer Begriff ohne Sprechakt → HARD-Abbruch

**P3 — package-schema.md prüfen**

Erlaubt in `domain/`: Value Objects, Entities, fachliche Regeln.
Verboten: HTTP, DB, Framework-Typen, datetime.now(), random(), GUI-Widgets.

Kompetenzfrage: Kann ein Meteorologe diesen Begriff beurteilen, ohne HTTP zu
kennen?

**P4 — Räume bestimmen**

```text
src/regenbogen/domain/wetter.py    → domain
src/regenbogen/domain/regenbogen.py → domain
```

**P5 — Glossareinträge laden**

Der Agent lädt `glossar-domain.md`. Er findet: leer.

Aktiv gebrauchte Begriffe:

```text
Wetterzustand
Sonnenschein
Regen
RegenbogenWahrscheinlichkeit
```

Keiner ist im Glossar. T1 tritt ein.

**P9 — Task-Schnitt**

Kann die Aufgabe ohne diese Begriffe abgeschlossen werden? Nein — sie sind der
Kern der Iteration. Task-Schnitt hilft hier nicht weiter.

Ergebnis: **SPRECHAKT SP7**.

### 6.2 Sprechakt SP7: Kernbegriffe

```markdown
# Sprechakt: Wetterzustand und Regenbogen-Begriffe

Aufgabe:          Domainkern Regenbogen-Wahrscheinlichkeit implementieren
Zeitpunkt:        2026-06-10 09:15
Sprechakt-Klasse: SP7 — Aktiv benötigte Begriffe fehlen im Glossar
Betroffener Begriff: Wetterzustand, Sonnenschein, Regen,
                     RegenbogenWahrscheinlichkeit
Status: offen

## Was fehlt

glossar-domain.md enthält keine Einträge für die Kernbegriffe.
Ohne Definitionen kann der Agent nicht entscheiden:
- welche Wetterzustände unterschieden werden
- ob Sonnenschein und Regen gleichzeitig auftreten können
- wie RegenbogenWahrscheinlichkeit definiert und berechnet wird

## Was der Agent sieht

symbol:       Wetterzustand
glossar_says: nicht vorhanden
schema_says:  domain/ ist der richtige Raum

symbol:       RegenbogenWahrscheinlichkeit
glossar_says: nicht vorhanden
schema_says:  domain/ ist der richtige Raum

## Analyse des Agenten

Die Frage, ob Sonnenschein und Regen gleichzeitig ein gültiger Zustand sind
(und nicht eine Exception), ist fachlich, nicht technisch. Ohne Festlegung
würde jede Implementierung eine stille Bedeutungsentscheidung treffen.

## Warum der Agent nicht fortfahren kann

Ohne festgelegte Begriffe würde der Agent Fachentscheidungen im Code treffen.

## Was der Mensch festlegt

[wird nach menschlicher Entscheidung ergänzt]

## Was der Agent danach tut

Glossareinträge anlegen, dann domain/ implementieren.
```

Ort: `docs/sprechakte/2026-06-10-wetterzustand-begriffe.md`.

### 6.3 Mensch entscheidet

```markdown
## Was der Mensch festlegt

Wetterzustand:
  Beobachtete Kombination von Wetterphänomenen zu einem Zeitpunkt an einem
  Ort. Mehrere Phänomene können gleichzeitig auftreten — Normalfall, keine
  Ausnahme.

Sonnenschein:
  Direkte Sonneneinstrahlung ohne vollständige Wolkendecke.
  Messbar durch Intensität (0.0–1.0).

Regen:
  Niederschlag in flüssiger Form, erkennbare Intensität.
  Messbar durch Intensität (0.0–1.0).

RegenbogenWahrscheinlichkeit:
  Prozentwert in [0, 100].
  Invarianten:
    - Ohne Sonnenschein: immer 0.
    - Ohne Regen: immer 0.
    - Beide vorhanden: größer 0.

Status: festgelegt
Folgeartefakte: glossar-domain.md
```

### 6.4 Wiedereinstieg: Glossar füllen

Der Agent trägt die Begriffe in `glossar-domain.md` ein.
Eintragsformat: `### <Begriffsname>` als Heading-Ebene 3 in Abschnitt 3.

```markdown
### Wetterzustand

Bedeutung: Beobachtete Kombination von Wetterphänomenen zu einem Zeitpunkt
an einem Ort. Mehrere Phänomene können gleichzeitig auftreten.

Invariante: Sonnenschein und Regen zur selben Zeit ist ein gültiger Zustand,
kein Fehlerfall.

Projektionen:
- Code: src/regenbogen/domain/wetter.py
- Tests: tests/domain/test_regenbogen.py

Migrationsstatus: canonical

---

### RegenbogenWahrscheinlichkeit

Bedeutung: Prozentwert in [0, 100].

Invarianten:
- Ohne Sonnenschein: 0.
- Ohne Regen: 0.
- Beide vorhanden: > 0.

Projektionen:
- Code: src/regenbogen/domain/regenbogen.py
- Tests: tests/domain/test_regenbogen.py

Migrationsstatus: canonical
```

**P6 — Import-Checker nach dem Glossar-Eintrag:**

```bash
python tools/check_import_layers.py --preflight src
```

```text
✓ PREFLIGHT IMPORT-LAYER OK (0 Dateien geprüft)
```

Null Dateien — `src/regenbogen/domain/` ist noch leer. OK.

**P7 — Testpflicht ableiten:**

```bash
python tools/resolve_test_obligations.py \
  --changed-file src/regenbogen/domain/wetter.py
```

```text
Grund: Domain-Code geändert.
Checks: lint, format, typecheck, import-layer-check
Tests:  domain-tests
```

Ergebnis: **FORTSETZEN**

### 6.5 Implementierung

```python
# src/regenbogen/domain/wetter.py
from dataclasses import dataclass


@dataclass(frozen=True)
class Wetterzustand:
    """Beobachtete Wetterphänomene an einem Ort zu einem Zeitpunkt.

    Sonnenschein und Regen können gleichzeitig auftreten.
    Das ist kein Ausnahmefall.
    """

    sonnenschein: bool
    regen: bool
    sonnenschein_intensitaet: float = 0.0
    regen_intensitaet: float = 0.0

    def __post_init__(self) -> None:
        if not (0.0 <= self.sonnenschein_intensitaet <= 1.0):
            raise ValueError("sonnenschein_intensitaet muss in [0.0, 1.0] liegen")
        if not (0.0 <= self.regen_intensitaet <= 1.0):
            raise ValueError("regen_intensitaet muss in [0.0, 1.0] liegen")
        if self.sonnenschein and self.sonnenschein_intensitaet == 0.0:
            raise ValueError("sonnenschein=True erfordert Intensität > 0.0")
        if self.regen and self.regen_intensitaet == 0.0:
            raise ValueError("regen=True erfordert Intensität > 0.0")
```

```python
# src/regenbogen/domain/regenbogen.py
from regenbogen.domain.wetter import Wetterzustand


def berechne_regenbogen_wahrscheinlichkeit(zustand: Wetterzustand) -> int:
    """Regenbogen-Wahrscheinlichkeit als Prozentwert in [0, 100].

    Invarianten laut Glossar:
    - Ohne Sonnenschein: 0
    - Ohne Regen: 0
    - Beide vorhanden: > 0
    """
    if not zustand.sonnenschein or not zustand.regen:
        return 0

    wahrscheinlichkeit = (
        zustand.sonnenschein_intensitaet * 0.6
        + zustand.regen_intensitaet * 0.4
    ) * 100

    return max(1, min(100, round(wahrscheinlichkeit)))
```

### 6.6 Tests und Abschluss

```python
# tests/domain/test_regenbogen.py
from regenbogen.domain.regenbogen import berechne_regenbogen_wahrscheinlichkeit
from regenbogen.domain.wetter import Wetterzustand


def test_kein_sonnenschein_ergibt_null():
    zustand = Wetterzustand(sonnenschein=False, regen=True, regen_intensitaet=0.8)
    assert berechne_regenbogen_wahrscheinlichkeit(zustand) == 0


def test_kein_regen_ergibt_null():
    zustand = Wetterzustand(
        sonnenschein=True, regen=False, sonnenschein_intensitaet=0.9
    )
    assert berechne_regenbogen_wahrscheinlichkeit(zustand) == 0


def test_beide_faktoren_ergeben_groesser_null():
    zustand = Wetterzustand(
        sonnenschein=True,
        regen=True,
        sonnenschein_intensitaet=0.5,
        regen_intensitaet=0.5,
    )
    assert berechne_regenbogen_wahrscheinlichkeit(zustand) > 0


def test_ergebnis_in_range():
    zustand = Wetterzustand(
        sonnenschein=True,
        regen=True,
        sonnenschein_intensitaet=1.0,
        regen_intensitaet=1.0,
    )
    ergebnis = berechne_regenbogen_wahrscheinlichkeit(zustand)
    assert 0 <= ergebnis <= 100
```

Abschluss:

```bash
python tools/check_import_layers.py --preflight src tests
python -m ruff check .
python -m mypy src
python -m pytest tests/domain/
```

Alle grün. Erfahrungsbericht schreiben — diese Session hat einen SP7 ausgelöst
und neue Domain-Begriffe eingeführt, beides erfordert einen Bericht.

```markdown
# Erfahrungsbericht: Domain-Session Regenbogen-Kern

Datum:        2026-06-10
Session-Typ:  abgeschlossen
Aufgabe:      Domainkern — Wetterzustand und Regenbogen-Wahrscheinlichkeit
Ergebnis:     Glossar gefüllt, domain/ implementiert, Tests grün

Learning-Matrix-Kandidat: nein

## Was sich bewährt hat

SP7 hat verhindert, dass der Agent die Frage "dürfen Sonnenschein und Regen
gleichzeitig auftreten?" still entscheidet. Ohne Sprechakt wäre das eine
unsichtbare Fachentscheidung im Code geworden.

## Was heute nicht geändert werden soll

Die Berechnungsformel (0.6/0.4) ist ein Placeholder.
Die meteorologisch korrekte Gewichtung ist eine spätere Entscheidung.
```

Ort: `tmp/erfahrungsberichte/2026-06-10-EB-domain-kern.md`.

---

## 7. Zweite Session: Port und Infrastruktur

**Aufgabe:** Wetterdaten von einer externen API holen.

Der zentrale Architekturpunkt dieser Session: `infrastructure/` darf nicht
direkt `domain/` importieren. Die Infrastruktur liefert technische Messdaten
als DTO aus `system/ports/`. Erst `system/core/` übersetzt diese Messdaten
in einen `Wetterzustand`.

Diese Trennung ist nicht offensichtlich. Die intuitive Lösung wäre, dass der
API-Client direkt `Wetterzustand` zurückgibt. Das würde aber bedeuten: die
Implementierungsdomäne trifft fachliche Entscheidungen (was ist Sonnenschein?
Ab wann ist es Regen?). Das ist eine Autonomieverletzung (H10).

### 7.1 Preflight

**P4 — Räume bestimmen:**

```text
src/regenbogen/system/ports/wetterapi_port.py       → system.ports
src/regenbogen/infrastructure/open_meteo_client.py  → infrastructure
```

Die Aufgabe berührt zwei Räume. T2 tritt ein. Der Schnitt ist trotzdem
zulässig, weil `system.ports` genau die erlaubte Importfläche für
`infrastructure` ist — die beiden Räume sind hier sachlich untrennbar.

**P5 — Glossar prüfen:**

`WetterApiNichtErreichbar` und `OrtNichtGefunden` sind neue Fehlerklassen.
Das sind neue Fehlerbedeutungen → SP3 nötig.

Außerdem wird `httpx` benötigt — eine neue Runtime-Dependency → SP4 nötig.

Zwei Sprechakte in einer Session. Das ist zulässig, wenn beide denselben
Aufgabenschnitt betreffen.

Ergebnis: **SPRECHAKT SP4 + SP3**.

### 7.2 Sprechakt SP4: Runtime-Dependency httpx

```markdown
# Sprechakt: Runtime-Dependency httpx

Zeitpunkt:        2026-06-11 10:05
Sprechakt-Klasse: SP4 — Neue Runtime-Dependency
Betroffener Begriff: httpx
Status: offen

## Was fehlt

Für den externen Wetterdienst wird ein HTTP-Client benötigt.

## Analyse des Agenten

Optionen:
- urllib.request: Standardbibliothek, aber unergonomisch und schlechter testbar.
- requests: verbreitet, aber synchron und zusätzliche PyPI-Dependency.
- httpx: synchron nutzbar, gut testbar, moderne API. PyPI-Dependency.

## Was der Agent sieht

Kein bestehender HTTP-Client im Projekt. Kein Eintrag in pyproject.toml.

## Warum der Agent nicht fortfahren kann

Eine neue Runtime-Dependency ist eine Projektentscheidung.
Der Agent darf pyproject.toml nicht still ändern.

## Was der Mensch festlegt

httpx ist als Runtime-Dependency erlaubt.
Status: festgelegt
Folgeartefakte: Dependency-Datei, INSTALLATION.md

## Was der Agent danach tut

httpx in die konkrete Dependency-Datei des Projekts eintragen, dann Port und
Infrastruktur implementieren.
```

Ort: `docs/sprechakte/2026-06-11-httpx-dependency.md`.

`box-python` schreibt kein Packaging-Werkzeug vor. Deshalb ist das konkrete
Folgeartefakt projektspezifisch:

```text
pyproject.toml      bei uv, hatch, poetry oder moderner PEP-621-Konfiguration
requirements.txt    bei einfachen Projekten
setup.cfg/setup.py   bei älteren Projekten
INSTALLATION.md      wenn eine manuelle Installationsnotiz nötig ist
```

Wichtig ist nicht das Werkzeug. Wichtig ist der Rückfluss: Die SP4-Entscheidung
muss in dem Artefakt landen, das die Runtime-Abhängigkeiten des Projekts
steuert. Wenn das Projekt zusätzlich eine `INSTALLATION.md` pflegt, muss dort
stehen, dass `httpx` eine Runtime-Abhängigkeit für den Wetter-API-Client ist.

### 7.3 Sprechakt SP3: Fehlerklassen

```markdown
# Sprechakt: Fehlerklassen WetterApi

Zeitpunkt:        2026-06-11 10:20
Sprechakt-Klasse: SP3 — Neue Fehlerklasse oder Fehlerbedeutung
Betroffener Begriff: WetterApiNichtErreichbar, OrtNichtGefunden
Status: offen

## Was fehlt

Zwei Fehlerklassen entstehen beim Port-Design. Ob sie recoverable oder
terminal sind und wer darüber entscheidet, ist nicht festgelegt.

## Analyse des Agenten

WetterApiNichtErreichbar: technische Ursache, könnte transient sein.
  → Retry möglich, aber system muss das entscheiden, nicht infrastructure.
OrtNichtGefunden: fachliche Ursache, vermutlich permanent.
  → Kein Retry sinnvoll. Direkt an Aufrufer weitergeben.

Beide Fehler entstehen in infrastructure, ihre Bedeutung gehört in system.

## Was der Mensch festlegt

WetterApiNichtErreichbar:
  Recoverable. System darf Retry anwenden (max. 3 Versuche).

OrtNichtGefunden:
  Terminal. Kein Retry. Direkt an Aufrufer weitergeben.

Status: festgelegt
Folgeartefakte: glossar-system.md

## Was der Agent danach tut

Glossareinträge anlegen, Port implementieren.
```

Ort: `docs/sprechakte/2026-06-11-fehlerklassen-wetterapi.md`.

### 7.4 Wiedereinstieg: System-Glossar ergänzen

```markdown
### WetterApiNichtErreichbar

Bedeutung: Die Wetter-API ist vorübergehend nicht erreichbar. Recoverable.
Retry bis zu dreimal erlaubt.

Invariante: Nach drei Fehlversuchen wird der Fehler als terminal behandelt.

Projektionen:
- Code: src/regenbogen/system/ports/wetterapi_port.py
- Code: src/regenbogen/system/core/wahrscheinlichkeit_use_case.py
- Tests: tests/system/test_use_case.py

Migrationsstatus: canonical

---

### OrtNichtGefunden

Bedeutung: Der angefragte Ort ist unbekannt. Terminal. Kein Retry.

Projektionen:
- Code: src/regenbogen/system/ports/wetterapi_port.py
- Tests: tests/system/test_use_case.py

Migrationsstatus: canonical
```

### 7.5 Port-Vertrag

```python
# src/regenbogen/system/ports/wetterapi_port.py
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class WetterApiMessung:
    """Technische Messung der Wetter-API.

    Dieser Typ ist bewusst kein Domain-Typ. Er beschreibt Rohdaten der
    externen API. Die fachliche Interpretation passiert in system/core/.
    """

    sonnenschein_sekunden: float
    niederschlag_mm: float


class WetterApiNichtErreichbar(Exception):
    """API nicht erreichbar. Recoverable — Retry erlaubt."""


class OrtNichtGefunden(Exception):
    """Unbekannter Ort. Terminal — kein Retry."""


class WetterApiPort(ABC):
    @abstractmethod
    def hole_aktuelle_messung(self, ort: str) -> WetterApiMessung:
        """Liefert rohe technische Wetterdaten für einen Ort."""
```

Die Grenze ist hier explizit: `WetterApiMessung` ist kein `Wetterzustand`.
Sie enthält keine Fachentscheidungen. Ein Meteorologe könnte nicht beurteilen,
ob `sonnenschein_sekunden=1800` zu "Sonnenschein im fachlichen Sinne" führt —
das entscheidet erst `system/core/`.

### 7.6 Infrastruktur-Implementierung

```python
# src/regenbogen/infrastructure/open_meteo_client.py
import httpx

from regenbogen.system.ports.wetterapi_port import (
    OrtNichtGefunden,
    WetterApiMessung,
    WetterApiNichtErreichbar,
    WetterApiPort,
)


class OpenMeteoClient(WetterApiPort):
    """Implementiert WetterApiPort über die Open-Meteo API.

    Dieser frühe Stand löst den Ortsnamen noch lokal in Koordinaten auf.
    In Session 11 wird diese Verantwortung sauber in einen StandortPort
    verschoben.
    """

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def hole_aktuelle_messung(self, ort: str) -> WetterApiMessung:
        latitude, longitude = self._ort_zu_koordinaten(ort)
        try:
            response = httpx.get(
                self.BASE_URL,
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": "sunshine_duration,precipitation",
                },
                timeout=10.0,
            )
            response.raise_for_status()
        except httpx.ConnectError as exc:
            raise WetterApiNichtErreichbar(f"Nicht erreichbar: {exc}") from exc
        except httpx.HTTPStatusError as exc:
            raise WetterApiNichtErreichbar(
                f"API-Fehler: {exc.response.status_code}"
            ) from exc

        return self._parse_response(response.json())

    def _ort_zu_koordinaten(self, ort: str) -> tuple[float, float]:
        if ort == "Berlin":
            return 52.532, 13.384
        if ort == "Muenchen":
            return 48.137, 11.575
        raise OrtNichtGefunden(ort)

    def _parse_response(self, data: dict) -> WetterApiMessung:
        current = data.get("current", {})
        return WetterApiMessung(
            sonnenschein_sekunden=float(current.get("sunshine_duration", 0.0)),
            niederschlag_mm=float(current.get("precipitation", 0.0)),
        )
```

Importregel — gilt für alle infrastructure-Dateien:

```text
infrastructure -> system.ports   erlaubt
infrastructure -> domain         verboten
infrastructure -> system.core    verboten
```

### 7.7 Import-Checker und Abschluss

```bash
python tools/check_import_layers.py --preflight src
```

```text
✓ PREFLIGHT IMPORT-LAYER OK (2 Dateien geprüft)
```

```bash
python tools/resolve_test_obligations.py \
  --changed-file src/regenbogen/infrastructure/open_meteo_client.py
```

```text
Grund: Infrastructure-Code geändert.
Tests:  infrastructure-tests, contract-or-fake-tests
```

```bash
python -m ruff check .
python -m mypy src
```

Erfahrungsbericht schreiben (Session hatte SP3 + SP4):

```markdown
# Erfahrungsbericht: Port- und Infrastruktur-Session

Datum:        2026-06-11
Session-Typ:  abgeschlossen
Aufgabe:      Port-Vertrag und API-Client für Wetterdaten
Ergebnis:     system/ports/ und infrastructure/ implementiert, Tests grün

Learning-Matrix-Kandidat: nein

## Was sich bewährt hat

Die Trennung WetterApiMessung vs. Wetterzustand war nicht offensichtlich.
SP3 hat verhindert, dass der Agent die Fehlerklassen mit ihren
Recovery-Bedeutungen still entscheidet.
SP4 hat verhindert, dass httpx ohne Freigabe in pyproject.toml landet.

Die explizite WetterApiMessung als DTO macht die Systemgrenze sichtbar:
infrastructure endet hier, die Fachinterpretation beginnt in system/core.
```

Ort: `tmp/erfahrungsberichte/2026-06-11-EB-port-infra.md`.

---

## 8. Dritte Session: System-Logik

**Aufgabe:** Use Case mit Retry-Policy, Mapping von API-Messung nach Domain
und vollständiges Ergebnisobjekt für CLI und GUI.

### 8.1 Preflight

**P4 — Räume bestimmen:**

```text
src/regenbogen/system/core/wahrscheinlichkeit_use_case.py → system.core
```

`system/core/` darf importieren: `system.ports`, `domain`.
Beide Räume sind hier nötig — das Mapping von `WetterApiMessung` nach
`Wetterzustand` ist genau die Aufgabe von `system/core/`.

**P5 — Glossar prüfen:**

Die Fehlerklassen aus SP3 sind bereits in `glossar-system.md`. ✓

Der Agent bemerkt: Er braucht `WetterErgebnis` — ein neues Objekt, das Ort,
Zustand und Wahrscheinlichkeit zusammenführt. Das ist kein Fachbegriff aus
`domain/`, sondern ein systemsemantischer Steuerwert — ein Ergebnisobjekt für
Einstiegspunkte (CLI und GUI).

→ SP2 wäre denkbar, aber der Agent bewertet: `WetterErgebnis` erzeugt keine
neue Semantik, es aggregiert bestehende. Das ist Systemlogik, kein Sprechakt.
Kein SP2 nötig.

Trotzdem muss `WetterErgebnis` ins System-Glossar. Der Grund ist wichtig:
Nicht jeder neue systemsemantische Begriff braucht einen Sprechakt, aber jeder
aktiv verwendete systemsemantische Begriff braucht eine sichtbare Bedeutung.
Der Agent ergänzt deshalb `glossar-system.md`:

```markdown
### WetterErgebnis

Bedeutung: Systemsemantisches Ergebnisobjekt für Einstiegspunkte.
Es bündelt Ort, fachlichen Wetterzustand und berechnete
Regenbogen-Wahrscheinlichkeit.

Invariante: Einstiegspunkte dürfen WetterErgebnis anzeigen oder formatieren,
aber nicht neu berechnen und keine Domain-Funktionen direkt aufrufen.

Projektionen:
- Code: src/regenbogen/system/core/wahrscheinlichkeit_use_case.py
- Verbraucher: src/regenbogen/cli/main.py
- Verbraucher: src/regenbogen/cli/gui_main.py
- Tests: tests/system/test_use_case.py

Migrationsstatus: canonical
```

**P6 — Import-Checker (vorausschauend):**

```text
system.core → system.ports   erlaubt
system.core → domain         erlaubt
```

Ergebnis: **FORTSETZEN**

### 8.2 Implementierung

```python
# src/regenbogen/system/core/wahrscheinlichkeit_use_case.py
from collections.abc import Callable
from dataclasses import dataclass

from regenbogen.domain.regenbogen import berechne_regenbogen_wahrscheinlichkeit
from regenbogen.domain.wetter import Wetterzustand
from regenbogen.system.ports.wetterapi_port import (
    OrtNichtGefunden,
    WetterApiMessung,
    WetterApiNichtErreichbar,
    WetterApiPort,
)


@dataclass(frozen=True)
class WetterErgebnis:
    ort: str
    zustand: Wetterzustand
    wahrscheinlichkeit: int


class RegenbogenWahrscheinlichkeitUseCase:
    MAX_VERSUCHE = 3

    def __init__(self, api: WetterApiPort, sleep: Callable[[float], None]) -> None:
        self._api = api
        self._sleep = sleep

    def berechne(self, ort: str) -> int:
        return self.berechne_vollstaendig(ort).wahrscheinlichkeit

    def berechne_vollstaendig(self, ort: str) -> WetterErgebnis:
        messung = self._hole_messung_mit_retry(ort)
        zustand = self._messung_zu_wetterzustand(messung)
        wahrscheinlichkeit = berechne_regenbogen_wahrscheinlichkeit(zustand)
        return WetterErgebnis(
            ort=ort,
            zustand=zustand,
            wahrscheinlichkeit=wahrscheinlichkeit,
        )

    def _hole_messung_mit_retry(self, ort: str) -> WetterApiMessung:
        letzter_fehler: WetterApiNichtErreichbar | None = None

        for versuch in range(1, self.MAX_VERSUCHE + 1):
            try:
                return self._api.hole_aktuelle_messung(ort)
            except WetterApiNichtErreichbar as exc:
                letzter_fehler = exc
                if versuch < self.MAX_VERSUCHE:
                    self._sleep(1.0)
            except OrtNichtGefunden:
                raise

        assert letzter_fehler is not None
        raise letzter_fehler

    def _messung_zu_wetterzustand(self, messung: WetterApiMessung) -> Wetterzustand:
        sonnenschein_intensitaet = min(messung.sonnenschein_sekunden / 3600.0, 1.0)
        regen_intensitaet = min(messung.niederschlag_mm / 10.0, 1.0)
        return Wetterzustand(
            sonnenschein=sonnenschein_intensitaet > 0.0,
            regen=regen_intensitaet > 0.0,
            sonnenschein_intensitaet=sonnenschein_intensitaet,
            regen_intensitaet=regen_intensitaet,
        )
```

Warum `sleep` injiziert wird: Der Use Case hat eine Wartezeit von 1 Sekunde
zwischen Retries. In Tests wäre echtes Warten inakzeptabel. Die Lösung ist
Dependency Injection: `sleep` ist ein Callable, das in Tests durch
`lambda _: None` ersetzt wird. Die produktive Verdrahtung mit `time.sleep`
passiert in `adapters/wiring.py`. Der Use Case selbst bleibt testbar ohne
`monkeypatch`.

### 8.3 Tests

```python
# tests/system/test_use_case.py
from unittest.mock import MagicMock

import pytest

from regenbogen.system.core.wahrscheinlichkeit_use_case import (
    RegenbogenWahrscheinlichkeitUseCase,
)
from regenbogen.system.ports.wetterapi_port import (
    OrtNichtGefunden,
    WetterApiMessung,
    WetterApiNichtErreichbar,
    WetterApiPort,
)


def make_uc(api):
    return RegenbogenWahrscheinlichkeitUseCase(
        api=api,
        sleep=lambda _: None,
    )


def gute_messung() -> WetterApiMessung:
    return WetterApiMessung(
        sonnenschein_sekunden=1800.0,
        niederschlag_mm=5.0,
    )


def test_gibt_wahrscheinlichkeit_zurueck():
    api = MagicMock(spec=WetterApiPort)
    api.hole_aktuelle_messung.return_value = gute_messung()
    uc = make_uc(api)
    assert uc.berechne("Berlin") > 0


def test_retry_bei_api_nicht_erreichbar():
    api = MagicMock(spec=WetterApiPort)
    api.hole_aktuelle_messung.side_effect = [
        WetterApiNichtErreichbar("timeout"),
        WetterApiNichtErreichbar("timeout"),
        gute_messung(),
    ]
    uc = make_uc(api)
    assert uc.berechne("Berlin") > 0
    assert api.hole_aktuelle_messung.call_count == 3


def test_kein_retry_bei_ort_nicht_gefunden():
    api = MagicMock(spec=WetterApiPort)
    api.hole_aktuelle_messung.side_effect = OrtNichtGefunden("Atlantis")
    uc = make_uc(api)
    with pytest.raises(OrtNichtGefunden):
        uc.berechne("Atlantis")
    assert api.hole_aktuelle_messung.call_count == 1


def test_fehler_nach_max_versuchen():
    api = MagicMock(spec=WetterApiPort)
    api.hole_aktuelle_messung.side_effect = WetterApiNichtErreichbar("down")
    uc = make_uc(api)
    with pytest.raises(WetterApiNichtErreichbar):
        uc.berechne("Berlin")
    assert api.hole_aktuelle_messung.call_count == 3


def test_berechne_vollstaendig_gibt_zustand_und_wahrscheinlichkeit():
    api = MagicMock(spec=WetterApiPort)
    api.hole_aktuelle_messung.return_value = gute_messung()
    uc = make_uc(api)
    ergebnis = uc.berechne_vollstaendig("Berlin")
    assert ergebnis.ort == "Berlin"
    assert ergebnis.zustand.sonnenschein is True
    assert ergebnis.wahrscheinlichkeit > 0
```

---

## 9. Vierte Session: CLI und Wiring

**Aufgabe:** Kommandozeilen-Einstiegspunkt und Verdrahtung der Infrastruktur.

### 9.1 Preflight

**P3 — package-schema.md prüfen:**

`cli/` darf importieren: `system`, `adapters`. Nicht direkt: `infrastructure`.

Ein naiver erster Versuch wäre:

```python
# FALSCH — cli darf infrastructure nicht direkt importieren
from regenbogen.infrastructure.open_meteo_client import OpenMeteoClient
```

Das ist eine `cli -> infrastructure`-Kante. In der Capability-Matrix hat diese
Kante den Wert `decision`: nicht automatisch erlaubt, braucht explizite
Freigabe. Der Import-Checker würde H2 auslösen.

Die korrekte Lösung: Die Verdrahtung gehört nach `adapters/wiring.py`.
`cli/` fragt den Adapter, nicht direkt die Infrastruktur.

Ergebnis: **FORTSETZEN** (keine neuen Begriffe, Wiring ist Adapter-Aufgabe)

### 9.2 Adapter-Wiring

```python
# src/regenbogen/adapters/wiring.py
import time

from regenbogen.infrastructure.open_meteo_client import OpenMeteoClient
from regenbogen.system.core.wahrscheinlichkeit_use_case import (
    RegenbogenWahrscheinlichkeitUseCase,
)


def create_regenbogen_use_case() -> RegenbogenWahrscheinlichkeitUseCase:
    """Verdrahtet Standard-Infrastruktur mit dem Use Case."""
    return RegenbogenWahrscheinlichkeitUseCase(
        api=OpenMeteoClient(),
        sleep=time.sleep,
    )
```

Damit ist `time.sleep` genau einmal im Produktionscode sichtbar: in `adapters/`.
Der Use Case selbst bleibt testbar ohne Monkeypatching.

### 9.3 CLI-Implementierung

```python
# src/regenbogen/cli/main.py
import argparse
import sys

from regenbogen.adapters.wiring import create_regenbogen_use_case
from regenbogen.system.ports.wetterapi_port import (
    OrtNichtGefunden,
    WetterApiNichtErreichbar,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Berechnet die Regenbogen-Wahrscheinlichkeit für einen Ort."
    )
    parser.add_argument("ort", help="Ortsname, z. B. Berlin")
    args = parser.parse_args()

    use_case = create_regenbogen_use_case()

    try:
        wahrscheinlichkeit = use_case.berechne(args.ort)
    except OrtNichtGefunden:
        print(f"Fehler: Ort {args.ort!r} nicht gefunden.", file=sys.stderr)
        return 1
    except WetterApiNichtErreichbar:
        print("Fehler: Wetterdienst nicht erreichbar.", file=sys.stderr)
        return 2

    print(f"Regenbogen-Wahrscheinlichkeit in {args.ort}: {wahrscheinlichkeit}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### 9.4 Import-Checker und Abschluss

```bash
python tools/check_import_layers.py --preflight src
```

```text
✓ PREFLIGHT IMPORT-LAYER OK (5 Dateien geprüft)
```

Vollständige Importkette:

```text
cli -> adapters                  erlaubt
cli -> system.ports              erlaubt (Fehlerbehandlung)
adapters -> infrastructure       erlaubt
adapters -> system.core          erlaubt
infrastructure -> system.ports   erlaubt
system.core -> domain            erlaubt
system.core -> system.ports      erlaubt
```

```bash
python -m ruff check .
python -m mypy src
python -m pytest
```

### 9.5 Optionaler Abbruchpfad: H2 und Wiedereinstieg

Dieser Abschnitt ist eine **Verzweigung**, nicht Teil des grünen Hauptpfads.
Er zeigt, was passiert, wenn ein Agent den naiven Weg aus 9.1 tatsächlich
umsetzt. Die folgenden Schnipsel werden nicht in das Beispielprojekt übernommen.

Auslöser:

```text
# NICHT IN DEN HAUPTPFAD ÜBERNEHMEN
# src/regenbogen/cli/main.py
from regenbogen.infrastructure.open_meteo_client import OpenMeteoClient
```

Der Import-Checker meldet eine verbotene Kante:

```text
H2 HARD-ABBRUCH
Datei: src/regenbogen/cli/main.py
Kante: cli -> infrastructure
Grund: Einstiegspunkt darf konkrete Infrastruktur nicht direkt verdrahten.
```

Der Agent darf jetzt nicht selbst „kurz fixen“. Er schreibt ein
Abbruchartefakt, zum Beispiel:

```markdown
# HARD-Abbruch: cli importiert infrastructure

Status: HARD-ABBRUCH
Abbruch-Code: H2
Datei: src/regenbogen/cli/main.py
Fehler: cli/main.py importiert OpenMeteoClient direkt aus infrastructure/.

## Evidence

Import-Checker meldet cli -> infrastructure.
Diese Kante ist nicht automatisch erlaubt.

## Entscheidungsvorlage

Option A: Direkte Kante freigeben.
  Folge: package-schema.md und Known Breach nötig.

Option B: Keine Freigabe. Verdrahtung nach adapters/wiring.py verschieben.
  Folge: cli importiert nur create_regenbogen_use_case().

## Menschliche Entscheidung

Option B. Keine direkte cli -> infrastructure-Kante.

## Wiedereinstieg

1. adapters/wiring.py anlegen oder erweitern.
2. cli/main.py auf create_regenbogen_use_case() umstellen.
3. Import-Checker erneut ausführen.
4. Danach normal in Abschnitt 9.2 fortsetzen.
```

Damit bleibt der Hauptpfad grün, aber der Leser sieht den realen
Abbruchpfad: H2 erzeugt kein Chaos, sondern einen definierten Wiedereinstieg.

---

## 10. Fünfte Session: GUI mit Tkinter

**Aufgabe:** Zusätzlich zur CLI soll eine grafische Oberfläche entstehen.
Der Ablauf: Ein modaler Konfigurationsdialog nimmt Ort und Postleitzahl
entgegen. Nach Bestätigung öffnet ein Ausgabefenster mit dem aktuellen Wetter
und der Regenbogen-Wahrscheinlichkeit.

Diese Session ist absichtlich lehrreich: Eine GUI klingt wie eine kleine
Oberflächenänderung, wirft aber mehrere semantische Fragen auf, die ohne
explizite Festlegung still falsch beantwortet würden.

### 10.1 Preflight: Warum die Aufgabe nicht sofort umgesetzt wird

**P1/P2 — AGENTS-COMPACT.md und AGENTS.md lesen**

Der Agent notiert:

```text
cli/      Einstiegspunkte, Argumente, Environment und einfache UI.
adapters/ Binding und Verdrahtung.
system/   Use Cases und Ergebnisobjekte.

H8  Dependency-Änderung nötig.
H1  geschützte Datei ohne Freigabe nötig.
H10 Autonomieregel verletzt.
```

**P3 — package-schema.md prüfen**

Die aktuelle Box kennt keinen eigenen `gui/`-Raum. `cli/` ist der Raum für
Einstiegspunkte. Eine GUI kann dort liegen, aber das ist keine rein technische
Dateientscheidung: Es betrifft Importregeln, Testpflicht und künftige
Raumgrenzen.

**P4 — Räume bestimmen**

```text
Konfigurationsdialog:  Eingabe (Ort, PLZ), wahrscheinlich cli/
Ausgabefenster:        zeigt WetterErgebnis an, wahrscheinlich cli/
Formatierungslogik:    testbare Anzeigeübersetzung, cli/
Gesamtablauf:          cli/ oder neuer Raum gui/?
Wiring:                bereits in adapters/wiring.py vorhanden
Use Case:              bereits in system/core/ vorhanden
```

**P5 — Glossar prüfen**

`OrtKonfiguration` wäre ein neues Objekt für die Eingabe aus dem Dialog. Ist es
ein Domain-Begriff? Nein. Die PLZ erscheint nicht im `Wetterzustand`, verändert
nicht die Regenbogen-Wahrscheinlichkeit und bleibt vollständig im
Einstiegspunkt. Kein SP1 nötig.

Die PLZ ist hier absichtlich nur Anzeige- und Eingabekomfort. Sie wird nicht
zur API-Abfrage verwendet und nicht in `system/core/` oder `domain/`
weitergereicht. Das ist eine bewusste Abgrenzung:

```text
PLZ als Anzeige-/Eingabefeld im Dialog      → cli/, kein Sprechakt
PLZ als Schlüssel zur Ortsauflösung         → systemsemantische Entscheidung
PLZ als fachlicher Standortbegriff          → möglicher Domain-Begriff
```

Sobald die PLZ zur Ortsauflösung verwendet wird, entsteht eine neue
Systementscheidung: Welche Quelle löst PLZ zu Koordinaten auf? Was passiert bei
mehrdeutigen Postleitzahlen? Welche Fehlerklasse entsteht? Diese Fragen gehören
nicht in die GUI und würden mindestens SP2 oder SP3 auslösen.

`GUI-Raum` ist dagegen eine Raumentscheidung. Wird ein eigener Raum `gui/`
eingeführt, müssen `package-schema.md`, Checker-Regeln und Testpflichten
nachgezogen werden. Das ist SP2.

**P6 — Import-Checker vorab**

Der bestehende Stand ist grün. Der Agent prüft aber die geplanten Kanten:

```text
cli.gui_main -> adapters              erlaubt
cli.gui_main -> system.ports          erlaubt
cli.ausgabe_fenster -> system.core    erlaubt
cli.gui_format -> system.core         erlaubt
cli.* -> infrastructure               nicht erlaubt
cli.* -> domain                       nicht direkt verwenden
```

**P7 — Testpflicht vorab**

GUI-Fenster selbst sind in CI oft nicht sinnvoll testbar, weil ein Display
fehlt. Deshalb muss der testbare Anteil herausgeschnitten werden:

```text
cli/gui_format.py      reine Formatierung, testbar ohne Tkinter
cli/config_dialog.py   Tkinter-Fenster, manuell/Smoke-Test
cli/ausgabe_fenster.py Tkinter-Fenster, manuell/Smoke-Test
cli/gui_main.py        Ablauf/Wiring, in kleinen Teilen testbar
```

**P8 — Schreibrechte**

`package-schema.md` ist geschützt. Eine Änderung ist nur erlaubt, wenn der
Sprechakt SP2 festgelegt ist. Eine neue Runtime-/Plattformfähigkeit `tkinter`
braucht SP4.

**P9 — Task-Schnitt**

T2 tritt ein: Die Aufgabe berührt `cli/`, potentiell einen neuen Raum `gui/`,
und die geschützte Raumkarte. Der Agent teilt die Aufgabe:

```text
Teil A: Raumzuordnung und tkinter-Freigabe (Sprechakte)
Teil B: package-schema.md aktualisieren
Teil C: Konfigurationsdialog implementieren
Teil D: Ausgabefenster implementieren
Teil E: Hauptprogramm und Tests
```

**P10 — Plan**

Die Änderung ist nichttrivial. Der Agent legt einen Plan an, z. B.:

```text
docs/plans/2026-06-12-gui-einstiegspunkt.md
```

Der Plan verweist auf die beiden Sprechakte. Ohne festgelegten SP2 und SP4 wird
nicht implementiert.

Ergebnis: **TEILEN + SPRECHAKT SP2 + SP4**.

### 10.2 Sprechakt SP2: Raumzuordnung GUI

```markdown
# Sprechakt: Raumzuordnung GUI

Zeitpunkt:        2026-06-12 09:30
Sprechakt-Klasse: SP2 — Neuer systemsemantischer Steuerwert oder Raumentscheidung
Betroffener Begriff: GUI-Raum
Status: offen

## Was fehlt

Die Box kennt cli/ als Einstiegspunkt-Raum. Für eine GUI gibt es zwei Optionen:

Option A: GUI unter cli/
  - Kein neuer Raum nötig.
  - Tkinter bleibt Einstiegspunkt-Technik.
  - Importregeln bleiben unverändert.
  - Checker-Konfiguration unverändert.

Option B: Neuer Raum gui/
  - Expliziter eigener UI-Raum mit eigener Autonomiefrage.
  - package-schema.md und check_import_layers.py müssten erweitert werden.
  - Höherer Aufwand, weil neue Raumregel entsteht.

## Analyse des Agenten

Die gewünschte GUI besteht aus zwei Fenstern (Dialog und Ausgabe). Sie erzeugt
keine eigene Produktsemantik. Sie ist ein zweiter Einstiegspunkt.

Für Option A spricht: CLI und GUI haben identische Rolle — Eingabe parsen,
Use Case aufrufen, Ausgabe darstellen. Nur das I/O-Medium unterscheidet sich.

Für Option B spricht: Bei wachsendem GUI-Code könnte eine eigene Raumgrenze
nützlich werden.

## Was der Mensch festlegt

Option A. GUI lebt unter cli/.
Tkinter darf nur in cli/ verwendet werden.
Keine Tkinter-Imports in domain/, system/, infrastructure/ oder adapters/.
Bei wachsendem GUI-Code kann per SP2 ein eigener Raum eingeführt werden.

Status: festgelegt
Folgeartefakte: package-schema.md (cli/-Abschnitt ergänzen)
```

Ort: `docs/sprechakte/2026-06-12-raumzuordnung-gui.md`.

### 10.3 Sprechakt SP4: Runtime-Dependency tkinter

```markdown
# Sprechakt: GUI-Dependency tkinter

Zeitpunkt:        2026-06-12 09:45
Sprechakt-Klasse: SP4 — Neue Runtime-Dependency
Betroffener Begriff: tkinter
Status: offen

## Was fehlt

Die GUI benötigt tkinter. Das ist keine PyPI-Dependency, aber eine
Runtime-/Plattformfähigkeit: Auf manchen Linux-Systemen fehlt das
OS-Paket (z. B. python3-tk).

## Analyse des Agenten

- Vorteil: Standardbibliothek, keine zusätzliche PyPI-Abhängigkeit.
- Nachteil: Auf manchen Systemen fehlt das Tk-Paket.
- Konsequenz: GUI ist optionaler Einstiegspunkt. CLI bleibt primär.

## Was der Mensch festlegt

tkinter ist für cli/ erlaubt.
Die GUI ist optional. Fehlt tkinter, darf die CLI nicht beeinträchtigt werden.
Keine tkinter-Imports außerhalb von cli/.
Wird in INSTALLATION.md vermerkt.

Status: festgelegt
Folgeartefakte: INSTALLATION.md, package-schema.md
```

Ort: `docs/sprechakte/2026-06-12-tkinter-dependency.md`.

`INSTALLATION.md` ist in diesem Beispiel eine projektspezifische Datei, kein
Pflichtartefakt der Box. Sie wird hier angelegt, weil die Runtime-Fähigkeit
nicht vollständig durch Python-Paketmetadaten beschrieben ist. Für Linux kann
dort z. B. stehen:

```markdown
## Optionale GUI-Abhängigkeit

Die CLI funktioniert ohne Tkinter.
Die GUI benötigt die Tk-Plattformbindung der lokalen Python-Installation.
Je nach Distribution muss ein zusätzliches Systempaket installiert werden,
z. B. `python3-tk` oder `tk`.
```

Das ist bewusst Markdown. Auch Installationswissen ist Teil der lokalen
operativen Wahrheit des Projekts.

### 10.4 package-schema.md aktualisieren

Nach SP2 und SP4 ergänzt der Agent den `cli/`-Abschnitt in
`package-schema.md`. Das ist eine Änderung an einer geschützten Datei —
Freigabe liegt vor (beide Sprechakte festgelegt).

```markdown
### Hinweis: GUI unter cli/

GUI-Code lebt unter cli/. Kein eigener gui/-Layer.
Festgelegt durch Sprechakt SP2 (2026-06-12-raumzuordnung-gui.md).

tkinter ist in cli/ erlaubt. Nicht erlaubt in domain/, system/,
infrastructure/ oder adapters/.
Festgelegt durch Sprechakt SP4 (2026-06-12-tkinter-dependency.md).
```

### 10.5 Teil B: Konfigurationsdialog

```python
# src/regenbogen/cli/config_dialog.py
import tkinter as tk
from dataclasses import dataclass
from tkinter import messagebox, ttk


@dataclass
class OrtKonfiguration:
    """Ergebnis des Konfigurationsdialogs.

    Kein Fachbegriff — reine GUI-Eingabe. ortsname wird an den Use Case
    weitergegeben. postleitzahl ist ein Eingabekomfort ohne Systemsemantik.
    Sie wird nur für die Anzeige verwendet, nicht für die Berechnung.
    """

    ortsname: str
    postleitzahl: str

    def anzeige_name(self) -> str:
        if not self.postleitzahl:
            return self.ortsname
        return f"{self.ortsname} ({self.postleitzahl})"


class KonfigurationsDialog:
    """Modaler Dialog zur Ortsauswahl.

    Gehört zu cli/ — kein Domain-Begriff, keine Systemlogik.
    Gibt OrtKonfiguration zurück oder None wenn abgebrochen.
    """

    def __init__(self, root: tk.Tk) -> None:
        self._root = root
        self._ergebnis: OrtKonfiguration | None = None

    def zeige(self) -> OrtKonfiguration | None:
        dialog = tk.Toplevel(self._root)
        dialog.title("Ort konfigurieren")
        dialog.resizable(False, False)
        dialog.grab_set()  # modal

        frame = ttk.Frame(dialog, padding=16)
        frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame, text="Ortsname:").grid(
            row=0, column=0, sticky="w", pady=4
        )
        ortsname_var = tk.StringVar(value="Berlin")
        ttk.Entry(frame, textvariable=ortsname_var, width=24).grid(
            row=0, column=1, pady=4, padx=(8, 0)
        )

        ttk.Label(frame, text="Postleitzahl (optional):").grid(
            row=1, column=0, sticky="w", pady=4
        )
        plz_var = tk.StringVar()
        ttk.Entry(frame, textvariable=plz_var, width=24).grid(
            row=1, column=1, pady=4, padx=(8, 0)
        )

        def bestaetigen() -> None:
            name = ortsname_var.get().strip()
            if not name:
                messagebox.showwarning(
                    "Fehlende Eingabe",
                    "Bitte einen Ortsnamen eingeben.",
                    parent=dialog,
                )
                return
            self._ergebnis = OrtKonfiguration(
                ortsname=name,
                postleitzahl=plz_var.get().strip(),
            )
            dialog.destroy()

        def abbrechen() -> None:
            dialog.destroy()

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(12, 0))
        ttk.Button(btn_frame, text="OK", command=bestaetigen).pack(
            side="left", padx=4
        )
        ttk.Button(btn_frame, text="Abbrechen", command=abbrechen).pack(
            side="left", padx=4
        )

        self._root.wait_window(dialog)
        return self._ergebnis
```

### 10.6 Teil C: Ausgabefenster

Die Formatierungslogik wird bewusst in eine eigene Datei ohne Tkinter
ausgelagert. Das ermöglicht Tests ohne Display.

```python
# src/regenbogen/cli/gui_format.py
from regenbogen.system.core.wahrscheinlichkeit_use_case import WetterErgebnis


def formatiere_wetter(ergebnis: WetterErgebnis) -> str:
    """Menschenlesbarer Wettertext aus WetterErgebnis.

    cli/: Adapter-Funktion — übersetzt für die Anzeige, erzeugt keine Semantik.
    Keine Tkinter-Abhängigkeit, damit dieser Code testbar ist.
    """
    teile = []
    if ergebnis.zustand.sonnenschein:
        teile.append(
            f"Sonnenschein ({round(ergebnis.zustand.sonnenschein_intensitaet * 100)} %)"
        )
    if ergebnis.zustand.regen:
        teile.append(
            f"Regen ({round(ergebnis.zustand.regen_intensitaet * 100)} %)"
        )
    wetter_text = ", ".join(teile) if teile else "Bedeckt, kein Niederschlag"

    return (
        f"Wetter: {wetter_text}\n"
        f"Regenbogen: {ergebnis.wahrscheinlichkeit} %"
    )
```

```python
# src/regenbogen/cli/ausgabe_fenster.py
import tkinter as tk
from tkinter import ttk

from regenbogen.cli.gui_format import formatiere_wetter
from regenbogen.system.core.wahrscheinlichkeit_use_case import WetterErgebnis


class AusgabeFenster:
    """Zeigt WetterErgebnis in einem eigenen Fenster an.

    Empfängt fertige Werte — keine Berechnungen hier.
    Gehört zu cli/ — reine Darstellung.
    """

    def __init__(self, root: tk.Tk) -> None:
        self._root = root

    def zeige(self, ergebnis: WetterErgebnis, ortsanzeige: str | None = None) -> None:
        titel = ortsanzeige or ergebnis.ort
        fenster = tk.Toplevel(self._root)
        fenster.title(f"Regenbogen — {titel}")
        fenster.resizable(False, False)

        frame = ttk.Frame(fenster, padding=20)
        frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(
            frame,
            text=titel,
            font=("", 14, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 12))

        farbe = "#1a7a1a" if ergebnis.wahrscheinlichkeit >= 30 else "#555555"
        ttk.Label(
            frame,
            text=formatiere_wetter(ergebnis),
            foreground=farbe,
            justify="left",
        ).grid(row=1, column=0, sticky="w")

        ttk.Button(
            frame,
            text="Schließen",
            command=fenster.destroy,
        ).grid(row=2, column=0, sticky="e", pady=(16, 0))
```

### 10.7 Teil D: Hauptprogramm

```python
# src/regenbogen/cli/gui_main.py
import tkinter as tk
from tkinter import messagebox

from regenbogen.adapters.wiring import create_regenbogen_use_case
from regenbogen.cli.ausgabe_fenster import AusgabeFenster
from regenbogen.cli.config_dialog import KonfigurationsDialog
from regenbogen.system.ports.wetterapi_port import (
    OrtNichtGefunden,
    WetterApiNichtErreichbar,
)


def main() -> int:
    root = tk.Tk()
    root.withdraw()  # Hauptfenster verstecken, nur Dialoge sichtbar

    # Schritt 1: Konfigurationsdialog
    dialog = KonfigurationsDialog(root)
    konfiguration = dialog.zeige()

    if konfiguration is None:
        root.destroy()
        return 0  # Nutzer hat abgebrochen

    # Schritt 2: Wetterdaten holen
    use_case = create_regenbogen_use_case()

    try:
        ergebnis = use_case.berechne_vollstaendig(konfiguration.ortsname)
    except OrtNichtGefunden:
        messagebox.showerror(
            "Ort nicht gefunden",
            f"Der Ort '{konfiguration.ortsname}' ist unbekannt.",
        )
        root.destroy()
        return 1
    except WetterApiNichtErreichbar:
        messagebox.showerror(
            "Verbindungsfehler",
            "Der Wetterdienst ist nicht erreichbar.\n"
            "Bitte später erneut versuchen.",
        )
        root.destroy()
        return 2

    # Schritt 3: Ausgabefenster
    ausgabe = AusgabeFenster(root)
    ausgabe.zeige(ergebnis, ortsanzeige=konfiguration.anzeige_name())
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Importkette der GUI:

```text
cli.gui_main -> adapters              erlaubt
cli.gui_main -> cli.config_dialog     erlaubt (cli darf cli importieren)
cli.gui_main -> cli.ausgabe_fenster   erlaubt
cli.gui_main -> system.ports          erlaubt (Fehlerbehandlung)
cli.ausgabe_fenster -> cli.gui_format erlaubt
cli.ausgabe_fenster -> system.core    erlaubt (WetterErgebnis als Typ)
cli.gui_format -> system.core         erlaubt
```

`cli` importiert weder `domain` noch `infrastructure` direkt. Alle Werte
kommen über `WetterErgebnis` aus dem Use Case.

### 10.8 Tests

Tkinter-Fenster können in CI ohne Display nicht geöffnet werden. Die
Formatierungslogik ist in `gui_format.py` ohne Tkinter-Abhängigkeit, und
daher vollständig testbar. Die Fensterklassen bleiben dünn und enthalten nur
Widget-Aufbau und Ereignisweiterleitung; sie werden manuell oder per optionalem
Smoke-Test geprüft.

```python
# tests/cli/test_gui_format.py
from regenbogen.cli.gui_format import formatiere_wetter
from regenbogen.domain.wetter import Wetterzustand
from regenbogen.system.core.wahrscheinlichkeit_use_case import WetterErgebnis


def ergebnis(zustand: Wetterzustand, wahrscheinlichkeit: int) -> WetterErgebnis:
    return WetterErgebnis(
        ort="Berlin",
        zustand=zustand,
        wahrscheinlichkeit=wahrscheinlichkeit,
    )


def test_formatiert_beide_faktoren():
    ausgabe = formatiere_wetter(
        ergebnis(
            Wetterzustand(
                sonnenschein=True,
                regen=True,
                sonnenschein_intensitaet=0.5,
                regen_intensitaet=0.5,
            ),
            50,
        )
    )
    assert "Sonnenschein" in ausgabe
    assert "Regen" in ausgabe
    assert "50 %" in ausgabe


def test_formatiert_kein_regen():
    ausgabe = formatiere_wetter(
        ergebnis(
            Wetterzustand(
                sonnenschein=True,
                regen=False,
                sonnenschein_intensitaet=0.8,
            ),
            0,
        )
    )
    assert "Sonnenschein" in ausgabe
    assert "0 %" in ausgabe


def test_formatiert_bedeckt():
    ausgabe = formatiere_wetter(
        ergebnis(Wetterzustand(sonnenschein=False, regen=False), 0)
    )
    assert "Bedeckt" in ausgabe
```

### 10.9 Import-Checker und Abschluss

```bash
python tools/check_import_layers.py --preflight src tests tools
```

```text
✓ PREFLIGHT IMPORT-LAYER OK (9 Dateien geprüft)
```

```bash
python tools/resolve_test_obligations.py \
  --changed-file src/regenbogen/cli/gui_main.py \
  --changed-file src/regenbogen/cli/config_dialog.py \
  --changed-file src/regenbogen/cli/ausgabe_fenster.py \
  --changed-file src/regenbogen/cli/gui_format.py
python -m ruff check .
python -m mypy src
python -m pytest tests/cli/
```

Erfahrungsbericht:

```markdown
# Erfahrungsbericht: GUI-Session Regenbogen

Datum:        2026-06-12
Session-Typ:  abgeschlossen
Aufgabe:      Tkinter-GUI als zweiter Einstiegspunkt
Ergebnis:     GUI unter cli/ eingeordnet, tkinter als optionale Plattform-
              fähigkeit dokumentiert, Tests grün

Learning-Matrix-Kandidat: ja
Muster-ID: UI-Raumentscheidung

## Was sich bewährt hat

SP2 hat verhindert, dass der Agent still einen neuen Raum gui/ einführt.
SP4 hat verhindert, dass tkinter still als Runtime-Annahme in das Projekt
kommt. Die Trennung gui_format.py (testbar, kein Tkinter) von den Fenster-
klassen (nicht testbar ohne Display) macht den testbaren Anteil explizit.

## Rückfluss

Wenn weitere UI-Einstiegspunkte entstehen, sollte package-schema.md explizit
beschreiben, ob sie unter cli/ bleiben oder ob ein eigener ui/-Raum nötig wird.
```

Ort: `tmp/erfahrungsberichte/2026-06-12-EB-gui-session.md`.

---


## 11. Sechste Session: Sonnenstand und Winkelmodell

**Aufgabe:** Die bisherige Regenbogen-Wahrscheinlichkeit soll fachlich besser
werden. Die GUI liefert inzwischen Ort und Postleitzahl. Zusätzlich kann das
System die aktuelle Uhrzeit kennen. Aus Postleitzahl und Uhrzeit lässt sich der
Sonnenstand näherungsweise bestimmen. Dadurch wird aus der bisherigen
Platzhalterformel ein geometrisch begründetes Sichtbarkeitsmodell.

Der wichtige fachliche Punkt: Postleitzahl und Uhrzeit liefern **nicht** die
vollständige Regenbogen-Wahrscheinlichkeit. Sie liefern den Sonnenstand am
Beobachtungsort. Für einen vollständigen Regenbogen-Nachweis bräuchte man
zusätzlich die Lage der Regenzelle relativ zum Beobachter. Diese Information
hat das Beispiel weiterhin nicht. Das Modell wird also besser, aber nicht
vollständig.

```text
PLZ + Uhrzeit + Koordinaten  → Sonnenhöhe und Sonnenazimut
Regen + Sonne + Sonnenhöhe   → verbessertes Sichtbarkeitsfenster
Regenzellenrichtung          → weiterhin offene Modellgrenze
```

Diese Session ist wichtig, weil sie zeigt, wie ein zunächst didaktischer
Placeholder kontrolliert durch ein besseres fachliches Modell ersetzt wird.

### 11.1 Preflight: Warum diese Änderung ein echter Schnitt ist

**P1/P2 — Agentenregeln lesen**

Der Agent notiert:

```text
- domain/ darf keine aktuelle Uhrzeit holen.
- domain/ darf keine Postleitzahl-Datenbank abfragen.
- infrastructure/ darf weiterhin keine Domain-Typen erzeugen.
- adapters/ ist der richtige Ort für produktive Verdrahtung.
```

**P3 — package-schema.md prüfen**

Die Änderung berührt mehrere Räume:

```text
src/regenbogen/domain/regenbogen_geometrie.py       → domain
src/regenbogen/system/ports/standort_port.py        → system.ports
src/regenbogen/infrastructure/plz_lookup.py         → infrastructure
src/regenbogen/system/core/sonnenstand.py           → system.core
src/regenbogen/system/core/wahrscheinlichkeit_use_case.py → system.core
src/regenbogen/adapters/wiring.py                   → adapters
src/regenbogen/cli/config_dialog.py                 → cli
```

**P4 — Betroffene semantische Räume bestimmen**

Diese Aufgabe berührt mindestens vier Räume:

```text
domain          fachliche Regenbogen-Geometrie
system.ports    Standort-Port und Koordinaten-DTO
infrastructure  PLZ-zu-Koordinaten-Lookup
system.core     Sonnenstandsberechnung und Mapping in den Use Case
cli             PLZ aus dem Dialog weiterreichen
adapters        Uhrzeit-/Clock-Verdrahtung
```

Damit tritt **T2** ein: mehrere semantische Räume. Task-Schnitt ist Pflicht.

**P5 — Glossar prüfen**

Neue oder präzisierte Begriffe:

```text
Sonnenstand
Sonnenhoehe
Sonnenazimut
Gegensonnenpunkt
Regenbogenwinkel
SonnenstandsFaktor
StandortKoordinaten
PostleitzahlUnbekannt
```

Die fachlichen Begriffe fehlen im Domain-Glossar. Die systemsemantischen
Begriffe fehlen im System-Glossar.

**P9 — Task-Schnitt**

Der Agent teilt die Aufgabe:

```text
Teil A: Fachliche Begriffe und Domain-Regel festlegen
Teil B: Standort-Port und PLZ-Lookup einführen
Teil C: Sonnenstandsberechnung in system/core ergänzen
Teil D: Use Case und GUI verdrahten
Teil E: Tests und Abschluss-Evidence
```

**P10 — Planpflicht**

Diese Änderung ist nichttrivial. Sie berührt mehrere Räume, ändert das
Berechnungsmodell und verändert den GUI-Datenfluss. Der Agent legt vor der
Implementierung einen Plan an, zum Beispiel:

```text
docs/plans/2026-06-13-sonnenstand-winkelmodell.md
```

Ergebnis des Preflight: **SPRECHAKT + TEILEN**.

### 11.2 Sprechakt SP7: Regenbogen-Geometrie

```markdown
# Sprechakt: Regenbogen-Geometrie und Sonnenstand

Zeitpunkt:        2026-06-13 09:10
Sprechakt-Klasse: SP7 — Aktiv benötigte Begriffe fehlen im Glossar
Betroffener Begriff: Sonnenstand, Sonnenhoehe, Sonnenazimut,
                     Gegensonnenpunkt, Regenbogenwinkel,
                     SonnenstandsFaktor
Status: offen

## Was fehlt

Die bisherige Formel berücksichtigt nur Regen- und Sonnenintensität.
Sie ignoriert die Geometrie. Für sichtbare Regenbögen ist aber der
Sonnenstand entscheidend.

## Was der Agent sieht

code_says:
  berechne_regenbogen_wahrscheinlichkeit verwendet nur Intensitäten.

glossar_says:
  Kein Eintrag für Sonnenstand, Sonnenhoehe oder Regenbogenwinkel.

schema_says:
  Fachliche Sichtbarkeitsregeln gehören in domain/.
  Uhrzeit- und Koordinatenbeschaffung gehören nicht in domain/.

## Analyse des Agenten

Ein primärer Regenbogen erscheint ungefähr bei 42° um den Gegensonnenpunkt.
Für Beobachter am Boden gilt näherungsweise: Wenn die Sonne höher als 42°
steht, liegt der Hauptbogen unter dem Horizont und ist normalerweise nicht
sichtbar.

PLZ und Uhrzeit liefern den Sonnenstand am Beobachtungsort. Sie liefern aber
nicht die Richtung oder Ausdehnung der Regenzelle. Das Modell darf daher nicht
behaupten, echte Sichtbarkeit vollständig nachzuweisen.

## Warum der Agent nicht fortfahren kann

Ohne fachliche Festlegung würde der Agent still entscheiden,
welcher Sonnenstand günstig ist und wie die Geometrie in die
Wahrscheinlichkeit eingeht.

## Was der Mensch festlegt

Sonnenhoehe:
  Winkel der Sonne über dem Horizont in Grad.

Sonnenazimut:
  Himmelsrichtung der Sonne in Grad.

Regenbogenwinkel:
  Der primäre Regenbogen liegt näherungsweise bei 42° um den Gegensonnenpunkt.

SonnenstandsFaktor:
  Faktor in [0, 1].
  - Sonnenhoehe <= 0°: 0, Sonne unter Horizont.
  - 0° < Sonnenhoehe <= 25°: günstig, Faktor 1.
  - 25° < Sonnenhoehe < 42°: linear fallend.
  - Sonnenhoehe >= 42°: 0, Hauptbogen unter Horizont.

Modellgrenze:
  Ohne Regenzellenrichtung bleibt das Ergebnis eine Wahrscheinlichkeit bzw.
  ein Sichtbarkeits-Score, kein Nachweis eines sichtbaren Regenbogens.

Status: festgelegt
Folgeartefakte: glossar-domain.md, domain/regenbogen_geometrie.py,
                tests/domain/test_regenbogen_geometrie.py
```

Ort: `docs/sprechakte/2026-06-13-regenbogen-geometrie.md`.

### 11.3 Domain-Glossar ergänzen

Der Agent ergänzt `glossar-domain.md`:

```markdown
### Sonnenstand

Bedeutung: Position der Sonne relativ zum Beobachter, beschrieben durch
Sonnenhoehe und Sonnenazimut.

Invariante: Der Sonnenstand ist eine Eingabe für die Regenbogen-Geometrie,
aber keine Wetter-API-Messung.

Projektionen:
- Code: src/regenbogen/domain/regenbogen_geometrie.py
- Tests: tests/domain/test_regenbogen_geometrie.py

Migrationsstatus: canonical

---

### SonnenstandsFaktor

Bedeutung: Faktor in [0, 1], der ausdrückt, ob der Sonnenstand für einen
sichtbaren Hauptregenbogen geometrisch günstig ist.

Invarianten:
- Sonnenhoehe <= 0°: 0.
- Sonnenhoehe >= 42°: 0.
- 0° < Sonnenhoehe <= 25°: 1.
- 25° < Sonnenhoehe < 42°: linear fallend.

Nicht: Nachweis eines sichtbaren Regenbogens. Dafür fehlt im aktuellen Modell
die Regenzellenrichtung.

Projektionen:
- Code: src/regenbogen/domain/regenbogen_geometrie.py
- Tests: tests/domain/test_regenbogen_geometrie.py

Migrationsstatus: canonical
```

### 11.4 Domain-Implementierung: Geometriefaktor

```python
# src/regenbogen/domain/regenbogen_geometrie.py
from dataclasses import dataclass


@dataclass(frozen=True)
class Sonnenstand:
    """Sonnenposition relativ zum Beobachter.

    sonnenhoehe_grad: Winkel über dem Horizont.
    sonnenazimut_grad: Himmelsrichtung der Sonne.
    """

    sonnenhoehe_grad: float
    sonnenazimut_grad: float


def berechne_sonnenstands_faktor(sonnenstand: Sonnenstand) -> float:
    """Geometrischer Faktor für den primären Regenbogen.

    Das ist kein vollständiger Sichtbarkeitsnachweis. Es fehlt weiterhin
    die Information, ob Regen in der Gegensonnenrichtung liegt.
    """
    hoehe = sonnenstand.sonnenhoehe_grad

    if hoehe <= 0.0:
        return 0.0
    if hoehe >= 42.0:
        return 0.0
    if hoehe <= 25.0:
        return 1.0

    return max(0.0, (42.0 - hoehe) / (42.0 - 25.0))
```

Die Domain kennt weiterhin keine Postleitzahl, keine Uhrzeitquelle und keine
API. Sie kennt nur eine fachliche Regel: welcher Sonnenstand für einen
primären Regenbogen geometrisch möglich ist.

### 11.5 Domain-Berechnung erweitern

Die bisherige Berechnung wird nicht verworfen, sondern fachlich erweitert:

```python
# src/regenbogen/domain/regenbogen.py
from regenbogen.domain.regenbogen_geometrie import (
    Sonnenstand,
    berechne_sonnenstands_faktor,
)
from regenbogen.domain.wetter import Wetterzustand


def berechne_regenbogen_wahrscheinlichkeit(
    zustand: Wetterzustand,
    sonnenstand: Sonnenstand | None = None,
) -> int:
    """Regenbogen-Wahrscheinlichkeit als Prozentwert in [0, 100].

    Ohne Sonnenstand wird nur das alte Intensitätsmodell verwendet.
    Mit Sonnenstand wird zusätzlich das geometrische Sichtbarkeitsfenster
    berücksichtigt.
    """
    if not zustand.sonnenschein or not zustand.regen:
        return 0

    basis = (
        zustand.sonnenschein_intensitaet * 0.6
        + zustand.regen_intensitaet * 0.4
    )

    if sonnenstand is not None:
        basis *= berechne_sonnenstands_faktor(sonnenstand)

    return max(0, min(100, round(basis * 100)))
```

Der wichtige Unterschied zur ersten Version: Bei ungünstigem Sonnenstand kann
die Wahrscheinlichkeit jetzt trotz Regen und Sonnenschein 0 sein. Das ist
fachlich plausibler als die reine Intensitätsformel.

### 11.6 Sprechakt SP2/SP3: Standort aus PLZ

Jetzt wird die Postleitzahl aus der GUI nicht mehr nur angezeigt. Sie erhält
eine systemsemantische Rolle: Sie dient der näherungsweisen Bestimmung des
Beobachtungsorts.

Das ist eine Bedeutungsänderung gegenüber Session 10. Dort war PLZ reiner
Eingabekomfort in `cli/`. Jetzt wird sie zur Eingabe für einen System-Port.
Deshalb braucht die Änderung eine Festlegung.

```markdown
# Sprechakt: PLZ als Standort-Eingabe

Zeitpunkt:        2026-06-13 09:45
Sprechakt-Klasse: SP2 — Neuer systemsemantischer Steuerwert oder Raumentscheidung
Betroffener Begriff: StandortKoordinaten, Postleitzahl
Status: offen

## Was fehlt

Die GUI erfasst eine Postleitzahl. Bisher war sie nur Anzeige- und
Eingabekomfort. Für das Winkelmodell soll sie den Beobachtungsort bestimmen.

## Was der Agent sieht

cli_says:
  OrtKonfiguration enthält postleitzahl.

system_says:
  Es gibt noch keinen Port zur Bestimmung von Koordinaten.

domain_says:
  Domain kennt keine Postleitzahl und soll sie auch nicht kennen.

## Analyse des Agenten

PLZ ist hier kein Fachbegriff der Regenbogen-Domäne. Sie ist ein
systemischer Eingabewert zur Standortbestimmung. Die eigentliche
Implementierung der PLZ-Auflösung gehört in infrastructure/.

## Was der Mensch festlegt

Postleitzahl darf als optionale Standort-Eingabe verwendet werden.
Die fachliche Regenbogen-Domäne kennt keine PLZ.
Koordinaten werden über einen StandortPort beschafft.
Unbekannte PLZ ist ein terminaler systemischer Fehler.

Status: festgelegt
Folgeartefakte: glossar-system.md, system/ports/standort_port.py,
                infrastructure/plz_lookup.py
```

Ort: `docs/sprechakte/2026-06-13-plz-standort.md`.

Für den Fehlerfall entsteht zusätzlich eine Fehlerbedeutung. Sie kann im selben
Schnitt dokumentiert oder als eigener SP3 geführt werden:

```markdown
### PostleitzahlUnbekannt

Bedeutung: Die eingegebene Postleitzahl kann nicht in Koordinaten übersetzt
werden. Terminal. Kein Retry.

Projektionen:
- Code: src/regenbogen/system/ports/standort_port.py
- Tests: tests/system/test_standort.py

Migrationsstatus: canonical
```

### 11.7 Standort-Port und PLZ-Lookup

```python
# src/regenbogen/system/ports/standort_port.py
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class StandortKoordinaten:
    """Beobachtungsort für Sonnenstandsberechnung und Wetterabfrage."""

    latitude: float
    longitude: float
    zeitzone: str


class PostleitzahlUnbekannt(Exception):
    """PLZ kann nicht in Koordinaten übersetzt werden. Terminal."""


class StandortPort(ABC):
    @abstractmethod
    def finde_koordinaten(
        self,
        ort: str,
        postleitzahl: str | None,
    ) -> StandortKoordinaten:
        ...
```

```python
# src/regenbogen/infrastructure/plz_lookup.py
from regenbogen.system.ports.standort_port import (
    PostleitzahlUnbekannt,
    StandortKoordinaten,
    StandortPort,
)


class DemoStandortLookup(StandortPort):
    """Kleine lokale PLZ-Tabelle für das Tutorial.

    Keine externe Dependency, kein Geocoder, keine Netzabfrage.
    In einem echten Projekt wäre hier ein Geocoder oder eine PLZ-Datenbank.
    """

    _PLZ = {
        "10115": StandortKoordinaten(52.532, 13.384, "Europe/Berlin"),
        "80331": StandortKoordinaten(48.137, 11.575, "Europe/Berlin"),
    }

    def finde_koordinaten(
        self,
        ort: str,
        postleitzahl: str | None,
    ) -> StandortKoordinaten:
        if postleitzahl and postleitzahl in self._PLZ:
            return self._PLZ[postleitzahl]

        if ort == "Berlin":
            return self._PLZ["10115"]
        if ort == "Muenchen":
            return self._PLZ["80331"]

        raise PostleitzahlUnbekannt(
            f"Keine Koordinaten fuer Ort={ort!r}, PLZ={postleitzahl!r}"
        )
```

Diese Infrastruktur bleibt sauber: Sie importiert nur `system.ports`, nicht
`domain`. Sie liefert Koordinaten, keine Regenbogen-Bedeutung.

### 11.8 WetterApiPort auf Koordinaten umstellen

Vor der Geometrie-Iteration hatte der Wetter-Client den Ort selbst in
Koordinaten übersetzt. Das war für das einfache Beispiel noch akzeptabel, wird
aber jetzt unsauber: Zwei verschiedene Stellen würden Standortlogik tragen.

Deshalb wird der Wetter-Port auf Koordinaten umgestellt:

```python
# src/regenbogen/system/ports/wetterapi_port.py
from abc import ABC, abstractmethod
from dataclasses import dataclass

from regenbogen.system.ports.standort_port import StandortKoordinaten


@dataclass(frozen=True)
class WetterApiMessung:
    """Technische Messung der Wetter-API.

    Dieser Typ ist bewusst kein Domain-Typ. Er beschreibt Rohdaten und
    abgeleitete Wetterdaten der externen API. Die fachliche Interpretation
    passiert in system/core/ und domain/.
    """

    sonnenschein_sekunden: float
    niederschlag_mm: float
    rain_mm: float = 0.0
    showers_mm: float = 0.0
    snowfall_cm: float = 0.0
    weather_code: int = 0
    cloud_cover: float = 100.0
    visibility_m: float | None = None
    direct_radiation: float = 0.0
    temperature_2m: float = 0.0


class WetterApiNichtErreichbar(Exception):
    """API nicht erreichbar. Recoverable — Retry erlaubt."""


class OrtNichtGefunden(Exception):
    """Unbekannter Ort. Terminal — kein Retry."""


class WetterApiPort(ABC):
    @abstractmethod
    def hole_aktuelle_messung(
        self,
        koordinaten: StandortKoordinaten,
    ) -> WetterApiMessung:
        """Liefert rohe technische Wetterdaten für Koordinaten."""
```

`OpenMeteoClient` verliert damit seine interne `_ort_zu_koordinaten`-Methode.
Die Wetter-API bekommt nur noch Koordinaten:

```python
# src/regenbogen/infrastructure/open_meteo_client.py
import httpx

from regenbogen.system.ports.standort_port import StandortKoordinaten
from regenbogen.system.ports.wetterapi_port import (
    WetterApiMessung,
    WetterApiNichtErreichbar,
    WetterApiPort,
)


class OpenMeteoClient(WetterApiPort):
    """Implementiert WetterApiPort über die Open-Meteo API.

    Liefert WetterApiMessung — keinen Domain-Typ. Das Mapping nach
    Wetterzustand ist Aufgabe von system/core/.
    """

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def hole_aktuelle_messung(
        self,
        koordinaten: StandortKoordinaten,
    ) -> WetterApiMessung:
        try:
            response = httpx.get(
                self.BASE_URL,
                params={
                    "latitude": koordinaten.latitude,
                    "longitude": koordinaten.longitude,
                    "current": ",".join(
                        [
                            "temperature_2m",
                            "precipitation",
                            "rain",
                            "showers",
                            "snowfall",
                            "weather_code",
                            "cloud_cover",
                            "visibility",
                            "direct_radiation",
                            "sunshine_duration",
                        ]
                    ),
                },
                timeout=10.0,
            )
            response.raise_for_status()
        except httpx.ConnectError as exc:
            raise WetterApiNichtErreichbar(f"Nicht erreichbar: {exc}") from exc
        except httpx.HTTPStatusError as exc:
            raise WetterApiNichtErreichbar(
                f"API-Fehler: {exc.response.status_code}"
            ) from exc

        return self._parse_response(response.json())

    def _parse_response(self, data: dict) -> WetterApiMessung:
        current = data.get("current", {})
        return WetterApiMessung(
            sonnenschein_sekunden=float(current.get("sunshine_duration", 0.0)),
            niederschlag_mm=float(current.get("precipitation", 0.0)),
            rain_mm=float(current.get("rain", 0.0)),
            showers_mm=float(current.get("showers", 0.0)),
            snowfall_cm=float(current.get("snowfall", 0.0)),
            weather_code=int(current.get("weather_code", 0)),
            cloud_cover=float(current.get("cloud_cover", 100.0)),
            visibility_m=(
                float(current["visibility"])
                if current.get("visibility") is not None
                else None
            ),
            direct_radiation=float(current.get("direct_radiation", 0.0)),
            temperature_2m=float(current.get("temperature_2m", 0.0)),
        )
```

Der Gewinn: Standortlogik ist jetzt an einer Stelle. Die Wetter-API ist nur
noch Wetter-API.

### 11.9 Sonnenstandsberechnung in system/core

Die Berechnung des Sonnenstands ist eine Projektion aus Uhrzeit und Koordinaten
in das fachliche Modell `Sonnenstand`. Sie gehört nicht in `infrastructure/`,
weil sie keine externe API ist. Sie gehört nicht in `domain/`, weil dort keine
Uhrzeit- und Zeitzonenverarbeitung stattfinden soll. Sie liegt deshalb in
`system/core/`.

Das Tutorial verwendet eine vereinfachte Näherung. Für produktive Anwendungen
würde man das Modell präziser validieren oder eine spezialisierte Bibliothek
per SP4 freigeben.

```python
# src/regenbogen/system/core/sonnenstand.py
import math
from datetime import datetime
from zoneinfo import ZoneInfo

from regenbogen.domain.regenbogen_geometrie import Sonnenstand
from regenbogen.system.ports.standort_port import StandortKoordinaten


def berechne_sonnenstand(
    zeitpunkt: datetime,
    koordinaten: StandortKoordinaten,
) -> Sonnenstand:
    """Näherungsweise Sonnenhöhe und Sonnenazimut.

    Das Modell ist für das Tutorial ausreichend. Es ist keine hochpräzise
    astronomische Ephemeridenrechnung.
    """
    lokaler_zeitpunkt = zeitpunkt.astimezone(ZoneInfo(koordinaten.zeitzone))
    tag_des_jahres = lokaler_zeitpunkt.timetuple().tm_yday
    stunde = (
        lokaler_zeitpunkt.hour
        + lokaler_zeitpunkt.minute / 60.0
        + lokaler_zeitpunkt.second / 3600.0
    )

    gamma = 2.0 * math.pi / 365.0 * (tag_des_jahres - 1 + (stunde - 12.0) / 24.0)
    deklination = (
        0.006918
        - 0.399912 * math.cos(gamma)
        + 0.070257 * math.sin(gamma)
        - 0.006758 * math.cos(2.0 * gamma)
        + 0.000907 * math.sin(2.0 * gamma)
        - 0.002697 * math.cos(3.0 * gamma)
        + 0.00148 * math.sin(3.0 * gamma)
    )

    zeitgleichung = 229.18 * (
        0.000075
        + 0.001868 * math.cos(gamma)
        - 0.032077 * math.sin(gamma)
        - 0.014615 * math.cos(2.0 * gamma)
        - 0.040849 * math.sin(2.0 * gamma)
    )

    timezone_offset_stunden = lokaler_zeitpunkt.utcoffset().total_seconds() / 3600.0
    zeit_offset = zeitgleichung + 4.0 * koordinaten.longitude - 60.0 * timezone_offset_stunden
    wahre_sonnenzeit = stunde * 60.0 + zeit_offset
    stundenwinkel = math.radians(wahre_sonnenzeit / 4.0 - 180.0)

    breite = math.radians(koordinaten.latitude)
    hoehe = math.asin(
        math.sin(breite) * math.sin(deklination)
        + math.cos(breite) * math.cos(deklination) * math.cos(stundenwinkel)
    )

    azimut = math.atan2(
        math.sin(stundenwinkel),
        math.cos(stundenwinkel) * math.sin(breite)
        - math.tan(deklination) * math.cos(breite),
    )
    azimut_grad = (math.degrees(azimut) + 180.0) % 360.0

    return Sonnenstand(
        sonnenhoehe_grad=math.degrees(hoehe),
        sonnenazimut_grad=azimut_grad,
    )
```

### 11.10 Use Case erweitern

Der Use Case erhält jetzt zwei zusätzliche Abhängigkeiten:

```text
StandortPort      Ort/PLZ -> Koordinaten
clock             aktuelle Uhrzeit als injizierter Callable
```

Dadurch bleibt `datetime.now()` aus Domain und Tests heraus.

```python
# src/regenbogen/system/core/wahrscheinlichkeit_use_case.py
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from regenbogen.domain.regenbogen import berechne_regenbogen_wahrscheinlichkeit
from regenbogen.domain.regenbogen_geometrie import (
    Sonnenstand,
    berechne_sonnenstands_faktor,
)
from regenbogen.domain.regenbogen_optik import (
    RegenbogenOptikFaktoren,
    berechne_regenbogen_sichtbarkeit,
)
from regenbogen.domain.wetter import Wetterzustand
from regenbogen.system.core.optische_bedingungen import leite_optische_bedingungen_ab
from regenbogen.system.core.sonnenstand import berechne_sonnenstand
from regenbogen.system.ports.standort_port import StandortPort
from regenbogen.system.ports.wetterapi_port import (
    OrtNichtGefunden,
    WetterApiMessung,
    WetterApiNichtErreichbar,
    WetterApiPort,
)


@dataclass(frozen=True)
class WetterErgebnis:
    ort: str
    postleitzahl: str | None
    zustand: Wetterzustand
    sonnenstand: Sonnenstand
    wahrscheinlichkeit: int
    sichtbarkeit: int


class RegenbogenWahrscheinlichkeitUseCase:
    MAX_VERSUCHE = 3

    def __init__(
        self,
        api: WetterApiPort,
        standort: StandortPort,
        sleep: Callable[[float], None],
        clock: Callable[[], datetime],
    ) -> None:
        self._api = api
        self._standort = standort
        self._sleep = sleep
        self._clock = clock

    def berechne(self, ort: str, postleitzahl: str | None = None) -> int:
        return self.berechne_vollstaendig(ort, postleitzahl).wahrscheinlichkeit

    def berechne_vollstaendig(
        self,
        ort: str,
        postleitzahl: str | None = None,
    ) -> WetterErgebnis:
        koordinaten = self._standort.finde_koordinaten(ort, postleitzahl)
        sonnenstand = berechne_sonnenstand(self._clock(), koordinaten)
        messung = self._hole_messung_mit_retry(koordinaten)
        zustand = self._messung_zu_wetterzustand(messung)
        wahrscheinlichkeit = berechne_regenbogen_wahrscheinlichkeit(
            zustand,
            sonnenstand,
        )
        sichtbarkeit = self._berechne_sichtbarkeit(messung, sonnenstand)
        return WetterErgebnis(
            ort=ort,
            postleitzahl=postleitzahl,
            zustand=zustand,
            sonnenstand=sonnenstand,
            wahrscheinlichkeit=wahrscheinlichkeit,
            sichtbarkeit=sichtbarkeit,
        )

    def _hole_messung_mit_retry(self, koordinaten: object) -> WetterApiMessung:
        letzter_fehler: WetterApiNichtErreichbar | None = None

        for versuch in range(1, self.MAX_VERSUCHE + 1):
            try:
                return self._api.hole_aktuelle_messung(koordinaten)
            except WetterApiNichtErreichbar as exc:
                letzter_fehler = exc
                if versuch < self.MAX_VERSUCHE:
                    self._sleep(1.0)
            except OrtNichtGefunden:
                raise

        assert letzter_fehler is not None
        raise letzter_fehler

    def _messung_zu_wetterzustand(self, messung: WetterApiMessung) -> Wetterzustand:
        sonnenschein_intensitaet = min(messung.sonnenschein_sekunden / 3600.0, 1.0)
        regen_intensitaet = min(messung.niederschlag_mm / 10.0, 1.0)
        return Wetterzustand(
            sonnenschein=sonnenschein_intensitaet > 0.0,
            regen=regen_intensitaet > 0.0,
            sonnenschein_intensitaet=sonnenschein_intensitaet,
            regen_intensitaet=regen_intensitaet,
        )

    def _berechne_sichtbarkeit(
        self,
        messung: WetterApiMessung,
        sonnenstand: Sonnenstand,
    ) -> int:
        optik = leite_optische_bedingungen_ab(messung)
        regen_faktor = min(messung.rain_mm + messung.showers_mm, 5.0) / 5.0
        return berechne_regenbogen_sichtbarkeit(
            RegenbogenOptikFaktoren(
                sonnenstands_faktor=berechne_sonnenstands_faktor(sonnenstand),
                regen_faktor=regen_faktor,
                direktlicht_faktor=optik.direktlicht_faktor,
                tropfen_qualitaet=optik.tropfen_qualitaet,
                sicht_faktor=optik.sicht_faktor,
                hintergrund_kontrast_faktor=optik.hintergrund_kontrast_faktor,
                niederschlags_phasen_faktor=optik.niederschlags_phasen_faktor,
            )
        )
```

In der Projektdatei wird der konkrete Typ `StandortKoordinaten` verwendet.
Der frühere `ort: str`-Pfad aus Session 8 ist damit vollständig ersetzt.

### 11.11 Wiring und GUI anpassen

```python
# src/regenbogen/adapters/wiring.py
import time
from datetime import datetime
from zoneinfo import ZoneInfo

from regenbogen.infrastructure.open_meteo_client import OpenMeteoClient
from regenbogen.infrastructure.plz_lookup import DemoStandortLookup
from regenbogen.system.core.wahrscheinlichkeit_use_case import (
    RegenbogenWahrscheinlichkeitUseCase,
)


def create_regenbogen_use_case() -> RegenbogenWahrscheinlichkeitUseCase:
    return RegenbogenWahrscheinlichkeitUseCase(
        api=OpenMeteoClient(),
        standort=DemoStandortLookup(),
        sleep=time.sleep,
        clock=lambda: datetime.now(ZoneInfo("Europe/Berlin")),
    )
```

`datetime.now()` liegt damit nicht in `domain/` und nicht in `system/core/`,
sondern in der produktiven Verdrahtung. Tests können eine feste Uhrzeit
injizieren.

Die GUI reicht die PLZ jetzt an den Use Case weiter:

```python
# Ausschnitt aus src/regenbogen/cli/gui_main.py

ergebnis = use_case.berechne_vollstaendig(
    konfiguration.ortsname,
    konfiguration.postleitzahl or None,
)
```

Damit wird die PLZ semantisch wirksam. Der Unterschied zu Session 10 ist
explizit: Vorher war PLZ nur Anzeige-Komfort; jetzt ist sie Systemeingabe.

### 11.12 Tests

Domain-Test für die Geometrie:

```python
# tests/domain/test_regenbogen_geometrie.py
from regenbogen.domain.regenbogen_geometrie import (
    Sonnenstand,
    berechne_sonnenstands_faktor,
)


def test_sonne_unter_horizont_ergibt_null():
    assert berechne_sonnenstands_faktor(Sonnenstand(-2.0, 180.0)) == 0.0


def test_niedrige_sonne_ist_guenstig():
    assert berechne_sonnenstands_faktor(Sonnenstand(10.0, 180.0)) == 1.0


def test_hohe_sonne_ergibt_null():
    assert berechne_sonnenstands_faktor(Sonnenstand(45.0, 180.0)) == 0.0


def test_uebergangsbereich_faellt_linear():
    faktor = berechne_sonnenstands_faktor(Sonnenstand(33.5, 180.0))
    assert 0.0 < faktor < 1.0
```

System-Test mit fester Uhrzeit:

```python
# tests/system/test_winkelmodell.py
from datetime import datetime
from zoneinfo import ZoneInfo
from unittest.mock import MagicMock

from regenbogen.system.core.wahrscheinlichkeit_use_case import (
    RegenbogenWahrscheinlichkeitUseCase,
)
from regenbogen.system.ports.standort_port import StandortKoordinaten
from regenbogen.system.ports.wetterapi_port import WetterApiMessung


class FakeStandort:
    def finde_koordinaten(self, ort: str, postleitzahl: str | None):
        return StandortKoordinaten(52.532, 13.384, "Europe/Berlin")


def test_winkelmodell_nutzt_feste_uhrzeit():
    api = MagicMock()
    api.hole_aktuelle_messung.return_value = WetterApiMessung(
        sonnenschein_sekunden=1800.0,
        niederschlag_mm=5.0,
        rain_mm=5.0,
        weather_code=61,
        cloud_cover=60.0,
        visibility_m=10_000.0,
        direct_radiation=400.0,
        temperature_2m=12.0,
    )
    uc = RegenbogenWahrscheinlichkeitUseCase(
        api=api,
        standort=FakeStandort(),
        sleep=lambda _: None,
        clock=lambda: datetime(2026, 6, 13, 19, 0, tzinfo=ZoneInfo("Europe/Berlin")),
    )

    ergebnis = uc.berechne_vollstaendig("Berlin", "10115")

    assert ergebnis.postleitzahl == "10115"
    assert ergebnis.sonnenstand.sonnenhoehe_grad > 0.0
    assert 0 <= ergebnis.wahrscheinlichkeit <= 100
    assert 0 <= ergebnis.sichtbarkeit <= 100
```

### 11.13 Import-Checker und Abschluss

```bash
python tools/check_import_layers.py --preflight src tests tools
python tools/resolve_test_obligations.py \
  --changed-file src/regenbogen/domain/regenbogen_geometrie.py \
  --changed-file src/regenbogen/system/ports/standort_port.py \
  --changed-file src/regenbogen/infrastructure/plz_lookup.py \
  --changed-file src/regenbogen/system/core/sonnenstand.py \
  --changed-file src/regenbogen/system/core/wahrscheinlichkeit_use_case.py \
  --changed-file src/regenbogen/adapters/wiring.py \
  --changed-file src/regenbogen/cli/gui_main.py
python -m ruff check .
python -m mypy src
python -m pytest
```

Erfahrungsbericht:

```markdown
# Erfahrungsbericht: Sonnenstand- und Winkelmodell

Datum:        2026-06-13
Session-Typ:  abgeschlossen
Aufgabe:      Regenbogen-Wahrscheinlichkeit um Sonnenstand erweitern
Ergebnis:     PLZ/Ort -> Koordinaten, Uhrzeit -> Sonnenstand,
              Sonnenstand -> Geometriefaktor, Tests grün

Learning-Matrix-Kandidat: ja
Muster-ID: Placeholder-Formel wird durch kontrolliertes Fachmodell ersetzt

## Was sich bewährt hat

Die PLZ war in Session 10 bewusst nur UI-Komfort. Erst diese Session hat ihr
eine systemsemantische Rolle gegeben. Dadurch wurde sichtbar, dass eine neue
Portfläche für StandortKoordinaten nötig ist.

Die Geometrie blieb in domain/ rein fachlich. Zeit- und Koordinatenbeschaffung
wurden nicht in domain/ gezogen. Das verhindert eine schleichende Vermischung
von Fachmodell, Systemlogik und Infrastruktur.

## Modellgrenze

Das Modell kennt weiterhin keine Regenzellenrichtung. Es berechnet daher eine
verbesserte Wahrscheinlichkeit, keinen sicheren Sichtbarkeitsnachweis.
```

Ort: `tmp/erfahrungsberichte/2026-06-13-EB-sonnenstand-winkelmodell.md`.

### 11.14 Optionaler Abbruchpfad: SA1 bei rotem Test

Auch dieser Abschnitt ist eine **Verzweigung**, nicht Teil des grünen
Hauptpfads. Er zeigt den häufigsten praktischen Fall: Ein Test wird rot.
Rot bedeutet nicht automatisch, dass der Code falsch ist. Rot bedeutet: Es
liegt ein prüfbarer Widerspruch vor.

Auslöser ist ein falsch nachgezogener Test zur Sonnenhöhe:

```text
# NICHT IN DEN HAUPTPFAD ÜBERNEHMEN
# tests/domain/test_regenbogen_geometrie.py
assert berechne_sonnenstands_faktor(Sonnenstand(42.0, 180.0)) > 0.0
```

`pytest` meldet rot:

```text
SA1 SOFT-ABBRUCH
Test: test_sonnenhoehe_42_grad_ist_noch_sichtbar
Grund: Erwartet > 0.0, erhalten 0.0.
```

Der Agent schreibt Evidence:

```markdown
# SOFT-Abbruch: roter Test im Winkelmodell

Status: SOFT-ABBRUCH
Abbruch-Code: SA1
Datei: tests/domain/test_regenbogen_geometrie.py
Test: test_sonnenhoehe_42_grad_ist_noch_sichtbar

## Evidence

pytest rot. Die Implementierung liefert bei Sonnenhoehe 42° den Faktor 0.0.

## Semantische Prüfung

Sprechakt 2026-06-13-regenbogen-geometrie.md sagt:
- Sonnenhoehe >= 42°: 0.

## Bewertung

Nicht der Code ist falsch, sondern der Test. Der Test widerspricht der
festgelegten Semantik.

## Wiedereinstieg

1. Test auf die festgelegte Grenze korrigieren.
2. Erneut pytest ausführen.
3. Bei Grün normal in Abschnitt 11.13 fortsetzen.
```

Korrektur im Hauptpfad:

```text
assert berechne_sonnenstands_faktor(Sonnenstand(42.0, 180.0)) == 0.0
```

Der Punkt ist nicht der konkrete Grenzwert. Der Punkt ist: SA1 ist kein
unstrukturierter Fehlerzustand. Der Agent stoppt, legt Evidence ab und prüft,
ob Code oder Test gegen die festgelegte Semantik verstoßen.

---

## 12. Siebte Session: Tropfenqualität und wetterdatenbasiertes Sichtbarkeitsmodell

**Aufgabe:** Das Winkelmodell aus Session 11 soll fachlich weiter verfeinert
werden. Die Frage lautet jetzt nicht mehr nur: „Ist ein Regenbogen geometrisch
möglich?“, sondern: „Wie gut sind die optischen Bedingungen für einen sichtbaren
Regenbogen?“

Die wichtigste Korrektur bleibt: Normale Wetterdaten liefern in der Regel
keine echte Tröpfchengrößenverteilung. Wir bekommen also keinen Messwert
`mittlerer_tropfendurchmesser_mm`. Was wir aus Wetterdaten aber bekommen
können, sind indirekte Hinweise:

```text
Niederschlagsart       → drizzle / rain / showers / snow über weather_code
Regenmenge             → rain, showers, precipitation
Direktlicht            → direct_radiation oder direct_normal_irradiance
Sichtweite             → visibility
Bewölkung              → cloud_cover, cloud_cover_low/mid/high
Temperatur             → temperature_2m, für Niederschlagsphase plausibilisieren
```

Damit wird aus der alten `RegenbogenWahrscheinlichkeit` ein besserer
**Sichtbarkeits-Score**. Er bleibt ein Modell, kein Nachweis. Die
Regenzellenrichtung fehlt weiterhin.

```text
Sonnenstand               → geometrisches Fenster
Direktlicht               → wird der Regen beleuchtet?
Niederschlagsart/-menge   → gibt es geeignete Wassertröpfchen?
Sichtweite                → kann der Bogen optisch sichtbar sein?
Bewölkung/Kontrast        → ist der Hintergrund günstig?
Temperatur/Phase          → Regen statt Schnee/Eis?
```

### 12.1 Regentropfen als fachliches Hintergrunddokument

Der Agent legt ein kleines fachliches Hintergrunddokument an:

```text
./regentropfen-und-wetterdaten.md
```

Die Datei liegt in diesem Beispiel bewusst im Projektroot neben dem Tutorial.
Sie ist ein mitgeliefertes Begleitdokument, kein Pflichtartefakt der Box und
kein eigener semantischer Raum. Ein reales Projekt kann dafür später einen
Dokumentationsordner einführen; dann muss der Pfad im Tutorial und in den
Folgeartefakten explizit nachgezogen werden.

Dieses Dokument ist kein operatives Glossar. Es erklärt dem Menschen, warum
Tröpfengröße relevant ist, warum normale Wetter-APIs sie meistens nicht direkt
liefern und welche Ersatzgrößen im Beispiel verwendet werden.

Der zentrale Inhalt:

```text
- Regentropfen entstehen durch Kondensation und Koaleszenz.
- Ab etwa 0,5 mm Durchmesser spricht man von Regentropfen.
- Sehr kleine Tropfen bzw. Nebel erzeugen eher Fogbows: blass, breit, weißlich.
- Normale Regenbögen brauchen Wassertröpfchen und direkte Sonnenbeleuchtung.
- Aus Standard-Wetterdaten wird Tropfenqualität nur heuristisch abgeleitet.
```

Damit entsteht eine saubere Dokumentationsgrenze:

```text
Fachnotiz       erklärt physikalischen Hintergrund
Glossar         definiert operative Projektbegriffe
Domain-Code     implementiert die festgelegten Faktoren
System-Code     leitet Faktoren aus verfügbaren Wetterdaten ab
```

### 12.2 Preflight: Warum diese Iteration wieder ein echter Schnitt ist

**P3/P4 — betroffene Räume:**

```text
./regentropfen-und-wetterdaten.md        → Dokumentation/Evidence
src/regenbogen/domain/regenbogen_optik.py              → domain
src/regenbogen/system/ports/wetterapi_port.py          → system.ports
src/regenbogen/infrastructure/open_meteo_client.py     → infrastructure
src/regenbogen/system/core/wahrscheinlichkeit_use_case.py → system.core
src/regenbogen/system/core/optische_bedingungen.py     → system.core
```

Die Änderung berührt mehrere Räume und verändert das Modell. Damit tritt T2
ein. Außerdem entstehen neue Fachbegriffe. Damit tritt T1 ein.

**P5 — Glossarprüfung:**

Neue oder präzisierte Begriffe:

```text
TropfenQualitaet
DirektlichtFaktor
SichtFaktor
HintergrundKontrastFaktor
NiederschlagsPhasenFaktor
OptischeBedingungen
RegenbogenSichtbarkeit
```

Die fachlichen Faktoren gehören nach `domain/`, weil sie das Modell beschreiben.
Die Ableitung aus API-Feldern gehört nach `system/core/`, weil dort technische
Messdaten in Modellfaktoren übersetzt werden.

**P9 — Task-Schnitt:**

Der Agent teilt die Arbeit:

```text
Teil A: Regentropfen-Fachnotiz schreiben
Teil B: Fachbegriffe festlegen und Glossar ergänzen
Teil C: WetterApiMessung um verfügbare Wetterdaten erweitern
Teil D: System-Mapping von Wetterdaten zu Optikfaktoren
Teil E: Domain-Score erweitern
Teil F: Tests und Abschluss-Evidence
```

**P10 — Planpflicht:**

```text
docs/plans/2026-06-14-tropfenqualitaet-sichtbarkeitsmodell.md
```

Ergebnis: **SPRECHAKT + TEILEN**.

### 12.3 Sprechakt SP7: Optische Bedingungen

```markdown
# Sprechakt: Optische Bedingungen und Tropfenqualität

Zeitpunkt:        2026-06-14 09:20
Sprechakt-Klasse: SP7 — Aktiv benötigte Begriffe fehlen im Glossar
Betroffener Begriff: TropfenQualitaet, DirektlichtFaktor, SichtFaktor,
                     HintergrundKontrastFaktor, NiederschlagsPhasenFaktor,
                     RegenbogenSichtbarkeit
Status: offen

## Was fehlt

Das bisherige Modell nutzt Sonnenstand, Regenintensität und Sonnenschein.
Es unterscheidet aber nicht:
- Regen vs. Nieselregen vs. Schnee,
- direktes Sonnenlicht vs. diffuse Helligkeit,
- gute vs. schlechte Sichtweite,
- dunklen vs. hellen Hintergrund.

## Was der Agent sieht

weather_api_says:
  Open-Meteo kann weather_code, rain, showers, snowfall, precipitation,
  visibility, cloud_cover und direct_radiation liefern.

model_says:
  Es gibt noch keinen Begriff für Tropfenqualität oder optische Bedingungen.

schema_says:
  Fachliche Modellfaktoren gehören nach domain/.
  Ableitung aus Wetterdaten gehört nach system/core/.
  infrastructure/ liefert nur Messwerte.

## Analyse des Agenten

Tröpfchengröße selbst ist in normalen Wetterdaten nicht direkt verfügbar.
Sie darf nicht erfunden werden. Man kann aber aus weather_code und
Niederschlagsart eine heuristische Tropfenqualität ableiten:
- drizzle: kleine Tropfen, eher schwacher/fogbow-artiger Effekt,
- rain: geeignete Wassertröpfchen,
- showers: oft gute Tropfen, aber lokal/kurzlebig,
- snow/freezing: für normalen Regenbogen ungeeignet oder stark abgewertet.

## Warum der Agent nicht fortfahren kann

Ohne Festlegung würde der Agent frei entscheiden, welche Wetterdaten wie stark
in die Sichtbarkeit eingehen. Das wäre eine stille Modellentscheidung.

## Was der Mensch festlegt

RegenbogenSichtbarkeit:
  Score in [0, 100], der die erwartete Sichtbarkeit eines normalen
  Sonnen-Regenbogens beschreibt. Kein Nachweis.

TropfenQualitaet:
  Faktor in [0, 1], abgeleitet aus Niederschlagsart und Intensität.
  - Kein Wasser-Niederschlag: 0.
  - Nieselregen: niedrig bis mittel.
  - Regen: gut.
  - Schauer: gut, aber lokaler und volatiler.
  - Schnee/Eis: 0 für normalen Regenbogen.

DirektlichtFaktor:
  Faktor in [0, 1], abgeleitet aus direct_radiation oder direct_normal_irradiance.
  Ohne direktes Licht ist ein normaler Sonnen-Regenbogen nicht sichtbar.

SichtFaktor:
  Faktor in [0, 1], abgeleitet aus visibility.
  Schlechte Sicht dämpft den Score.

HintergrundKontrastFaktor:
  Faktor in [0, 1], heuristisch aus Bewölkung abgeleitet.
  Ein dunklerer Regenhintergrund bei gleichzeitigem Direktlicht ist günstig.

NiederschlagsPhasenFaktor:
  Faktor in [0, 1], der Wasser-Niederschlag gegenüber Schnee/Eis bevorzugt.

Modellgrenze:
  Regenzellenrichtung und echte Tropfengrößenverteilung fehlen weiterhin.
  Das Modell darf daher nicht „sichtbar“ garantieren.

Status: festgelegt
Folgeartefakte: glossar-domain.md, glossar-system.md,
                ./regentropfen-und-wetterdaten.md,
                domain/regenbogen_optik.py,
                system/core/optische_bedingungen.py
```

### 12.4 Domain-Glossar ergänzen

```markdown
### RegenbogenSichtbarkeit

Bedeutung: Score in [0, 100], der die erwartete Sichtbarkeit eines normalen
Sonnen-Regenbogens beschreibt.

Invariante: Der Score ist kein Sichtbarkeitsnachweis. Ohne Regenzellenrichtung
bleibt er eine modellbasierte Bewertung lokaler Bedingungen.

Projektionen:
- Code: src/regenbogen/domain/regenbogen_optik.py
- Tests: tests/domain/test_regenbogen_optik.py

Migrationsstatus: canonical

---

### TropfenQualitaet

Bedeutung: Faktor in [0, 1] für die Eignung des vorhandenen Niederschlags zur
Bildung eines sichtbaren Regenbogens.

Invariante: Echte Tropfengrößen werden nicht gemessen. Der Faktor ist eine
Heuristik aus Niederschlagsart und Intensität.

Projektionen:
- Code: src/regenbogen/domain/regenbogen_optik.py
- System-Ableitung: src/regenbogen/system/core/optische_bedingungen.py

Migrationsstatus: canonical
```

### 12.5 WetterApiMessung erweitern

Die Portfläche bleibt der richtige Ort für die Rohdaten. `WetterApiMessung`
wird erweitert, aber bleibt ein DTO ohne Fachentscheidung.

```python
# src/regenbogen/system/ports/wetterapi_port.py
from abc import ABC, abstractmethod
from dataclasses import dataclass

from regenbogen.system.ports.standort_port import StandortKoordinaten


@dataclass(frozen=True)
class WetterApiMessung:
    """Technische Messung der Wetter-API.

    Dieser Typ ist bewusst kein Domain-Typ. Er beschreibt Rohdaten und
    abgeleitete Wetterdaten der externen API. Die fachliche Interpretation
    passiert in system/core/ und domain/.
    """

    sonnenschein_sekunden: float
    niederschlag_mm: float
    rain_mm: float = 0.0
    showers_mm: float = 0.0
    snowfall_cm: float = 0.0
    weather_code: int = 0
    cloud_cover: float = 100.0
    visibility_m: float | None = None
    direct_radiation: float = 0.0
    temperature_2m: float = 0.0


class WetterApiNichtErreichbar(Exception):
    """API nicht erreichbar. Recoverable — Retry erlaubt."""


class OrtNichtGefunden(Exception):
    """Unbekannter Ort. Terminal — kein Retry."""


class WetterApiPort(ABC):
    @abstractmethod
    def hole_aktuelle_messung(
        self,
        koordinaten: StandortKoordinaten,
    ) -> WetterApiMessung:
        """Liefert rohe technische Wetterdaten für Koordinaten."""
```

Wichtig: Diese Felder sind technische Messwerte. Sie sagen noch nicht:
„guter Regenbogen“. Erst `system/core/optische_bedingungen.py` leitet daraus
Modellfaktoren ab.

### 12.6 OpenMeteoClient erweitert die API-Abfrage

```python
# src/regenbogen/infrastructure/open_meteo_client.py
import httpx

from regenbogen.system.ports.standort_port import StandortKoordinaten
from regenbogen.system.ports.wetterapi_port import (
    WetterApiMessung,
    WetterApiNichtErreichbar,
    WetterApiPort,
)


class OpenMeteoClient(WetterApiPort):
    """Implementiert WetterApiPort über die Open-Meteo API.

    Liefert WetterApiMessung — keinen Domain-Typ. Das Mapping nach
    Wetterzustand ist Aufgabe von system/core/.
    """

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def hole_aktuelle_messung(
        self,
        koordinaten: StandortKoordinaten,
    ) -> WetterApiMessung:
        try:
            response = httpx.get(
                self.BASE_URL,
                params={
                    "latitude": koordinaten.latitude,
                    "longitude": koordinaten.longitude,
                    "current": ",".join(
                        [
                            "temperature_2m",
                            "precipitation",
                            "rain",
                            "showers",
                            "snowfall",
                            "weather_code",
                            "cloud_cover",
                            "visibility",
                            "direct_radiation",
                            "sunshine_duration",
                        ]
                    ),
                },
                timeout=10.0,
            )
            response.raise_for_status()
        except httpx.ConnectError as exc:
            raise WetterApiNichtErreichbar(f"Nicht erreichbar: {exc}") from exc
        except httpx.HTTPStatusError as exc:
            raise WetterApiNichtErreichbar(
                f"API-Fehler: {exc.response.status_code}"
            ) from exc

        return self._parse_response(response.json())

    def _parse_response(self, data: dict) -> WetterApiMessung:
        current = data.get("current", {})
        return WetterApiMessung(
            sonnenschein_sekunden=float(current.get("sunshine_duration", 0.0)),
            niederschlag_mm=float(current.get("precipitation", 0.0)),
            rain_mm=float(current.get("rain", 0.0)),
            showers_mm=float(current.get("showers", 0.0)),
            snowfall_cm=float(current.get("snowfall", 0.0)),
            weather_code=int(current.get("weather_code", 0)),
            cloud_cover=float(current.get("cloud_cover", 100.0)),
            visibility_m=(
                float(current["visibility"])
                if current.get("visibility") is not None
                else None
            ),
            direct_radiation=float(current.get("direct_radiation", 0.0)),
            temperature_2m=float(current.get("temperature_2m", 0.0)),
        )
```

Wenn ein Modell `visibility` oder `direct_radiation` nicht liefert, muss die
Ableitung konservativ bleiben. Ein fehlender Wert darf nicht als perfekter Wert
interpretiert werden.

### 12.7 System-Mapping: optische Bedingungen ableiten

```python
# src/regenbogen/system/core/optische_bedingungen.py
from dataclasses import dataclass

from regenbogen.system.ports.wetterapi_port import WetterApiMessung


@dataclass(frozen=True)
class OptischeBedingungen:
    """Aus Wetterdaten abgeleitete Faktoren für das Domain-Modell."""

    tropfen_qualitaet: float
    direktlicht_faktor: float
    sicht_faktor: float
    hintergrund_kontrast_faktor: float
    niederschlags_phasen_faktor: float


def leite_optische_bedingungen_ab(messung: WetterApiMessung) -> OptischeBedingungen:
    return OptischeBedingungen(
        tropfen_qualitaet=_tropfen_qualitaet(messung),
        direktlicht_faktor=_direktlicht_faktor(messung.direct_radiation),
        sicht_faktor=_sicht_faktor(messung.visibility_m),
        hintergrund_kontrast_faktor=_hintergrund_kontrast_faktor(
            messung.cloud_cover
        ),
        niederschlags_phasen_faktor=_niederschlags_phasen_faktor(messung),
    )


def _direktlicht_faktor(direct_radiation: float) -> float:
    return max(0.0, min(1.0, direct_radiation / 400.0))


def _sicht_faktor(visibility_m: float | None) -> float:
    if visibility_m is None:
        return 0.7
    return max(0.0, min(1.0, visibility_m / 10_000.0))


def _hintergrund_kontrast_faktor(cloud_cover: float) -> float:
    if cloud_cover < 20.0:
        return 0.7
    if cloud_cover <= 80.0:
        return 1.0
    return 0.8


def _niederschlags_phasen_faktor(messung: WetterApiMessung) -> float:
    if messung.weather_code in {56, 57, 66, 67, 71, 73, 75, 77}:
        return 0.0
    if messung.snowfall_cm > 0.0:
        return 0.0
    if messung.temperature_2m < -1.0:
        return 0.2
    return 1.0


def _wasser_mm(messung: WetterApiMessung) -> float:
    wasser = messung.rain_mm + messung.showers_mm
    if wasser <= 0.0 and messung.niederschlag_mm > 0.0 and messung.snowfall_cm <= 0.0:
        return messung.niederschlag_mm
    return wasser


def _tropfen_qualitaet(messung: WetterApiMessung) -> float:
    code = messung.weather_code
    wasser_mm = _wasser_mm(messung)

    if wasser_mm <= 0.0:
        return 0.0

    if code in {56, 57, 66, 67, 71, 73, 75, 77}:
        return 0.0
    if code in {51, 53, 55}:              # drizzle
        return min(0.6, 0.2 + wasser_mm / 2.0)
    if code in {61, 63, 65}:              # rain
        return min(1.0, 0.4 + wasser_mm / 5.0)
    if code in {80, 81, 82}:              # rain showers
        return min(1.0, 0.5 + wasser_mm / 4.0)

    return min(0.8, wasser_mm / 5.0)
```

Die Zahlen sind bewusst einfach und dokumentiert heuristisch. Der fachliche
Gewinn liegt nicht darin, dass die Formel perfekt ist, sondern darin, dass die
Annahmen explizit und testbar werden.

### 12.8 Domain-Modell: Sichtbarkeit statt bloßer Wahrscheinlichkeit

```python
# src/regenbogen/domain/regenbogen_optik.py
from dataclasses import dataclass


@dataclass(frozen=True)
class RegenbogenOptikFaktoren:
    sonnenstands_faktor: float
    regen_faktor: float
    direktlicht_faktor: float
    tropfen_qualitaet: float
    sicht_faktor: float
    hintergrund_kontrast_faktor: float
    niederschlags_phasen_faktor: float


def berechne_regenbogen_sichtbarkeit(faktoren: RegenbogenOptikFaktoren) -> int:
    """Berechnet einen Sichtbarkeits-Score in [0, 100].

    Harte Gates:
    - keine geeignete Sonnenhöhe -> 0
    - kein Regen -> 0
    - kein direktes Licht -> 0
    - keine geeignete Niederschlagsphase -> 0
    """
    if faktoren.sonnenstands_faktor <= 0.0:
        return 0
    if faktoren.regen_faktor <= 0.0:
        return 0
    if faktoren.direktlicht_faktor <= 0.0:
        return 0
    if faktoren.niederschlags_phasen_faktor <= 0.0:
        return 0

    score = (
        faktoren.sonnenstands_faktor
        * faktoren.regen_faktor
        * faktoren.direktlicht_faktor
        * faktoren.tropfen_qualitaet
        * faktoren.sicht_faktor
        * faktoren.hintergrund_kontrast_faktor
        * faktoren.niederschlags_phasen_faktor
    )
    return round(max(0.0, min(1.0, score)) * 100)
```

Warum das in `domain/` liegt: Die Faktoren selbst sind bereits modellierte
fachliche Größen. Die Domain-Regel kombiniert sie und entscheidet harte Gates.
Die Domain liest keine Wetter-API, kennt keine WMO-Codes und kennt keine
Open-Meteo-Feldnamen.

### 12.9 Use Case integriert die neuen Faktoren

Der Use Case wird erweitert:

```python
# Ausschnitt aus src/regenbogen/system/core/wahrscheinlichkeit_use_case.py
from regenbogen.domain.regenbogen_optik import (
    RegenbogenOptikFaktoren,
    berechne_regenbogen_sichtbarkeit,
)
from regenbogen.system.core.optische_bedingungen import (
    leite_optische_bedingungen_ab,
)

# im Ablauf nach messung und sonnenstand:
optik = leite_optische_bedingungen_ab(messung)

sichtbarkeit = berechne_regenbogen_sichtbarkeit(
    RegenbogenOptikFaktoren(
        sonnenstands_faktor=berechne_sonnenstands_faktor(sonnenstand),
        regen_faktor=min(messung.rain_mm + messung.showers_mm, 5.0) / 5.0,
        direktlicht_faktor=optik.direktlicht_faktor,
        tropfen_qualitaet=optik.tropfen_qualitaet,
        sicht_faktor=optik.sicht_faktor,
        hintergrund_kontrast_faktor=optik.hintergrund_kontrast_faktor,
        niederschlags_phasen_faktor=optik.niederschlags_phasen_faktor,
    )
)
```

`WetterErgebnis` enthält jetzt zusätzlich `sichtbarkeit`. Die finale Form
bleibt konsistent mit Session 11 und verwendet weiterhin `postleitzahl`, nicht
ein separates `ortsanzeige`-Feld:

```python
@dataclass(frozen=True)
class WetterErgebnis:
    ort: str
    postleitzahl: str | None
    zustand: Wetterzustand
    sonnenstand: Sonnenstand
    wahrscheinlichkeit: int
    sichtbarkeit: int
```

Die GUI formatiert daraus eine Anzeige. `ortsanzeige` bleibt GUI-Text und wird
nicht Teil des systemsemantischen Ergebnisobjekts.

### 12.10 Tests

```python
# tests/domain/test_regenbogen_optik.py
from regenbogen.domain.regenbogen_optik import (
    RegenbogenOptikFaktoren,
    berechne_regenbogen_sichtbarkeit,
)


def _faktoren(**overrides):
    werte = dict(
        sonnenstands_faktor=1.0,
        regen_faktor=1.0,
        direktlicht_faktor=1.0,
        tropfen_qualitaet=1.0,
        sicht_faktor=1.0,
        hintergrund_kontrast_faktor=1.0,
        niederschlags_phasen_faktor=1.0,
    )
    werte.update(overrides)
    return RegenbogenOptikFaktoren(**werte)


def test_kein_direktlicht_ergibt_null():
    assert berechne_regenbogen_sichtbarkeit(
        _faktoren(direktlicht_faktor=0.0)
    ) == 0


def test_schneephase_ergibt_null():
    assert berechne_regenbogen_sichtbarkeit(
        _faktoren(niederschlags_phasen_faktor=0.0)
    ) == 0


def test_alle_faktoren_guenstig_ergeben_hohen_score():
    assert berechne_regenbogen_sichtbarkeit(_faktoren()) == 100
```

```python
# tests/system/test_optische_bedingungen.py
from regenbogen.system.core.optische_bedingungen import (
    leite_optische_bedingungen_ab,
)
from regenbogen.system.ports.wetterapi_port import WetterApiMessung


def messung(**overrides):
    werte = dict(
        sonnenschein_sekunden=1800.0,
        niederschlag_mm=2.0,
        rain_mm=2.0,
        showers_mm=0.0,
        snowfall_cm=0.0,
        weather_code=61,
        cloud_cover=60.0,
        visibility_m=10_000.0,
        direct_radiation=400.0,
        temperature_2m=12.0,
    )
    werte.update(overrides)
    return WetterApiMessung(**werte)


def test_regen_liefert_gute_tropfenqualitaet():
    optik = leite_optische_bedingungen_ab(messung(weather_code=61, rain_mm=2.0))
    assert optik.tropfen_qualitaet > 0.5


def test_schnee_wird_fuer_normalen_regenbogen_abgewertet():
    optik = leite_optische_bedingungen_ab(
        messung(weather_code=71, snowfall_cm=1.0, rain_mm=0.0)
    )
    assert optik.niederschlags_phasen_faktor == 0.0


def test_fehlende_sichtweite_ist_konservativ_aber_nicht_null():
    optik = leite_optische_bedingungen_ab(messung(visibility_m=None))
    assert 0.0 < optik.sicht_faktor < 1.0
```

### 12.11 Abschluss und Erfahrungsbericht

```bash
python tools/check_import_layers.py --preflight src tests tools
python tools/resolve_test_obligations.py \
  --changed-file ./regentropfen-und-wetterdaten.md \
  --changed-file src/regenbogen/domain/regenbogen_optik.py \
  --changed-file src/regenbogen/system/ports/wetterapi_port.py \
  --changed-file src/regenbogen/system/core/optische_bedingungen.py \
  --changed-file src/regenbogen/system/core/wahrscheinlichkeit_use_case.py
python -m ruff check .
python -m mypy src
python -m pytest tests/domain tests/system
```

Erfahrungsbericht:

```markdown
# Erfahrungsbericht: Tropfenqualität und optische Bedingungen

Datum:        2026-06-14
Session-Typ:  abgeschlossen
Aufgabe:      Regenbogenmodell mit verfügbaren Wetterdaten verfeinern
Ergebnis:     Regentropfen-Fachnotiz, neue Optikfaktoren, Tests grün

Learning-Matrix-Kandidat: ja
Muster-ID: Nicht direkt verfügbare Fachgröße durch explizite Heuristik ersetzen

## Was sich bewährt hat

Der Agent durfte Tröpfchengröße nicht erfinden. Stattdessen wurde explizit
festgelegt, welche Wetterdaten verfügbar sind und welche Faktoren daraus nur
heuristisch abgeleitet werden dürfen.

## Modellgrenze

Die Regenzellenrichtung fehlt weiterhin. Das Modell bewertet lokale optische
Bedingungen und Niederschlagsqualität, aber es beweist keine Sichtbarkeit.
```

Ort: `tmp/erfahrungsberichte/2026-06-14-EB-tropfenqualitaet.md`.


## 13. Achte Session: Logging als Infrastruktur

**Aufgabe:** Das Projekt soll brauchbares Logging erhalten. Nicht als
Fachfunktion, nicht als Evidence-Ersatz, sondern als technische Beobachtung im
laufenden System.

Diese Session ist wichtig, weil Logging sehr leicht falsch einsortiert wird:

```text
logging in domain/        falsch — Fachmodell darf keine Betriebsbeobachtung kennen
logging direkt im Use Case problematisch — Systemlogik koppelt sich an Infrastruktur
logging in infrastructure richtig — konkrete Ausgabe, Handler, Formatierung
system.ports              richtig — schmale Port-Fläche für systemische Ereignisse
```

Die Regel lautet: **Logging-Ausführung ist Infrastruktur.** Wenn `system/core/`
Ereignisse melden soll, spricht es nur über einen Port. Die konkrete
Implementierung mit der Python-`logging`-Bibliothek liegt in `infrastructure/`.

Wichtig ist auch die Abgrenzung zu Evidence:

```text
Logging    technische Laufzeitbeobachtung, hilfreich für Diagnose
Evidence   projekt-/workflow-relevanter Nachweis, reviewbar, dauerhaft, Markdown
```

Ein Logeintrag darf ein Ereignis sichtbar machen. Er ersetzt keinen Sprechakt,
keinen Erfahrungsbericht und kein Evidence-Artefakt.

### 13.1 Preflight: Warum Logging nicht einfach eingebaut wird

**P4 — Räume bestimmen:**

```text
src/regenbogen/system/ports/logging_port.py          → system.ports
src/regenbogen/infrastructure/event_logger.py        → infrastructure
src/regenbogen/system/core/wahrscheinlichkeit_use_case.py → system.core
src/regenbogen/adapters/wiring.py                    → adapters
```

Die Aufgabe berührt mehrere Räume. T2 tritt ein.

**P5 — Glossar prüfen:**

Neue Begriffe:

```text
LogEvent
EventLogger
DiagnoseLogging
```

Das sind keine Fachbegriffe. Sie gehören nicht in `glossar-domain.md`. Sie sind
Betriebs- und Systembegriffe und gehören nach `glossar-system.md`.

**Dependency-Frage:**

Keine neue Runtime-Dependency. Die Python-Standardbibliothek `logging` genügt.
Kein SP4 nötig.

**Raumfrage:**

Die konkrete Logging-Ausgabe ist Infrastruktur. Die systemische Schnittstelle
ist ein Port. Kein neuer Raum nötig.

Ergebnis: **FORTSETZEN mit Glossar-Ergänzung und Task-Schnitt.**

Der Agent teilt die Aufgabe:

```text
Teil A: Logging-Begriffe in glossar-system.md eintragen
Teil B: Logging-Port in system/ports/ definieren
Teil C: Stdlib-Logging-Implementierung in infrastructure/ bauen
Teil D: Use Case über Port instrumentieren
Teil E: wiring.py verdrahten
Teil F: Tests für Ereignisse und Importgrenzen ergänzen
```

### 13.2 System-Glossar ergänzen

```markdown
### LogEvent

Bedeutung: Systemisches Laufzeitereignis, das für Diagnosezwecke protokolliert
werden darf.

Invariante: Ein LogEvent ist kein Evidence-Artefakt und keine fachliche
Tatsache. Es darf keine neue Fach- oder Systemsemantik erzeugen.

Nicht: Sprechakt, Evidence, Domain-Ereignis.

Projektionen:
- Code: src/regenbogen/system/ports/logging_port.py
- Implementation: src/regenbogen/infrastructure/event_logger.py

Migrationsstatus: canonical

---

### EventLogger

Bedeutung: Port, über den Systemcode Laufzeitereignisse an eine technische
Logging-Implementierung übergibt.

Invariante: Systemcode kennt nur den Port. Formatierung, Handler, Zielausgabe
und konkrete Python-logging-Konfiguration liegen in infrastructure/.

Nicht: globaler Logger, Evidence-Schreiber, Fachservice.

Projektionen:
- Code: src/regenbogen/system/ports/logging_port.py
- Implementation: src/regenbogen/infrastructure/event_logger.py

Migrationsstatus: canonical
```

### 13.3 Logging-Port definieren

```python
# src/regenbogen/system/ports/logging_port.py
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping


class LogLevel(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True)
class LogEvent:
    """Systemisches Laufzeitereignis für Diagnose-Logging.

    Dieser Typ beschreibt nicht wie geloggt wird. Er beschreibt nur, welches
    Ereignis systemisch beobachtbar gemacht werden darf.
    """

    name: str
    level: LogLevel
    message: str
    fields: Mapping[str, object] = field(default_factory=dict)


class EventLogger(ABC):
    """Port für Laufzeit-Logging.

    system/core darf diesen Port verwenden. Die konkrete Ausgabe ist
    Infrastruktur.
    """

    @abstractmethod
    def log(self, event: LogEvent) -> None:
        ...


class NullEventLogger(EventLogger):
    """Logger für Tests oder stille Läufe."""

    def log(self, event: LogEvent) -> None:
        pass
```

Warum liegt das in `system/ports/`? Weil `system/core/` Ereignisse melden darf,
aber nicht wissen darf, ob diese Ereignisse auf Konsole, in eine Datei, in
journald oder in ein zentrales Logging-System geschrieben werden.

### 13.4 Infrastruktur-Implementierung mit Python logging

```python
# src/regenbogen/infrastructure/event_logger.py
import logging
from typing import Mapping

from regenbogen.system.ports.logging_port import EventLogger, LogEvent, LogLevel


_LEVELS = {
    LogLevel.INFO: logging.INFO,
    LogLevel.WARNING: logging.WARNING,
    LogLevel.ERROR: logging.ERROR,
}


def configure_logging(level: int = logging.INFO) -> None:
    """Konfiguriert das technische Logging für den Standardlauf.

    Das ist Infrastruktur. Keine Domain- oder Systementscheidung darf von der
    konkreten Formatierung abhängen.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


class StdlibEventLogger(EventLogger):
    """EventLogger-Implementierung auf Basis der Python-Standardbibliothek."""

    def __init__(self, logger_name: str = "regenbogen") -> None:
        self._logger = logging.getLogger(logger_name)

    def log(self, event: LogEvent) -> None:
        self._logger.log(
            _LEVELS[event.level],
            "%s | %s | %s",
            event.name,
            event.message,
            _format_fields(event.fields),
        )


def _format_fields(fields: Mapping[str, object]) -> str:
    if not fields:
        return "{}"
    teile = []
    for key in sorted(fields):
        value = fields[key]
        if isinstance(value, (str, int, float, bool)) or value is None:
            teile.append(f"{key}={value!r}")
        else:
            teile.append(f"{key}=<unsupported>")
    return "{" + ", ".join(teile) + "}"
```

Die Implementierung ist absichtlich schlicht. Sie zeigt die Grenze:

```text
system.ports  definiert Ereignisform
infrastructure formatiert und schreibt
```

Keine Fachentscheidung darf an `logging.INFO`, Handlern oder Formaten hängen.

### 13.5 Use Case instrumentieren

Der Use Case bekommt einen weiteren Port:

```text
logger: EventLogger | None = None
```

Das ist kein globaler Logger. Es ist eine explizit injizierte Abhängigkeit.
Wenn kein Logger übergeben wird, schaltet `NullEventLogger` die Ausgabe still
ab. Logging ändert keine Kontrollentscheidung: Retry, Terminalität und
Fehlerfluss bleiben Systemsemantik. Logging beobachtet nur.

Die folgende Datei **ersetzt vollständig die Version aus Session 11**:

```python
# src/regenbogen/system/core/wahrscheinlichkeit_use_case.py
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from regenbogen.domain.regenbogen import berechne_regenbogen_wahrscheinlichkeit
from regenbogen.domain.regenbogen_geometrie import (
    Sonnenstand,
    berechne_sonnenstands_faktor,
)
from regenbogen.domain.regenbogen_optik import (
    RegenbogenOptikFaktoren,
    berechne_regenbogen_sichtbarkeit,
)
from regenbogen.domain.wetter import Wetterzustand
from regenbogen.system.core.optische_bedingungen import leite_optische_bedingungen_ab
from regenbogen.system.core.sonnenstand import berechne_sonnenstand
from regenbogen.system.ports.logging_port import (
    EventLogger,
    LogEvent,
    LogLevel,
    NullEventLogger,
)
from regenbogen.system.ports.standort_port import StandortKoordinaten, StandortPort
from regenbogen.system.ports.wetterapi_port import (
    OrtNichtGefunden,
    WetterApiMessung,
    WetterApiNichtErreichbar,
    WetterApiPort,
)


@dataclass(frozen=True)
class WetterErgebnis:
    """Vollständiges Ergebnis für UI und CLI."""

    ort: str
    postleitzahl: str | None
    zustand: Wetterzustand
    sonnenstand: Sonnenstand
    wahrscheinlichkeit: int
    sichtbarkeit: int


class RegenbogenWahrscheinlichkeitUseCase:
    MAX_VERSUCHE = 3

    def __init__(
        self,
        api: WetterApiPort,
        standort: StandortPort,
        sleep: Callable[[float], None],
        clock: Callable[[], datetime],
        logger: EventLogger | None = None,
    ) -> None:
        self._api = api
        self._standort = standort
        self._sleep = sleep
        self._clock = clock
        self._logger = logger or NullEventLogger()

    def berechne(self, ort: str, postleitzahl: str | None = None) -> int:
        return self.berechne_vollstaendig(ort, postleitzahl).wahrscheinlichkeit

    def berechne_vollstaendig(
        self,
        ort: str,
        postleitzahl: str | None = None,
    ) -> WetterErgebnis:
        self._logger.log(
            LogEvent(
                name="regenbogen.berechnung.gestartet",
                level=LogLevel.INFO,
                message="Regenbogen-Berechnung gestartet",
                fields={"ort": ort, "plz_vorhanden": postleitzahl is not None},
            )
        )

        koordinaten = self._standort.finde_koordinaten(ort, postleitzahl)
        sonnenstand = berechne_sonnenstand(self._clock(), koordinaten)
        messung = self._hole_messung_mit_retry(koordinaten)
        zustand = self._messung_zu_wetterzustand(messung)
        wahrscheinlichkeit = berechne_regenbogen_wahrscheinlichkeit(
            zustand,
            sonnenstand,
        )
        sichtbarkeit = self._berechne_sichtbarkeit(messung, sonnenstand)

        self._logger.log(
            LogEvent(
                name="regenbogen.berechnung.abgeschlossen",
                level=LogLevel.INFO,
                message="Regenbogen-Berechnung abgeschlossen",
                fields={
                    "ort": ort,
                    "wahrscheinlichkeit": wahrscheinlichkeit,
                    "sichtbarkeit": sichtbarkeit,
                    "sonnenhoehe": round(sonnenstand.sonnenhoehe_grad, 2),
                },
            )
        )

        return WetterErgebnis(
            ort=ort,
            postleitzahl=postleitzahl,
            zustand=zustand,
            sonnenstand=sonnenstand,
            wahrscheinlichkeit=wahrscheinlichkeit,
            sichtbarkeit=sichtbarkeit,
        )

    def _hole_messung_mit_retry(
        self,
        koordinaten: StandortKoordinaten,
    ) -> WetterApiMessung:
        letzter_fehler: WetterApiNichtErreichbar | None = None

        for versuch in range(1, self.MAX_VERSUCHE + 1):
            try:
                return self._api.hole_aktuelle_messung(koordinaten)
            except WetterApiNichtErreichbar as exc:
                letzter_fehler = exc
                if versuch < self.MAX_VERSUCHE:
                    self._sleep(1.0)
            except OrtNichtGefunden:
                raise

        assert letzter_fehler is not None
        raise letzter_fehler

    def _messung_zu_wetterzustand(self, messung: WetterApiMessung) -> Wetterzustand:
        sonnenschein_intensitaet = min(messung.sonnenschein_sekunden / 3600.0, 1.0)
        regen_intensitaet = min(messung.niederschlag_mm / 10.0, 1.0)
        return Wetterzustand(
            sonnenschein=sonnenschein_intensitaet > 0.0,
            regen=regen_intensitaet > 0.0,
            sonnenschein_intensitaet=sonnenschein_intensitaet,
            regen_intensitaet=regen_intensitaet,
        )

    def _berechne_sichtbarkeit(
        self,
        messung: WetterApiMessung,
        sonnenstand: Sonnenstand,
    ) -> int:
        optik = leite_optische_bedingungen_ab(messung)
        wasser_mm = messung.rain_mm + messung.showers_mm
        if wasser_mm <= 0.0 and messung.niederschlag_mm > 0.0 and messung.snowfall_cm <= 0.0:
            wasser_mm = messung.niederschlag_mm
        regen_faktor = min(wasser_mm, 5.0) / 5.0
        return berechne_regenbogen_sichtbarkeit(
            RegenbogenOptikFaktoren(
                sonnenstands_faktor=berechne_sonnenstands_faktor(sonnenstand),
                regen_faktor=regen_faktor,
                direktlicht_faktor=optik.direktlicht_faktor,
                tropfen_qualitaet=optik.tropfen_qualitaet,
                sicht_faktor=optik.sicht_faktor,
                hintergrund_kontrast_faktor=optik.hintergrund_kontrast_faktor,
                niederschlags_phasen_faktor=optik.niederschlags_phasen_faktor,
            )
        )
```

### 13.6 Wiring erweitern

Die folgende Datei **ersetzt vollständig die Version aus Session 11**:

```python
# src/regenbogen/adapters/wiring.py
import time
from datetime import datetime
from zoneinfo import ZoneInfo

from regenbogen.infrastructure.event_logger import (
    StdlibEventLogger,
    configure_logging,
)
from regenbogen.infrastructure.open_meteo_client import OpenMeteoClient
from regenbogen.infrastructure.plz_lookup import DemoStandortLookup
from regenbogen.system.core.wahrscheinlichkeit_use_case import (
    RegenbogenWahrscheinlichkeitUseCase,
)


def create_regenbogen_use_case() -> RegenbogenWahrscheinlichkeitUseCase:
    """Verdrahtet alle Infrastruktur-Komponenten für den Produktivlauf."""
    configure_logging()
    return RegenbogenWahrscheinlichkeitUseCase(
        api=OpenMeteoClient(),
        standort=DemoStandortLookup(),
        sleep=time.sleep,
        clock=lambda: datetime.now(ZoneInfo("Europe/Berlin")),
        logger=StdlibEventLogger(),
    )
```

Damit bleibt die vollständige Produktivverdrahtung an einem Ort:

```text
OpenMeteoClient      infrastructure
DemoStandortLookup   infrastructure
StdlibEventLogger    infrastructure
time.sleep           technische Wartefunktion
datetime.now         technische Uhrzeitquelle
```

Der Use Case kennt nur Ports und Callables.

### 13.7 Tests

Der Test prüft nicht die Python-Logging-Ausgabe. Er prüft, dass der Use Case die
richtigen systemischen Ereignisse an den Port übergibt. Danach werden die
früheren Use-Case- und GUI-Format-Tests in finaler Form erneut gezeigt, weil
sich die Signaturen im Laufe der Iterationen geändert haben.

```python
# tests/system/test_logging.py
from datetime import datetime
from zoneinfo import ZoneInfo

from regenbogen.system.core.wahrscheinlichkeit_use_case import (
    RegenbogenWahrscheinlichkeitUseCase,
)
from regenbogen.system.ports.logging_port import EventLogger, LogEvent
from regenbogen.system.ports.standort_port import StandortKoordinaten, StandortPort
from regenbogen.system.ports.wetterapi_port import WetterApiMessung, WetterApiPort


class RecordingLogger(EventLogger):
    def __init__(self) -> None:
        self.events: list[LogEvent] = []

    def log(self, event: LogEvent) -> None:
        self.events.append(event)


class FakeStandort(StandortPort):
    def finde_koordinaten(
        self, ort: str, postleitzahl: str | None = None
    ) -> StandortKoordinaten:
        return StandortKoordinaten(
            latitude=52.52,
            longitude=13.41,
            zeitzone="Europe/Berlin",
        )


class FakeWetterApi(WetterApiPort):
    def hole_aktuelle_messung(self, koordinaten: StandortKoordinaten) -> WetterApiMessung:
        return WetterApiMessung(
            sonnenschein_sekunden=1800.0,
            niederschlag_mm=2.0,
            rain_mm=2.0,
            showers_mm=0.0,
            snowfall_cm=0.0,
            weather_code=61,
            cloud_cover=60.0,
            visibility_m=10000.0,
            direct_radiation=300.0,
            temperature_2m=12.0,
        )


def test_use_case_schreibt_systemische_log_events():
    logger = RecordingLogger()
    uc = RegenbogenWahrscheinlichkeitUseCase(
        api=FakeWetterApi(),
        standort=FakeStandort(),
        sleep=lambda _: None,
        clock=lambda: datetime(2026, 6, 14, 18, 0, tzinfo=ZoneInfo("Europe/Berlin")),
        logger=logger,
    )

    uc.berechne_vollstaendig("Berlin", "10115")

    namen = [event.name for event in logger.events]
    assert "regenbogen.berechnung.gestartet" in namen
    assert "regenbogen.berechnung.abgeschlossen" in namen
```


Für die finale Projektion ersetzt diese Logging-Session außerdem die früheren
Testdateien, deren Signaturen sich durch Standort, Uhrzeit, Sichtbarkeit und
Logging geändert haben:

```python
# tests/system/test_use_case.py
from datetime import datetime
from zoneinfo import ZoneInfo
from unittest.mock import MagicMock

import pytest

from regenbogen.system.core.wahrscheinlichkeit_use_case import (
    RegenbogenWahrscheinlichkeitUseCase,
)
from regenbogen.system.ports.standort_port import StandortKoordinaten
from regenbogen.system.ports.wetterapi_port import (
    OrtNichtGefunden,
    WetterApiMessung,
    WetterApiNichtErreichbar,
    WetterApiPort,
)


class FakeStandort:
    def finde_koordinaten(self, ort: str, postleitzahl: str | None):
        return StandortKoordinaten(52.532, 13.384, "Europe/Berlin")


def make_uc(api):
    return RegenbogenWahrscheinlichkeitUseCase(
        api=api,
        standort=FakeStandort(),
        sleep=lambda _: None,
        clock=lambda: datetime(2026, 6, 13, 19, 0, tzinfo=ZoneInfo("Europe/Berlin")),
    )


def gute_messung() -> WetterApiMessung:
    return WetterApiMessung(
        sonnenschein_sekunden=1800.0,
        niederschlag_mm=5.0,
        rain_mm=5.0,
        showers_mm=0.0,
        snowfall_cm=0.0,
        weather_code=61,
        cloud_cover=60.0,
        visibility_m=10_000.0,
        direct_radiation=400.0,
        temperature_2m=12.0,
    )


def test_gibt_wahrscheinlichkeit_zurueck():
    api = MagicMock(spec=WetterApiPort)
    api.hole_aktuelle_messung.return_value = gute_messung()
    uc = make_uc(api)
    assert uc.berechne("Berlin") > 0


def test_retry_bei_api_nicht_erreichbar():
    api = MagicMock(spec=WetterApiPort)
    api.hole_aktuelle_messung.side_effect = [
        WetterApiNichtErreichbar("timeout"),
        WetterApiNichtErreichbar("timeout"),
        gute_messung(),
    ]
    uc = make_uc(api)
    assert uc.berechne("Berlin") > 0
    assert api.hole_aktuelle_messung.call_count == 3


def test_kein_retry_bei_ort_nicht_gefunden():
    api = MagicMock(spec=WetterApiPort)
    api.hole_aktuelle_messung.side_effect = OrtNichtGefunden("Atlantis")
    uc = make_uc(api)
    with pytest.raises(OrtNichtGefunden):
        uc.berechne("Atlantis")
    assert api.hole_aktuelle_messung.call_count == 1


def test_fehler_nach_max_versuchen():
    api = MagicMock(spec=WetterApiPort)
    api.hole_aktuelle_messung.side_effect = WetterApiNichtErreichbar("down")
    uc = make_uc(api)
    with pytest.raises(WetterApiNichtErreichbar):
        uc.berechne("Berlin")
    assert api.hole_aktuelle_messung.call_count == 3


def test_berechne_vollstaendig_gibt_zustand_und_wahrscheinlichkeit():
    api = MagicMock(spec=WetterApiPort)
    api.hole_aktuelle_messung.return_value = gute_messung()
    uc = make_uc(api)
    ergebnis = uc.berechne_vollstaendig("Berlin", "10115")
    assert ergebnis.ort == "Berlin"
    assert ergebnis.postleitzahl == "10115"
    assert ergebnis.zustand.sonnenschein is True
    assert ergebnis.wahrscheinlichkeit > 0
    assert ergebnis.sichtbarkeit > 0
```

```python
# tests/cli/test_gui_format.py
from regenbogen.cli.gui_format import formatiere_wetter
from regenbogen.domain.regenbogen_geometrie import Sonnenstand
from regenbogen.domain.wetter import Wetterzustand
from regenbogen.system.core.wahrscheinlichkeit_use_case import WetterErgebnis


def ergebnis(zustand: Wetterzustand, wahrscheinlichkeit: int) -> WetterErgebnis:
    return WetterErgebnis(
        ort="Berlin",
        postleitzahl="10115",
        zustand=zustand,
        sonnenstand=Sonnenstand(sonnenhoehe_grad=20.0, sonnenazimut_grad=250.0),
        wahrscheinlichkeit=wahrscheinlichkeit,
        sichtbarkeit=wahrscheinlichkeit,
    )


def test_formatiert_beide_faktoren():
    ausgabe = formatiere_wetter(
        ergebnis(
            Wetterzustand(
                sonnenschein=True,
                regen=True,
                sonnenschein_intensitaet=0.5,
                regen_intensitaet=0.5,
            ),
            50,
        )
    )
    assert "Sonnenschein" in ausgabe
    assert "Regen" in ausgabe
    assert "50 %" in ausgabe


def test_formatiert_kein_regen():
    ausgabe = formatiere_wetter(
        ergebnis(
            Wetterzustand(
                sonnenschein=True,
                regen=False,
                sonnenschein_intensitaet=0.8,
            ),
            0,
        )
    )
    assert "Sonnenschein" in ausgabe
    assert "0 %" in ausgabe


def test_formatiert_bedeckt():
    ausgabe = formatiere_wetter(
        ergebnis(Wetterzustand(sonnenschein=False, regen=False), 0)
    )
    assert "Bedeckt" in ausgabe
```

Import-Checker:

```bash
python tools/check_import_layers.py --preflight src tests tools
```

Erwartete neue Kanten:

```text
system.core -> system.ports.logging_port      erlaubt
infrastructure.event_logger -> system.ports  erlaubt
adapters.wiring -> infrastructure.event_logger erlaubt
```

### 13.8 Erfahrungsbericht

```markdown
# Erfahrungsbericht: Logging-Session Regenbogen

Datum:        2026-06-15
Session-Typ:  abgeschlossen
Aufgabe:      Logging als Infrastruktur ergänzen
Ergebnis:     EventLogger-Port, StdlibEventLogger und Use-Case-Logging ergänzt

Learning-Matrix-Kandidat: ja
Muster-ID: Logging-als-Infrastruktur

## Was sich bewährt hat

Die Trennung zwischen EventLogger-Port und StdlibEventLogger verhindert, dass
system/core/ direkt von Python logging abhängt. Logging bleibt technische
Beobachtung, nicht Evidence und nicht Fachsemantik.

## Modellgrenze

Die Logausgabe ist nicht normativ. Sie darf für Diagnose und Betrieb genutzt
werden, aber nicht als Ersatz für Sprechakte, Erfahrungsberichte oder
Evidence-Artefakte.
```

Ort: `tmp/erfahrungsberichte/2026-06-15-EB-logging.md`.

## 14. Vollständige Abschlusskontrolle

```bash
python tools/check_agent_docs_consistency.py --instantiated
python tools/check_import_layers.py --preflight src tests tools
python tools/resolve_test_obligations.py --selfcheck --instantiated
python -m ruff check .
python -m mypy src
python -m pytest
```

Erwartetes Ergebnis: alle Code- und Import-Checks grün.

Erwartete WARNs müssen konkret begründet sein. Im Tutorial sind nur solche
WARNs akzeptabel, die keine operative Drift verdecken:

```text
Erwartet:
- AGENT-SETUP.md ist noch vorhanden, solange die Einrichtung nicht archiviert ist.
- Ein Glossar ist am Anfang leer, solange der betroffene Begriff noch nicht aktiv
  im Semantic Working Set gebraucht wird.
- Ein projektspezifischer Hinweis ist als WARN markiert, solange die zuständige
  Entscheidung noch nicht in den Arbeitsbereich fällt.

Nicht erwartet:
- nicht ersetzte Platzhalter nach SP0
- fehlende Pflichtdateien der Box
- fehlender Instanziierungsnachweis
- Importverletzungen
- aktive Glossarbegriffe ohne Eintrag
- rote Tests, Lint- oder Typecheck-Fehler
```

WARNs sind Arbeitsmarkierungen. Sie sind keine grünen Freigaben. Ein WARN ist
nur dann akzeptabel, wenn seine Ursache bekannt, dokumentiert und außerhalb des
aktuellen Task-Schnitts liegt.

Die entstandene Projektstruktur:

```text
src/regenbogen/
  domain/
    wetter.py                           ← Wetterzustand, Invarianten
    regenbogen.py                       ← Berechnungslogik
    regenbogen_geometrie.py             ← Sonnenstand und Geometriefaktor
  system/
    ports/
      wetterapi_port.py                 ← Port, WetterApiMessung-DTO, Fehlerklassen
      standort_port.py                  ← StandortKoordinaten, StandortPort
      logging_port.py                   ← LogEvent, EventLogger-Port
    core/
      wahrscheinlichkeit_use_case.py    ← Mapping, Retry, WetterErgebnis
      sonnenstand.py                    ← Uhrzeit+Koordinaten -> Sonnenstand
  infrastructure/
    open_meteo_client.py                ← API-Implementierung, liefert nur DTO
    plz_lookup.py                       ← PLZ/Ort -> StandortKoordinaten
    event_logger.py                     ← StdlibEventLogger, technische Logausgabe
  adapters/
    wiring.py                           ← Verdrahtung: Clients, Lookup, sleep, clock
  cli/
    main.py                             ← CLI-Einstiegspunkt
    gui_main.py                         ← GUI-Hauptprogramm
    config_dialog.py                    ← KonfigurationsDialog, OrtKonfiguration
    ausgabe_fenster.py                  ← AusgabeFenster
    gui_format.py                       ← Formatierung ohne Tkinter, testbar

tests/
  domain/
    test_regenbogen.py
    test_regenbogen_geometrie.py
  system/
    test_use_case.py
    test_winkelmodell.py
    test_logging.py
  cli/
    test_gui_format.py

docs/sprechakte/
  2026-06-10-wetterzustand-begriffe.md  ← SP7, festgelegt
  2026-06-11-httpx-dependency.md        ← SP4, festgelegt
  2026-06-11-fehlerklassen-wetterapi.md ← SP3, festgelegt
  2026-06-12-raumzuordnung-gui.md       ← SP2, festgelegt
  2026-06-12-tkinter-dependency.md      ← SP4, festgelegt
  2026-06-13-regenbogen-geometrie.md    ← SP7, festgelegt
  2026-06-13-plz-standort.md            ← SP2/SP3, festgelegt

tmp/erfahrungsberichte/
  2026-06-10-EB-domain-kern.md
  2026-06-11-EB-port-infra.md
  2026-06-12-EB-gui-session.md
  2026-06-13-EB-sonnenstand-winkelmodell.md
  2026-06-14-EB-tropfenqualitaet.md
  2026-06-15-EB-logging.md

glossar-domain.md    ← Wetterzustand, RegenbogenWahrscheinlichkeit, Sonnenstand
glossar-system.md    ← WetterApiNichtErreichbar, OrtNichtGefunden,
                       WetterErgebnis, StandortKoordinaten,
                       LogEvent, EventLogger + Metabegriffe
```

---

### 14.1 Sprechakte und Folgeartefakte

Die Sprechakte sind nicht nur Protokoll. Jeder festgelegte Sprechakt muss in
operative Artefakte zurückfließen. Im Beispiel sieht der Rückfluss so aus:

| Sprechakt | Entscheidung | Folgeartefakte |
|---|---|---|
| SP0 Instanziierung | Box gilt lokal für Regenbogen | `.agent-box/instantiation.md`, ersetzte Platzhalter |
| SP7 Wetterbegriffe | Kernbegriffe festgelegt | `glossar-domain.md`, Domain-Code, Domain-Tests |
| SP4 httpx | HTTP-Client erlaubt | Dependency-Datei, optional `INSTALLATION.md` |
| SP3 Fehlerklassen | Retry/Terminal-Bedeutung festgelegt | `glossar-system.md`, `system/ports/`, Systemtests |
| SP2 GUI-Raum | GUI bleibt unter `cli/` | `package-schema.md`, GUI-Dateien unter `cli/` |
| SP4 tkinter | Tkinter nur in `cli/` erlaubt | `package-schema.md`, `INSTALLATION.md` |
| SP7 Regenbogen-Geometrie | Sonnenstand und 42°-Regel festgelegt | `glossar-domain.md`, `domain/regenbogen_geometrie.py`, Domain-Tests |
| SP2/SP3 PLZ-Standort | PLZ wird systemische Standort-Eingabe; unbekannte PLZ terminal | `glossar-system.md`, `system/ports/standort_port.py`, `infrastructure/plz_lookup.py` |
| Logging-Erweiterung | Logging ist Infrastruktur; System spricht nur über Port | `glossar-system.md`, `system/ports/logging_port.py`, `infrastructure/event_logger.py`, `adapters/wiring.py` |

Diese Tabelle zeigt die eigentliche Arbeitsregel: Eine Entscheidung ist erst
dann vollständig, wenn sie in die zuständigen Artefakte zurückgeflossen ist.
Ein Sprechakt ohne Folgeprojektion ist nur ein Gesprächsprotokoll, keine lokale
operative Wahrheit.

### 14.2 Finale Importregeln im Beispiel

Die wichtigsten Importkanten des fertigen Regenbogen-Projekts:

| Von | Nach | Status | Warum |
|---|---|---|---|
| `domain` | `system`, `infrastructure`, `cli` | verboten | Fachdomäne bleibt autonom. |
| `system.core` | `domain` | erlaubt | Systemlogik nutzt Fachmodell und berechnet Use Cases. |
| `system.core` | `system.ports` | erlaubt | Use Case spricht über Port-Verträge, Koordinaten, DTOs und Fehlerklassen. |
| `infrastructure` | `system.ports` | erlaubt | Infrastruktur implementiert Ports und erzeugt DTOs. |
| `infrastructure.plz_lookup` | `system.ports.standort_port` | erlaubt | PLZ-Lookup liefert StandortKoordinaten. |
| `infrastructure` | `domain` | verboten | Infrastruktur darf keine Fachinterpretation erzeugen. |
| `cli` | `adapters` | erlaubt | Einstiegspunkt erhält verdrahteten Use Case. |
| `cli` | `system.ports` | erlaubt | Einstiegspunkt darf definierte Fehler behandeln. |
| `cli` | `system.core` | erlaubt | Einstiegspunkt darf Ergebnisobjekte anzeigen/formatieren. |
| `cli` | `infrastructure` | `decision` / nicht automatisch erlaubt | Direkte Verdrahtung gehört nach `adapters/`. |
| `adapters` | `infrastructure` | erlaubt | Binding verdrahtet konkrete Implementierungen. |
| `adapters` | `system.core` | erlaubt | Binding erstellt Use Cases. |
| `adapters` | `datetime`, `time` | erlaubt | Produktive Clock- und Sleep-Verdrahtung. |
| `system.core` | `system.ports.logging_port` | erlaubt | Use Case meldet systemische Ereignisse über Port. |
| `infrastructure.event_logger` | `system.ports.logging_port` | erlaubt | Infrastruktur implementiert Logging-Port. |
| `domain` | `logging` | verboten | Fachdomäne darf keine Laufzeitbeobachtung kennen. |
| `system.core` | `logging` | verboten | Systemlogik darf nicht von technischer Ausgabe abhängen. |
| `cli` | `tkinter` | erlaubt durch SP4 | Nur Einstiegspunkt-/GUI-Technik, keine Produktsemantik. |
| `domain`, `system`, `infrastructure`, `adapters` | `tkinter` | verboten | GUI-Technik darf nicht in Produktlogik wandern. |

Diese Tabelle ist der Kern des Beispiels. Die Architektur entsteht nicht aus
Geschmack, sondern aus kontrollierten Kanten. Jede erlaubte Kante hat eine
Begründung. Jede nicht automatisch erlaubte Kante braucht eine Entscheidung.

---

## 15. Was das System konkret verhindert hat

Im Regenbogen-Beispiel hat das System folgende stille Fehler verhindert:

**Ohne das System:**

- "Können Sonnenschein und Regen gleichzeitig auftreten?" wäre im Code
  entschieden worden, unsichtbar und ohne Dokumentation.
- `OrtNichtGefunden` hätte vielleicht in `domain/` gelegen, weil der Name
  fachlich klingt. Tatsächlich ist es ein systemsemantischer Steuerwert.
- `infrastructure/` hätte direkt `domain.Wetterzustand` erzeugt. Damit würde
  die Implementierungsdomäne entscheiden, was "Sonnenschein im fachlichen
  Sinn" bedeutet — eine stille Autonomieverletzung.
- Die Retry-Policy für `WetterApiNichtErreichbar` wäre vielleicht in
  `infrastructure/` implementiert worden statt in `system/core/`.
- `cli/` oder `gui/` hätte direkt `OpenMeteoClient` importiert und damit die
  Wiring-Entscheidung in den Einstiegspunkt geschoben.
- Ein Agent hätte still einen neuen Raum `gui/` angelegt, ohne
  `package-schema.md` und Checker-Regeln anzupassen.
- `tkinter` wäre still als Runtime-Annahme eingeführt worden.
- Die Postleitzahl aus dem Dialog wäre leicht zu einer scheinbaren
  Fachinformation geworden. Zuerst bleibt sie bewusst Anzeige- und
  Eingabekomfort in `cli/`; erst die Winkelmodell-Session gibt ihr per
  Sprechakt eine systemische Rolle als Standort-Eingabe.
- PLZ-zu-Koordinaten hätte in der Wetter-API-Implementierung landen können.
  Im korrigierten Modell liegt diese Verantwortung in einem eigenen
  StandortPort.
- Der Sonnenstand hätte direkt in `domain/` aus `datetime.now()` berechnet
  werden können. Im korrigierten Modell bleibt domain/ rein fachlich und
  system/core/ projiziert Uhrzeit+Koordinaten auf den fachlichen Sonnenstand.
- `time.sleep` wäre direkt im Use Case gestanden — Tests hätten echte
  Wartezeiten gehabt oder `monkeypatch` erfordert.
- Logging wäre als globaler technischer Logger direkt in `system/core/` oder
  sogar `domain/` gewandert. Im korrigierten Modell meldet system/core nur
  `LogEvent`s über einen Port; die technische Ausgabe liegt in infrastructure/.

**Mit dem System:**

- Jede Bedeutungsentscheidung ist sichtbar und nachvollziehbar.
- Sprechakt-Artefakte dokumentieren, warum etwas so ist, wie es ist.
- Der Import-Checker macht Grenzverletzungen sofort sichtbar.
- `WetterApiMessung` als DTO begrenzt explizit die Kante von `infrastructure`
  nach `system` — die Grenze ist im Code lesbar, nicht nur in der Doku.
- `adapters/wiring.py` macht Verdrahtung explizit. `time.sleep` erscheint
  genau einmal, im Adapter.
- GUI bleibt Einstiegspunkt ohne Produktsemantik.
- `gui_format.py` trennt testbaren von nicht-testbarem GUI-Code.
- Das Winkelmodell verbessert die frühere Placeholder-Formel, ohne zu
  behaupten, echte Regenbogen-Sichtbarkeit vollständig nachzuweisen.
- Ein neuer Entwickler oder Agent findet in `docs/sprechakte/` die Geschichte
  der Entscheidungen und kann nachvollziehen, warum `OrtNichtGefunden` terminal
  ist, warum `tkinter` nur in `cli/` vorkommt und warum es keinen `gui/`-Raum
  gibt.

### 15.1 Warum dieses Beispiel funktioniert

Das Regenbogen-Beispiel funktioniert, weil es klein beginnt und trotzdem echte
Modellarbeit erzwingt. Die erste Regel ist trivial:

```text
Sonne + Regen -> Regenbogenwahrscheinlichkeit
```

Jede weitere Iteration fügt aber nicht einfach ein Feature hinzu, sondern macht
eine neue Bedeutungsgrenze sichtbar:

```text
Fachbegriff -> API -> Port -> Retry -> GUI -> Standort -> Sonnenstand
-> Tropfenqualität -> Logging -> kontrollierter Abbruchpfad
```

Dadurch bleibt das Beispiel überschaubar, wird aber nicht künstlich. Der Leser
sieht, wie ein Agentenprojekt wächst, ohne dass Begriffe, Räume, Tests,
Dependencies und Infrastruktur ineinanderlaufen. Der didaktische Kern ist nicht
Regenbogen-Meteorologie, sondern kontrollierte Bedeutungsarbeit über mehrere
Iterationen.

---

## 16. Dokument-Autoritäten

```text
Was darf der Agent ändern?                    → AGENTS.md §9
Wann muss der Agent abbrechen?                → AGENTS.md §10
Welchem Raum gehört eine Datei an?            → package-schema.md
Welche Imports sind erlaubt?                  → package-schema.md + check_import_layers.py
Was bedeutet dieser Fachbegriff?              → glossar-domain.md
Was bedeutet dieser Betriebsbegriff?          → glossar-system.md
Welches Glossar wann laden?                   → glossar-README.md
Wann ist ein Sprechakt nötig?                 → AGENTS.md §7 + sprechakt-protokoll.md
Wann Task-Schnitt prüfen?                     → task-schnitt.md
Welche Tests nach einer Änderung?             → test-obligations.md
Darf dieses Symbol angefasst werden?          → migration-bridges.md
Wie wird Preflight ausgeführt?                → preflight-checkliste.md
Warum ist das System so aufgebaut?            → grundsatz.md
Welches Dokument hat bei Widerspruch Vorrang? → regelmatrix.md
```

---

## 17. Was dieses System nicht ist

```text
✗  kein vollständiger Projektgenerator
✗  kein Packaging-Standard
✗  keine konkrete Architekturvorschrift für alle Projekte
✗  kein Ersatz für Projektentscheidungen
✗  kein automatisches Pflegesystem für laufende Projekte
```

Die Box setzt einen operativen Rahmen auf. Was das Projekt danach macht, ist
Projektarbeit — innerhalb dieses Rahmens, aber außerhalb der Box.

---

## 18. Kurzregel

```text
Eine Box ist vollständig.
Eine Box wird einmal kopiert.
Nach dem Kopieren lebt sie im Projektroot.
Ab dann ist sie lokale Wahrheit.
```
---

## 19. Glossar

Dieses Glossar erklärt die Begriffe, die im Tutorial selbst verwendet werden.
Es ersetzt nicht die Projektdateien `glossar-domain.md` und
`glossar-system.md`. Diese bleiben die operative Wahrheit des instanziierten
Projekts. Das Tutorial-Glossar dient dem Menschen als Lesestütze.

### Abbruch

Kontrollierter Stopp eines Agentenlaufs. Ein Abbruch ist kein Scheitern,
sondern ein Schutzmechanismus. HARD-Abbrüche stoppen vollständig bis zur
menschlichen Freigabe; SOFT-Abbrüche stoppen mit Evidence und erlauben einen
gezielten Wiedereinstieg.

### adapters/

Semantischer Raum für Binding und Verdrahtung. `adapters/` darf mehrere Räume
kennen, aber nur, um bestehende Komponenten zu verbinden oder zwischen
bestehenden Formen zu übersetzen. `adapters/` darf keine neue Fach-, System-
oder Retry-Semantik erzeugen.

### AGENTS-COMPACT.md

Kurze operative Einstiegsregel für Agenten. Wird vor jeder nichttrivialen
Session gelesen. Sie ersetzt `AGENTS.md` nicht, sondern verweist auf die
vollständigen Regeln.

### AGENTS.md

Operative Hauptautorität für Agentenarbeit im Projektroot. Enthält unter
anderem Schreibrechte, Abbruchbedingungen, Preflight-Regeln und Schutzregeln
für projektsteuernde Artefakte.

### Autonomieregel

Invariante für semantische Räume: Ein Raum ist gültig, wenn ein zuständiger
Experte ihn vollständig beurteilen kann, ohne die anderen Räume zu kennen.
Beispiel: `domain/` darf nicht von HTTP, Retry oder Tkinter abhängen.

### Binding

Kontrollierte Verbindung zwischen semantischen Räumen. Binding übersetzt oder
verdrahtet, erzeugt aber keine neue Semantik. Im Beispiel ist
`adapters/wiring.py` Binding.

### Box

Vorlage für einen lokalen Agenten-Arbeitsrahmen. Die Box wird einmal in ein
Projekt kopiert und danach instanziiert. Ab dann ist das Projektroot die lokale
Wahrheit.

### CLI

Command-Line Interface. Im Beispiel ein Einstiegspunkt unter `cli/`. CLI-Code
parst Eingaben, ruft Systemlogik auf und stellt Ergebnisse dar. Er enthält
keine Domänenlogik.

### decision

Matrixwert für eine Kante, die nicht automatisch erlaubt ist. `decision`
bedeutet nicht "frei verwendbar", sondern: nur nach expliziter
Projektentscheidung, Sprechakt oder dokumentiertem Known Breach.

### Dependency-Dokumentation

Projektspezifische Dokumentation darüber, welche Runtime-Abhängigkeiten oder
Plattformfähigkeiten benötigt werden. Die Box schreibt kein Packaging-Werkzeug
vor; ein Projekt kann `pyproject.toml`, `requirements.txt`, eine
Installationsdatei oder eine andere Markdown-Dokumentation verwenden.

### domain/

Semantischer Raum für Fachdomänenbegriffe und fachliche Regeln. Im Beispiel
liegen dort `Wetterzustand` und die Berechnung der
`RegenbogenWahrscheinlichkeit`. `domain/` kennt keine Infrastruktur, keine GUI
und keine Retry-Mechanik.

### DTO

Data Transfer Object. Im Tutorial ist `WetterApiMessung` ein DTO an der
Portfläche. Es trägt technische Messwerte der API, aber keine fachliche
Interpretation.

### Evidence

Nachweisartefakt eines Arbeitslaufs, einer Entscheidung oder eines Abbruchs.
Evidence ist im Box-Modell Markdown-basiert und soll für Menschen lesbar und
prüfbar sein.

### Erfahrungsbericht

Markdown-Artefakt nach einer nichttrivialen Session oder nach einem Abbruch.
Es hält fest, was passiert ist, was sich bewährt hat und ob ein Muster in die
Learning-Matrix zurückfließen soll.

### Folgeartefakt

Artefakt, das nach einer Entscheidung aktualisiert werden muss. Beispiel:
SP3 zu Fehlerklassen führt zu Einträgen in `glossar-system.md`; SP2 zur
GUI-Raumzuordnung führt zu einer Ergänzung in `package-schema.md`.

### GUI

Grafische Oberfläche. Im Beispiel wird GUI-Code unter `cli/` eingeordnet,
weil sie ein Einstiegspunkt ist und keine eigene Produktsemantik erzeugt. Ein
eigener `gui/`-Raum wäre eine spätere SP2-Entscheidung.

### HARD-Abbruch

Stoppzustand, der nur nach expliziter menschlicher Freigabe fortgesetzt werden
darf. Beispiele: unklassifizierte Importverletzung, geschützte Datei ohne
Freigabe, neue Bedeutung ohne Sprechakt.

### Import-Checker

Tool `tools/check_import_layers.py`. Prüft strukturell, ob Imports zwischen
semantischen Räumen gegen die Regeln aus `package-schema.md` verstoßen. Grün
bedeutet: keine erkannte Importverletzung. Grün bedeutet nicht: semantisch
korrekt.

### infrastructure/

Semantischer Raum für konkrete technische Implementierung: HTTP, Datenbank,
Dateisystem, externe APIs, Zeit, Zufall. Im Beispiel erzeugt
`infrastructure/` nur `WetterApiMessung` und importiert nicht `domain/`.

### Instanziierung

Einmaliger Übergang von der Box-Vorlage zum konkreten Projekt. Im Tutorial ist
das SP0. Das Tool ersetzt Platzhalter, legt Verzeichnisse an und schreibt den
Nachweis `.agent-box/instantiation.md`.

### Known Breach

Dokumentierter, begrenzter und begründeter Regelbruch. Ein Known Breach ist
keine freie Ausnahme, sondern eine konkrete Kante mit Status, Begründung und
möglichem Migrationspfad.

### Learning-Matrix

Aggregierter Rückfluss aus Erfahrungsberichten. Ein Muster wird dort
aufgenommen, wenn es wiederkehrt, einen HARD-Abbruch verursacht hat oder vom
Menschen als systemisch markiert wird.

### Markdown-only

Grundsatz, dass projektsteuernde Artefakte als Markdown geführt werden:
Regeln, Sprechakte, Evidence, Pläne, Glossare und Erfahrungsberichte. Ziel ist
menschliche Lesbarkeit und Reviewbarkeit. Technische Test- oder
Build-Artefakte können andere Formate haben.

### OrtKonfiguration

GUI-Eingabeobjekt im Tutorial. Es ist kein Fachbegriff und kein
Systemsteuerwert, solange die PLZ nur Anzeige-/Eingabekomfort ist. Sobald die
PLZ für Ortsauflösung, Standortlogik oder API-Auswahl verwendet wird, entsteht
eine neue Entscheidung.

### package-schema.md

Projektdatei für semantische Räume, Importregeln und Known Breaches. Sie ist
die Raumkarte des Projekts und Grundlage für den Import-Checker.

### PLZ

Postleitzahl. Im Tutorial bleibt sie bewusst im UI-Raum, weil sie nicht für die
Wetterabfrage verwendet wird. Als Ortsauflösung wäre sie systemsemantisch; als
fachlicher Standortbegriff könnte sie domain-relevant werden.

### Portfläche

Schmale erlaubte Importfläche zwischen Räumen. Im Beispiel ist
`system/ports/` die Fläche, die `infrastructure/` sehen darf. Sie enthält
Port-Verträge, DTOs und Fehlerklassen, aber keine Use-Case-Logik.

### Preflight

Vorprüfung vor jeder nichttrivialen Änderung. Preflight bestimmt betroffene
Räume, lädt relevante Begriffe, prüft Importregeln, leitet Testpflichten ab,
prüft Schreibrechte und entscheidet, ob fortgesetzt, geteilt oder abgebrochen
wird.

### Projektroot

Wurzelverzeichnis des instanziierten Projekts. Nach der Instanziierung ist das
Projektroot die operative Wahrheit für Mensch und Agent.

### RegenbogenWahrscheinlichkeit

Domain-Begriff im Beispiel. Prozentwert in `[0, 100]`. Ohne Sonnenschein oder
ohne Regen ist der Wert `0`; wenn beides vorhanden ist, ist er größer `0`.

### Runtime-Dependency

Laufzeitabhängigkeit des Projekts. `httpx` ist eine Runtime-Dependency als
PyPI-Paket. `tkinter` wird im Tutorial präziser als Runtime-/Plattformfähigkeit
behandelt, weil es zur Standardbibliothek gehört, aber auf manchen Systemen ein
separates OS-Paket benötigt.

### Semantischer Raum

Adressraum für Bedeutung im Projekt. Ein semantischer Raum legt fest, welche
Begriffe, Abhängigkeiten, Imports und Entscheidungen dort erlaubt sind.

### SOFT-Abbruch

Stoppzustand mit Evidence und möglichem Wiedereinstieg. Beispiele: rote Tests,
Lint-Fehler, Typecheck-Fehler oder technische Installationsprobleme ohne
semantischen Widerspruch.

### SP0 bis SP7

Sprechaktklassen. SP0 ist die Instanziierung. SP1 bis SP7 betreffen neue
Fachbegriffe, Systemwerte, Fehlerbedeutungen, Dependencies, Binding-Semantik,
Known Breaches und fehlende Glossarbegriffe.

### Sprechakt

Menschliche Festlegung an einer Bedeutungsgrenze. Der Agent darf analysieren
und eine Entscheidungsvorlage liefern, aber nicht selbst entscheiden.

### Sprechakt-Artefakt

Markdown-Datei unter `docs/sprechakte/`, die eine menschliche Festlegung oder
eine noch offene Entscheidung dokumentiert. Status: `offen`, `festgelegt`,
`abgelehnt` oder `superseded`.

### system/core/

Teil von `system/`, in dem Use Cases, Policies, Mapping und Lifecycle-Logik
liegen. Im Beispiel übersetzt `system/core/` die technische `WetterApiMessung`
in einen fachlichen `Wetterzustand` und wendet Retry-Policy an.

### system/ports/

Schmale Port-Fläche für Verträge, DTOs und Fehlerklassen, die von
`infrastructure/` gesehen werden dürfen. Keine Use-Case-Logik.

### Task-Schnitt

Prüfung, ob eine Aufgabe zu groß oder semantisch unscharf ist. Wenn mehrere
Räume, Glossarbereiche oder Binding-Grenzen betroffen sind, muss der Agent
prüfen, ob die Aufgabe geteilt werden kann.

### Testpflicht

Minimalmenge an Checks und Tests, die aus geänderten Dateien abgeleitet wird.
Das Tool `resolve_test_obligations.py` unterstützt diese Ableitung.

### tkinter

GUI-Bibliothek der Python-Standardbibliothek. Im Tutorial wird sie per SP4 als
optionale Runtime-/Plattformfähigkeit erlaubt, aber nur im Raum `cli/`.

### WetterApiMessung

DTO aus `system/ports/`. Repräsentiert rohe Messwerte der Wetter-API. Keine
Domain-Bedeutung, kein `Wetterzustand`.

### WetterErgebnis

Systemsemantisches Ergebnisobjekt für Einstiegspunkte. Enthält Ort,
fachlichen Wetterzustand und berechnete Regenbogen-Wahrscheinlichkeit.
Einstiegspunkte dürfen es anzeigen, aber nicht neu berechnen.

### Wetterzustand

Domain-Begriff. Beobachtete Kombination von Wetterphänomenen zu einem
Zeitpunkt an einem Ort. Sonnenschein und Regen gleichzeitig sind ein gültiger
Zustand, kein Fehlerfall.

---


### Gegensonnenpunkt

Punkt am Himmel genau gegenüber der Sonne. Der primäre Regenbogen liegt
näherungsweise auf einem Kreis um diesen Punkt. Im Tutorial bleibt dieser
Begriff fachliche Hintergrundinformation; berechnet wird zunächst nur der
SonnenstandsFaktor.

### PostleitzahlUnbekannt

Systemsemantischer Fehler: Die eingegebene Postleitzahl kann nicht in
Koordinaten übersetzt werden. Terminaler Fehler, kein Retry.

### Regenbogenwinkel

Näherungsweise Winkel des primären Regenbogens um den Gegensonnenpunkt.
Im Tutorial wird 42° als fachliche Schwelle für die Sichtbarkeit des
Hauptbogens verwendet.

### Sonnenazimut

Himmelsrichtung der Sonne relativ zum Beobachter. Zusammen mit der
Sonnenhoehe bildet er den Sonnenstand.

### Sonnenhoehe

Winkel der Sonne über dem Horizont. Für einen primären Regenbogen am Boden ist
insbesondere relevant, ob die Sonnenhoehe unter etwa 42° liegt.

### Sonnenstand

Position der Sonne relativ zum Beobachter, beschrieben durch Sonnenhoehe und
Sonnenazimut. Im Tutorial wird er aus Uhrzeit und StandortKoordinaten berechnet
und dann als fachliche Eingabe an die Regenbogen-Geometrie übergeben.

### SonnenstandsFaktor

Faktor in [0, 1], der ausdrückt, ob der Sonnenstand geometrisch günstig für
einen sichtbaren Hauptregenbogen ist. Kein vollständiger Sichtbarkeitsnachweis,
weil die Regenzellenrichtung fehlt.

### StandortKoordinaten

Systemisches DTO mit Latitude, Longitude und Zeitzone. Es beschreibt den
Beobachtungsort für Wetterabfrage und Sonnenstandsberechnung.

### StandortPort

Port in `system/ports/`, der Ort und Postleitzahl in StandortKoordinaten
übersetzt. Die Implementierung liegt in `infrastructure/`.


### DirektlichtFaktor

Faktor in `[0, 1]`, der beschreibt, wie stark direktes Sonnenlicht verfügbar
ist. Im Beispiel wird er aus `direct_radiation` abgeleitet. Ohne direktes Licht
ist ein normaler Sonnen-Regenbogen nicht sichtbar.

### HintergrundKontrastFaktor

Heuristischer Faktor in `[0, 1]` für den optischen Kontrast des Hintergrunds.
Ein dunklerer Regenhintergrund bei direktem Sonnenlicht erhöht die
Sichtbarkeit; vollständige Bewölkung reduziert aber oft das Direktlicht.

### NiederschlagsPhasenFaktor

Faktor in `[0, 1]`, der Wasser-Niederschlag gegenüber Schnee, Eis oder
Mischphase bevorzugt. Für einen normalen Regenbogen braucht das Modell
flüssige Wassertröpfchen.

### OptischeBedingungen

Systemsemantischer Typ, der technische Wetterdaten in fachlich verwendbare
Optikfaktoren übersetzt: Tropfenqualität, Direktlicht, Sichtweite,
Hintergrundkontrast und Niederschlagsphase.

### RegenbogenSichtbarkeit

Domain-Score in `[0, 100]`, der die erwartete Sichtbarkeit eines normalen
Sonnen-Regenbogens beschreibt. Kein Nachweis, weil Regenzellenrichtung und
echte Tropfengrößenverteilung fehlen.

### SichtFaktor

Faktor in `[0, 1]`, der Sichtweite, Dunst und Nebel approximiert. Im Beispiel
wird er aus `visibility` abgeleitet; fehlende Sichtweite wird konservativ
bewertet.

### TropfenQualitaet

Faktor in `[0, 1]`, der beschreibt, wie gut der vorhandene Niederschlag für
einen sichtbaren Regenbogen geeignet ist. Da echte Tropfengröße in normalen
Wetterdaten fehlt, wird sie heuristisch aus `weather_code`, `rain`, `showers`
und `snowfall` abgeleitet.

### EventLogger

Port für systemische Laufzeitereignisse. Systemcode nutzt den Port;
`infrastructure/` implementiert die konkrete Ausgabe.

### LogEvent

Systemisches Laufzeitereignis für Diagnose-Logging. Kein Evidence-Artefakt,
kein Sprechakt und keine fachliche Tatsache.

## 20. Index

Der Index verweist auf die wichtigsten Begriffe und die Abschnitte, in denen
sie im Tutorial besonders relevant sind.

| Begriff | Relevante Abschnitte |
|---|---|
| Abbruch | [4.4](#44-abbrüche), [9.5](#95-optionaler-abbruchpfad-h2-und-wiedereinstieg), [11.14](#1114-optionaler-abbruchpfad-sa1-bei-rotem-test) |
| adapters/ | [4.1](#41-semantische-räume), [9.2](#92-adapter-wiring), [14.2](#142-finale-importregeln-im-beispiel) |
| AGENTS-COMPACT.md | [3](#3-was-in-der-box-steckt), [4.3](#43-preflight), [6.1](#61-preflight) |
| AGENTS.md | [3](#3-was-in-der-box-steckt), [4.3](#43-preflight), [16](#16-dokument-autoritäten) |
| Autonomieregel | [4.1](#41-semantische-räume), [7](#7-zweite-session-port-und-infrastruktur), [15](#15-was-das-system-konkret-verhindert-hat) |
| Binding | [4.1](#41-semantische-räume), [9.2](#92-adapter-wiring), [15](#15-was-das-system-konkret-verhindert-hat) |
| CLI | [4.1](#41-semantische-räume), [9](#9-vierte-session-cli-und-wiring), [10](#10-fünfte-session-gui-mit-tkinter) |
| decision | [9.1](#91-preflight), [14.2](#142-finale-importregeln-im-beispiel) |
| Dependency | [7.2](#72-sprechakt-sp4-runtime-dependency-httpx), [10.3](#103-sprechakt-sp4-runtime-dependency-tkinter) |
| domain/ | [4.1](#41-semantische-räume), [6](#6-erste-session-domainkern), [14.2](#142-finale-importregeln-im-beispiel) |
| DTO | [7.5](#75-port-vertrag), [8.2](#82-implementierung), [15](#15-was-das-system-konkret-verhindert-hat) |
| Evidence | [2](#2-das-grundprinzip), [4.4](#44-abbrüche), [6.6](#66-tests-und-abschluss) |
| Erfahrungsbericht | [6.6](#66-tests-und-abschluss), [7.7](#77-import-checker-und-abschluss), [10.9](#109-import-checker-und-abschluss) |
| Folgeartefakt | [6.3](#63-mensch-entscheidet), [7.2](#72-sprechakt-sp4-runtime-dependency-httpx), [14.1](#141-sprechakte-und-folgeartefakte) |
| GUI | [10](#10-fünfte-session-gui-mit-tkinter), [10.2](#102-sprechakt-sp2-raumzuordnung-gui), [10.8](#108-tests) |
| HARD-Abbruch | [4.4](#44-abbrüche), [9.5](#95-optionaler-abbruchpfad-h2-und-wiedereinstieg), [15](#15-was-das-system-konkret-verhindert-hat) |
| httpx | [7.2](#72-sprechakt-sp4-runtime-dependency-httpx), [7.6](#76-infrastruktur-implementierung), [14.1](#141-sprechakte-und-folgeartefakte) |
| Import-Checker | [4.1](#41-semantische-räume), [7.7](#77-import-checker-und-abschluss), [14.2](#142-finale-importregeln-im-beispiel) |
| infrastructure/ | [4.1](#41-semantische-räume), [7](#7-zweite-session-port-und-infrastruktur), [15](#15-was-das-system-konkret-verhindert-hat) |
| Instanziierung | [5.2](#schritt-2-instanziierungs-sprechakt-sp0), [5.3](#schritt-3-ergebnis-prüfen) |
| Known Breach | [3](#3-was-in-der-box-steckt), [16](#16-dokument-autoritäten) |
| Learning-Matrix | [3](#3-was-in-der-box-steckt), [10.9](#109-import-checker-und-abschluss) |
| Markdown-only | [2](#markdown-only), [3](#3-was-in-der-box-steckt) |
| OrtKonfiguration | [10.5](#105-teil-b-konfigurationsdialog), [15](#15-was-das-system-konkret-verhindert-hat) |
| package-schema.md | [3](#3-was-in-der-box-steckt), [10.4](#104-package-schemamd-aktualisieren), [16](#16-dokument-autoritäten) |
| PLZ | [5](#5-projekt-aufsetzen-regenbogen), [10.5](#105-teil-b-konfigurationsdialog), [15](#15-was-das-system-konkret-verhindert-hat) |
| Portfläche | [4.1](#41-semantische-räume), [7.5](#75-port-vertrag), [14.2](#142-finale-importregeln-im-beispiel) |
| Preflight | [4.3](#43-preflight), [6.1](#61-preflight), [10.1](#101-preflight-warum-die-aufgabe-nicht-sofort-umgesetzt-wird) |
| RegenbogenWahrscheinlichkeit | [6.2](#62-sprechakt-sp7-kernbegriffe), [6.5](#65-implementierung), [8.2](#82-implementierung) |
| Regenbogen-Beispiel | [5](#5-projekt-aufsetzen-regenbogen), [15.1](#151-warum-dieses-beispiel-funktioniert) |
| Runtime-Dependency | [7.2](#72-sprechakt-sp4-runtime-dependency-httpx), [10.3](#103-sprechakt-sp4-runtime-dependency-tkinter) |
| Semantischer Raum | [4.1](#41-semantische-räume), [5.4](#schritt-4-eigene-räume-anlegen), [14.2](#142-finale-importregeln-im-beispiel) |
| SOFT-Abbruch | [4.4](#44-abbrüche), [11.14](#1114-optionaler-abbruchpfad-sa1-bei-rotem-test) |
| SP0 | [5.2](#schritt-2-instanziierungs-sprechakt-sp0) |
| SP2 | [10.2](#102-sprechakt-sp2-raumzuordnung-gui), [14.1](#141-sprechakte-und-folgeartefakte) |
| SP3 | [7.3](#73-sprechakt-sp3-fehlerklassen), [14.1](#141-sprechakte-und-folgeartefakte) |
| SP4 | [7.2](#72-sprechakt-sp4-runtime-dependency-httpx), [10.3](#103-sprechakt-sp4-runtime-dependency-tkinter) |
| SP7 | [6.2](#62-sprechakt-sp7-kernbegriffe), [14.1](#141-sprechakte-und-folgeartefakte) |
| Sprechakt | [4.2](#42-sprechakte), [6.2](#62-sprechakt-sp7-kernbegriffe), [14.1](#141-sprechakte-und-folgeartefakte) |
| system/core/ | [4.1](#41-semantische-räume), [8](#8-dritte-session-system-logik), [14.2](#142-finale-importregeln-im-beispiel) |
| system/ports/ | [4.1](#41-semantische-räume), [7.5](#75-port-vertrag), [14.2](#142-finale-importregeln-im-beispiel) |
| Task-Schnitt | [4.5](#45-task-schnitt), [6.1](#61-preflight), [10.1](#101-preflight-warum-die-aufgabe-nicht-sofort-umgesetzt-wird) |
| Testpflicht | [4.3](#43-preflight), [6.4](#64-wiedereinstieg-glossar-füllen), [10.9](#109-import-checker-und-abschluss) |
| tkinter | [10.3](#103-sprechakt-sp4-runtime-dependency-tkinter), [10.5](#105-teil-b-konfigurationsdialog), [10.8](#108-tests) |
| WetterApiMessung | [7.5](#75-port-vertrag), [7.6](#76-infrastruktur-implementierung), [8.2](#82-implementierung) |
| WetterErgebnis | [8.1](#81-preflight), [8.2](#82-implementierung), [10.6](#106-teil-c-ausgabefenster) |
| Wetterzustand | [6.2](#62-sprechakt-sp7-kernbegriffe), [6.5](#65-implementierung), [8.2](#82-implementierung) |
| DirektlichtFaktor | [12.7](#127-system-mapping-optische-bedingungen-ableiten), [19](#19-glossar) |
| HintergrundKontrastFaktor | [12.7](#127-system-mapping-optische-bedingungen-ableiten), [19](#19-glossar) |
| NiederschlagsPhasenFaktor | [12.7](#127-system-mapping-optische-bedingungen-ableiten), [19](#19-glossar) |
| OptischeBedingungen | [12.7](#127-system-mapping-optische-bedingungen-ableiten), [19](#19-glossar) |
| RegenbogenSichtbarkeit | [12.3](#123-sprechakt-sp7-optische-bedingungen), [12.8](#128-domain-modell-sichtbarkeit-statt-bloßer-wahrscheinlichkeit), [19](#19-glossar) |
| SichtFaktor | [12.7](#127-system-mapping-optische-bedingungen-ableiten), [19](#19-glossar) |
| TropfenQualitaet | [12.3](#123-sprechakt-sp7-optische-bedingungen), [12.7](#127-system-mapping-optische-bedingungen-ableiten), [19](#19-glossar) |

| Gegensonnenpunkt | [11.2](#112-sprechakt-sp7-regenbogen-geometrie), [19](#19-glossar) |
| PostleitzahlUnbekannt | [11.6](#116-sprechakt-sp2sp3-standort-aus-plz), [19](#19-glossar) |
| Regenbogenwinkel | [11.2](#112-sprechakt-sp7-regenbogen-geometrie), [19](#19-glossar) |
| Sonnenazimut | [11.2](#112-sprechakt-sp7-regenbogen-geometrie), [11.9](#119-sonnenstandsberechnung-in-systemcore), [19](#19-glossar) |
| Sonnenhoehe | [11.2](#112-sprechakt-sp7-regenbogen-geometrie), [11.4](#114-domain-implementierung-geometriefaktor), [19](#19-glossar) |
| Sonnenstand | [11](#11-sechste-session-sonnenstand-und-winkelmodell), [19](#19-glossar) |
| SonnenstandsFaktor | [11.3](#113-domain-glossar-ergänzen), [11.4](#114-domain-implementierung-geometriefaktor), [19](#19-glossar) |
| StandortKoordinaten | [11.7](#117-standort-port-und-plz-lookup), [19](#19-glossar) |
| StandortPort | [11.7](#117-standort-port-und-plz-lookup), [19](#19-glossar) |
| Uhrzeit | [11.9](#119-sonnenstandsberechnung-in-systemcore), [11.10](#1110-use-case-erweitern), [11.11](#1111-wiring-und-gui-anpassen) |
| Winkelmodell | [11](#11-sechste-session-sonnenstand-und-winkelmodell) |
| EventLogger | [13](#13-achte-session-logging-als-infrastruktur), [19](#19-glossar) |
| Infrastruktur-Logging | [13](#13-achte-session-logging-als-infrastruktur) |
| LogEvent | [13](#13-achte-session-logging-als-infrastruktur), [19](#19-glossar) |
| Logging | [13](#13-achte-session-logging-als-infrastruktur) |
| StdlibEventLogger | [13.4](#134-infrastruktur-implementierung-mit-python-logging) |
| H2-Wiedereinstieg | [9.5](#95-optionaler-abbruchpfad-h2-und-wiedereinstieg) |
| SA1-Testabbruch | [11.14](#1114-optionaler-abbruchpfad-sa1-bei-rotem-test) |

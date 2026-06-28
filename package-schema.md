# package-schema.md — Python-Projekt: Semantische Paket- und Modulräume

> Ebene: REPOSITORY
> Rolle: lokaler Architektur- und Importvertrag
> Geltung: dieses Projekt
> Autoritative Frage: Welcher Modulpfad ist fuer welche Semantik zustaendig?
> Nicht zustaendig fuer: menschliche Freigaben, Laufsteuerung, konkrete Aufgaben

> Dieses Dokument beschreibt die semantischen Adressräume dieses Python-Projekts.
>
> Es beantwortet nicht: „Welche Ordner gibt es?"
>
> Es beantwortet: **Was berechtigt ein Symbol dazu, unter einem bestimmten Modulpfad zu stehen?**

---

## 0. Platzhalter

```text
regenbogen
src
tests
docs
tools
```

Nicht ersetzte Platzhalter in aktiven Regeln sind Abbruchgrund H7.

---

## 1. Grundsatz

Ein Python-Modulpfad ist ein semantischer Adressraum, keine Ablagekonvention.

```text
regenbogen.domain.customer
regenbogen.system.retry_policy
regenbogen.infrastructure.http_client
regenbogen.adapters.persistence
```

Ein Modulpfad, der nicht erklären kann welche Mitglieder dort erlaubt sind,
welche Invarianten gelten, welche Tests ihn prüfen und welche Unterräume er besitzt,
ist kein stabiler semantischer Adressraum.

---

## 2. Standard-Raumkarte

```text
regenbogen/
  domain/
  system/
  infrastructure/
  adapters/
  cli/          (oder entrypoints/)
  shared/
  tests/
  tools/
```

Wenn das Projekt andere Namen verwendet:
Alle betroffenen Stellen nachziehen: dieses Dokument, `AGENTS.md` (Semantische Räume),
`LAYER_BY_PACKAGE_PART` sowie `SOURCE_ROOTS` / `TEST_ROOTS` / `TOOLS_ROOTS`
in `tools/check_import_layers.py`.

---

## 3. G(PKG) — Paket als semantischer Adressraum

Jedes semantische Paket wird durch vier Eigenschaften definiert:

```text
G(PKG) = (Members, Invariants, Projections, SubspaceMap)

Members:      Welche Symbole dürfen hier leben?
Invariants:   Was gilt für alle Mitglieder ohne Ausnahme?
Projections:  Wo ist der Raum sichtbar und prüfbar?
SubspaceMap:  Welche Unterräume existieren und warum?
```

Die Abschnitte 4.1–4.8 wenden dieses Schema auf jeden Standardraum an.

---

## 4. Semantische Räume

### 4.1 `domain/`

**Members**

```text
Erlaubt:
  Value Objects, Entities, fachliche Regeln, fachliche Fehler,
  fachliche Services, pure functions mit fachlicher Bedeutung.

Verboten:
  HTTP, Datenbank, Filesystem, Framework-Typen, Retry-Zähler,
  technische Timeouts, Logger als semantischer Akteur,
  datetime.now(), time.time(), random(), os.environ,
  requests / httpx / aiohttp,
  sqlalchemy / django / pydantic als Infrastrukturmodell (sofern nicht explizit freigegeben).
```

Kompetenzfrage: Kann ein Domänenexperte diesen Begriff prüfen, ohne Systemlaufzeit und Infrastruktur zu kennen?
Wenn nein: nicht domain.

**Invariants**

```text
domain importiert keine infrastructure, kein system, keine adapters, kein cli.
domain enthält keine Laufzeitmechanik (→ I1 in AGENTS.md).
```

**Projections**

```text
Domain-Tests
Glossar
Typen / Value Objects im Code
Import-Layer-Check (Negativbeweis)
```

**SubspaceMap**

```text
Projektspezifisch eintragen.
Jeder Unterraum braucht eine Bedeutung — kein Unterraum aus Bequemlichkeit.
Beispiel:
  domain/customer/   Kundenbegriffe
  domain/order/      Bestellbegriffe
  domain/payment/    Zahlungsbegriffe
```

**Importregeln**

```text
darf importieren:   domain
nur mit Ausnahme:  shared (projektbewusst freigegeben und als Known Breach klassifiziert)
darf nicht:         system, infrastructure, adapters, cli / entrypoints, tools
```

---

### 4.2 `system/`

**Members**

```text
Erlaubt:
  Use Cases, Application Services, Policies, Lifecycle-Regeln,
  Fehlerklassifikation, Retry-/Timeout-Bedeutung, Idempotenzregeln,
  Ports / abstrakte Protokolle, Transaktionsgrenzen als semantische Regeln.

Verboten:
  konkrete DB-Clients, konkrete HTTP-Clients, konkretes Filesystem-IO,
  Framework-Router, CLI-Argumentparser, produktive Secrets, direkte Prozessumgebung.
```

Kompetenzfrage: Beschreibt dieser Typ, wie das System korrekt operiert, ohne eine konkrete technische Plattform festzulegen?
Wenn ja: system.

**Invariants**

```text
system urteilt über Ablaufbedeutung — infrastructure beobachtet nur (→ I2).
Keine konkreten Plattformdetails in system.
```

**Projections**

```text
Use-Case-Tests, Policy-Tests, Fehlerklassifikations-Tests
Import-Layer-Check
```

**SubspaceMap**

```text
Projektspezifisch eintragen.
```

**Importregeln**

```text
darf importieren:   domain, system
nur mit Ausnahme:  shared (projektbewusst freigegeben und als Known Breach klassifiziert)
darf nicht:         infrastructure-Details, adapters, cli / entrypoints, konkrete externe Clients
```

### Hinweis: GUI unter cli/

GUI-Code lebt unter `cli/`. Kein eigener `gui/`-Layer.
Festgelegt durch Sprechakt SP2 (`docs/sprechakte/2026-06-12-raumzuordnung-gui.md`).

`tkinter` ist in `cli/` erlaubt. Nicht erlaubt in `domain/`, `system/`,
`infrastructure/` oder `adapters/`.

---

### 4.3 `infrastructure/`

**Members**

```text
Erlaubt:
  HTTP-Clients, DB-Adapter, Filesystem-Adapter, Queue-Adapter,
  Framework-Integration, Serializer, Clock- / Random-Implementierungen,
  externe API-Clients, technische Exception-Erfassung.

Verboten:
  neue Fachbegriffe, neue systemsemantische Policies,
  fachliche Endentscheidungen, stille Fehlerumdeutung.
```

Kompetenzfrage: Kann ein Entwickler diesen Typ prüfen, ohne Fachdomäne zu kennen?
Wenn ja: infrastructure.

**Invariants**

```text
infrastructure darf keine fachliche oder systemsemantische Bedeutung erfinden (→ I2).
infrastructure darf domain nur an explizit erlaubten Adaptergrenzen sehen.
```

**Projections**

```text
Adapter- / Gateway-Tests, Fake- / Contract-Tests
Integration-Tests (klar markiert)
Import-Layer-Check
```

**SubspaceMap**

```text
Projektspezifisch eintragen.
```

**Importregeln**

```text
darf importieren:   infrastructure, technische Bibliotheken
nur mit Ausnahme:  system-Ports / abstrakte Verträge, shared
darf domain sehen: nur wenn explizite Adaptergrenze dokumentiert ist
                   und der Checker diese Ausnahme als Known Breach kennt
```

---

### 4.4 `adapters/`

**Members**

```text
Erlaubt:
  DTO → Domain, Domain → DTO,
  technischer Fehler → systemsemantisch beobachtbarer Fehlerwert,
  externer Response → interner Result-/Error-Typ,
  CLI-Request → Use-Case-Request,
  Persistence Model → Domain Model.

Verboten:
  neue Fachbegriffe, neue Policies, neue Fehlerbedeutungen,
  stille Fallbacks, Geschäftslogik,
  Ablaufsteuerung, die in system gehört.
```

Kompetenzfrage: Verschwindet dieser Code, wenn beide Seiten dieselbe Sprache sprechen würden?
Wenn ja: adapters.

**Invariants**

```text
adapters erzeugen keine neue Semantik (→ I3).
Adapter-Entscheidungen sind Übersetzungsentscheidungen, keine Fachentscheidungen.
```

**Projections**

```text
Mapping-Tests, Fehlerübersetzungs-Tests, Roundtrip-Tests
Import-Layer-Check
```

**SubspaceMap**

```text
Projektspezifisch eintragen.
```

**Importregeln**

```text
darf importieren:   domain, system, infrastructure, adapters
nur mit Ausnahme:  shared (projektbewusst freigegeben und als Known Breach klassifiziert)
darf nicht:         cli / entrypoints, tools, neue Semantik erzeugen
```

---

### 4.5 `cli/` oder `entrypoints/`

**Members**

```text
Erlaubt:
  Argumentparser, Environment-Lesen, Konfiguration laden,
  Logging initialisieren, Use Case aufrufen, Exit-Code setzen.

Verboten:
  Domänenlogik, systemsemantische Policy,
  direkte DB-/HTTP-Fachentscheidung, komplexe Ablaufsteuerung.
```

**Invariants**

```text
cli enthält keine Domänenlogik (→ AGENTS.md, Semantische Räume).
Neue CLI-Option mit semantischer Bedeutung ist freigabepflichtig.
```

**Projections**

```text
CLI-Tests, Smoke-Tests, Argument-/Environment-Tests
```

**SubspaceMap**

```text
Projektspezifisch eintragen.
```

**Importregeln**

```text
darf importieren:   domain, system-Services, adapters, cli
nur mit Ausnahme:  infrastructure-Konfiguration (init), shared
darf nicht:         tools
```

---

### 4.6 `shared/`

`shared/` ist der gefährlichste Raum im System.

**Members**

```text
Erlaubt:
  kleine Hilfstypen ohne Domänen- oder Systemsemantik,
  allgemeine Result- / Either- / Option-Typen,
  allgemeine String- / Pfad- / Parsing-Hilfen ohne Projektsemantik.

Verboten:
  Sammelbecken für Unklassifiziertes,
  versteckte Domain, versteckte System Semantics, versteckte Infrastructure,
  Convenience-Layer.
```

Regel: Wenn ein shared-Typ eine Bedeutungsebene trägt, gehört er nicht nach shared.

**Invariants**

```text
shared importiert keine anderen Projekträume (domain, system, infrastructure, adapters, cli).
Ein shared-Modul, das projektinterne Räume importiert, verliert seine semantische Neutralität.
Der Import-Checker schlägt bei shared → projektintern explizit an.
```

**Projections**

```text
Import-Layer-Check (besonders wichtig für shared)
Unit-Tests der Hilfstypen
Überprüfung: ist dieser Typ wirklich semantisch neutral?
```

**SubspaceMap**

```text
Projektspezifisch eintragen. Wenn shared leer bleibt: streichen.
```

**Importregeln**

```text
darf importieren:   shared
darf nicht:         domain, system, infrastructure, adapters, cli, tools
```

---

### 4.7 `tests/`

**Members**

```text
Tests prüfen: Verhalten, Struktur, Importgrenzen, Regressionen, Beispiele.
Tests definieren nicht: neue Fachbegriffe, neue Policies, neue Fehlerbedeutungen, neue öffentliche API.
```

Wenn ein Test neue Semantik braucht: Sprechakt oder Planentscheidung (→ I4).

**Invariants**

```text
Tests sind Projektionen, keine Semantikquelle.
```

**Projections**

```text
Test-Runner-Output
Import-Layer-Check (Tests dürfen alles importieren — das ist bewusst)
```

---

### 4.8 `tools/`

**Members**

```text
Erlaubt:
  Import-Checker, Testpflichtableitung, Dokumentkonsistenzchecker,
  Generatoren, lokale Hilfsskripte.

Verboten:
  produktive Projektlogik,
  stille Änderung von Source-Dateien ohne expliziten Auftrag,
  Unterdrückung von Fehlern in Lint / Test / Typecheck.
```

**Invariants**

```text
Änderungen an tools/ sind geschützt (→ H5, H1).
Kein Tool darf zur Fehlerunterdrückung geändert werden.
```

---

## 5. Capability-Matrix (Importmatrix)

```text
FROM \ TO        domain   system   infra    adapters  cli    shared
domain            yes      no       no       no        no     decision
system            yes      yes      no       no        no     decision
infrastructure    decision ports    yes      no        no     decision
adapters          yes      yes      yes      yes       no     decision
cli               yes      yes      init     yes       yes    decision
tests             yes      yes      yes      yes       yes    yes
tools             no       no       no       no        no     yes
shared            no       no       no       no        no     yes
```

`decision` = nicht automatisch erlaubt. Die Kante ist nicht grundsätzlich unmöglich,
aber sie braucht eine explizite Projektentscheidung, einen Sprechakt oder eine
klassifizierte Ausnahme in `KNOWN_BREACHES`.

`ports` = nur abstrakte Ports / Protokolle unter `src/regenbogen/system/ports/`, keine konkreten Implementierungen.

`init` = nur zur Konfigurationsinitialisierung beim Prozessstart.

### 5.1 System Ports

`system/ports/` ist ein echter Unterraum der Systemdomäne:

```text
src/regenbogen/system/ports/
```

Regel:

```text
infrastructure darf system.ports importieren.
infrastructure darf kein anderes system.* importieren.
```

Ein Port beschreibt einen abstrakten Vertrag, den Infrastruktur implementieren
oder verwenden darf. Ein Port enthält keine konkrete Infrastrukturmechanik.

**Wenn package-schema.md einen neuen Raum oder eine neue Ausnahme einführt:**
`LAYER_BY_PACKAGE_PART`, `FORBIDDEN_IMPORTS`, `ALLOWED_SPECIAL_IMPORTS` und gegebenenfalls
`SOURCE_ROOTS` / `TEST_ROOTS` / `TOOLS_ROOTS` in `tools/check_import_layers.py`
nachziehen. Sonst läuft der Checker mit veralteter Konfiguration.

---

## 6. Bekannte Brüche (Known Breaches)

Bekannte Brüche sind klassifizierte Ausnahmen — keine neue Regel, keine freie Fläche.
Ein vorhandener Bruch wird nicht dadurch zum Known Breach, dass er im Bestand
bereits existiert.

Format:

```text
KB-<NR>:
  Datei:              <Pfad>
  Regelverletzung:    <welche Invariante / Importregel>
  Scope:              <konkrete Kante / Symbolmenge>
  Warum vorläufig:    <Begründung>
  Folgeplan:          <docs/plans/YYYY-MM-DD-...md>
  No-growth:          <wie Wachstum verhindert wird>
  Review/Ablauf:      <Datum oder Ereignis>
  Freigabe:           <Sprechakt / menschliche Entscheidung>
  Checker-Eintrag:    KNOWN_BREACHES in check_import_layers.py
```

Ein Agent darf bekannte Brüche nicht verschieben, erweitern oder umdeuten.
Umklassifizierung ist Sprechakt SP6 / Freigabe.

Brownfield-Inventur erzeugt keine Known Breaches. Sie erzeugt Befunde,
vorläufige Klassifikationen und Entscheidungsvorlagen. Erst eine explizite
menschliche Entscheidung darf daraus einen Known Breach machen.

---

## 7. Öffentliche API-Flächen

Projektspezifisch eintragen:

```text
- src/regenbogen/__init__.py
- src/regenbogen/api.py
- CLI-Kommandos
- dokumentierte Konfigurationsdateien
- dokumentierte Environment-Variablen
- Plugin-Schnittstellen
- importierbare Top-Level-Symbole
```

### 7.1 Top-Level-`__init__.py`

Explizite Regel für das Projektpaket:

```text
src/regenbogen/__init__.py
```

ist kein normaler semantischer Raum wie `domain`, `system`, `adapters` oder `cli`.

Erlaubt ohne Freigabe:

```text
- Datei fehlt
- Datei ist leer
- Datei enthält nur Kommentar / Modul-Docstring / pass
- Datei enthält nur einfache Metadaten wie __version__
```

Nicht still erlaubt:

```text
from regenbogen.domain.foo import Foo
from regenbogen.system.bar import Bar
__all__ = ["Foo", "Bar"]
class Foo: ...
def make_foo(...): ...
```

Solcher Inhalt ist **öffentliche API**. Er ist nicht automatisch falsch, aber
freigabepflichtig (→ H9), weil dadurch importierbare Top-Level-Symbole entstehen.

Der Import-Layer-Checker behandelt diesen Sonderfall explizit:

```text
leer / inert         → erlaubt
Import / Re-Export  → PUBLIC_API-Fund, H9 prüfen
```

Die Regel verhindert einen falschen Layer-Fehler für ein leeres
Top-Level-`__init__.py`, ohne Re-Exports zu verstecken.

Änderung an öffentlicher API ist freigabepflichtig (→ H9).

---

## 8. Python-spezifische Raumgefahren

### 8.1 Relative Imports

Diese Box setzt eine harte Agentenregel: **absolute Imports im Produktionscode.**

```text
Grund:
  Ein Modulpfad ist eine semantische Adresse (siehe Abschnitt 1).
  Ein absoluter Import macht den Zielraum sichtbar:
    from my_project.system.retry_policy import RetryBudget
  Ein relativer Import verschleiert ihn:
    from ..retry_policy import RetryBudget
  Der Layer-Checker kann relative Imports nicht zuverlässig klassifizieren.
```

Regel:

```text
Produktionscode:  absolute Imports. Relative Imports → check_import_layers meldet sie.
Tests:            relative Imports tolerierbar, aber absolut bevorzugt.
```

Wenn ein Projekt relative Imports bewusst zulassen will:
Diese Regel hier und in AGENTS.md ändern und den Checker entsprechend anpassen.
Default der Box: relative Imports im Produktionscode werden gemeldet.

### 8.2 Dynamische Imports

Verboten, wenn sie Layer-Regeln umgehen.
Nur erlaubt mit explizit freigegebenem Plugin-System, dokumentiertem Modulraum
und Checker-/Test-Abdeckung.

### 8.3 sys.path-Manipulation

Verboten in Produktionscode.
In Tests nur als explizit dokumentierte Harness-Mechanik.

### 8.4 Monkeypatching

In Produktionscode verboten.
In Tests erlaubt: lokal, sichtbar, nicht zur Definition von Produktsemantik.

### 8.5 Framework-Kollaps

Framework-Strukturen sind nicht automatisch Domain:

```text
Django Model       → infrastructure oder adapters
SQLAlchemy Model   → infrastructure oder adapters
Pydantic Model     → infrastructure oder adapters (oder domain, nur mit expliziter Entscheidung)
FastAPI Route      → nicht Application Service
```

### 8.6 Primitive Obsession

Wenn ein Begriff existiert, nicht dauerhaft als Primitive transportieren:

```text
UserId   nicht dauerhaft str
Money    nicht dict
RetryBudget nicht int
```

Parser / Serializer dürfen Primitives sehen. Danach muss reifiziert werden.

---

## 9. Neue Pakete und Module

Vor neuem Paket prüfen:

```text
1. Welcher semantische Raum?
2. Welcher Name?
3. Welche Members (G(PKG).Members)?
4. Welche Invarianten (G(PKG).Invariants)?
5. Welche erlaubten Imports?
6. Welche Tests (G(PKG).Projections)?
7. Welche Unterräume (G(PKG).SubspaceMap)?
8. LAYER_BY_PACKAGE_PART in check_import_layers.py nachziehen?
```

Wenn eine dieser Fragen nicht beantwortet werden kann: nicht anlegen.

---

## 10. Schlussregel

Ein Paketpfad ist eine kognitive Adresse.
Ein falscher Paketpfad erzeugt eine falsche Karte des Projekts.

Wenn die richtige Adresse unklar ist: nicht raten.
Task-Schnitt prüfen. Sprechakt auslösen.

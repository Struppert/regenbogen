# glossar-system.md — System Semantics: Betriebsbegriffe

**Dokumenttyp: Operativ / autoritativ**

> Dieses Glossar ist operative Infrastruktur, nicht Dokumentation.
>
> Es ist der Sortierraum für System-Semantics-Begriffe:
> Betriebsregeln des laufenden Systems, die ein Systemarchitekt ohne konkrete
> Plattform-Details beurteilen kann.
>
> Ein Agent konsultiert es beim Preflight (P5) und beim Task-Schnitt (T1, SP7).
> Neue System-Semantics entstehen durch Sprechakt SP2 — nicht durch Implementierung.

---

## 0. Platzhalter

```text
Regenbogen
regenbogen
src
```

---

## 1. Laderegel (Preflight P5)

```text
Nur laden wenn Betriebsbegriffe in der aktuellen Iteration aktiv gebraucht werden:
  - Use Cases, Policies, Lifecycle-Regeln
  - Fehlerklassifikation, Retry-Bedeutung, Idempotenz
  - Phasenbegriffe, Orchestrierung

Nicht laden wenn nur Fachdomänenbegriffe geändert werden
→ dann reicht glossar-domain.md
```

---

## 2. Eintrag-Format

```markdown
### <Begriff>

**Semantischer Raum:** system

**Kompetenzfrage:**
Beschreibt dieser Begriff wie das System korrekt operiert,
ohne eine konkrete technische Plattform festzulegen?
→ Wenn nein: gehört nicht nach system.

**Bedeutung:**
<Was ist dieser Begriff? Aus Sicht der Systemarchitektur, ohne Plattform-Details.>

**Invarianten:**
<Was gilt für alle Instanzen dieses Begriffs ohne Ausnahme?>
<Wer kann eine Verletzung erkennen?>

**Erlaubt:**
<Welche Zustände, Übergänge, Werte sind erlaubt?>

**Verboten:**
<Was darf dieser Begriff nicht modellieren?>
<Welche konkreten Plattform-Details würden ihn verletzen?>

**Projektionen:**
- Code: <Modulpfad>
- Tests: <Use-Case-Tests, Policy-Tests>
- Checker: <welcher Check>

**Abgrenzung:**
<Von welchen verwandten Begriffen muss dieser Begriff klar unterschieden werden?>

**Migrationsstatus:** canonical | legacy-bridge | deprecated
```

---

## 3. Begriffe

### WetterApiNichtErreichbar

Bedeutung: Die Wetter-API ist voruebergehend nicht erreichbar. Recoverable.

Invariante: Retry bis zu dreimal erlaubt.

Projektionen:
- Code: src/regenbogen/system/ports/wetterapi_port.py
- Tests: tests/system/test_use_case.py

Migrationsstatus: canonical

### OrtNichtGefunden

Bedeutung: Der angefragte Ort ist unbekannt. Terminal. Kein Retry.

Projektionen:
- Code: src/regenbogen/system/ports/wetterapi_port.py
- Tests: tests/system/test_use_case.py

Migrationsstatus: canonical

### WetterErgebnis

Bedeutung: Systemsemantisches Ergebnisobjekt fuer Einstiegspunkte.

Invariante: Einstiegspunkte duerfen WetterErgebnis anzeigen oder formatieren,
aber nicht neu berechnen.

Projektionen:
- Code: src/regenbogen/system/core/wahrscheinlichkeit_use_case.py
- Tests: tests/system/test_use_case.py

Migrationsstatus: canonical

### PostleitzahlUnbekannt

Bedeutung: Die eingegebene Postleitzahl kann nicht in Koordinaten uebersetzt werden.

Projektionen:
- Code: src/regenbogen/system/ports/standort_port.py
- Tests: tests/system/test_winkelmodell.py

Migrationsstatus: canonical

### LogEvent

Bedeutung: Systemisches Laufzeitereignis, das fuer Diagnosezwecke protokolliert werden darf.

Projektionen:
- Code: src/regenbogen/system/ports/logging_port.py
- Tests: tests/system/test_logging.py

Migrationsstatus: canonical

### EventLogger

Bedeutung: Port, ueber den Systemcode Laufzeitereignisse an eine technische Logging-Implementierung uebergibt.

Projektionen:
- Code: src/regenbogen/system/ports/logging_port.py
- Tests: tests/system/test_logging.py

Migrationsstatus: canonical

---

**Metasystem-Begriffe der Agenten-Box**

Diese Begriffe beschreiben das Agenten-Metasystem. Sie stehen bewusst im
Systemglossar, damit `AGENTS.md` und `AGENTS-COMPACT.md` nicht zum Handbuch
werden.

### Agenten-Box

Bedeutung: Vollständiger Satz lokaler Markdown-Artefakte, Regeln und Tools, der
einen Zielprojekt-Artefaktraum für Agentenarbeit operationalisiert.

Invariante: Eine instanziierte Agenten-Box ist lokale Projektwahrheit; sie darf
nicht auf eine externe gemeinsame Basis als operative Autorität verweisen.

### Instanziierungs-Sprechakt

Bedeutung: Einmaliger initialer Sprechakt, der eine Template-Box in einem
Zielprojekt materialisiert.

Invariante: Der Nachweis liegt in `.agent-box/instantiation.md`; erneute
Instanziierung ist ohne explizite menschliche Freigabe verboten.

### Projektanzeigename

Bedeutung: Menschlicher Name des Projekts, z. B. `Regenbogen`.

Invariante: Der Projektanzeigename ist nicht automatisch ein Python-Importname.

### Python-Package-Name

Bedeutung: Python-Import- und Pfadname unter `src`, z. B.
`regenbogen`.

Invariante: Der Python-Package-Name ist kleingeschrieben und ein gültiger
Python-Identifier.

### Produktcode-Raum

Bedeutung: Codeprojektion unter `src/regenbogen/`.

Invariante: Produktive semantische Räume werden dort als Paketpfade
materialisiert.

### Operationsraum

Bedeutung: Artefakträume wie `tools/`, `docs/`, `tests/` und `tmp/`, die
Agentenarbeit prüfen, dokumentieren oder protokollieren.

Invariante: Operationsräume sind nicht selbst Quelle fachlicher Bedeutung.

### Projektionsraum

Bedeutung: Konkreter Artefaktbereich, in dem eine Bedeutung sichtbar wird, z. B.
Code, Tests, Sprechakte, Pläne oder Evidence.

Invariante: Änderungen an Bedeutung müssen ihre relevanten Projektionen nennen.

### Evidence

Bedeutung: Nachweis, welche Prüfung, Beobachtung oder Entscheidung zu einem
Agentenergebnis geführt hat.

Invariante: Evidence wird in dieser Box als Markdown geführt.

### Sprechakt-Artefakt

Bedeutung: Markdown-Dokument, das eine menschliche Festlegung dokumentiert.

Invariante: Jedes normale Sprechakt-Artefakt hat einen Status: offen,
festgelegt, abgelehnt oder superseded.

### Known Breach

Bedeutung: Bewusst klassifizierter Regelbruch mit Begründung und Folgeplan.

Invariante: Ein Known Breach entschärft nur die benannte Kante, nicht die ganze
Datei oder den ganzen Raum.

### Migration Bridge

Bedeutung: Benannte Übergangsbrücke für laufende Symbol-, Bedeutungs- oder
Kompatibilitätsmigrationen.

Invariante: Eine Bridge darf nicht mechanisch umgedeutet werden.

### H-Code

Bedeutung: Kennung eines HARD-Abbruchs.

Invariante: H-Codes bezeichnen Stoppbedingungen, nicht Empfehlungen.

### SP-Code

Bedeutung: Kennung einer Sprechaktklasse.

Invariante: SP-Codes verlangen menschliche Festlegung, nicht agentische
Erfindung.

### Semantic Working Set

Bedeutung: Menge der Begriffe, Dateien, Regeln und Projektionen, die ein Agent
für eine Aufgabe gleichzeitig korrekt halten muss.

Invariante: Wenn das Semantic Working Set zu groß oder unscharf wird, muss die
Aufgabe geschnitten werden.

---

## 4. Bekannte Lücken

<!-- Begriffe die gebraucht werden aber noch keinen vollständigen Eintrag haben. -->

---

## 5. Abgrenzung zum Domain-Glossar

```text
glossar-domain.md:
  Fachbegriffe. Domänenexperte urteilt ohne Systemlaufzeit.

Dieses Glossar (glossar-system.md):
  Betriebsbegriffe. Systemarchitekt urteilt ohne konkrete Plattform.
  Use Cases, Policies, Lifecycle, Fehlerklassifikation, Retry-Bedeutung.

Bei Zweifel:
  Braucht die Beurteilung dieses Begriffs Wissen über konkrete Plattform?
  → Ja und kein Systemkonzept: infrastructure
  → Nein, aber Systemwissen nötig: system
  → Weder Plattform- noch Systemwissen: domain
```

---

## 6. Schlussregel

Ein Systemglossareintrag ist fertig wenn ein Systemarchitekt ihn lesen und
jeden Code-Typ im zugehörigen Modulraum damit vollständig beurteilen kann —
ohne konkrete Plattformdetails zu kennen.

Wenn das nicht möglich ist: der Eintrag ist unvollständig → Sprechakt SP7.


---

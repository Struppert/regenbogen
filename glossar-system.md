# glossar-system.md — System Semantics: Betriebsbegriffe

> Ebene: REPOSITORY
> Rolle: lokaler Systemsemantik-Vertrag
> Geltung: dieses Projekt
> Autoritative Frage: Welche Betriebsbegriffe und Systementscheidungen gelten?
> Nicht zustaendig fuer: Fachdomaene, Infrastrukturdetails, konkrete Ausfuehrung

**Dokumenttyp: Operativ / autoritativ**

> Dieses Glossar ist operative Infrastruktur, nicht Dokumentation.
>
> Es ist der Sortierraum für System-Semantics-Begriffe:
> Betriebsregeln des laufenden Systems, die ein Systemarchitekt ohne konkrete
> Plattform-Details beurteilen kann.
>
> Ein Agent konsultiert es beim Preflight (PF-GLOSSAR) und beim Task-Schnitt (T1, SP7).
> Neue System-Semantics entstehen durch Sprechakt SP2 — nicht durch Implementierung.

---

## 0. Platzhalter

```text
Regenbogen
regenbogen
src
```

---

## 1. Laderegel (Preflight PF-GLOSSAR)

```text
Nur laden wenn Betriebsbegriffe im aktuellen Arbeitspaket aktiv gebraucht werden:
  - Use Cases, Policies, Lifecycle-Regeln
  - Fehlerklassifikation, Retry-Bedeutung, Idempotenz
  - Phasenbegriffe, Orchestrierung

Nicht laden wenn nur Fachdomänenbegriffe oder Meta-Begriffe geändert werden:
  - Fachdomänenbegriffe → glossar-domain.md
  - Agenten-/Regel-/Evidence-Begriffe → glossar-meta.md
```

---

## 2. Eintrag-Format

Jeder Glossareintrag hat folgende Felder. Das Feld `Eintragstiefe` ist
Pflicht. Ein minimaler Eintrag ist explizit begrenzt, nicht unvollständig.

Minimaler Eintrag genügt für: Referenz, Suche, bestehende Projektion lesen,
semantikneutrale oder mechanische Änderung.

Vollständiger Eintrag nötig für: neue Implementierung, neue Invariante,
neue Zustände oder Übergänge, neue API, systemische Entscheidung.

Die Änderung der Eintragstiefe allein braucht keinen Sprechakt.
Neue normative Bedeutung, Invarianten, Grenzen oder erlaubte Übergänge
brauchen weiterhin die zuständige menschliche Festlegung.

```markdown
### <Begriff>

**Eintragstiefe:** vollständig | minimal

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
[nur bei vollständig]

**Erlaubt:**
<Welche Zustände, Übergänge, Werte sind erlaubt?>
[nur bei vollständig]

**Verboten:**
<Was darf dieser Begriff nicht modellieren?>
<Welche konkreten Plattform-Details würden ihn verletzen?>
[nur bei vollständig]

**Projektionen:**
- Code: <Modulpfad>
- Tests: <Use-Case-Tests, Policy-Tests>
- Checker: <welcher Check>

**Abgrenzung:**
<Von welchen verwandten Begriffen muss dieser Begriff klar unterschieden werden?>
[nur bei vollständig]

**Migrationsstatus:** canonical | legacy-bridge | deprecated
```

---

## 3. Begriffe

### WetterApiNichtErreichbar

**Eintragstiefe:** minimal

Bedeutung: Die Wetter-API ist voruebergehend nicht erreichbar. Recoverable.

Invariante: Retry bis zu dreimal erlaubt.

Projektionen:
- Code: src/regenbogen/system/ports/wetterapi_port.py
- Tests: tests/system/test_use_case.py

Migrationsstatus: canonical

### OrtNichtGefunden

**Eintragstiefe:** minimal

Bedeutung: Der angefragte Ort ist unbekannt. Terminal. Kein Retry.

Projektionen:
- Code: src/regenbogen/system/ports/wetterapi_port.py
- Tests: tests/system/test_use_case.py

Migrationsstatus: canonical

### WetterErgebnis

**Eintragstiefe:** minimal

Bedeutung: Systemsemantisches Ergebnisobjekt fuer Einstiegspunkte.

Invariante: Einstiegspunkte duerfen WetterErgebnis anzeigen oder formatieren,
aber nicht neu berechnen.

Projektionen:
- Code: src/regenbogen/system/core/wahrscheinlichkeit_use_case.py
- Tests: tests/system/test_use_case.py

Migrationsstatus: canonical

### PostleitzahlUnbekannt

**Eintragstiefe:** minimal

Bedeutung: Die eingegebene Postleitzahl kann nicht in Koordinaten uebersetzt werden.

Projektionen:
- Code: src/regenbogen/system/ports/standort_port.py
- Tests: tests/system/test_winkelmodell.py

Migrationsstatus: canonical

### LogEvent

**Eintragstiefe:** minimal

Bedeutung: Systemisches Laufzeitereignis, das fuer Diagnosezwecke protokolliert werden darf.

Projektionen:
- Code: src/regenbogen/system/ports/logging_port.py
- Tests: tests/system/test_logging.py

Migrationsstatus: canonical

### EventLogger

**Eintragstiefe:** minimal

Bedeutung: Port, ueber den Systemcode Laufzeitereignisse an eine technische Logging-Implementierung uebergibt.

Projektionen:
- Code: src/regenbogen/system/ports/logging_port.py
- Tests: tests/system/test_logging.py

Migrationsstatus: canonical

### StundlicheWetterApiMessung

**Eintragstiefe:** minimal

Bedeutung: Port-DTO das eine WetterApiMessung mit ihrem UTC-Zeitpunkt verbindet.
Transportcontainer zwischen WetterApiPort und TagesPrognoseUseCase.
Kein Fachbegriff — technisches Transportobjekt im system/ports-Raum.

Invariante: zeitpunkt_utc ist immer timezone-aware (UTC).

Projektionen:
- Code: src/regenbogen/system/ports/wetterapi_port.py
- Tests: tests/system/test_tagesprognose_use_case.py

Migrationsstatus: canonical

---

Metasystem-Begriffe der Agenten-Box (Agenten-Box, Evidence, H-Code, SP-Code,
Semantic Working Set usw.) stehen in `glossar-meta.md`.
Laderegel: nur bei Agenten-Box-Arbeit laden, nicht bei normaler Produktarbeit.

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

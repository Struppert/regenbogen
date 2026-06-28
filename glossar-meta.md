# glossar-meta.md — Agenten-Metasystem: Begriffe und Bedeutungen

> Ebene: REPOSITORY
> Rolle: lokaler Metabegriffsvertrag
> Geltung: dieses Projekt
> Autoritative Frage: Was bedeuten Agenten-, Regel-, Evidence- und Prozessbegriffe?
> Nicht zustaendig fuer: fachliche Bedeutung, konkrete Ausfuehrung

**Dokumenttyp: Operativ / autoritativ**

> Dieses Glossar ist operative Infrastruktur, nicht Dokumentation.
>
> Es ist der Sortierraum fuer Begriffe des Agenten-Metasystems:
> Box, Instanziierung, Preflight, Sprechakt, Evidence, Abbruchcodes,
> Migrationsstatus und aehnliche Begriffe der lokalen Agentensteuerung.
>
> Ein Agent konsultiert es beim Preflight (PF-GLOSSAR), wenn aktive Begriffe aus dem
> Agenten-, Regel- oder Evidence-System gebraucht werden.

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
Nur laden wenn Meta-Begriffe im aktuellen Arbeitspaket aktiv gebraucht werden:
  - Agenten-Box, Instanziierung, Preflight, Sprechakt
  - Evidence, Abbruch, H-Code, SP-Code
  - Brownfield, Observed State, Accepted Local Truth, Known Breach
  - Migration Bridge, Migrationsevidence, Semantic Working Set
  - Schreibrechte, geschuetzte Dateien, Lern- und Erfahrungsartefakte

Nicht laden wenn nur Domain- oder Systembegriffe des Zielprojekts beruehrt sind.
```

Konsequenz: Bei normaler Facharbeit (Feature, Refactoring, Test) wird dieses
Glossar nicht geladen. Es ist kein Hintergrundwissen, sondern Werkzeug
fuer System- und Migrationspflege.

---

## 2. Eintrag-Format

Das folgende Vollformat zeigt alle verfuegbaren Felder. Fuer Standardeintraege
genuegt das Minimalformat mit nur **Bedeutung** und **Invariante**. Das
Vollformat ist verbindlich, wenn Projektionsorte, Abgrenzungsregeln oder
normative Felder (Erlaubt/Verboten) benoetigt werden.

```markdown
### <Begriff>

**Semantischer Raum:** meta

**Kompetenzfrage:**
Beschreibt dieser Begriff das Agenten-Betriebssystem oder die lokale
Projektsteuerung, ohne Fachdomaene oder konkrete technische Laufzeit
vorauszusetzen?
→ Wenn nein: gehoert nicht nach meta.

**Bedeutung:**
<Was ist dieser Begriff im Agenten-Metasystem?>

**Invarianten:**
<Was gilt fuer alle Verwendungen dieses Begriffs?>

**Erlaubt:**
<Welche Operationen oder Zustände sind erlaubt?>

**Verboten:**
<Welche Umdeutung wuerde das Agentensystem verletzen?>

**Projektionen:**
- Regeln: <Regeldokument>
- Tools: <Checker oder Werkzeug>
- Evidence: <Artefaktraum>

**Abgrenzung:**
<Von welchen Domain- oder Systembegriffen muss dieser Begriff getrennt bleiben?>

**Migrationsstatus:** canonical | legacy-bridge | deprecated
```

---

## 3. Begriffe

Diese Begriffe beschreiben das Agenten-Metasystem. Sie stehen bewusst in
`glossar-meta.md`, damit `glossar-system.md` fuer Betriebsbegriffe des
Zielprojekts frei bleibt.

### Agenten-Box

Bedeutung: Vollstaendiger Satz lokaler Markdown-Artefakte, Regeln und Tools,
der einen Zielprojekt-Artefaktraum fuer Agentenarbeit operationalisiert.

Invariante: Eine instanziierte Agenten-Box ist lokale Projektwahrheit; sie darf
nicht auf eine externe gemeinsame Basis als operative Autoritaet verweisen.

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

Invariante: Der Python-Package-Name ist kleingeschrieben und ein gueltiger
Python-Identifier.

### Produktcode-Raum

Bedeutung: Codeprojektion unter `src/regenbogen/`.

Invariante: Produktive semantische Raeume werden dort als Paketpfade
materialisiert.

### Operationsraum

Bedeutung: Artefaktraeume wie `tools/`, `docs/`, `tests/` und `tmp/`, die
Agentenarbeit pruefen, dokumentieren oder protokollieren.

Invariante: Operationsraeume sind nicht selbst Quelle fachlicher Bedeutung.

### Projektionsraum

Bedeutung: Konkreter Artefaktbereich, in dem eine Bedeutung sichtbar wird, z. B.
Code, Tests, Sprechakte, Plaene oder Evidence.

Invariante: Aenderungen an Bedeutung muessen ihre relevanten Projektionen nennen.

### Evidence

Bedeutung: Nachweis, welche Pruefung, Beobachtung oder Entscheidung zu einem
Agentenergebnis gefuehrt hat.

Invariante: Evidence wird in dieser Box als Markdown gefuehrt.

### Sprechakt-Artefakt

Bedeutung: Markdown-Dokument, das eine menschliche Festlegung dokumentiert.

Invariante: Jedes normale Sprechakt-Artefakt hat einen Status: offen,
festgelegt, abgelehnt, superseded oder widerrufen.

### Known Breach

Bedeutung: Bewusst klassifizierter, begrenzter und vorlaeufig geduldeter
Regelbruch mit Begruendung, Folgeplan, No-growth-Regel und Freigabe.

Invariante: Ein Known Breach entschaerft nur die benannte Kante, nicht die ganze
Datei oder den ganzen Raum.

Verboten: Ein Known Breach darf nicht automatisch aus Brownfield-Inventur oder
blossem Bestand entstehen.

### Migration Bridge

Bedeutung: Benannte Uebergangsbruecke fuer laufende Symbol-, Bedeutungs- oder
Kompatibilitaetsmigrationen.

Invariante: Eine Bridge darf nicht mechanisch umgedeutet werden.

### H-Code

Bedeutung: Kennung eines HARD-Abbruchs.

Invariante: H-Codes bezeichnen Stoppbedingungen, nicht Empfehlungen.

### SP-Code

Bedeutung: Kennung einer Sprechaktklasse.

Invariante: SP-Codes verlangen menschliche Festlegung, nicht agentische
Erfindung.

Beispiel: SP7 bezeichnet den Fall, dass ein aktiv benoetigter Begriff im
zuständigen Glossar fehlt oder unvollstaendig ist.

### Semantic Working Set

Bedeutung: Menge der Begriffe, Dateien, Regeln und Projektionen, die ein Agent
fuer eine Aufgabe gleichzeitig korrekt halten muss.

Invariante: Wenn das Semantic Working Set zu gross oder unscharf wird, muss die
Aufgabe geschnitten werden.

### Brownfield-Aufnahme

Bedeutung: Ein bestehendes Projekt ohne bisherige Agenten-Box wird in die
Regelwelt aufgenommen, ohne den Bestand zu ueberschreiben oder automatisch zu
bestaetigen.

Invariante: Brownfield-Aufnahme trennt Discover, Describe, Classify, Decide,
Project, Migrate und Verify.

### Observed State

Bedeutung: Tatsaechlich vorgefundener Zustand im Bestand, z. B. Datei,
Importkante, Test, Build-Konfiguration, Workaround oder API-Flaeche.

Invariante: Observed State ist Befund, nicht Freigabe.

### Unknown / Unclassified

Bedeutung: Brownfield-Befund, der noch nicht ausreichend verstanden ist.

Invariante: Ein unklassifizierter Befund darf nicht normativ projiziert werden.

### Accepted Local Truth

Bedeutung: Explizit bestaetigte lokale operative Wahrheit eines Zielprojekts.

Invariante: Accepted Local Truth entsteht durch zustaendige Projektartefakte
oder menschliche Entscheidung, nicht durch blosse Existenz von Code.

### Accepted Alternative

Bedeutung: Abweichung vom Template-Zielmodell, die lokal konsistent und
ausdruecklich akzeptiert ist.

Invariante: Eine Accepted Alternative ist keine Altlast und kein Known Breach.

### Migration Candidate

Bedeutung: Befund, der an ein Zielmodell angenaehert oder umgebaut werden soll,
ohne bereits als akuter Defekt klassifiziert zu sein.

Invariante: Ein Migration Candidate braucht Zielrichtung und Plan, aber nicht
automatisch einen Known Breach.

### Legacy Defect

Bedeutung: Vorhandener Zustand, der einer gueltigen lokalen Invariante oder dem
entschiedenen Zielmodell widerspricht und nicht akzeptiert ist.

Invariante: Legacy Defect ist nicht automatisch Known Breach.

### Baseline

Bedeutung: Deskriptiver Nachweis des aktuellen Zustands vor einer Aenderung
oder Migration, inklusive bereits roter Checks.

Invariante: Baseline beschreibt, was ist; sie entscheidet nicht, was gelten soll.

### Zielmodell

Bedeutung: Normativer Zielzustand, der durch Projektartefakte, Sprechakte oder
menschliche Entscheidung festgelegt ist.

Invariante: Zielmodell und Baseline duerfen nicht vermischt werden.

### Migrationsevidence

Bedeutung: Markdown-Nachweis, was bei einer Brownfield-Migration tatsaechlich
geprueft, entschieden, geaendert, verworfen oder offengelassen wurde.

Invariante: Migrationsevidence ersetzt keine Sprechakte fuer neue Bedeutung.

### Datei-Aktionsklasse

Bedeutung: Brownfield-Klassifikation einer Datei als add, preserve, merge,
replace, inspect oder forbidden.

Invariante: Die Aktionsklasse bestimmt den Umgang mit der Datei, nicht ihre
semantische Gueltigkeit.

### Autonomieregel

Bedeutung: Eigenschaft eines Glossareintrags oder semantischen Raums — ein
einzelner Experte kann den Begriff vollstaendig beurteilen ohne andere
semantische Raeume oder Fachdomaenen kennen zu muessen.

Invariante: Ist die Autonomieregel verletzt, liegt eine falsch gezogene
Grenze oder ein unvollstaendiger Eintrag vor. Reaktion: H10 ausloesen,
Sprechakt oder Task-Schnitt pruefen.

Projektionen:
- Regeln: glossar-README.md §5
- Preflight: preflight-checkliste.md PF-GLOSSAR

### BF-Code

Bedeutung: Kennung eines Brownfield-spezifischen HARD-Abbruchs.

Invariante: BF-Codes stoppen Brownfield-Arbeit, wenn Bestand, Zielmodell,
Freigabe oder Evidence nicht tragfaehig getrennt sind.

### Herkunftsmarker

Bedeutung: Datei unter `.agent-box/`, die belegt, wie ein Projekt seine
Agenten-Box erhalten hat.

Invariante: Greenfield → `.agent-box/instantiation.md`; Brownfield →
`.agent-box/adoption.md`. Fehlt die Datei, ist der Projektstatus unklar
und Preflight PF-AGENTS schlaegt fehl.

Projektionen:
- Regeln: sprechakt-protokoll.md §2 (SP0)
- Preflight: preflight-checkliste.md PF-AGENTS

### Wirkungsgate

Bedeutung: Kontrollpunkt, der vor einer Repository-Mutation geprueft wird.
Ergibt gruen (Mutation erlaubt) oder sperrt die Aktion. In dieser Box ist
`WG-MUTATION` das einzige definierte Wirkungsgate.

Invariante: Ein Wirkungsgate ist eine fortlaufende Invariante, kein
einmaliger Preflight-Schritt. Es bleibt asserted solange der Gate-Zustand
unveraendert ist. Eine vollstaendige Neubewertung erfolgt bei Zustandswechsel
(Wirkungstyp, Scope, Mandatsstatus oder Grundlagenversion). In Brownfield-
Laeufen projiziert sich das Gate auf die freigegebene Datei-Aktionsmatrix.

Projektionen:
- Regeln: ausfuehrungsmandat-protokoll.md, Abschnitt „Wirkungsgate WG-MUTATION"
- Preflight: preflight-checkliste.md §0a

---

## 4. Bekannte Luecken

<!-- Meta-Begriffe die gebraucht werden aber noch keinen vollstaendigen Eintrag haben. -->

---

## 5. Abgrenzung zu anderen Glossaren

```text
glossar-domain.md:
  Fachbegriffe. Domaenenexperte urteilt ohne Systemlaufzeit.

glossar-system.md:
  Betriebsbegriffe des Zielprojekts. Systemarchitekt urteilt ohne konkrete Plattform.

Dieses Glossar (glossar-meta.md):
  Agenten-, Regel-, Evidence- und Prozessbegriffe der lokalen Projektsteuerung.
```

Bei Zweifel:

```text
Beschreibt der Begriff Agentenarbeit, Regelautoritaet, Evidence oder Abbruch?
  → Ja: meta

Beschreibt der Begriff fachliche Bedeutung des Produkts?
  → domain

Beschreibt der Begriff Betriebsverhalten des Produkts?
  → system
```

---

## 6. Schlussregel

Ein Meta-Glossareintrag ist fertig, wenn ein Projektmaintainer ihn lesen und
die zugehoerigen Agentenregeln, Artefakte oder Tools damit pruefen kann, ohne
Fachdomaene oder konkrete Laufzeitplattform zu kennen.

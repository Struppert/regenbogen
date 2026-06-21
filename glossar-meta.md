# glossar-meta.md — Agenten-Metasystem: Begriffe und Bedeutungen

**Dokumenttyp: Operativ / autoritativ**

> Dieses Glossar enthält die Metasystem-Begriffe der Agenten-Box.
> Es beschreibt nicht die Fachdomäne oder Systemsemantik des Produkts —
> sondern die Begriffe des Agenten-Betriebs selbst.
>
> Autorität: wer das Agenten-System pflegt und weiterentwickelt.
>
> Laderegel: nur laden wenn Agenten-Box-Arbeit aktiv stattfindet
> (Systempflege, Regeländerungen, Instanziierung, Dokumentdrift-Prüfung).
> Nicht laden bei normaler Fach- oder Systemarbeit am Produkt.

---

## 1. Laderegel

```text
Laden bei:
  - Arbeit an AGENTS.md, AGENTS-COMPACT.md, preflight-checkliste.md
  - Arbeit an Glossar-Struktur oder Ladeprotokoll
  - Instanziierung oder Re-Instanziierung
  - Sprechakt-Protokoll-Änderungen
  - Dokumentdrift-Prüfung im Metasystem
  - Brownfield-Aufnahme oder Box-Versionsmigration

Nicht laden bei:
  - Domain-Facharbeit (glossar-domain.md reicht)
  - Systemsemantik des Produkts (glossar-system.md reicht)
  - normalen Produktionscode-Änderungen
```

Fehlt für die geplante Nutzung ein ausreichend tiefer Metabegriff:
zuerst Task-Schnitt T1, danach — wenn der Begriff aktiv nötig bleibt — Sprechakt SP7.

---

## 2. Eintrag-Format

```markdown
### <Begriff>

**Semantischer Raum:** meta

**Kompetenzfrage:**
Beschreibt dieser Begriff das Agenten-Betriebssystem oder die lokale
Projektsteuerung, ohne Fachdomäne oder konkrete technische Laufzeit
vorauszusetzen?
→ Wenn nein: gehört nicht nach meta.

**Bedeutung:**
<Was ist dieser Begriff im Agenten-Metasystem?>

**Invarianten:**
<Was gilt für alle Verwendungen dieses Begriffs?>

**Erlaubt:**
<Welche Operationen oder Zustände sind erlaubt?>

**Verboten:**
<Welche Umdeutung würde das Agentensystem verletzen?>

**Projektionen:**
- Regeln: <Regeldokument>
- Tools: <Checker oder Werkzeug>
- Evidence: <Artefaktraum>

**Abgrenzung:**
<Von welchen Domain- oder Systembegriffen muss dieser Begriff getrennt bleiben?>

**Migrationsstatus:** canonical | legacy-bridge | deprecated
```

Die Einträge unten sind bewusst knapp gehalten (Bedeutung + Invariante).
Ein Meta-Begriff beschreibt Agentenarbeit, Regelautorität, Evidence, Abbruch
oder Brownfield-Steuerung — nicht die Fachdomäne oder die Systemsemantik des
Produkts.

---

## 3. Begriffe

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

Bedeutung: Python-Import- und Pfadname unter `src`, z. B. `regenbogen`.

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

### Brownfield-Aufnahme

Bedeutung: Ein bestehendes Projekt ohne bisherige Agenten-Box wird in die
Regelwelt aufgenommen, ohne den Bestand zu überschreiben oder automatisch zu
bestätigen.

Invariante: Brownfield-Aufnahme trennt Discover, Describe, Classify, Decide,
Project, Migrate und Verify.

### Observed State

Bedeutung: Tatsächlich vorgefundener Zustand im Bestand, z. B. Datei,
Importkante, Test, Build-Konfiguration, Workaround oder API-Fläche.

Invariante: Observed State ist Befund, nicht Freigabe.

### Unknown / Unclassified

Bedeutung: Brownfield-Befund, der noch nicht ausreichend verstanden ist.

Invariante: Ein unklassifizierter Befund darf nicht normativ projiziert werden.

### Accepted Local Truth

Bedeutung: Explizit bestätigte lokale operative Wahrheit eines Zielprojekts.

Invariante: Accepted Local Truth entsteht durch zuständige Projektartefakte
oder menschliche Entscheidung, nicht durch bloße Existenz von Code.

### Accepted Alternative

Bedeutung: Abweichung vom Template-Zielmodell, die lokal konsistent und
ausdrücklich akzeptiert ist.

Invariante: Eine Accepted Alternative ist keine Altlast und kein Known Breach.

### Migration Candidate

Bedeutung: Befund, der an ein Zielmodell angenähert oder umgebaut werden soll,
ohne bereits als akuter Defekt klassifiziert zu sein.

Invariante: Ein Migration Candidate braucht Zielrichtung und Plan, aber nicht
automatisch einen Known Breach.

### Legacy Defect

Bedeutung: Vorhandener Zustand, der einer gültigen lokalen Invariante oder dem
entschiedenen Zielmodell widerspricht und nicht akzeptiert ist.

Invariante: Legacy Defect ist nicht automatisch Known Breach.

### Baseline

Bedeutung: Deskriptiver Nachweis des aktuellen Zustands vor einer Änderung
oder Migration, inklusive bereits roter Checks.

Invariante: Baseline beschreibt, was ist; sie entscheidet nicht, was gelten soll.

### Zielmodell

Bedeutung: Normativer Zielzustand, der durch Projektartefakte, Sprechakte oder
menschliche Entscheidung festgelegt ist.

Invariante: Zielmodell und Baseline dürfen nicht vermischt werden.

### Migrationsevidence

Bedeutung: Markdown-Nachweis, was bei einer Brownfield-Migration tatsächlich
geprüft, entschieden, geändert, verworfen oder offengelassen wurde.

Invariante: Migrationsevidence ersetzt keine Sprechakte für neue Bedeutung.

### Datei-Aktionsklasse

Bedeutung: Brownfield-Klassifikation einer Datei als add, preserve, merge,
replace, inspect oder forbidden.

Invariante: Die Aktionsklasse bestimmt den Umgang mit der Datei, nicht ihre
semantische Gültigkeit.

### BF-Code

Bedeutung: Kennung eines Brownfield-spezifischen HARD-Abbruchs.

Invariante: BF-Codes stoppen Brownfield-Arbeit, wenn Bestand, Zielmodell,
Freigabe oder Evidence nicht tragfähig getrennt sind.

---

## 4. Abgrenzung zu anderen Glossaren

```text
glossar-domain.md:
  Fachbegriffe. Domänenexperte urteilt ohne Systemlaufzeit.

glossar-system.md:
  Betriebsbegriffe des Zielprojekts. Systemarchitekt urteilt ohne konkrete Plattform.

Dieses Glossar (glossar-meta.md):
  Agenten-, Regel-, Evidence- und Prozessbegriffe der lokalen Projektsteuerung.
```

Bei Zweifel:

```text
Beschreibt der Begriff Agentenarbeit, Regelautorität, Evidence oder Abbruch?
  → Ja: meta

Beschreibt der Begriff fachliche Bedeutung des Produkts?
  → domain

Beschreibt der Begriff Betriebsverhalten des Produkts?
  → system
```

---

## 5. Schutz

Dieses Dokument ist geschützt (AGENTS.md Abschnitt 9).
Neue Metabegriffe entstehen durch Sprechakt SP2.

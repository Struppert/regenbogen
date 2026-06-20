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

Nicht laden bei:
  - Domain-Facharbeit (glossar-domain.md reicht)
  - Systemsemantik des Produkts (glossar-system.md reicht)
  - normalen Produktionscode-Änderungen
```

---

## 2. Begriffe

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

---

## 3. Schutz

Dieses Dokument ist geschützt (AGENTS.md Abschnitt 9).
Neue Metabegriffe entstehen durch Sprechakt SP2.

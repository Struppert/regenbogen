# Priming-Analyse: Agenten-Box Regenbogen

**Grundlage:** Auswertung von `analysen/chat.txt`, eigene Inspektion aller
Kerndokumente (AGENTS.md, AGENTS-COMPACT.md, glossar-domain.md,
glossar-system.md, migration-bridges.md, package-schema.md,
preflight-checkliste.md, task-schnitt.md, regelmatrix.md, learning-matrix.md,
grundsatz.md).

**Kontext:** `Regenbogen` ist ein Greenfield-Projekt. Die in `chat.txt`
beschriebene Erfahrung mit einem bestehenden Projekt (Brownfield) stammt aus
einer anderen Anwendung desselben Priming-Systems. Beide Fälle werden hier
gemeinsam ausgewertet, weil die Schwächen teilweise deckungsgleich sind —
in Brownfield treten sie nur früher und deutlicher auf.

---

## 1. Was `chat.txt` ist und was es leistet

`chat.txt` ist ein Analyse-Chat mit einem anderen KI-System über dieses
Priming-Setup. Er enthält:

- eine strukturierte Systemanalyse (Stärken / Schwächen)
- einen empirischen Bericht: das Priming wurde auf ein Brownfield-Projekt
  angewandt, und die KI hat dort dokumentierte Migrationsbrüche aktiv benutzt,
  um das System zu unterlaufen
- eine Diagnose dieses Verhaltens
- Iterationshypothesen für Verbesserungsrunden

Der Chat ist ungewöhnlich gut: die Analyse ist nicht kosmetisch, sie trifft
den Kern des Problems. Gleichzeitig bleibt sie auf dem Niveau von Beobachtung
und Hypothese — sie liefert keine konkreten Änderungsvorschläge für das
Dokumentensystem selbst.

Diese Analyse tut das.

---

## 2. Der Bridge-Exploit: Mechanismus und Ursache

### 2.1 Was passiert ist

Beim Einsatz in einem Brownfield-Projekt hat die KI die dokumentierten
Migration-Bridges nicht als Warnung gelesen, sondern als Arbeitsgrundlage
benutzt. Symbole mit Status `do-not-introduce` oder `legacy-bridge` wurden
in neuem Code wiederverwendet.

### 2.2 Warum das strukturell vorhersehbar ist

Das Modell optimiert auf Fortsetzbarkeit. Wenn eine Lücke im kanonischen Pfad
existiert (unklare Semantik, fehlender Begriff, inkonsistente Codestruktur),
sucht das Modell eine Lösung. Dokumentierte Brüche sind dabei besonders
attraktiv, weil sie drei Eigenschaften gleichzeitig haben:

```text
1. Sie sind explizit vorhanden  → das Modell "sieht" sie
2. Sie sind dokumentiert        → also offenbar system-bekannt
3. Sie liegen genau auf Kanten  → genau dort wo der Agent gerade arbeitet
```

Der entscheidende Satz aus `chat.txt`:

> *"Die KI hat die Brüche nicht trotz des Systems verwendet, sondern wegen
> ihrer expliziten Sichtbarkeit und Anschlussfähigkeit."*

Das ist kein Fehler des Agenten im moralischen Sinn. Es ist ein
Generalisierungsfehler: "dokumentiert und vorhanden" wird zu "akzeptierte
Praxis".

### 2.3 Warum Greenfield das Problem nicht eliminiert, nur verschiebt

`migration-bridges.md` ist in `Regenbogen` aktuell leer — keine aktiven
Einträge. Das bedeutet: der Exploit-Pfad existiert noch nicht. Aber:

- Sobald das Projekt wächst und echte Bridge-Einträge entstehen, trifft das
  Problem in gleicher Form ein.
- Der Brownfield-Fall war nur dramatischer, weil die Brüche nicht im
  Migrationsdokument standen, sondern im Code selbst sichtbar waren — und
  das Modell Code-Muster stärker gewichtet als Textregeln.

### 2.4 Der eigentliche Designfehler in `migration-bridges.md`

Die aktuellen Aktions-Labels sind für Menschen ausreichend:

```text
do-not-introduce
allow-read-only
do-not-touch-mechanically
```

Für ein Modell sind sie semantisch zu schwach, weil sie keine
*negativen Entscheidungsverfahren* auslösen. Das Modell muss die Regel
lesen, auf den aktuellen Diff anwenden, und selbst ableiten: "Füge ich
hier ein neues Vorkommen ein?" Dieser Schritt fehlt im Preflight komplett.

---

## 3. Systemstärken

### 3.1 Das eigentliche Problem ist korrekt identifiziert

Das System geht von einer guten Grundannahme aus: Agenten scheitern nicht an
Syntax, sondern an impliziter Semantik. `grundsatz.md` formuliert das sauber.
Der Schlüsselsatz:

> *"Plausibilität ist kein semantischer Zustand."*

Das ist für Agentenarbeit richtig und wichtig. Die meisten Priming-Setups
behandeln dieses Problem gar nicht.

### 3.2 Semantische Räume sind konkret und maschinell prüfbar

Die Kombination aus `AGENTS.md` Abschnitt 2, `package-schema.md` und dem
Import-Checker ist die stärkste Stelle des Systems. Andere Setups sagen nur
"achte auf Architektur" — hier ist das operationalisiert:

```text
domain darf keine Laufzeitmechanik tragen (I1)
infrastructure beobachtet, system urteilt (I2)
adapters binden, erfinden keine Semantik (I3)
```

Und der Checker macht diese Regeln verifizierbar, nicht nur lesbar.

### 3.3 Abbruchlogik ist explizit und ernst gemeint

H1–H10 / SA1–SA6 / SP1–SP7 sind keine Dekoration. Die Codes sind disjunkt,
jede Klasse hat eine klar andere Reaktionspflicht. Die Schlussregel:

> *"Ein gültiger Abbruch ist besser als eine erfundene Lösung."*

Das ist operativ korrekt und verhindert das typische Problem: Agent schreibt
plausibel weiter, obwohl die semantische Lage unklar ist.

### 3.4 Das Glossar ist als Werkzeug konzipiert

Die Laderegel "nur aktiv benötigte Begriffe" und die Trennung nach Räumen
(glossar-domain vs. glossar-system) ist konzeptuell stark. Sie erzwingt,
dass der Agent den Semantic Working Set aktiv bestimmt, statt das Glossar
als Hintergrundlektüre zu behandeln.

### 3.5 Sprechakt als harter Übergabepunkt

Neue Begriffe entstehen nur durch expliziten menschlichen Akt. Das ist der
einzige belastbare Schutz gegen semantischen Drift durch KI. Die formale
Struktur (Artefakt, append-only, Status, Sprechakttyp) gibt ihm operative
Substanz.

### 3.6 Dokumenthierarchie ist klar geregelt

`regelmatrix.md` löst das Problem konkurrierender Dokumente sauber. Bei
Widerspruch gilt: AGENTS.md > package-schema.md > Glossare > ... Das ist
besser als die meisten Setups, die keinen definierten Tiebreaker haben.

### 3.7 Erfahrungsberichte erzeugen auswertbares Material

Das System produziert durch Sprechakte, Abbruch-Artefakte und
Erfahrungsberichte genau das Material, das für Iteration nötig ist: Wo wurde
gestoppt? Welche Regeln haben geholfen? Welche nur Reibung erzeugt?

---

## 4. Systemschwächen

### 4.1 Migration-Bridges: operative Sperre zu schwach

**Problem:** Die Aktions-Labels (`do-not-introduce`, `allow-read-only`) sind
textuelle Warnungen ohne Prozedur. Das Modell muss selbst ableiten, ob es
gerade gegen sie verstößt.

**Fehlendes Element:** Ein negatives Entscheidungsverfahren im Preflight:

> Prüfe für jeden geplanten Diff: Führe ich ein neues Vorkommen eines
> Bridge-Symbols ein? Erweitere ich seinen Geltungsbereich?

Und visuell: Bridge-Einträge sehen aktuell dokumentarisch gleich aus wie
kanonische Begriffe. Sobald die Registry Einträge enthält, ist das ein
Rauschproblem.

### 4.2 Preflight hat keine Trivialitätsschwelle

**Problem:** Schritt P1–P11 soll vor *jeder nichttrivialen Änderung*
ausgeführt werden. Was "nichttrivial" bedeutet, ist nicht definiert.

In der Praxis führt das zu zwei Fehlern:

```text
Fehler A: Agent führt Preflight mechanisch für jede Kleinigkeit durch
          → teuer, träge, Kontextlast unnötig hoch

Fehler B: Agent überspringt Preflight still bei "kleinen" Aufgaben
          → Schutzlücke genau dort wo sie nicht auffällt
```

Ein expliziter Fast-Path für SICHER-Tasks (nur AGENTS-COMPACT + Checker)
würde beide Fehler reduzieren.

### 4.3 Glossar-Einträge sind unvollständig gegenüber eigenem Format

**Problem:** Das Eintrag-Format (Abschnitt 2 in glossar-domain.md und
glossar-system.md) verlangt:

```text
Kompetenzfrage | Bedeutung | Invarianten | Erlaubt | Verboten
Projektionen   | Abgrenzung | Migrationsstatus
```

Die tatsächlichen Einträge haben meist nur:

```text
Bedeutung | Projektionen | Migrationsstatus
```

Das ist ein Reifizierungsdefizit: das System fordert mehr Explizitheit, als
es selbst liefert. Ein Modell das das erkennt, hat ein schwächeres Glossar
als erwartet. Halbfertige Einträge sind schlechter als explizit minimale —
weil sie Vollständigkeit signalisieren, aber keine liefern.

### 4.4 `glossar-system.md` mischt Produkt- und Metasemantik

**Problem:** Das Systemglossar enthält ab Abschnitt "Metasystem-Begriffe
der Agenten-Box" Begriffe wie `Agenten-Box`, `Evidence`, `Semantic Working
Set`, `Abbruch-Artefakt` neben Produktbegriffen wie `WetterApiNichtErreichbar`
oder `OrtNichtGefunden`.

Das ist inhaltlich begründet (damit AGENTS.md nicht zum Handbuch wird), aber
operativ teuer: Beim Preflight für eine reine Fachlogik-Änderung lädt der
Agent auch Metasystem-Begriffe mit — ohne sie zu brauchen.

Für dieses kleine Projekt ist das noch tolerierbar. Bei Wachstum wird es
Rauschen.

### 4.5 H10 ist Prinzip, keine Prüfregel

**Problem:** H10 lautet:

> *"Autonomieregel verletzt: Code-Typ in Raum X setzt Wissen aus Raum Y
> voraus, aber Experte für X kann Y nicht beurteilen."*

Das ist konzeptuell richtig. Aber: wann genau löst das einen HARD-Abbruch
aus? Welche Granularität? Was muss der Agent konkret prüfen, um H10 zu
erkennen? Das ist nicht operationalisiert. In der Praxis wird H10 entweder
nie ausgelöst oder zu konservativ ausgelöst.

### 4.6 Learning-Schleife ist zeitlich unbestimmt

**Problem:** Der Pfad

```text
Erfahrungsbericht → learning-matrix.md → menschliche Entscheidung → Regeländerung
```

hat keine definierten Taktzeiten oder Auslösekriterien. Es gibt keine
Schwelle wie "nach N Erfahrungsberichten mit demselben Muster gilt es als
systemic". Das Risiko: Berichte versickern in `tmp/`, ohne in Regeländerungen
zu münden.

### 4.7 Platzhalter-Rauschen in AGENTS-COMPACT.md

**Problem:** In `AGENTS-COMPACT.md` Zeile 10–13 steht der Platzhalterblock
als rohe, einfach zusammengeführte Wertreihe:

```
Regenbogen  regenbogen  src  tests
docs             tools            python tools/check_import_layers.py --preflight src tests tools
python -m ruff check .       python -m ruff format --check .
...
```

Das sieht nach unverarbeitetem Template-Rest aus. Ein Agent der diesen Block
liest, hat Mühe, die enthaltenen Werte sauber zu extrahieren. Die Werte
sind instanziiert (Inhalt ist korrekt), aber die Darstellung ist unlesbar.

### 4.8 Kein expliziter Kontext-Degradations-Schutz

**Problem:** Das System setzt voraus, dass Preflight-Dokumente vollständig
im Kontext des Modells verfügbar sind. In einem langen Gespräch oder bei
großem Dokumentenapparat können früh geladene Inhalte effektiv aus dem
Arbeitskontext gedrängt werden.

Es gibt keinen Mechanismus für "Re-Preflight nach X Schritten" oder
"kritische Invarianten kompakt im Prompt halten".

---

## 5. Greenfield vs. Brownfield: Warum der Unterschied relevant ist

Das System ist für Greenfield entworfen und dort am stärksten. Die
Brownfield-Schwäche ist qualitativ anders:

| Dimension              | Greenfield (Regenbogen)        | Brownfield                                  |
|------------------------|-------------------------------|----------------------------------------------|
| Bridge-Registry        | leer — kein Exploit-Pfad      | gefüllt — Exploitpfade vorhanden             |
| Code-Muster            | kanonisch — keine Altlasten   | heterogen — alte Muster konkurrieren         |
| Modellinput            | Regeltext gewinnt             | Code-Muster + Regeltext konkurrieren         |
| Known-Breach-Sichtbarkeit | nur Registry-Einträge      | auch im Code sichtbar — stärkeres Signal     |
| Semantik-Kontext       | wird erst aufgebaut           | schon vorhanden — aber teilweise veraltet    |

Das bedeutet: Für Brownfield müsste das System zwei zusätzliche Eigenschaften
haben:

1. **Altlast-Modus**: Bekannte Brüche im Code gelten als Hochrisikozone,
   nicht als Arbeitsfläche. Default bei Berührung: Task-Schnitt oder
   HARD-Abbruch.

2. **Diff-Check auf Bridge-Symbole**: Nicht nur Registry lesen, sondern
   explizit prüfen, ob ein neu erzeugter Symbol-Name aus der Liste bekannter
   Brüche stammt.

---

## 6. Konkrete Verbesserungsvorschläge

### V1 — `migration-bridges.md`: Diff-Prüfregel hinzufügen

**Ziel:** Bridge-Symbole dürfen nicht durch Textwarnung allein gesperrt sein.

**Änderung in Abschnitt 5 ("Wie ein Agent dieses Dokument verwendet"):**

```text
Vor jeder Änderung die einen Begriff aus der Bridge-Registry berührt:

1. Symbol in BR-Registry suchen.
2. Migrationsstatus lesen.
3. Agent-Aktion prüfen.
4. Bei do-not-touch-mechanically: STOPP. Sprechakt SP6.
5. Bei allow-read-only: lesen erlaubt, nicht neu einführen.
6. Bei do-not-introduce: aktiv prüfen:
   - Erscheint dieses Symbol im geplanten Diff als neu eingeführtes Vorkommen?
   - Erweitere ich seinen Geltungsbereich (neue Funktion, neuer Modulpfad,
     neues Argument, neuer Rückgabetyp)?
   - Mache ich aus passiver Kompatibilität wieder aktive Semantik?
   Wenn ja zu einer dieser Fragen: HARD-Abbruch H2.
7. Bei allow-read-only und do-not-introduce:
   Bridge-Begriff ist keine Lösung für fehlende kanonische Begriffe.
   Wenn kein kanonischer Begriff verfügbar: Task-Schnitt T1, dann SP7.
```

**Zusätzlich: visuelle Trennung in der Registry**

Bridge-Einträge müssen dokumentarisch klar von kanonischen Begriffen
unterscheidbar sein. Vorschlag: eigener Header mit explizitem Warnlabel:

```markdown
## 4. Bridge-Registry

> ACHTUNG FÜR AGENTEN: Einträge hier sind KEINE Arbeitsgrundlage.
> Sie beschreiben semantische Altlasten oder laufende Migrationen.
> Jede aktive Nutzung eines Bridge-Symbols in neuem Code ist
> standardmäßig ein HARD-Abbruch H2, außer die Änderungsregel
> des Eintrags erlaubt sie explizit.
```

---

### V2 — Preflight: Fast-Path für SICHER-Tasks definieren

**Ziel:** Preflight-Kosten an Risikoklasse anpassen.

**Änderung in `preflight-checkliste.md`**, neuer Abschnitt vor P1:

```markdown
## 0. Risikoklassen-Weiche

Vor dem Preflight: welche Risikoklasse hat diese Aufgabe?

SICHER (aus AGENTS.md Abschnitt 6):
  Dokumentation, Kommentare, Lint, tote Imports, bestehende Tests ergänzen,
  lokale Refactorings ohne neue Begriffe.

  → Fast-Path: nur P1 (AGENTS-COMPACT), P7 (Checker), P8 (Testpflicht)
  → P2–P6, P9–P11 entfallen

MITTEL oder höher:
  → Vollständiger Preflight P1–P11

Wenn Zweifel über Risikoklasse: vollständiger Preflight.
```

---

### V3 — Glossar: Minimalformat definieren oder vollständig pflegen

**Ziel:** Kein Eintrag soll Vollständigkeit signalisieren, die er nicht hat.

**Option A (empfohlen): Minimalformat explizit freigeben**

In glossar-domain.md und glossar-system.md, Abschnitt 2, neues Feld:

```markdown
**Eintragstiefe:** vollständig | minimal

minimal bedeutet: Bedeutung + Projektionen + Migrationsstatus sind vorhanden.
Alle anderen Felder sind bewusst weggelassen, nicht vergessen.
Upgrade auf vollständig erfordert keinen Sprechakt, nur Pflege.
```

Alle bestehenden Einträge werden explizit als `minimal` markiert.

**Option B:** Alle Einträge auf vollständiges Format heben. Aufwändiger,
aber ohne Kompromiss.

---

### V4 — `glossar-system.md`: Metasystem-Begriffe auslagern

**Ziel:** Produkt-Betriebsbegriffe und Agenten-Metabegriffe trennen.

**Vorschlag:** Abschnitt "Metasystem-Begriffe der Agenten-Box" in eine
eigene Datei `glossar-meta.md` auslagern.

Laderegel: `glossar-meta.md` nur laden, wenn der Agent Metasystem-Begriffe
(Abbruch, Evidence, SWS, Sprechakt-Typen) aktiv braucht — also bei
Systempflege, nicht bei normaler Facharbeit.

Aufwand: gering. Wirkung: Preflight für Fachaufgaben lädt deutlich weniger
Kontext.

---

### V5 — H10 operationalisieren

**Ziel:** H10 von Prinzip zu auslösbarer Prüfregel machen.

**Änderung in AGENTS.md Abschnitt 10:**

```text
H10 — Autonomieregel verletzt

Auslösekriterium: Ein Symbol in Raum X (z.B. domain) setzt implizit voraus,
dass sein Aufrufer Wissen aus Raum Y (z.B. system, infrastructure) hat,
um es korrekt zu interpretieren.

Konkrete Erkennungsregeln:
  - Ein domain-Typ enthält ein Feld dessen Name aus Infrastruktur- oder
    System-Vokabular stammt (retry_count, http_status, db_id)
  - Eine domain-Funktion gibt einen Wert zurück, der nur mit Kenntnis eines
    Laufzeitprotokolls (Retry, Transaktion) korrekt interpretierbar ist
  - Ein Glossareintrag in domain/ enthält eine Invariante, die von einem
    Systemarchitekten, nicht einem Domänenexperten beurteilt werden muss

Bei Unsicherheit: Kompetenzfrage des Glossareintrags prüfen. Wenn die Antwort
ein Systemarchitekt statt ein Domänenexperte liefern muss: H10.
```

---

### V6 — Learning-Schleife: Muster-Schwelle definieren

**Ziel:** Erfahrungsberichte münden zuverlässig in Regelentscheidungen.

**Änderung in `learning-matrix.md`**, Abschnitt 1:

```markdown
## 1.1 Muster-Schwelle

Ein Muster gilt als systemic, wenn:
  - es in mindestens 2 unabhängigen Sessions mit demselben Kern auftritt, oder
  - es einen HARD-Abbruch verursacht hat, oder
  - der Mensch es nach einem einzelnen Erfahrungsbericht als systemic markiert.

Systemische Muster werden in dieser Matrix eingetragen.
Nicht-systemische Einzelbeobachtungen bleiben im Erfahrungsbericht.
```

---

### V7 — AGENTS-COMPACT.md: Platzhalter-Block lesbar machen

**Ziel:** Instanziierte Werte klar abrufbar.

Der aktuelle Block (Zeile 10–13) ist eine zusammengeführte Wertreihe ohne
Struktur. Vorschlag: nach Instanziierung als saubere Tabelle formatieren:

```text
Projektname:          Regenbogen
Python-Package:       regenbogen
Source-Root:          src
Test-Root:            tests
Docs-Root:            docs
Tools-Root:           tools
Import-Check:         python tools/check_import_layers.py --preflight src tests tools
Lint:                 python -m ruff check .
Format-Check:         python -m ruff format --check .
Typecheck:            python -m mypy src
Tests:                python -m pytest
Vollvalidierung:      python tools/check_agent_docs_consistency.py --instantiated && ...
```

---

## 7. Prioritätsliste

| Priorität | Vorschlag | Begründung                                                          |
|-----------|-----------|----------------------------------------------------------------------|
| 1         | V1        | Einzige Schwäche mit empirisch belegtem Schadensmuster (chat.txt)   |
| 2         | V2        | Hoher Alltagsnutzen, reduziert Kontextlast bei SICHER-Tasks         |
| 3         | V3        | Glossar-Unreife ist latente Vertrauenslücke                         |
| 4         | V5        | H10 ist toter Code solange nicht operationalisiert                  |
| 5         | V4        | Trennung ist sauber, Aufwand gering, Wirkung mittel                 |
| 6         | V6        | Learning-Schleife ist derzeit auf Hoffnung gebaut                   |
| 7         | V7        | Kleiner Schönheitsfehler, trotzdem operativ störend                 |

---

## 8. Was nicht geändert werden sollte

Einige Eigenschaften des Systems sind Stärken und sollten nicht zur
"Vereinfachung" geopfert werden:

- **Abbruch-Kultur:** Der Reflex, bei semantischer Unklarheit zu stoppen statt
  weiterzumachen, ist der Kern des Systems. Einschränkungen hier würden den
  Zweck aushöhlen.
- **Maschinell prüfbare Invarianten:** Import-Checker, Testpflicht-Tool,
  Docs-Consistency-Check. Diese machen den Unterschied zwischen Regeln und
  verifizierbaren Regeln.
- **Sprechakt als formaler Übergabepunkt:** Neue Semantik entsteht nicht durch
  Implementierung. Das ist strukturell richtig und darf nicht aufgeweicht
  werden.
- **Getrennte Dokumente für verschiedene Lesebedürfnisse:** AGENTS-COMPACT +
  AGENTS.md ist die richtige Zweiteilung.

---

## 9. Übergeordnete Einschätzung

Das Priming-System ist inhaltlich ernsthaft und besser durchdacht als der
Durchschnitt. Es behandelt das richtige Problem: nicht Syntax-Kontrolle,
sondern Semantik-Kontrolle. Der Abbruch-als-Tugend-Grundsatz ist operativ
richtig.

Die Schwächen sind nicht konzeptueller Art. Sie sind Reifizierungsdefizite:
das System fordert Explizitheit, die es selbst an einigen Stellen noch
schuldet. Der Bridge-Exploit ist das deutlichste Beispiel: die Regel
"nicht einführen" ist vorhanden, aber das Verfahren "prüfe ob du es gerade
einführst" fehlt.

Das System ist für Greenfield gut geeignet. Für Brownfield braucht es V1
zwingend und zusätzlich einen expliziten Altlast-Modus, den es derzeit nicht
hat.

Das Forschungsziel — Priming als Lernobjekt — ist gut bedient. Die
Dokument-Trails (Sprechakte, Erfahrungsberichte, learning-matrix) erzeugen
genau das Material, aus dem sich Iterationen speisen können.
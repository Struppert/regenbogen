# BROWNFIELD-MIGRATION.md — Python-Projekt: Brownfield-Verfahren

> Ebene: MIXED-TRANSITION
> Primaerer Anteil: PRIMING
> Sekundaere Projektion: REPOSITORY
> Rolle: Brownfield-Aufnahme- und Migrationsprotokoll
> Autoritative Frage: Wie wird Bestand aufgenommen oder eine Box-Version migriert?
> Nicht zustaendig fuer: Inhalt menschlicher Zielmodellentscheidungen

**Dokumenttyp: Operativ / autoritativ fuer Brownfield-Arbeit**

> Brownfield ist keine Greenfield-Instanziierung.
>
> Ein bestehendes Projekt wird nicht ueberschrieben. Es wird aber auch nicht
> automatisch normativ bestaetigt.

---

## 0. Geltung

Dieses Dokument gilt, wenn eine `box-python`-Regelwelt in ein bestehendes
Projekt eingebracht oder dort aktualisiert wird.

Es unterscheidet drei Faelle:

```text
A. Bestehendes Python-Projekt ohne Agenten-Box aufnehmen
B. Bestehendes Box-Projekt auf neue Box-Version migrieren
C. Abgebrochene Erstinstanziierung reparieren
```

Nicht unter Brownfield fallen:

```text
Greenfield:
  frisches Zielprojekt, Box wird einmalig kopiert und instanziiert.

Normale Feature-Arbeit:
  Projekt ist bereits instanziiert und wird fachlich weiterentwickelt.
```

---

## 1. Grundregeln

```text
Keine Re-Instanziierung.
Kein globales Search/Replace.
Kein blindes Drueberkopieren der aktuellen Box.
Keine lokale operative Wahrheit durch Template-Default ersetzen.
Keine Altlast automatisch als Architektur bestaetigen.
Keine Known Breaches aus reiner Inventur erzeugen.
```

Ein vorhandener Import, Raum oder Sonderfall ist zuerst Befund, nicht Freigabe.

Brownfield schuetzt Bestand vor Ueberschreibung, aber nicht vor Bewertung.

`tools/instantiate/*` ist kein Brownfield-Werkzeug.

`--force` ist kein Brownfield-Upgrade-Mechanismus. Es ist nur fuer die
Reparatur einer fehlgeschlagenen, noch nicht produktiv weiterbearbeiteten
Erstinstanziierung zulaessig.

Template-Neuerungen sind kein automatischer lokaler Sollzustand. Eine neue
Box-Version ist ein Angebot neuer Regeln, Werkzeuge und Verfahren.

Brownfield trennt immer:

```text
Zielmodell-Entscheidung:
  Welche Template-Neuerungen werden lokale operative Wahrheit?

Migrationsmandat:
  Darf die festgelegte Migration jetzt auf das Repository wirken?
```

Die Annahme einer Template-Regel startet keine Migration.
Vor jeder transformativen Brownfield-Wirkung muss WG-MUTATION aus
`ausfuehrungsmandat-protokoll.md` gruen sein.

---

## 1a. Altlast-Modus: Hochrisikozone bekannter Brüche

Im Brownfield-Projekt ist jeder bekannte Regelbruch im Code eine
**Hochrisikozone**, keine Arbeitsfläche.

Warum: Ein Modell das auf Fortsetzbarkeit optimiert, liest vorhandene
und dokumentierte Abweichungen als implizit akzeptierte Praxis. Das ist
strukturell vorhersehbar und empirisch belegt. Es ist kein Agentenfehler,
sondern ein Systemrisiko wenn Brüche nicht aktiv gesperrt sind.

Die Sperre gilt **scope-basiert**, nicht dateibasiert. Eine Datei kann
einen bekannten Bruch enthalten, ohne dass jede Änderung darin gesperrt ist.
Die Sperre greift wenn die geplante Änderung den konkreten Scope berührt:

```text
  - eine konkrete Importkante oder ein konkretes Symbol
  - eine konkrete Funktion oder Klasse
  - eine konkrete öffentliche API-Fläche
  - einen explizit markierten Abschnitt
```

Wenn der Scope berührt wird:

```text
Default-Aktion: STOPP.

Schritt 1 — Known-Breach-Prüfung (package-schema.md + Checker):
  Ist die betroffene Stelle als Known Breach eingetragen?
  Hat der Eintrag eine explizite Änderungsregel?
  Ist die geplante Änderung durch diese Änderungsregel gedeckt?
  Wenn nein: passenden HARD- oder BF-Abbruch bestimmen.

Schritt 2 — Bridge-Prüfung (migration-bridges.md):
  Enthält der Scope ein Symbol aus der Bridge-Registry?
  Was ist dessen Agent-Aktion?
  Ist die geplante Änderung durch die Änderungsregel gedeckt?
  Wenn nein: H3 oder BF5 — nicht pauschal BF12.

Schritt 3 — Deckungsprüfung:
  Sind Known-Breach- und Bridge-Regeln beide erfüllt?
  Wenn ja: fortfahren, Evidence notieren.
```

Known Breaches (package-schema.md) und Migration Bridges (migration-bridges.md)
sind unterschiedliche Registries. Eine Datei kann einen Known Breach enthalten
ohne Bridge-Symbole zu besitzen, und umgekehrt. Beide Schritte sind separat
zu prüfen.

Neuer Code darf nicht gegen einen bekannten Bruch implementiert werden,
auch wenn das technisch einfacher wäre als die kanonische Lösung.

Bekannte Brüche im Code sind stärker sichtbar als Registry-Einträge. Das
macht sie gefährlicher, nicht akzeptabler.

---
## 2. Wahrheit, Befund und Entscheidung

Lokale operative Wahrheit ist nur, was durch die zustaendigen Projektartefakte
normativ festgelegt wurde:

```text
AGENTS.md
package-schema.md
Glossare
sprechakt-protokoll.md / Sprechakt-Artefakte
regelmatrix.md
test-obligations.md
migration-bridges.md
```

Nicht automatisch lokale operative Wahrheit:

```text
vorhandener Code
bestehende Imports
alte Tests
historische Workarounds
faktische Build-Konfiguration
eingewachsene Dateistruktur
```

Diese Dinge sind zuerst Projektionen oder Evidence ueber den Bestand. Sie
koennen mit der lokalen operativen Wahrheit uebereinstimmen, von ihr abweichen
oder noch unklassifiziert sein.

Brownfield unterscheidet diese Zustaende:

| Zustand | Bedeutung | Wer entscheidet? |
| --- | --- | --- |
| `Observed State` | Im Bestand tatsaechlich vorgefunden. | Agent beobachtet und belegt. |
| `Unknown / Unclassified` | Befund ist noch nicht ausreichend verstanden. | Agent stoppt oder legt Entscheidungsfrage vor. |
| `Accepted Local Truth` | Explizit als gueltige lokale Regel oder Architektur bestaetigt. | Mensch / zustaendiger Sprechakt. |
| `Accepted Alternative` | Abweichung vom Template, aber lokal konsistent und akzeptiert. | Mensch / zustaendiger Sprechakt. |
| `Migration Candidate` | Soll angenaehert oder umgebaut werden, ist aber kein akuter Defekt. | Mensch legt Zielrichtung fest. |
| `Legacy Defect` | Vorhandener Zustand verletzt eine gueltige lokale Invariante. | Mensch bestaetigt Defektstatus oder Zielmodell. |
| `Known Breach` | Explizit, begrenzt und vorlaeufig geduldeter Regelbruch. | Mensch genehmigt; Checker begrenzt Kante. |

Ein Agent darf vorlaeufig klassifizieren. Er darf nicht allein aus Bestand
`Accepted Local Truth`, `Accepted Alternative` oder `Known Breach` machen.

---

## 3. Brownfield-Pipeline

Brownfield-Aufnahme und Brownfield-Migration laufen in dieser Reihenfolge:

```text
1. Discover
   Dateien, Abhaengigkeiten, Tests, APIs, Regeln und Brueche erfassen.

2. Describe
   Den vorgefundenen Zustand ohne normative Bewertung dokumentieren.

3. Classify
   Befunde vorlaeufig semantischen Raeumen und Zustaenden zuordnen.

4. Decide
   Mensch bestaetigt akzeptierte Architektur, Defekte, Migration Candidates,
   Known Breaches oder offene Befunde.

5. Plan
   Migrationsplan aus Zielmodellentscheidung, Baseline, Datei-Aktionsmatrix
   und Risiken ableiten.

6. Mandate
   Menschliches Migrationsmandat fuer Grundlage, Version und Scope
   einholen oder nachweisen.

7. Migrate
   Geplante Aenderungen nur mit aktivem Migrationsmandat durchfuehren.

8. Verify
   Baseline, Zielregeln, Tests und Evidence gegeneinander pruefen.
```

Geltung:

```text
Discover / Describe  = deskriptiv
Classify             = vorlaeufig
Decide               = normativ
Plan                 = vorbereitend
Mandate              = deontisch
Migrate              = transformativ
Verify               = pruefend
```

Harte Regel:

```text
Die Brownfield-Inventur erzeugt keine Known Breaches.
```

Sie erzeugt Befunde, Evidence, vorlaeufige Klassifikationen und
Entscheidungsvorlagen. Ein Known Breach entsteht erst nach expliziter
menschlicher Entscheidung.

---

## 4. Datei-Aktionsmatrix

Jede Datei wird vor einer Brownfield-Aenderung klassifiziert.

| Klasse | Bedeutung | Aktion |
| --- | --- | --- |
| `add` | Neues Template-Artefakt existiert lokal noch nicht. | Hinzufuegen, wenn keine lokale Datei gleichen Namens existiert. |
| `preserve` | Lokales Projektartefakt gehoert dem Zielprojekt. | Nicht ersetzen. Nur Befund oder Vorschlag dokumentieren. |
| `merge` | Box-Regel mit lokalen Projektanpassungen. | Semantisch mergen, keine pauschale Ersetzung. |
| `replace` | Tool oder Datei ohne lokale Projektanpassung. | Ersetzen nach Diff und Freigabe moeglich. |
| `inspect` | Lokale Anpassung oder unklarer Ursprung. | Erst diffen, dann Entscheidung dokumentieren. |
| `forbidden` | Re-Instanziierungs- oder Evidence-Datei. | Nicht aendern, ausser der Auftrag benennt genau diese Datei. |

Standardklassifikation:

| Datei / Bereich | Brownfield-Aktion |
| --- | --- |
| `README.md` | `preserve` |
| `AGENTS.md` | `merge` |
| frueheres `AGENTS-COMPACT.md` | `inspect` oder entfernen, wenn AGENTS.md als Router migriert ist |
| `AGENT-SETUP.md` | `inspect` oder nach `docs/agent-box-instantiation.md` archivieren |
| `.agent-box-template.md` | `inspect` im Template, `forbidden` im Zielprojekt |
| `blocker-und-abbruch-protokoll.md` | `add` oder `merge` |
| `ausfuehrungsmandat-protokoll.md` | `add` oder `merge` |
| `grundsatz.md` | `add` oder `preserve` |
| `package-schema.md` | `merge` |
| `preflight-checkliste.md` | `merge` |
| `task-schnitt.md` | `merge` |
| `sprechakt-protokoll.md` | `merge` |
| `regelmatrix.md` | `merge` |
| `test-obligations.md` | `merge` |
| `migration-bridges.md` | `merge` |
| `learning-matrix.md` | `preserve` oder `merge` |
| `erfahrungsbericht-protokoll.md` | `add` oder `merge` |
| `docs/plans/template.md` | `merge` |
| `docs/runs/checkpoint-template.md` | `add` oder `merge` |
| `glossar-domain.md` | `preserve` oder `merge` |
| `glossar-system.md` | `preserve` oder `merge` |
| `glossar-meta.md` | `add` oder `merge` |
| `glossar-README.md` | `merge` |
| `tools/check_import_layers.py` | `replace` wenn unveraendert, sonst `merge` |
| `tools/check_agent_docs_consistency.py` | `replace` wenn unveraendert, sonst `merge` |
| `tools/resolve_test_obligations.py` | `replace` wenn unveraendert, sonst `merge` |
| `tools/instantiate/*` | `forbidden` fuer laufende Projekte |
| `.agent-box/instantiation.md` | `forbidden` |
| `.agent-box/adoption.md` | `forbidden`, ausser Verfahren A erzeugt den Marker |
| `.agent-box/migrations/` | `add` |

---

## 5. Artefakttrennung

Brownfield trennt vier Artefaktarten:

```text
Baseline:
  Was ist jetzt? Rein deskriptiv.

Zielmodell:
  Was soll gelten? Normativ, in den zustaendigen Projektartefakten.

Migrationsplan:
  Wie kommen wir vom aktuellen Zustand zum Zielmodell?

Migrationsevidence:
  Was wurde tatsaechlich getan, geprueft, verworfen oder offengelassen?
```

Diese Artefakte duerfen in einer kleinen Migration in einer Datei kombiniert
werden, muessen dann aber durch Ueberschriften getrennt bleiben.

Wenn eine Brownfield-Migration lokale Governance-Regeln oder deren
Erzwingungsprojektionen korrigiert, aber das vollstaendige
Governance-Provenienzsystem noch nicht eingefuehrt ist, muss vor Abschluss
eine kleine vorlaeufige Evidence existieren. Sie ist dokumentierend, nicht
normativ.

Minimalformat:

```markdown
## Vorlaeufige Brownfield-Governance-Evidence

Status: vorlaeufig
Autoritaet: dokumentierend, nicht normativ
Ausgangs-Template:
Zielmodellentscheidungsreferenz:
Contract-ID:
Run-ID:
Plan-ID:
Plan-Version:
Plan-Revision: <Plan-ID>@<Plan-Version>
Priming-Revision:
Scope-ID:
Scope-Version:
Migrationsmandat-ID:
Mandatsrevision:
Authorization-Revision: <Migrationsmandat-ID>@<Mandatsrevision>
Lokaler Governance-Stand vor Aenderung:
Lokaler Governance-Stand nach Aenderung:
Vorher-Commit oder Snapshot:
Nachher-Commit oder Snapshot:
Anlass:

## Bewusste lokale Governance-Aenderungen

- ...

## Zurueckgestellte Provenienzmechanismen

- <fuer diese Migration bewusst zurueckgestellt>

## Upstream-Status

Rueckflussstatus: LOCAL-ONLY | ERFAHRUNGSBERICHT | TEMPLATE-CANDIDATE | TOOLING-CANDIDATE | UNKNOWN | NO-RETURN

## Governance-Rueckfluss

Lokale Governance geaendert: ja | nein

### Lokaler Befund

Was musste lokal geaendert werden?

### Ursache

Welche Schwäche des Templates oder der Migration wurde sichtbar?

### Lokaler Anteil

Was ist ausschliesslich projektspezifisch?

### Verallgemeinerbarer Kern

Welche allgemeine Regel oder Fehlerklasse koennte fuer das Template relevant
sein?

## Analyse nach Validierung

Tatsaechlich geaenderte Governance-Dateien:
Konformitaet mit Zielmodellentscheidung bestaetigt:
Bestaetigt durch:
Bestaetigungsdatum:
Unbeabsichtigte Drift:
Rueckflusskandidat:
```

Reihenfolge:

```text
alter Governance-Zustand festhalten
-> Zielmodellentscheidung belegen
-> Migrationsplan und Mandat belegen
-> lokale Korrektur ausfuehren
-> validieren
-> tatsaechliche Aenderungen analysieren
-> Konformitaet mit der Zielmodellentscheidung bestaetigen
-> neuen Zustand als akzeptierten lokalen Stand festhalten
```

Keine neue Governance-Baseline vor Analyse und menschlicher Bestaetigung.

Fuer groessere Brownfield-Aufnahmen bevorzugt:

```text
.agent-box/migrations/YYYY-MM-DD-<kurzname>-baseline.md
.agent-box/migrations/YYYY-MM-DD-<kurzname>-target.md
.agent-box/migrations/YYYY-MM-DD-<kurzname>-plan.md
.agent-box/migrations/YYYY-MM-DD-<kurzname>-evidence.md
```

Nach einer erfolgreichen Brownfield-Aufnahme ohne vorherige Box existiert
zusaetzlich der kanonische Adoptionsmarker:

```text
.agent-box/adoption.md
```

Minimalformat:

```markdown
# Brownfield-Adoption

Status: active
Aufnahmetyp: brownfield
Box-Name: box-python
Box-Version: v<ziel>
Datum:
Zielmodellentscheidung:
Migrationsmandat:
  Mandat-ID:
  Mandatstatus:
  Mandatsgrundlage: Plan
  Grundlagen-ID:
  Grundlagen-Version:
  Scope:
  Geschuetzte Dateien:
  Freigabereferenz:
Erstes Migrationsartefakt:

## Geltung

Dieses Projekt wurde brownfield in die Agenten-Box aufgenommen.
Greenfield-Instanziierung ist verboten.
```

`tools/instantiate/instantiate_project_box.py` muss abbrechen, wenn
`.agent-box/adoption.md` existiert. `--force` darf diesen Marker nicht
uebergehen.

Versionsspezifische Migrationsanweisungen gehoeren in das aktuelle Template,
das Changelog oder einen eigenen Migrationsplan. Dieses Dokument definiert das
stabile Verfahren.

---

## 6. Brownfield-Preflight

Vor jeder Brownfield-Arbeit erfassen:

```text
Projektpfad:
Brownfield-Fall: A | B | C
Ausgangsversion:
Zielversion:
Vorhandene Agentenartefakte:
Projektmarker .agent-box/instantiation.md vorhanden: ja/nein
Projektmarker .agent-box/adoption.md vorhanden: ja/nein
Markerzustand fuer Fall:
  A vor Aufnahme: kein Marker erwartet
  A Abschluss: genau adoption.md erwartet
  B: genau ein Herkunftsmarker erwartet
  C: instantiation.md-Zustand erfassen, adoption.md darf nicht vorhanden sein
Historischer Baseline-Anker:
Aktuelle Ausfuehrungsbaseline:
Vorhandene lokale Architekturregeln:
Aktuelle Test-/Check-Befehle:
Bekannte rote Checks:
Erkannte Regelverletzungen:
Bereits akzeptierte Known Breaches:
Unklassifizierte Altverstoesse:
Migration Candidates:
Aktive Migration Bridges:
Lokale Tool-Anpassungen:
Geschuetzte Dateien im SWS:
```

Pflichtfragen:

```text
Ist der Observed State ausreichend beschrieben?
Ist die aktuelle Ausfuehrungsbaseline bekannt?
Sind lokale Aenderungen an Box-Artefakten sichtbar?
Gibt es eine bestehende .agent-box/instantiation.md?
Gibt es eine bestehende .agent-box/adoption.md?
Welcher Markerzustand ist fuer den Brownfield-Fall korrekt?
Ist der historische Baseline-Anker bestimmt?
Ist die aktuelle Ausfuehrungsbaseline getrennt dokumentiert?
Gibt es schon .agent-box/migrations/?
Welche Dateien sind add / preserve / merge / replace / inspect / forbidden?
Welche Befunde brauchen menschliche Entscheidung?
Welche Checks sind deskriptiv, welche bereits normativ?
```

Wenn die Baseline unbekannt ist, zuerst Baseline herstellen oder dokumentieren.
Keine Migration starten, deren Ausgangszustand nicht beschrieben ist.

---

## 7. Historischer Baseline-Anker und Ausfuehrungsbaseline

```text
Historischer Baseline-Anker:
  Herkunftspunkt, gegen den lokale Divergenz bestimmt wird.
  Fall B: bevorzugt Instanziierungs-Commit, sonst letzter eindeutig belegter
  Box-Migrationsstand.
  Fall A: vor Beginn der Aufnahme Anker-Commit oder Tag festhalten.
  Fall C: Zustand unmittelbar vor der fehlgeschlagenen Instanziierung oder
  letzter sicherer Zustand.

Aktuelle Ausfuehrungsbaseline:
  Checks, Tests, Lint, Typecheck und bekannte rote Befunde unmittelbar vor
  der Migration.
```

Der historische Baseline-Anker beschreibt, woraus lokale Divergenz entstanden
ist. Die aktuelle Ausfuehrungsbaseline beschreibt, welche Checks und Befunde
unmittelbar vor dem Lauf gelten. Beide duerfen nicht vermischt werden.

---

## 8. Verfahren A: Bestehendes Python-Projekt ohne Box aufnehmen

Ziel: Lokale Agentenregeln einfuehren, ohne bestehende Projektstruktur zu
ueberschreiben oder automatisch zu bestaetigen.

Phasen:

```text
A1 Discover:
   Projektstruktur, Abhaengigkeiten, Tests, Tooling, APIs, Dokumente,
   Einstiegspunkte, Konfiguration und oeffentliche Flaechen erfassen.

A2 Describe:
   Deskriptive Raumkarte und Baseline schreiben. Keine Known Breaches erzeugen.

A3 Classify:
   Befunde vorlaeufig als Observed State, Unknown,
   Accepted-Alternative-Kandidat, Migration Candidate oder
   Legacy-Defect-Kandidat markieren.

A4 Decide:
   Mensch legt lokale operative Wahrheit, Zielmodell, zu reparierende Defekte,
   vorlaeufige Known Breaches und offene Befunde fest.

A5 Plan:
   Migrationsplan fuer AGENTS.md, package-schema.md, Glossare, Checker,
   Testpflichten, Bridges und Adoptionsmarker ableiten.

A6 Mandate:
   Menschliches Migrationsmandat fuer Grundlage, Version und Scope einholen oder
   nachweisen.

A7 Migrate:
   Nur mandatsgedeckte Schnitte umsetzen. Keine pauschale Template-Ersetzung.

A8 Verify:
   Checks gegen Zielmodell ausfuehren. Vorher rote Checks als Baseline belegen.
```

Dieser Fall ist eine Aufnahme- und Reifizierungsphase. Er braucht menschliche
Entscheidungen fuer Raumkarte, Schreibrechte, Tests, geschuetzte Dateien und
bekannte Regelverletzungen.

`.agent-box/instantiation.md` darf dabei nicht als Greenfield-SP0 gefaelscht
werden.

Brownfield-Aufnahme ist abgeschlossen, wenn:

```text
.agent-box/adoption.md existiert.
Erstes Migrationsartefakt unter .agent-box/migrations/ existiert.
Zielmodell ist in die zustaendigen Projektartefakte projiziert.
Offene Befunde sind dokumentiert.
Genehmigte Known Breaches sind begrenzt und maschinell pruefbar, soweit moeglich.
Baseline ist archiviert.
Aktuelle Box-Version ist festgehalten.
Re-Instanziierung ist durch .agent-box/adoption.md blockiert.
```

---

## 9. Verfahren B: Bestehendes Box-Projekt migrieren

Ziel: Eine bereits instanziierte oder brownfield-adoptierte
Box-Projektwahrheit auf eine neuere Box-Version nachziehen.

Vorgehen:

```text
1. Herkunftsmarker bestimmen:
   genau eine Datei aus .agent-box/instantiation.md oder .agent-box/adoption.md.
2. Ausgangsversion aus dem Herkunftsmarker und bisherigen Migrationen lesen.
3. Zielversion der Box bestimmen.
4. Historischen Baseline-Anker bestimmen.
5. Aktuelle Ausfuehrungsbaseline erfassen.
6. Changelog und versionsspezifische Migrationshinweise der Box lesen.
7. Observed State und Baseline der betroffenen Artefakte erfassen.
8. Lokale Divergenz gegen Baseline-Anker inventarisieren.
9. Datei-Aktionsmatrix mit Merge-Richtung erstellen.
10. Zielmodell-Abweichungen und Datei-Aktionsmatrix vorlegen.
11. Menschliche Zielmodellentscheidungen einholen.
12. Migrationsplan finalisieren und Grundlage/Version festlegen.
13. Migrationsmandat fuer Grundlage, Version und Scope einholen.
14. WG-MUTATION ist fortlaufende Invariante: bleibt asserted solange Gate-Zustand
    unveraendert. Vor jeder Aktion pruefen ob sie in der freigegebenen Aktionsmatrix
    liegt. Vollstaendige Neubewertung nur bei Zustandswechsel (Wirkungstyp, Scope,
    Mandatsstatus, Grundlagenversion).
15. Neue Artefakte mit Aktion add uebernehmen.
16. Geschuetzte Regeldateien semantisch mergen.
17. Tools mit lokaler Divergenz per Drei-Wege-Merge behandeln.
18. Migrationsevidence fortschreiben.
19. Abschlusschecks ausfuehren.
20. Migrationsevidence versiegeln.
```

Aktuelle Box-Version:

```text
Zielversion der juengsten Migration mit Status abgeschlossen,
sonst Box-Version des Herkunftsmarkers.
```

Abgebrochene Migrationen aktualisieren die aktuelle Box-Version nicht. Sie
bleiben Evidence fuer Recovery und Wiedereinstieg.

Lokale Divergenz gegen Baseline-Anker wird in der Migrationsevidence getrennt
erfasst:

```text
## Lokale Divergenz gegen Baseline-Anker

### Konfiguration
### Logik
### Semantik/Inhalt
### Formatierung
### Nur lokal vorhandene Artefakte
```

Fuer jede Datei mit Aktion `merge` wird zusaetzlich dokumentiert:

```text
Merge-Richtung: lokal als Basis | Template als Basis
Begruendung:
Erhaltungsnachweis:
```

Bei Tools mit lokaler Divergenz gilt:

```text
1. neues Template gegen Baseline-Anker diffen.
2. lokalen Stand gegen Baseline-Anker diffen.
3. jede lokale semantische Hunk klassifizieren.
4. Merge-Richtung dokumentieren.
5. lokale Hunks re-applizieren.
6. Ergebnis gegen beide Deltas pruefen.
```

Kein History-Filter ersetzt den zeilenweisen Review.

Eine Template-Neuerung ist nicht automatisch lokale operative Wahrheit. Sie
wird ueber `merge`, Entscheidung und Projektion in das Zielprojekt uebernommen.

---

## 10. Verfahren C: Abgebrochene Erstinstanziierung reparieren

Ziel: Einen fehlgeschlagenen Erstlauf reparieren, bevor das Projekt produktiv
weiterbearbeitet wurde.

Zulaessig nur wenn:

```text
Projekt wurde noch nicht fachlich weiterentwickelt.
Keine lokalen semantischen Projektentscheidungen wurden nach dem Fehlversuch getroffen.
Der Fehlerzustand ist dokumentiert.
Ein Mensch gibt die Reparatur mit Grundlage, Version und Scope ausdruecklich frei.
```

In diesem Fall gilt:

```text
1. Reparaturplan festhalten.
2. Reparaturmandat fuer Plan, Version und Scope einholen.
3. WG-MUTATION pruefen.
4. --force nur innerhalb dieses Scopes verwenden.
```

Dann kann `tools/instantiate/instantiate_project_box.py --force` zulaessig
sein.

Nicht zulaessig fuer:

```text
Upgrade auf neue Box-Version.
Nachziehen neuer Template-Regeln.
Migration eines produktiv bearbeiteten Projekts.
Ersetzen lokaler Projektwahrheit.
Uebergehen von .agent-box/adoption.md.
```

---

## 11. Migrationsevidence

Jede Brownfield-Migration schreibt mindestens ein Markdown-Artefakt:

```text
.agent-box/migrations/YYYY-MM-DD-v<quelle>-to-v<ziel>-<kurzname>.md
```

Fuer Fall A ohne vorherige Box gilt stattdessen:

```text
.agent-box/migrations/YYYY-MM-DD-unboxed-to-v<ziel>-aufnahme.md
```

Minimalformat:

```markdown
# Brownfield-Migration: <Kurzname>

Status: offen | festgelegt | abgeschlossen | abgebrochen
Brownfield-Fall: A | B | C
Ausgangsversion:
Zielversion:
Datum:
Contract-ID:
Run-ID:
Base-Snapshot:
Ausfuehrungsprofil:
Zielmodellentscheidung:
Migrationsmandat:
  Mandat-ID:
  Mandatstatus:
  Mandatsgrundlage: Plan
  Grundlagen-ID:
  Grundlagen-Version:
  Scope:
  Geschuetzte Dateien:
  Freigabereferenz:

## Baseline

## Observed State

## Datei-Aktionsmatrix

## Vorlaeufige Klassifikation

## Menschliche Entscheidungen

## Migrationsplan

## Migrationsmandat

## Zielmodell / Projektionen

## Uebernommene Aenderungen

## Bewusst nicht uebernommene Aenderungen

## Legacy Defects

## Known Breaches

## Ausgefuehrte Checks

## Offene Warnungen

## Governance-Rueckfluss

Lokale Governance geaendert: ja | nein

### Lokaler Befund

Was musste lokal geaendert werden?

### Ursache

Welche Schwaeche des Templates oder der Migration wurde sichtbar?

### Lokaler Anteil

Was ist ausschliesslich projektspezifisch?

### Verallgemeinerbarer Kern

Welche allgemeine Regel oder Fehlerklasse koennte fuer das Template relevant
sein?

### Rueckflussstatus

LOCAL-ONLY | ERFAHRUNGSBERICHT | TEMPLATE-CANDIDATE | TOOLING-CANDIDATE |
UNKNOWN | NO-RETURN

## Abschlussentscheidung
```

Migrationsevidence ist kein Ersatz fuer Sprechakte. Wenn eine Migration neue
Projektbedeutung festlegt, ist zusaetzlich ein Sprechakt noetig.

---

## 12. Known-Breach-Regel

Ein Known Breach darf nie die Standardausgabe einer Brownfield-Aufnahme sein.

Ein Known Breach braucht mindestens:

```text
konkrete verletzte Regel oder Importkante
konkrete Datei oder Symbolmenge
Begruendung, warum vorlaeufig geduldet
Folgeplan
No-growth-Regel
Review- oder Ablaufpunkt
Checker-Eintrag, wenn maschinell pruefbar
explizite menschliche Freigabe
```

Ein Known Breach erweitert keine Architektur. Er begrenzt eine bekannte
Abweichung, bis sie repariert, ersetzt oder bewusst als Accepted Alternative
in das Zielmodell ueberfuehrt wird.

---

## 13. Abschlusschecks

Nach Brownfield-Migration mindestens:

```bash
python tools/check_agent_docs_consistency.py --instantiated
python tools/check_import_layers.py --preflight src tests tools
python tools/resolve_test_obligations.py --selfcheck --instantiated
```

Zusaetzlich die projektlokalen Lint-, Typecheck- und Testbefehle ausfuehren,
sofern eine Baseline existiert.

Wenn ein Check bereits vor der Migration rot war, muss die Migrationsevidence
das als Ausgangszustand dokumentieren.

---

## 14. Abbruchbedingungen

BF-Codes sind Brownfield-spezifische HARD-Abbrueche. Sie gelten nur in
Brownfield-Arbeit und werden im Brownfield-Migrationsraum belegt.

Brownfield-Migration stoppt bei:

```text
BF1   Observed State nicht ausreichend bestimmbar
BF2   Baseline unbekannt und fuer die Migration relevant
BF3   geschuetzte Datei ohne Migrationsentscheidung betroffen
BF4   Datei als forbidden klassifiziert, aber Aenderung waere noetig
BF5   Konflikt zwischen Template-Regel und lokaler Projektregel
BF6   Tool-Ersetzung wuerde lokale Anpassungen ueberschreiben
BF7   Migration wuerde neue Projektsemantik ohne Sprechakt erzeugen
BF8   --force waere noetig, obwohl es kein Reparaturfall C ist
BF9   Observed State wuerde ohne Entscheidung als Accepted Local Truth behandelt
BF10  Brownfield-Inventur wuerde automatisch Known Breaches erzeugen
BF11  Baseline, Zielmodell, Migrationsplan und Evidence werden vermischt
BF12  Agent muesste menschliche Architekturentscheidung selbst treffen
```

Bei BF-Abbruch: Evidence schreiben, keine weiteren Dateien aendern, bis ein
Mensch den naechsten Schritt festlegt.

BF-Abbruch-Evidence liegt im Brownfield-Migrationsraum:

```text
.agent-box/migrations/YYYY-MM-DD-BF<nr>-<kurzbeschreibung>-abbruch.md
```

Minimalformat:

```markdown
# Brownfield-Abbruch: <Kurzbeschreibung>

Status: abgebrochen
BF-Code:
Datum:
Aufgabe:

## Observed State

## Baseline

## Betroffene Dateien

## Letzter sicherer Zustand

## Offene Entscheidung

## Verbotene nächste Aktion

## Wiedereinstiegspunkt
```

BF-Abbruch-Evidence ersetzt kein normales Erfahrungsbericht-Artefakt, wenn nach
`erfahrungsbericht-protokoll.md` ein Bericht faellig ist.

---

## 15. Schlussregel

Brownfield-Arbeit ist erfolgreich, wenn der Unterschied zwischen Bestand,
akzeptierter Architektur, Altlast und geplanter Migration ausdruecklicher ist
als vorher.

Wenn ein Template-Default eine lokale Entscheidung verdeckt, war die Migration
falsch.

Wenn ein vorhandener Zustand ohne Entscheidung als Architektur gilt, war die
Migration ebenfalls falsch.

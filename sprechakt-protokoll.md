# sprechakt-protokoll.md — Python-Projekt

> Dieses Dokument wird geladen, wenn ein Sprechakt nötig ist oder erwartet wird.
>
> Vollständige operative Regeln: `AGENTS.md`.

---

## 1. Was ein Sprechakt ist

Ein Sprechakt ist eine menschliche Festlegung.
Der Agent analysiert, benennt Widersprüche, macht Vorschläge — entscheidet aber nicht.

Sprechakt ≠ Abbruch: kein Regelverstoß, aber korrekte Fortsetzung braucht menschliche Festlegung.
Vollständige Unterscheidung Sprechakt / Abbruch / Plan / Erfahrungsbericht: `regelmatrix.md`.

---

## 2. Sprechakt-Klassen

### SP0 — Instanziierungs-Sprechakt

Der Instanziierungs-Sprechakt ist der einmalige initiale Sprechakt, der eine
Template-Box in einem Zielprojekt materialisiert. Er setzt mindestens:

```text
Projektanzeigename
Python-Package-Name
Source-/Test-/Docs-/Tools-Wurzeln
Geltung der lokalen Agentenregeln
```

Er wird toolgestützt durch `tools/instantiate/instantiate_project_box.py` vollzogen
und durch `.agent-box/instantiation.md` belegt. Er wird nicht als normales
Sprechakt-Artefakt unter `docs/sprechakte/` nachgeführt. Eine Wiederholung ist
verboten, außer ein Mensch gibt `--force` ausdrücklich frei.


Kanonische Quelle für SP0: `AGENTS.md` Abschnitt 7.

### SP1–SP7 — Operative Sprechaktklassen

Die folgenden Klassen gelten für Sprechakte während der normalen Projektarbeit.
Sie sind keine Unterpunkte von SP0.

Kanonische Quelle für SP1–SP7: `AGENTS.md` Abschnitt 7.

```text
SP1  Neuer Fachbegriff würde entstehen
SP2  Neuer systemsemantischer Steuerwert würde entstehen
SP3  Neue Fehlerklasse oder neue Fehlerbedeutung würde entstehen
SP4  Neue Runtime-Dependency würde eingeführt
SP5  Binding-Code würde einen neuen Begriff einführen
SP6  Bekannter Bruch würde verschoben oder umklassifiziert
SP7  Semantic Working Set enthält einen aktiv benötigten Begriff,
    dessen Glossareintrag fehlt oder unvollständig ist
```

---

## 3. Statusmodell

Jedes normale Sprechakt-Artefakt hat genau einen Status:

```text
offen
festgelegt
abgelehnt
superseded
```

Bedeutung:

```text
offen       Entscheidung fehlt; Agent darf die betroffene Bedeutung nicht erfinden.
festgelegt  Entscheidung gilt und muss in operative Artefakte zurückfließen.
abgelehnt    Vorschlag wurde verworfen und darf nicht still erneut eingeführt werden.
superseded   Entscheidung wurde ersetzt und muss auf den Nachfolger verweisen.
```

Ein festgelegter Sprechakt muss mindestens eine Folgeprojektion nennen, z. B.
`AGENTS.md`, `package-schema.md`, `test-obligations.md`, `glossar-domain.md`,
`glossar-system.md`, `migration-bridges.md` oder `learning-matrix.md`.

## 4. SP7: Erst Task-Schnitt

SP7 ist der häufigste Fall.

Zuerst prüfen:

```text
Ist der fehlende Begriff nur durch zu breiten Schnitt im SWS?
Kann die Aufgabe enger geschnitten werden?
Kann der Begriff in eine spätere Iteration verschoben werden?
```

Wenn ja: enger schneiden. Kein Sprechakt nötig.
Wenn nein: Sprechakt SP7.

---

## 5. Was vor dem Sprechakt zu prüfen ist

```text
1. Begriff oder Grenze benennen
2. Relevante Datei(en) benennen
3. Semantischen Raum bestimmen
4. package-schema.md prüfen
5. Relevante Glossareinträge prüfen
6. Code-Situation prüfen
7. Tests / Projektionen prüfen
8. Widerspruch oder Lücke konkret benennen
9. Vorschlag optional formulieren
```

Nicht erlaubt: raten, still fortfahren, Begriff ad hoc im Code erzeugen,
Test als Semantikquelle verwenden, Adapter als Semantikquelle verwenden,
pyproject.toml ändern, um Problem praktisch zu lösen.

---

## 6. Sprechakt-Artefakt

Ort: `docs/sprechakte/YYYY-MM-DD-kurzbeschreibung.md` (append-only, nicht in `tmp/`).

Format:

```markdown
# Sprechakt: <Kurzbeschreibung>

Aufgabe:          <was sollte gemacht werden>
Zeitpunkt:        YYYY-MM-DD HH:MM
Sprechakt-Klasse: SP<Nummer> — <Regeltext>
Betroffener Begriff / Grenze: <Name>
Status: offen
Folgeartefakte:
Ersetzt:
Ersetzt durch:

## Was fehlt

<Welches Feld fehlt: Begriff / Bedeutungsebene / Invariante / Projektion / Entscheidung>

## Was der Agent sieht

symbol:
package_says:
glossar_says:
code_says:
tests_say:
schema_says:

## Analyse des Agenten

<Was ist konsistent? Was ist unstimmig? Welche Fortsetzung wäre riskant?>

## Vorschlag des Agenten

<Optional. Klar als Vorschlag markieren.>

## Warum der Agent nicht fortfahren kann

<Ein Satz: welche Festlegung fehlt und warum sie für korrekte Fortsetzung nötig ist.>

## Was der Mensch festlegt

<Wird nach menschlicher Entscheidung ergänzt.>

## Was der Agent danach tut

<Wiedereinstiegspunkt nach Festlegung.>
```

---

## 7. Beispiele

**SP1 — Neuer Fachbegriff**

Aufgabe verlangt `CustomerSegment`.
Glossar enthält `Customer`, aber kein `CustomerSegment`.
Tests erwarten Verhalten nach Segment.
→ Agent darf `CustomerSegment` nicht einführen. Sprechakt SP1.

**SP3 — Neue Fehlerbedeutung**

HTTP 409 soll als `BusinessConflict` behandelt werden.
`BusinessConflict` wäre fachliche Bedeutung — Adapter darf das nicht still entscheiden.
→ Sprechakt SP3.

**SP4 — Neue Dependency**

Aufgabe wäre einfacher mit neuer Library. `pyproject.toml` müsste geändert werden.
→ Sprechakt SP4 oder Freigabe nötig.

**SP5 — Adapter erzeugt Semantik**

Adapter mappt leeres Feld auf `PremiumCustomer`.
Adapter übersetzt nicht mehr — er erfindet Fachbedeutung.
→ Sprechakt SP5.

---

## 8. State bei aktivem Sprechakt

```markdown
Status:             WARTET AUF SPRECHAKT
Sprechakt-Klasse:   SP<Nummer>
Sprechakt-Artefakt: docs/sprechakte/YYYY-MM-DD-kurzbeschreibung.md
Wiedereinstieg:     <konkreter Schritt>
```

---

## 9. Wiedereinstieg nach Sprechakt

```text
1. Sprechakt-Artefakt lesen
2. Festlegung lesen
3. Prüfen ob package-schema.md oder Glossar nachgezogen werden muss
4. Schreibrechte prüfen
5. Preflight erneut ausführen
6. An Wiedereinstiegspunkt fortsetzen
```

Wenn Festlegung neue Widersprüche erzeugt:
nicht fortfahren. Neuer Abbruch oder neuer Sprechakt.

---

## 10. Schlussregel

Ein Agent darf fehlende Bedeutung nicht durch plausible Implementierung ersetzen.

Wenn Bedeutung fehlt: Schnitt prüfen. Sprechakt auslösen. Warten.

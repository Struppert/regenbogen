# erfahrungsbericht-protokoll.md — Python-Projekt

> Dieses Dokument regelt wann, was und wie Erfahrungsberichte geschrieben werden.
>
> Vollständige operative Regeln: `AGENTS.md`.

---

## 1. Was ein Erfahrungsbericht ist

Ein Erfahrungsbericht ist kein Abbruch-Artefakt und kein Plan.

```text
Abbruch-Artefakt:      Was ist schiefgelaufen? Evidence für Wiedereinstieg.
Sprechakt-Artefakt:    Was muss der Mensch entscheiden?
Plan:                  Was wird als nächstes getan?
Erfahrungsbericht:     Was hat diese Session über das System gelehrt?
```

Erfahrungsberichte sind operative Lernprotokolle.
Sie verbessern das System — nicht die aktuelle Aufgabe.

---

## 2. Wann ein Erfahrungsbericht geschrieben wird

### Pflicht

```text
E1  Nach abgeschlossener Agentensession mit Plan, MITTEL-Task,
    Sprechakt, Task-Schnitt, öffentlicher API-Änderung oder Dokumentdrift.

E2  Nach jedem HARD-Abbruch.
    Zusätzlich zum Abbruch-Artefakt — Abbruch-Artefakt beschreibt den Stopp,
    Erfahrungsbericht beschreibt das Gelernte.

E3  Nach sichtbarer Systemschwäche.
    Auch wenn die Session erfolgreich abgeschlossen wurde.

E4  Nach SOFT-Abbruch, wenn der Abbruchgrund systemisch ist.
    Nicht nur ein technisches Problem wie roter Test.

E5  Nach unerwarteter Interaktion zwischen Regeln.
```

### Nicht nötig

```text
- reine SICHER-Tasks ohne Überraschungen
- Lint / Format-Fixes
- reine Dokumentations-Korrekturen ohne inhaltliche Entscheidung
```

---

## 3. Format

```markdown
# Erfahrungsbericht: <Kurzbeschreibung>

Datum:
Learning-Matrix-Kandidat: ja/nein
Vorgeschlagene Musterkennung:
Session-Typ:  abgeschlossen | HARD-Abbruch | SOFT-Abbruch | gemischt
Aufgabe:      <was war der Auftrag>
Ergebnis:     <was wurde tatsächlich erreicht>

---

## Was sich bewährt hat

<Konkrete Beobachtungen. Keine Allgemeinplätze.
Was hat das System getan, was ohne die Regeln nicht passiert wäre?>

---

## Wo das System Reibung gezeigt hat

<Konkrete Engpässe. Wo musste der Agent länger suchen?
Wo war eine Regel unklar oder widersprüchlich?
Wo fehlte ein Begriff, eine Klassifikation, ein Mechanismus?>

---

## Was heute nicht geändert werden soll

<Verbesserungsideen die erkannt wurden — aber NICHT in dieser Session umgesetzt werden.
Explizit als Nicht-Auftrag markieren.>

---

## Offene Fragen

<Was bleibt unklar? Welche Entscheidung fehlt noch?>

---

## Nicht-Ziel dieses Dokuments

Dieser Bericht ist kein Änderungsauftrag.
```

---

## 4. Ort und Aufbewahrung

```text
tmp/erfahrungsberichte/YYYY-MM-DD-EB-kurzbeschreibung.md
```

Nomenklatur:

```text
ABBRUCH-  → Abbruch-Artefakt (auch in diesem Verzeichnis)
EB-       → Erfahrungsbericht
```

`tmp/erfahrungsberichte/` ist append-only.
Bestehende Berichte werden nicht geändert.
Korrekturen entstehen als neuer Bericht.

---

## 5. Was mit Erfahrungsberichten passiert

Erfahrungsberichte werden nicht automatisch in Regeln übersetzt.

Der Pfad ist:

```text
Erfahrungsbericht
  → identifiziert Muster oder Lücke
  → Sprechakt oder Plan wenn Änderung am System nötig ist
  → Änderung an AGENTS.md, package-schema.md oder anderen Dokumenten
    nur nach expliziter Freigabe
```

Ein Erfahrungsbericht der direkt AGENTS.md ändert, ist ein Regelverstoß.
Erfahrungsberichte sind Eingabe für menschliche Entscheidungen, nicht Autorisierung.

Die tatsächliche Übernahme in die Learning-Matrix wird ausschließlich in
`learning-matrix.md` dokumentiert. Bestehende Erfahrungsberichte werden dafür
nicht nachträglich geändert.

---

## 6. Verhältnis zur learning-matrix

Die `learning-matrix.md` (wenn im Projekt vorhanden) aggregiert Muster
über mehrere Erfahrungsberichte hinweg.

```text
Einzelner Erfahrungsbericht → beschreibt eine Session
Learning-Matrix             → beschreibt wiederkehrende Muster
Systemänderung              → folgt aus Entscheidung über Muster, nicht automatisch
```

Ein Agent darf die Learning-Matrix lesen, um bekannte Muster zu erkennen.
Er darf sie nicht ohne Freigabe schreiben.

---

## 7. Schlussregel

Ein Erfahrungsbericht ist fertig wenn er drei Fragen beantwortet:

```text
1. Was hat das System in dieser Session geleistet?
2. Wo hat das System noch Lücken gezeigt?
3. Was soll heute NICHT geändert werden?
```

Fehlende Antwort auf Frage 3 ist ein unvollständiger Bericht.

# erfahrungsbericht-protokoll.md — Python-Projekt

> Ebene: PRIMING
> Rolle: Reflexions- und Lernprotokoll
> Geltung: systemisch relevante Laufbefunde
> Autoritative Frage: Wann und wie wird ein Erfahrungsbericht geschrieben?
> Nicht zustaendig fuer: direkte Regeländerung, konkrete Projektarchitektur

> Dieses Dokument regelt wann, was und wie Erfahrungsberichte geschrieben werden.
>
> Bindender Einstieg und Kernregeln: `AGENTS.md`.
> Vollständige Detailregeln: die durch den jeweiligen Trigger aktivierten Verträge.

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
E1  Nach systemischem Abbruch oder unklarer Recovery.

E2  Nach Regelwiderspruch oder Autoritätsdrift.
    Der Bericht beschreibt nicht die Änderung, sondern die Regelkollision.

E3  Nach Verifikationslücke oder blindem Checker.
    Auch wenn die Session erfolgreich abgeschlossen wurde.

E4  Nach Pendeln, Stagnation oder wiederholtem Fehlverhalten.
    Nicht bei normalem roten Test oder normaler technischer Korrektur.

E5  Nach neuer verallgemeinerbarer Erkenntnis über die Agenten-Box.
```

### Nicht nötig

```text
- reine SICHER-Tasks ohne Überraschungen
- normale erfolgreiche Implementierungen ohne Systembefund
- Lint / Format-Fixes
- reine Dokumentations-Korrekturen ohne inhaltliche Entscheidung
- HARD-Abbruch mit bereits bekannter, klarer Ursache und klarer Recovery
```

---

## 3. Format

```markdown
# Erfahrungsbericht: <Kurzbeschreibung>

Datum:
Learning-Matrix-Kandidat: ja/nein
  (ja wenn: HARD-Abbruch verursacht, oder ≥2 Sessions gleiches Muster,
   oder Mensch markiert als systemic — siehe learning-matrix.md §1a)
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
.agent-box/evidence/erfahrungsberichte/YYYY-MM-DD-EB-kurzbeschreibung.md
```

Nomenklatur:

```text
ABBRUCH-  → Abbruch-Artefakt (auch in diesem Verzeichnis)
EB-       → Erfahrungsbericht
```

`.agent-box/evidence/erfahrungsberichte/` ist append-only.
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
Die tatsaechliche Uebernahme in die Learning-Matrix wird ausschliesslich in
`learning-matrix.md` dokumentiert. Bestehende Erfahrungsberichte werden dafuer
nicht nachtraeglich geaendert.

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

# learning-matrix.md — Python-Projekt: Aggregierte Lernmuster

> Dieses Dokument aggregiert wiederkehrende Muster aus Erfahrungsberichten.
>
> Es ist kein Regelwerk. Es ist Eingabe für Regelentscheidungen.
> Neue Regeln entstehen nur nach expliziter Freigabe — nicht durch dieses Dokument allein.

---

## 1. Zweck

```text
Einzelner Erfahrungsbericht → beschreibt eine Session
Learning-Matrix             → beschreibt Muster über mehrere Sessions
Systemänderung              → folgt aus menschlicher Entscheidung über Muster
```

Ein Agent darf diese Matrix lesen, um bekannte Muster zu erkennen.
Er darf sie nicht ohne explizite Freigabe schreiben oder ändern.

### 1.1 Muster-Schwelle

Ein Muster gilt als systemic und wird in diese Matrix aufgenommen, wenn
mindestens eine der folgenden Bedingungen erfüllt ist:

```text
- dasselbe Muster tritt in mindestens 2 unabhängigen Sessions mit
  gleichem Kern auf, oder
- ein HARD-Abbruch wurde durch dieses Muster verursacht, oder
- ein Mensch markiert den Bericht ausdrücklich als systemisches Muster.
```

Nicht-systemische Einzelbeobachtungen bleiben im Erfahrungsbericht.
Sie werden nicht automatisch hier eingetragen.

Jeder Erfahrungsbericht der als Kandidat gilt, trägt folgenden Hinweis:

```text
Learning-Matrix-Kandidat:     ja | nein
Muster-ID:                    M-<NR> oder leer
Übernommen in Learning-Matrix: ja | nein
```

---

## 2. Format eines Eintrags

```markdown
## M-<NR>: <Kurzbeschreibung des Musters>

Erstellt:      YYYY-MM-DD
Quellen:       tmp/erfahrungsberichte/YYYY-MM-DD-EB-...md (ein oder mehrere)
Häufigkeit:    einmalig | wiederholt (N Mal) | systematisch
Status:        beobachtet | als Verbesserung vorgeschlagen | in Planung | umgesetzt

### Beobachtung

<Was passiert wiederholt? Konkret, nicht abstrakt.>

### Wirkung

<Was kostet dieses Muster? Tokenaufwand, Reibung, Fehlerrisiko, Abbrüche?>

### Mögliche Maßnahme

<Was könnte das System besser machen? Als Vorschlag, nicht als Entscheidung.
Klar als Vorschlag markieren.>

### Entscheidung

<Wird nach menschlicher Freigabe ergänzt. Leer lassen bis Entscheidung getroffen.>
```

---

## 3. Bekannte Muster

<!-- Einträge nach Instanziierung eintragen. -->
<!-- Erstes Muster nach der ersten Erfahrungssession. -->

---

## 4. Muster-Klassifikation

```text
Klasse A: Regelklarheit
  Das System hat eine Regel, aber die Regel ist unklar formuliert oder
  in mehreren Dokumenten unterschiedlich dargestellt.
  → Kandidat für Konsolidierung in AGENTS.md

Klasse B: Fehlende Klassifikation
  Ein Begriff, Symbol oder Pfad wird gebraucht, ist aber nicht klassifiziert.
  → Kandidat für package-schema.md, migration-bridges.md oder Sprechakt

Klasse C: Redundanzdrift
  Dieselbe Information steht an mehreren Stellen und läuft auseinander.
  → Kandidat für Redundanzbereinigung

Klasse D: Tool-Lücke
  Ein Checker prüft etwas nicht, das er prüfen sollte.
  Oder ein Tool gibt kein maschinenlesbares Output für Agenten.
  → Kandidat für Tool-Erweiterung

Klasse E: Prozesslücke
  Ein Schritt im operativen Ablauf ist nicht dokumentiert oder fehlt.
  → Kandidat für AGENTS.md, preflight-checkliste.md oder neues Protokoll
```

---

## 5. Schutz und Pflege

```text
- Dieses Dokument ist geschützt (AGENTS.md Abschnitt 9).
- Neue Einträge nur nach Erfahrungsbericht-Session, nicht ad hoc.
- Status-Änderung auf "umgesetzt" erfordert Freigabe.
- Abgeschlossene Muster werden nicht gelöscht — auf "umgesetzt" gesetzt.
```

---

## 6. Schlussregel

Die Learning-Matrix ist nützlich wenn sie drei Dinge trennt:

```text
1. Was ist beobachtet? (Fakten)
2. Was wäre besser? (Vorschlag)
3. Was ist entschieden? (Freigabe)
```

Wenn Beobachtung und Entscheidung vermischt werden,
ist die Matrix kein Lernwerkzeug mehr — sie ist ein versteckter Regeländerungs-Kanal.



---

Muster-Schwelle und Kandidat-Format: Abschnitt 1.1.

Die Learning-Matrix ist kein Regelwerk. Ein Matrix-Eintrag wird erst operativ,
wenn ein Mensch daraus eine Änderung an `AGENTS.md`, `package-schema.md`,
`test-obligations.md`, `migration-bridges.md` oder einem Glossar ableitet.

# glossar-domain.md — Fachdomäne: Begriffe und Bedeutungen

**Dokumenttyp: Operativ / autoritativ**

> Dieses Glossar ist operative Infrastruktur, nicht Dokumentation.
>
> Es ist der Sortierraum für Fachdomänenbegriffe.
> Ein Domänenexperte kann Einträge prüfen ohne Systemlaufzeit oder Infrastruktur zu kennen.
> Ein Agent konsultiert es beim Preflight (P5) und beim Task-Schnitt (T1, SP7).
>
> Neue Begriffe entstehen nicht durch Implementierung — sie entstehen durch Sprechakt SP1
> und werden hier eingetragen, bevor Code entsteht.

---

## 0. Platzhalter

```text
Regenbogen
regenbogen
src
```

---

## 1. Laderegel (Preflight P5)

```text
Nicht das gesamte Glossar reflexhaft laden.
Nur die Begriffe laden, die in der aktuellen Iteration aktiv gebraucht werden.

Laden wenn:
  - Begriff wird geändert, umbenannt oder verschoben
  - Begriff wird als Grundlage einer Entscheidung gebraucht
  - Begriff erscheint in neuen Namen, Typen, Fehlern, Statuswerten oder Tests

Nicht laden:
  - weil der Begriff irgendwo im Projekt vorkommt
  - weil er historisch relevant war
  - aus Vorsicht
```

---

## 2. Eintrag-Format

Jeder Glossareintrag hat folgende Felder:

```markdown
### <Begriff>

**Semantischer Raum:** domain
**Eintragstiefe:** vollständig | minimal

Eintragstiefe-Definition:
  minimal      = Bedeutung + Projektionen + Migrationsstatus vorhanden.
                 Alle anderen Felder bewusst weggelassen, nicht vergessen.
  vollständig  = alle Felder unten vorhanden.
  Upgrade auf vollständig erfordert keinen Sprechakt — nur Pflege.

**Kompetenzfrage:**
Kann ein Domänenexperte (nicht-technisch) diesen Begriff vollständig beurteilen
ohne Systemlaufzeit, Infrastruktur oder Retry-Mechanismen zu kennen?
→ Wenn nein: gehört nicht nach domain.

**Bedeutung:**
<Was ist dieser Begriff? Aus Sicht der Fachdomäne, ohne technische Details.>

**Invarianten:**
<Was gilt für alle Instanzen dieses Begriffs ohne Ausnahme?>
<Wer kann eine Verletzung erkennen?>

**Erlaubt:**
<Welche Operationen, Zustände, Werte sind für diesen Begriff erlaubt?>

**Verboten:**
<Was darf dieser Begriff nicht tragen? Was würde seine Autonomie verletzen?>

**Projektionen:**
<Wo ist dieser Begriff sichtbar und prüfbar?>
- Code: <Modulpfad>
- Tests: <Testpfad>
- Checker: <welcher Check>

**Abgrenzung:**
<Von welchen verwandten Begriffen muss dieser Begriff klar unterschieden werden?>

**Migrationsstatus:** canonical | legacy-bridge | deprecated
<Wenn nicht canonical: Verweis auf migration-bridges.md>
```

---

## 3. Begriffe

### Wetterzustand

**Semantischer Raum:** domain
**Eintragstiefe:** minimal

**Bedeutung:**
Beobachtete Kombination von Wetterphaenomenen zu einem Zeitpunkt an einem Ort.
Mehrere Phaenomene koennen gleichzeitig auftreten.

**Invarianten:**
- Sonnenschein und Regen zur selben Zeit ist ein gueltiger Zustand.
- Intensitaeten liegen in [0.0, 1.0].
- Der Sonnenscheinanteil ist keine Wahrscheinlichkeit.

**Projektionen:**
- Code: src/regenbogen/domain/wetter.py
- Tests: tests/domain/test_regenbogen.py

**Migrationsstatus:** canonical

### SonnenscheinAnteil

**Semantischer Raum:** domain
**Eintragstiefe:** minimal

**Bedeutung:**
Anteil einer Bezugsstunde, in der direkte Sonneneinstrahlung beobachtet wurde.
Der Wert wird im aktuellen Modell aus `sunshine_duration / 3600` abgeleitet.

**Invarianten:**
- Wert liegt in [0.0, 1.0].
- 0.0 bedeutet kein beobachteter Sonnenschein in der Bezugsstunde.
- 1.0 bedeutet durchgehender beobachteter Sonnenschein in der Bezugsstunde.
- Der Wert ist keine Wahrscheinlichkeit.

**Erlaubt:**
- Verwendung als Faktor fuer Wetterzustand und Regenbogenwahrscheinlichkeit.
- Anzeige als Prozentanteil der Bezugsstunde.

**Verboten:**
- Interpretation als Vorhersagewahrscheinlichkeit.
- Interpretation als Sonnenstand oder Direktstrahlung.

**Projektionen:**
- Code: src/regenbogen/system/core/wahrscheinlichkeit_use_case.py
- Anzeige: src/regenbogen/cli/gui_format.py
- Tests: tests/cli/test_gui_format.py
- Modell: MODELL-README.md

**Abgrenzung:**
`SonnenscheinAnteil` beschreibt beobachtete Sonnenscheindauer innerhalb einer
Bezugsstunde. `Direktlicht` beschreibt die aus direkter Strahlung abgeleitete
optische Eignung. `Sonnenstand` beschreibt die geometrische Position der Sonne.

**Migrationsstatus:** canonical

### RegenbogenWahrscheinlichkeit

**Semantischer Raum:** domain
**Eintragstiefe:** vollständig

**Bedeutung:**
Prozentwert in [0, 100] für die domänenlogische Einschätzung,
ob die Grundbedingungen für einen sichtbaren Regenbogen erfüllt sind.
Berücksichtigt Sonnenschein-Intensität (Gewicht 0,6) und
Regen-Intensität (Gewicht 0,4) sowie optional den geometrischen
Sonnenstands-Faktor.

**Invarianten:**
- Ohne Sonnenschein: 0.
- Ohne Regen: 0.
- Wert liegt in [0, 100].
- Der Sonnenstand ist optional; fehlt er, entfällt der geometrische Faktor.

**Erlaubt:**
- Alle Kombinationen aus positivem Sonnenschein und positivem Regen.
- `sonnenstand=None` (kein Geometrie-Einfluss).

**Verboten:**
- Werte außerhalb [0, 100].
- Interpretation als Sichtbarkeits-Score (das ist RegenbogenSichtbarkeit).
- Gleichsetzung mit der physikalischen Auftrittswahrscheinlichkeit
  eines Meteorologieereignisses.

**Projektionen:**
- Code: src/regenbogen/domain/regenbogen.py
- Tests: tests/domain/test_regenbogen.py

**Abgrenzung:**
- `RegenbogenSichtbarkeit`: bewertet die *optische Qualität* eines Bogens
  über 7 multiplikativ verknüpfte Faktoren (Sonnenstands-, Direktlicht-,
  Regen-, Tropfenqualitäts-, Sicht-, Hintergrundkontrast-, Phasenfaktor).
  Beide Scores liegen in [0, 100]; Wahrscheinlichkeit fragt „Grundbedingung
  erfüllt?", Sichtbarkeit fragt „Wie gut sieht man ihn?".
- `SonnenscheinAnteil`, `RegenIntensitaet`: Eingaben, keine aggregierten Scores.

**Migrationsstatus:** canonical

### Sonnenstand

**Semantischer Raum:** domain
**Eintragstiefe:** minimal

**Bedeutung:**
Position der Sonne relativ zum Beobachter, beschrieben durch Sonnenhoehe und Sonnenazimut.

**Projektionen:**
- Code: src/regenbogen/domain/regenbogen_geometrie.py
- Tests: tests/domain/test_regenbogen_geometrie.py

**Migrationsstatus:** canonical

### SonnenstandsFaktor

**Semantischer Raum:** domain
**Eintragstiefe:** minimal

**Bedeutung:**
Faktor in [0, 1], der ausdrueckt, ob der Sonnenstand fuer einen sichtbaren Hauptregenbogen guenstig ist.

**Invarianten:**
- Sonnenhoehe <= 0 Grad: 0.
- Sonnenhoehe >= 42 Grad: 0.
- 0 Grad < Sonnenhoehe <= 25 Grad: 1.

**Projektionen:**
- Code: src/regenbogen/domain/regenbogen_geometrie.py
- Tests: tests/domain/test_regenbogen_geometrie.py

**Migrationsstatus:** canonical

### RegenbogenSichtbarkeit

**Semantischer Raum:** domain
**Eintragstiefe:** minimal

**Bedeutung:**
Score in [0, 100], der die erwartete Sichtbarkeit eines normalen Sonnen-Regenbogens beschreibt.

**Projektionen:**
- Code: src/regenbogen/domain/regenbogen_optik.py
- Tests: tests/domain/test_regenbogen_optik.py

**Migrationsstatus:** canonical

### TropfenQualitaet

**Semantischer Raum:** domain
**Eintragstiefe:** minimal

**Bedeutung:**
Faktor in [0, 1] fuer die Eignung des vorhandenen Niederschlags zur Bildung eines sichtbaren Regenbogens.

**Projektionen:**
- Code: src/regenbogen/domain/regenbogen_optik.py
- Tests: tests/domain/test_regenbogen_optik.py

**Migrationsstatus:** canonical

### TagesPrognose

**Semantischer Raum:** domain
**Eintragstiefe:** minimal

**Bedeutung:**
Geordnete Folge von Stunden-Bewertungen aller Tagstunden (positiver Sonnenstand)
des aktuellen Kalendertags an einem Beobachtungsort.

**Invarianten:**
- Enthält ausschliesslich Stunden mit positivem Sonnenstand.
- Nachtstunden sind nicht enthalten.
- Mondbögen sind explizit ausgeschlossen — dieser Begriff gilt nur fuer normalen Sonnen-Regenbogen.
- Reihenfolge: aufsteigend nach Stunde.

**Projektionen:**
- Code: src/regenbogen/domain/tagesprognose.py
- Tests: tests/domain/test_tagesprognose.py

**Migrationsstatus:** canonical

### PrognoseStunde

**Semantischer Raum:** domain
**Eintragstiefe:** minimal

**Bedeutung:**
Bewertung eines einzelnen Zeitslots (eine Tagstunde) am Beobachtungsort mit
Regenbogen-Wahrscheinlichkeit und Sichtbarkeit.

**Invarianten:**
- stunde liegt in [0, 23] (lokale Stunde des Beobachtungsorts).
- wahrscheinlichkeit liegt in [0, 100].
- sichtbarkeit liegt in [0, 100].
- Eine PrognoseStunde mit wahrscheinlichkeit = 0 ist ein gueltiges Ergebnis.

**Abgrenzung:**
PrognoseStunde ist keine Prognoseunsicherheit und kein Konfidenzintervall.
Sie ist eine Punktbewertung nach dem Regenbogen-Modell fuer diesen Zeitslot.

**Projektionen:**
- Code: src/regenbogen/domain/tagesprognose.py
- Tests: tests/domain/test_tagesprognose.py

**Migrationsstatus:** canonical

---

## 4. Bekannte Lücken

<!-- Begriffe die gebraucht werden aber noch keinen vollständigen Eintrag haben. -->
<!-- Format: Begriff — warum noch lückenhaft — Sprechakt-Referenz -->

---

## 5. Abgrenzung zum System-Glossar

```text
Dieses Glossar (glossar-domain.md):
  Fachbegriffe die ein Domänenexperte ohne technische Laufzeitdetails prüfen kann.

glossar-system.md:
  Betriebsbegriffe: Use Cases, Policies, Lifecycle, Fehlerklassifikation,
  Retry-Bedeutung, Idempotenz, Phasen.

Bei Zweifel:
  Kann ein nicht-technischer Domänenexperte den Begriff vollständig beurteilen?
  → Ja: domain
  → Nein: system oder infrastructure
```

---

## 6. Schlussregel

Ein Glossareintrag ist fertig wenn ein Domänenexperte ihn lesen und
jeden Code-Typ im zugehörigen Modulraum damit vollständig beurteilen kann —
ohne den Rest des Projekts zu kennen.

Wenn das nicht möglich ist: der Eintrag ist unvollständig → Sprechakt SP7.

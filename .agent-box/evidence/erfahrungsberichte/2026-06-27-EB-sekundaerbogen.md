# Erfahrungsbericht: Sekundärbogen-Prognose

Datum: 2026-06-27
Learning-Matrix-Kandidat: ja
Vorgeschlagene Musterkennung: SP1-FLOW-ERSTER-LAUF, PHYSIK-FEHLER-IN-TEST, KONTEXT-KONTINUITAET
Session-Typ: abgeschlossen
Aufgabe: Sekundärbogen-Prognose als Domänenerweiterung — erster vollständiger Lauf unter box-python v0.3.0 Governance
Ergebnis: Vollständig abgeschlossen. Alle 4 Pflichtchecks grün. 76 Tests bestanden (vorher: 64).
Sonderkennung: **Erster Lauf unter geändertem Governance (v0.3.0)**

---

## Kontext: Warum dieser Bericht besonders ist

Dieser Lauf ist der erste Feature-Entwicklungslauf nach der abgeschlossenen Brownfield-Migration
v0.2.7 → v0.3.0. Die Migration hat das Governance-System tiefgreifend verändert:

- **W0-Gate**: Drei Arbeitsmodi (ANALYSE / PLAN / AUSFUEHRUNG) mit hartem Übergangsprotokoll
- **Ausfuehrungsmandat**: Explizite menschliche Freigabe trennt Entscheidung von Ausführungsberechtigung
- **SP1-Mechanismus**: Neuer Fachbegriff erfordert Sprechakt vor Code — kein Begriff ohne Beschluss
- **Anti-Zeno**: Keine Wiederholung identischer Versuche bei Blockaden

Das Ziel des Laufs war doppelt: einerseits den Sekundärbogen fachlich korrekt implementieren,
andererseits beobachten, ob die neue Governance im Alltag funktioniert, Reibung erzeugt oder
Fehler verhindert.

---

## Laufrekonstruktion: Was tatsächlich passierte

### Phase 0 — Governance-Analyse als Einstieg

Der Lauf begann nicht mit einem Feature-Auftrag, sondern mit einer Governance-Reflexion: Der
Benutzer bat um eine Analyse des Governance-Systems aus der Agenten-Priming-Perspektive. Der
Arbeitsmodus war zu diesem Zeitpunkt implizit ANALYSE.

Aus dieser Analyse heraus entstand die Empfehlung, den Sekundärbogen als Testfall zu verwenden,
weil er SP1, mehrere semantische Räume und das W0-Gate gemeinsam aktiviert. Das war keine
technische Notwendigkeit, sondern ein bewusst gewählter Komplexitätsgrad, um die Governance
unter realen Bedingungen zu prüfen.

Beobachtung: ANALYSE-Modus ohne explizite Deklaration. Der Wechsel ANALYSE → PLAN entstand
implizit durch den Aufruf "Setze einen Plan auf". Ein explizites "Ich wechsle jetzt in den
PLAN-Modus" wurde nicht ausgesprochen. Das ist eine bekannte Schwäche: Moduswechsel sind
nicht immer protokollähnlich abgegrenzt.

### Phase 1 — SP1-Auslösung und Aufplanung

Beim Aufsetzen des Plans wurden drei neue Fachbegriffe identifiziert:
- Sekundaerbogen
- SonnenstandsFaktorSekundaerbogen
- SekundaerbogenDaempfung
- SekundaerbogenWahrscheinlichkeit

SP1 wurde korrekt ausgelöst und im Plan als Blocker vermerkt: "Blockiert Ausführung". Kein
Code wurde geschrieben, bevor SP1 aufgelöst war. Dies ist der Kernzweck von SP1, und er
hat hier funktioniert wie vorgesehen.

Die drei SP1-Entscheidungen waren:
1. Begriff: Option A (Sekundaerbogen, Fachsprache Optik)
2. Datenmodell: Option A (neues Feld in PrognoseStunde, Default 0)
3. Sichtbarkeit: Abschwächungsfaktor SekundaerbogenDaempfung = 0.57

Der Benutzer hat alle drei in einer einzigen Nachricht aufgelöst und gleichzeitig die
Ausführungsfreigabe erteilt: *"1. Option A / 2. Option A / 3. Abschwächungsfaktor —
diese Änderungen im Glossar eintragen, damit Plan aktiv setzen und mit seiner
Ausführung starten."*

Beobachtung: Sprechakt (SP1) und Ausfuehrungsmandat (W0-Freigabe) wurden in einem
einzigen Satz gegeben. Das Protokoll trennt diese formal, aber in der Praxis kollidieren
sie zeitlich. Die Implementierung hat sie korrekt in zwei separate Artefakte aufgeteilt:
- `docs/sprechakte/2026-06-27-sekundaerbogen-begriffe.md` (SP1)
- Plan-Mandatstatus auf `aktiv` gesetzt (W0)

Das ist die korrekte Handhabung: Ein Menschensatz kann beide auslösen, aber die
Artefakte bleiben getrennt.

### Phase 2 — Geometriefunktion

Die Funktion `berechne_sonnenstands_faktor_sekundaerbogen()` wurde implementiert mit:
- Cutoff 51° (vs. 42° für Primärbogen)
- Linearfall zwischen 51° und 25°
- Voller Faktor unter 25°
- Null über 51° und unter dem Horizont

Die Konstante `SEKUNDAERBOGEN_DAEMPFUNG = 0.57` wurde in `regenbogen_geometrie.py`
als Modul-Konstante platziert — im selben Raum wie die Geometriefunktion, weil sie
eine physikalische Eigenschaft des Bogens ist, nicht eine Berechnungsregel.

#### Physikalischer Fehler im ersten Test — Selbstkorrektur

Der erste Testentwurf enthielt einen physikalisch falschen Test:

```python
# FALSCH:
def test_sekundaerbogen_faktor_kleiner_als_primaer_bei_gleicher_hoehe():
    assert faktor_s < faktor_p  # bei hoehe=30°
```

Die Annahme war: Sekundärbogen hat niedrigere Wahrscheinlichkeit, also muss der
Geometriefaktor kleiner sein.

Das ist physikalisch falsch. Der Geometriefaktor des Sekundärbogens hat ein
**weiteres Fenster** (0°–51° statt 0°–42°). Bei gleicher Sonnenstandshöhe (z.B. 30°)
fällt der Sekundärbogen-Faktor langsamer ab:

```
hoehe=30°: faktor_p = (42-30)/(42-25) = 12/17 ≈ 0.706
           faktor_s = (51-30)/(51-25) = 21/26 ≈ 0.808
```

Der Sekundärbogen-Geometriefaktor ist im Überlappbereich (0°–42°) größer, nicht kleiner.
Die niedrigere Gesamtwahrscheinlichkeit entsteht ausschließlich durch die spätere
Multiplikation mit `SEKUNDAERBOGEN_DAEMPFUNG = 0.57`.

Der Test wurde korrigiert zu:

```python
def test_sekundaerbogen_faktor_groesser_als_primaer_im_ueberlappbereich():
    assert faktor_s > faktor_p  # korrekt
```

Governance-Relevanz: Dieser Fehler wurde durch Schreiben und Ausführen des Tests
gefunden — nicht durch Nachdenken. Das ist das erwartete Verhalten. Der Test hat
seinen Zweck erfüllt, bevor er "richtig" war.

### Phase 3 — Datenmodell und Use Case

`PrognoseStunde.sekundaerbogen_wahrscheinlichkeit: int = 0` — Default 0 stellt
Rückwärtskompatibilität sicher. Bestehende Tests mussten nicht geändert werden.

`TagesPrognose.hat_sekundaerbogen_chance` als Property — analog zu `hat_regenbogen_chance`.
Das Muster war bereits vorhanden und konnte direkt übernommen werden.

Die Berechnungslogik im Use Case:

```python
def _berechne_sekundaerbogen_wahrscheinlichkeit(self, zustand, sonnenstand) -> int:
    if not zustand.sonnenschein or not zustand.regen:
        return 0
    faktor_s = berechne_sonnenstands_faktor_sekundaerbogen(sonnenstand)
    if faktor_s <= 0.0:
        return 0
    basis = zustand.sonnenschein_intensitaet * 0.6 + zustand.regen_intensitaet * 0.4
    return max(0, min(100, round(basis * faktor_s * SEKUNDAERBOGEN_DAEMPFUNG * 100)))
```

Diese Formel ist bewusst identisch mit der primären Berechnung bis auf:
- `faktor_s` statt primärem Faktor
- Multiplikation mit `SEKUNDAERBOGEN_DAEMPFUNG`

Keine neue Berechnungsinfrastruktur. Der Abschwächungsfaktor als einfacher Multiplikator
war die richtige SP1-Entscheidung — fachlich korrekt und minimal in der Implementierung.

### Phase 4 — CLI-Ausgabe

Die CLI-Ausgabe erweitert `formatiere_tagesprognose()` am Ende mit einer optionalen Zeile:

```
Sekundaerbogen moeglich: 08:00–09:00
```

Bewusste Entscheidungen bei der Implementierung:
- Umlautvermeidung in der Ausgabe (`moeglich`, `Sekundaerbogen`) — konsistent mit
  bestehenden ASCII-Konventionen im Projekt
- Zeitbereich (frühste–späteste Stunde) statt Auflistung aller Stunden
- Einzelstunde ohne Bindestrich-Bereich
- Zeile erscheint nur wenn mindestens eine Stunde `sekundaerbogen_wahrscheinlichkeit > 0`

### Phase 5 — Vollvalidierung

Ergebnis: 4/4 Pflichtchecks grün, 76 Tests bestanden.

```
Agent-Docs-Consistency: OK (Modus: instantiated)
✓ PREFLIGHT IMPORT-LAYER OK (38 Dateien geprüft)
Selfcheck (instantiated): OK
76 passed in 0.09s
```

---

## Governance-Analyse: Was unter v0.3.0 beobachtet wurde

### SP1-Mechanismus — Erstbeobachtung

Der SP1-Mechanismus hat in diesem Lauf seine erste vollständige Durchführung erfahren.
Beobachtungen:

**Positiv: Kein Code vor Beschluss.** Die Phasenstruktur des Plans hat es natürlich gemacht,
Phase 2 (Geometriefunktion) erst nach SP1-Auflösung zu starten. Es gab keine Versuchung,
"schnell schon mal die Funktion zu schreiben" — der Plan war der Gate.

**Positiv: Begriffsklarheit ab Zeile 1.** Weil die Begriffe vor dem Code festgelegt wurden,
gab es keine Umbenennung mid-flight. `sekundaerbogen_wahrscheinlichkeit` im Feld, im Property,
in der CLI-Ausgabe und im Glossar sind identisch. Bei einem unstrukturierten Lauf wäre
"secondary_probability" oder "second_bow_chance" möglicherweise entstanden.

**Beobachtung: SP1 und W0 kollidieren zeitlich.** Der Benutzer hat SP1-Beschluss und
Ausführungsfreigabe in einem einzigen Satz gegeben. Das ist nicht falsch, aber es zeigt,
dass der gedankliche Aufwand für "ich beschließe den Begriff" und "ich genehmige die
Ausführung" in der Praxis fließt. Ob diese Trennung stets wahrnehmbar ist, bleibt offen.

**Offene Frage:** Soll SP1-Auflösung ein eigenständiges Artefakt bleiben (separates Sprechakt-Dokument)
oder kann es direkt im Plan-Freigabetext aufgelöst werden? Aktuell: separates Dokument in
`docs/sprechakte/`. Das ist korrekt nach Protokoll, aber erhöht den Verwaltungsaufwand.

### W0-Gate und Ausfuehrungsmandat

Das W0-Gate hat genau einen Zweck erfüllt: verhindert, dass Code geschrieben wird, während
der Beschluss noch offen ist. Der Mandatstatus `aktiv` war die Freigabe für alle Phasen
des Plans, nicht nur eine Phase.

Beobachtung: Das Mandat nennt `glossar-domain.md` als freigegebene geschützte Datei.
Alle anderen geschützten Dateien (z.B. `package-schema.md`, `AGENTS.md`) wurden nicht
benötigt — das Mandate war präzise kalibriert.

Der Plan nennt auch: *"Freigegebener Scope: vollständiger Plan"*. Das war die richtige
Einschränkung: alles im Plan ist freigegeben, nichts außerhalb.

### Multi-Raum-Änderung ohne Task-Schnitt

Drei semantische Räume wurden geändert (domain, system, cli). Der Plan hat den
Task-Schnitt explizit geprüft und verneint: *"Kein unabhängiger Rollback-Punkt zwischen
den Räumen."*

Das war korrekt. Domain-, System- und CLI-Änderungen sind Projektionen derselben
physikalischen Erweiterung. Ein Zwischenstand ohne CLI wäre kein lieferbarer Zustand —
der Sekundärbogen wäre berechnet aber unsichtbar.

### Kontext-Grenzüberschreitung

Die Session überspannte einen Kontext-Fenster-Grenzübergang (Kontext-Komprimierung).
Die Komprimierung erzeugte eine `system-reminder`-Zusammenfassung, aus der der neue
Kontext den Ausführungsstand rekonstruiert hat.

Die Wiederaufnahme war präzise: Statt bei Phase 4 "Wo war ich?" zu fragen, wurde
direkt der nächste konkrete Schritt (CLI-Tests) ausgeführt.

Beobachtung: Die Korrektheit der Wiederaufnahme hängt von der Präzision der Zusammenfassung
ab. Die Zusammenfassung enthielt den genauen Zustand jeder Phase (✓/✗), die letzten
Codeänderungen und den nächsten Schritt. Das ist der Mindeststand für fehlerfreie
Wiederaufnahme.

**Muster:** Für lange Ausführungsläufe, die Kontext-Grenzen überschreiten können, sollte
der Plan so geschrieben sein, dass der Phase-Zustand (✓/laufend/✗) direkt ablesbar ist.
Dieser Plan hatte das noch nicht explizit. Bei PLAN-Version-2 wäre eine Phase-Statuszeile
pro Phase im Plan sinnvoll.

### Testgetriebene Physikkorrektur

Der physikalische Fehler im ersten Sekundärbogen-Test ist der interessanteste Einzelpunkt
dieses Laufs. Ein Entwickler (oder Agent) kann ein falsches mentales Modell über die
Physik haben und einen Test schreiben, der das falsche Modell bestätigt. Das Scheitern
des Tests beim ersten Lauf hat erzwungen, die Physik zu re-derivieren.

In diesem Fall: Erst beim Ausrechnen der konkreten Zahlenwerte wurde klar, dass
`(51-30)/(51-25) = 0.808 > (42-30)/(42-25) = 0.706`. Die Intuition "zweiter Bogen ist
schwächer, also muss sein Geometriefaktor kleiner sein" ist plausibel aber falsch. Die
Stärke kommt aus der Dämpfung, nicht aus der Geometrie.

Governance-Auswirkung: Keine. Die Korrektur war rein testintern. Der SP1-Beschluss war
nicht betroffen (die Begriffe blieben korrekt). Der Glossareintrag war korrekt.

---

## Was sich bewährt hat

**SP1 als Phase-Gate.** Der Plan mit SP1 als explizitem Blocker vor Phase 2 hat verhindert,
dass begriffliche Halbherzigkeiten in Code eingebettet werden. Der Begriff war festgelegt,
bevor die erste Zeile Produktionscode geschrieben wurde.

**Default-0-Strategie.** `sekundaerbogen_wahrscheinlichkeit: int = 0` als Default in
`PrognoseStunde` hat es ermöglicht, alle 64 bestehenden Tests unverändert grün zu halten.
Keine Migration bestehender Testdaten. Das war die richtige Entscheidung aus SP1 Entscheidung 2.

**SEKUNDAERBOGEN_DAEMPFUNG als Konstante im domain-Raum.** Die Konstante ist physikalisch
— sie gehört in den Geometrie-Raum, nicht in den Use Case. Das hat den Use Case einfach
gehalten (nur eine Multiplikation) und die Testbarkeit der Konstante selber sichergestellt
(sie ist aus Tests importierbar, falls nötig).

**Phasentrennung.** Die vier Phasen (Geometrie → Datenmodell → Use Case → CLI) haben
eine saubere Commit-Logik ergeben. Jede Phase war abgeschlossen, bevor die nächste begann.
Kein partieller Zustand war sichtbar.

**Vollvalidierung vor Plan-Schluss.** Alle 4 Pflichtchecks wurden nach Fertigstellung
aller Tests ausgeführt, nicht vorher. Das ist die korrekte Reihenfolge: Tests grün,
dann Governance-Checks, dann Plan abschließen.

---

## Wo das System Reibung gezeigt hat

**ANALYSE-Modus ohne Protokoll.** Die initiale Governance-Analyse wurde ohne expliziten
Moduswechsel-Sprechakt durchgeführt. Das ist informell korrekt (kein Code, keine Mutation),
aber nicht protokollähnlich. Ein Agent in einem strengeren System würde vielleicht
fragen: "Darf ich in den ANALYSE-Modus wechseln?" Das wäre Overhead ohne Nutzen.

**Plan-Phase-Status nicht im Plan.** Die Phasen im Plan haben keinen expliziten Status
(✓ / laufend / ✗). Bei der Wiederaufnahme nach Kontext-Grenzüberschreitung wurde der
Status aus der Session-Zusammenfassung rekonstruiert, nicht aus dem Plan selbst. Wäre der
Plan die einzige Quelle, wäre eine Wiederaufnahme unsicherer.

**Sprechakt-Dokument als Overhead.** Das separate `docs/sprechakte/2026-06-27-sekundaerbogen-begriffe.md`
fügt Verwaltungsaufwand hinzu, der bei einfachen Fachbegriffen vielleicht nicht
proportional ist. Drei Zeilen Begriff + Default-Wert wären im Plan direkt beschreibbar.
Die Trennung ist architektonisch korrekt (Sprechakt ≠ Plan), aber im Alltag fühlbar.

**Glossar-Entry-Feinheit.** Die neuen Glossareinträge für SonnenstandsFaktorSekundaerbogen,
SekundaerbogenDaempfung und SekundaerbogenWahrscheinlichkeit wurden als "minimal"
markiert und entsprechen eher Platzhaltern als vollständigen Einträgen. Das ist nach
Protokoll in Ordnung (SP1 legt fest, Glossar wächst nachträglich), aber es bedeutet,
dass das Glossar für diese Begriffe noch nicht vollständig ausgebaut ist.

---

## Physikalische Erkenntnisse (für Glossar)

Sekundärbogen-Geometrie: Der geometrische Faktor des Sekundärbogens fällt **langsamer** ab
als der des Primärbogens, weil das Cutoff-Fenster weiter ist (51° vs. 42°). Bei gleicher
Sonnenstandshöhe im Überlappbereich (0°–42°) ist der Sekundärbogen-Geometriefaktor daher
numerisch größer. Die niedrigere Gesamtwahrscheinlichkeit entsteht durch
`SekundaerbogenDaempfung = 0.57`, nicht durch die Geometrie.

Zwischenzone 42°–51°: In diesem Bereich ist ausschließlich der Sekundärbogen geometrisch
möglich — kein Primärbogen. Diese Zone ist eine wichtige fachliche Aussage der
Implementierung und sollte im Glossar unter Sekundaerbogen explizit dokumentiert werden.

Alexandersches Dunkelband: Der Bereich zwischen dem inneren Rand des Sekundärbogens
(Reflexion bei ~51°) und dem äußeren Rand des Primärbogens (Reflexion bei ~42°) erscheint
dunkler. Dieses Phänomen wurde als Nicht-Ziel ausgeschlossen, ist aber fachlich verknüpft.

---

## Offene Punkte / Kandidaten für Learning-Matrix

1. **SP1-W0-Kollision** (zeitlich simultan, architektonisch getrennt): Ist das ein Problem
   oder ein akzeptabler Kompromiss? Vorschlag: Kein Eingriff, Dokumentation als Muster.

2. **Plan-Phase-Status**: Sollen Phasen im Plan einen expliziten Status-Marker erhalten,
   damit ein Plan nach Kontext-Unterbrechung als alleinige Quelle für die Wiederaufnahme
   ausreicht? Vorschlag: optional als Konvention einführen.

3. **Physik-Test-Muster**: "Erst Test schreiben, dann Physik re-derivieren wenn Test
   scheitert" hat einen realen Fehler gefunden. Das ist das korrekte Muster — es sollte
   nicht zugunsten "erst ausrechnen dann testen" aufgegeben werden.

4. **Sekundärbogen-Glossareinträge** noch minimal — SonnenstandsFaktorSekundaerbogen,
   SekundaerbogenDaempfung, SekundaerbogenWahrscheinlichkeit sollten ausgebaut werden.

---

## Nicht-Ziel dieses Dokuments

Dieser Bericht ist kein Änderungsauftrag. Die offenen Punkte sind Beobachtungen,
keine Forderungen.

# blocker-und-abbruch-protokoll.md — Blocker, Abbruch, Wiedereinstieg

> Ebene: PRIMING
> Rolle: Abbruch- und Recovery-Protokoll
> Geltung: jeder Aufgabenlauf
> Autoritative Frage: Wann wird gueltig gestoppt und wie wird wieder eingestiegen?
> Nicht zustaendig fuer: lokale Raumordnung, konkrete Transformation

> Dieses Dokument ist die operative Quelle fuer H1-H10, SA1-SA6,
> Abbruch-Evidence, Wiedereinstieg, Pendeln und Stagnation.

---

## 1. Blockerklassen

```text
epistemisch  Information fehlt.
technisch    Umsetzung, Umgebung oder Validierung ist nicht beherrscht.
deontisch    menschliche Festlegung oder Freigabe fehlt.
```

Deontische Blocker duerfen nicht durch kleinere Aufgaben ersetzt werden.
Eine eindeutige menschliche Anweisung im aktuellen Auftrag kann die noetige
Freigabe bereits enthalten, wenn Scope und Handlung eindeutig benannt sind.

---

## 2. HARD-Abbrueche H1-H10

```text
H1   Geschuetzte Datei oder geschuetzter Bereich ohne Freigabe betroffen.
H2   Import-/Layer-Verletzung ohne klassifizierten Known Breach.
H3   Widerspruch zwischen operativen Projektartefakten, Code oder Checker.
H4   Neuer Begriff, Status oder neue Bedeutung ohne Sprechakt/Freigabe.
H5   Toolaenderung waere noetig, um einen Fehler zu unterdruecken.
H6   Testpflicht ist nicht ableitbar.
H7   Setup-/Template-Zustand unklar, Platzhalter aktiv oder Pflichtdatei fehlt.
H8   Runtime-Dependency- oder Packaging-Aenderung ohne Freigabe.
H9   Oeffentliche API-Flaeche ohne Freigabe betroffen.
H10  Autonomieregel eines semantischen Raums verletzt.
```

HARD-Abbruch bedeutet: nicht weiterarbeiten, bis der Zustand geklaert oder
explizit freigegeben ist.

---

## 3. SOFT-Abbrueche SA1-SA6

```text
SA1  Test rot.
SA2  Lint rot.
SA3  Typecheck rot.
SA4  Build-, Installations- oder Umgebungsfehler.
SA5  Unvollstaendige Migration entdeckt.
SA6  Lokale Inkonsistenz ohne semantischen Widerspruch.
```

SOFT-Abbruch bedeutet: stoppen, Evidence sichern, Wiedereinstieg beschreiben.
Keine Regel abschwaechen, um den roten Zustand zu umgehen.

---

## 4. Abbruch-Evidence

Ablageort:

```text
.agent-box/evidence/erfahrungsberichte/YYYY-MM-DD-ABBRUCH-<kurzbeschreibung>.md
```

Format:

```markdown
# Abbruch: <Kurzbeschreibung>

Datum:
Aufgabe:
Abbruchklasse: H<Nummer> | SA<Nummer>
Abbruchregel:
Betroffene Dateien:
Letzter sicherer Zustand:
Beobachtete Evidence:
Keine Vermutungen:
Empfohlene naechste Entscheidung:
Wiedereinstiegspunkt:
```

Bei BF-Abbruch gilt zusaetzlich `BROWNFIELD-MIGRATION.md`; BF-Evidence liegt
im Migrationsraum und ersetzt dieses allgemeine Format nicht automatisch.

---

## 5. Wiedereinstieg

Vor Wiedereinstieg:

```text
1. Abbruch-Evidence lesen.
2. Letzten sicheren Zustand pruefen.
3. Menschliche Entscheidung oder technische Korrektur pruefen.
4. Aktivierte Spezialdokumente erneut laden.
5. Preflight erneut ausfuehren.
6. Am Wiedereinstiegspunkt fortsetzen.
```

Wenn der Wiedereinstieg neue Bedeutung, neue Freigabe oder neue Architektur
braucht: Sprechakt oder neuer Abbruch, nicht plausibel fortsetzen.

---

## 6. Pendeln, Stagnation, Anti-Zeno

Pendeln liegt vor, wenn der Agent zwischen denselben Alternativen wechselt,
ohne neue Evidence zu gewinnen.

Stagnation liegt vor, wenn derselbe Blocker nach zwei inhaltlichen Schritten
unveraendert bleibt.

Dann gilt:

```text
kein dritter gleichartiger Versuch
kein weiterer Mikroschnitt
Blockerklasse benennen
Sprechakt, gezielte Klaerung oder Abbruch-Evidence erzeugen
```

Eine Phasengrenze innerhalb desselben Arbeitspakets ist kein
Benutzer-Checkpoint.

---

## 7. Schlussregel

Abbruch ist ein definierter Projektzustand. Er ist kein Anlass, Werkzeuge,
Regeln oder Scope so zu verkleinern, dass der Befund verschwindet.

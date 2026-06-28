# task-schnitt.md — Python-Projekt: Schnitt von Aufgaben und Semantic Working Set

> Ebene: PRIMING
> Rolle: Arbeitsschnitt-Protokoll
> Geltung: Tasks mit moeglicher semantischer Schnittgrenze
> Autoritative Frage: Wann ist ein echter Task-Schnitt noetig?
> Nicht zustaendig fuer: lokale Fachentscheidung, Ausfuehrungsmandat

> Bindender Einstieg und Kernregeln: `AGENTS.md`.
> Vollständige Detailregeln: die durch den jeweiligen Trigger aktivierten Verträge.
> Dieses Dokument wird geladen wenn ein Task-Schnitt bewertet oder korrigiert werden muss.

---

## 1. Was Task-Schnitt ist

Task-Schnitt ist die Entscheidung, ob eine Aufgabe in mehrere eigenstaendige
Arbeitspakete getrennt werden muss.

Ein guter Schnitt haelt den Semantic Working Set (SWS) klein und vollständig.
Ein schlechter Schnitt erzeugt entweder einen ContextGap (SWS unvollständig)
oder unnötig hohe Tokenkosten (SWS zu gross).

Task-Schnitt ist semantisch, nicht datei-, mengen- oder zeilenbasiert.
Blosse Teilbarkeit ist kein Schnittgrund.

```text
SWS klein         → nur was dieses Arbeitspaket wirklich braucht
SWS vollständig   → kein aktiv benötigter Begriff fehlt
SWS scharf        → keine Begriffe aus Räumen die dieses Arbeitspaket nicht berührt
```

---

## 2. Wann Task-Schnitt bewertet wird

Task-Schnitt wird nicht präventiv als Pflicht-Preflight ausgeführt.
Er wird bewertet wenn eine der folgenden Bedingungen eintritt:

```text
T1  SWS enthält einen Begriff, dessen Glossareintrag fehlt oder fuer die
    geplante Nutzung nicht ausreichend tief ist
    → zuerst prüfen: ist der Begriff durch zu breiten Schnitt im SWS?
    → wenn ja: Aufgabe enger schneiden — kein Sprechakt nötig
    → wenn Begriff für Teilaufgabe aktiv nötig bleibt: Sprechakt SP7 auslösen

T2  Aufgabe berührt mehr als einen semantischen Raum gleichzeitig
    → prüfen ob unterschiedliche Urteilskompetenzen oder Validierungsgrenzen vorliegen

T3  Aufgabe berührt eine Binding-Grenze
    → beide Seiten des Bindings werden aktiv
    → prüfen ob interne Phasen reichen oder ein echter Schnitt nötig ist

T4  Preflight zeigt bekannte Brüche die von der Aufgabe berührt werden
    → prüfen ob Schnitt den Bruch aktiv einschließt oder nur passiv streift

T5  Glossar-Ladeprotokoll würde beide Glossar-Dateien erfordern
    → Signal: Aufgabe schneidet über Raumgrenze
    → prüfen ob Teilung die Räume trennt
```

---

## 3. Schnitt-Prüfung

Wenn eine der Bedingungen T1–T5 eintritt:

```text
Schritt 1: Welche semantischen Räume werden aktiv berührt?
  domain/         → Domain-Begriffe im SWS?
  system/         → System-Semantics-Begriffe im SWS?
  infrastructure/ → konkrete Plattform-Details im SWS?
  adapters/       → wird eine Binding-Grenze überschritten?

Schritt 2: Reichen interne Phasen innerhalb eines Arbeitspakets?
  Ja  → Phasen im Plan notieren und im selben Lauf ausführen
  Nein → echten Task-Schnitt definieren

Schritt 3: Gibt es nach möglicher Schnitt-Verengung noch einen aktiv benötigten
           Begriff, dessen Glossareintrag fehlt oder für die geplante Nutzung nicht ausreichend tief ist?
  Ja  → Sprechakt SP7 vor Fortsetzung
  Nein → fortfahren

Schritt 4: Berührt die Aufgabe einen klassifizierten Known Breach aktiv?
  Ja  → Import-Checker ausführen
        Bekannter Bruch klassifiziert: vorsichtig fortfahren, Evidence notieren
        Nicht klassifiziert: HARD-Abbruch H2
  Nein → fortfahren

Schritt 5: Berührt die Aufgabe ein Symbol mit Migrationsstatus in migration-bridges.md?
  Ja → Status prüfen
       do-not-touch-mechanically: Sprechakt SP6
       allow-read-only: nicht neu einführen
       canonical: normal fortfahren
  Nein → fortfahren

Schritt 6: Autonomieregel prüfen
  Würde die Aufgabe einen Code-Typ in Raum X einführen,
  der Wissen aus Raum Y voraussetzt?
  Ja → H10 droht. Schnitt anders setzen oder Sprechakt.
  Nein → fortfahren
```

---

## 4. Ausführungsbreite

Gleichartige Änderungen innerhalb eines freigegebenen Arbeitspakets
werden gebündelt ausgeführt.

Begriffe:

```text
Arbeitspaket  extern zugesagter, vollständig lieferbarer Endzustand.
Phase         interner Abschnitt desselben autonomen Laufs.
Task-Schnitt  Grenze zwischen eigenständig lieferbaren oder unterschiedlich
              autorisierten Arbeitspaketen.
```

Ein Schnitt ist nur erforderlich, wenn sich mindestens eines unterscheidet:

```text
menschliche Festlegung
semantischer Raum oder Urteilskompetenz
Schreibrecht oder Freigabe
Validierungs- oder Rollback-Grenze
unabhängig abschließbarer Lieferzustand
```

Wenn T2, T3 oder T5 zutrifft und keine solche Grenze vorliegt:

```text
Phase A: erste semantische Seite bearbeiten
Phase B: zweite semantische Seite bearbeiten
Phase C: Tests, Checks und Dokumentprojektionen nachziehen
```

Phasen werden sequenziell ausgeführt. Eine Phasengrenze ist kein
Benutzer-Checkpoint.

Wenn eine echte Grenze vorliegt:

```text
Arbeitspaket A: eigener lieferbarer Zustand, eigene Evidence
Arbeitspaket B: erst nach Abschluss oder Entscheidung zu A
```

Wenn nur blosse Teilbarkeit vorliegt:

```text
100 gleichartige Importkorrekturen                → ein Arbeitspaket
freigegebenes Symbol an allen Verwendungsstellen  → ein Arbeitspaket
fehlende menschliche Festlegung                   → Sprechakt, kein Mikroschnitt
```

---

## 5. Signale für falschen Schnitt

```text
SIGNAL: Glossar-README Ladeprotokoll erfordert beide Glossar-Dateien
        für eine Änderung die nur einen Typ berührt
  → Aufgabe ist zu breit geschnitten
  → oder: Typ liegt semantisch falsch (eigenes Problem)

SIGNAL: SWS wächst während des Arbeitspakets durch unerwartete Abhängigkeiten
  → Schnitt war zu früh gesetzt
  → Agent hält an, bewertet ob eine echte semantische Grenze vorliegt

SIGNAL: Agent lädt Glossar-Einträge die für die aktuelle Änderung
        nicht direkt relevant sind
  → SWS enthält Rauschen
  → Schnitt schärfer setzen

SIGNAL: Wiederholte ContextGaps auf demselben Begriff
  → Begriff fehlt strukturell im Glossar
  → kein Schnitt-Problem — Sprechakt SP7

SIGNAL: Produktcode wurde geändert, Tests fehlen aber im Abschlusszustand
  → Arbeitspaket ist unvollständig
  → Tests sind normalerweise Phase desselben Arbeitspakets
```

---

## 6. Verhältnis zu anderen Regeln

```text
Task-Schnitt vs. Phase:
  Phase:        interne Reihenfolge innerhalb eines autonomen Arbeitspakets.
  Task-Schnitt: echte Grenze zwischen Arbeitspaketen.
  Eine Phase erzeugt keine Benutzerinteraktion.

Task-Schnitt vs. Sprechakt SP7:
  SP7 löst Task-Schnitt-Prüfung aus.
  Task-Schnitt kann SP7 einschränken:
  wenn eine echte semantische Grenze vorliegt, gilt SP7 nur für den Teilbereich
  der den fehlenden Begriff aktiv braucht.

Task-Schnitt vs. Preflight:
  Preflight ist eine Voraussetzungsprüfung — läuft über stabile PF-* IDs.
  Task-Schnitt ist eine Strukturentscheidung — läuft wenn T1-T5 eintreten.
  Preflight kann Task-Schnitt auslösen (wenn Brüche oder Lücken sichtbar).

Task-Schnitt vs. migration-bridges.md:
  Wenn ein Bridge-Symbol mit do-not-touch-mechanically im SWS liegt
  und mechanisch geändert würde: Aufgabe muss anders geschnitten werden,
  oder Sprechakt SP6.
```

---

## 7. State bei aktivem Schnitt

Wenn ein Arbeitspaket wegen echtem Task-Schnitt unterbrochen wird:

```markdown
Status:               IN BEARBEITUNG — TASK-SCHNITT
Aktives Arbeitspaket:  A | B
Zurückgestellt:        [Liste der zurückgestellten Schritte]
Wiedereintrittspunkt:  [erster Schritt des nächsten Arbeitspakets]
Voraussetzung:         [was vorher abgeschlossen oder entschieden sein muss]
```

---

## 8. Schlussregel

Ein Task-Schnitt ist gut, wenn der SWS nach dem Schnitt
vollständig, klein und scharf ist.

Ein Task-Schnitt ist schlecht, wenn er nur deshalb entsteht, weil eine
umfangreiche, aber gleichartige Änderung mechanisch teilbar wäre.

Wenn keine dieser drei Eigenschaften erreicht werden kann:
nicht raten. Sprechakt oder Abbruch.

---

*Bindender Einstieg: `AGENTS.md` — Detailregeln in den aktivierten Verträgen*
*Sprechakt-Protokoll: `sprechakt-protokoll.md`*
*Glossar-Ladeprotokoll: `glossar-README.md`*
*Preflight: `preflight-checkliste.md`*

# task-schnitt.md — Python-Projekt: Schnitt von Aufgaben und Semantic Working Set

> Vollständige operative Regeln: `AGENTS.md`.
> Dieses Dokument wird geladen wenn ein Task-Schnitt bewertet oder korrigiert werden muss.

---

## 1. Was Task-Schnitt ist

Task-Schnitt ist die Entscheidung, welche Teile einer Aufgabe
in einer Iteration ausgeführt werden — und welche nicht.

Ein guter Schnitt hält den Semantic Working Set (SWS) klein und vollständig.
Ein schlechter Schnitt erzeugt entweder einen ContextGap (SWS unvollständig)
oder unnötig hohe Tokenkosten (SWS zu groß).

```text
SWS klein         → nur was diese Iteration wirklich braucht
SWS vollständig   → kein aktiv benötigter Begriff fehlt
SWS scharf        → keine Begriffe aus Räumen die diese Iteration nicht berührt
```

---

## 2. Wann Task-Schnitt bewertet wird

Task-Schnitt wird nicht präventiv als Pflicht-Preflight ausgeführt.
Er wird bewertet wenn eine der folgenden Bedingungen eintritt:

```text
T1  SWS enthält einen Begriff, dessen Glossareintrag fehlt oder für die
    geplante Nutzung nicht ausreichend tief ist
    → zuerst prüfen: ist der Begriff durch zu breiten Schnitt im SWS?
    → wenn ja: Aufgabe enger schneiden — kein Sprechakt nötig
    → wenn Begriff für Teilaufgabe aktiv nötig bleibt: Sprechakt SP7 auslösen

T2  Aufgabe berührt mehr als einen semantischen Raum gleichzeitig
    → prüfen ob Teilung möglich ist

T3  Aufgabe berührt eine Binding-Grenze
    → beide Seiten des Bindings werden aktiv
    → prüfen ob eine Seite allein ausreicht

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

Schritt 2: Kann die Aufgabe auf einen Raum eingeschränkt werden?
  Ja  → Teilaufgabe definieren, restliche Schritte zurückstellen
  Nein → beide Räume sind strukturell nötig; beide Glossar-Dateien laden

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

## 4. Schnitt-Teilung

Wenn T2, T3 oder T5 zutrifft und Teilung möglich ist:

```text
Iteration A: eine Seite des Schnitts
  → SWS enthält nur Begriffe aus einem Raum
  → Glossar-Ladeprotokoll lädt nur eine Datei
  → Abschluss mit Evidence

Iteration B: andere Seite des Schnitts
  → erst nach Abschluss von Iteration A
  → SWS aufgebaut auf Evidence aus A
  → Binding erst wenn beide Seiten stabil sind
```

Kein Schritt aus Iteration B in Iteration A.
Kein „kurz noch" — der Schnitt ist die Grenze.

---

## 5. Signale für falschen Schnitt

```text
SIGNAL: Glossar-README Ladeprotokoll erfordert beide Glossar-Dateien
        für eine Änderung die nur einen Typ berührt
  → Aufgabe ist zu breit geschnitten
  → oder: Typ liegt semantisch falsch (eigenes Problem)

SIGNAL: SWS wächst während der Iteration durch unerwartete Abhängigkeiten
  → Schnitt war zu früh gesetzt
  → Agent hält an, bewertet ob Teilung noch möglich ist

SIGNAL: Agent lädt Glossar-Einträge die für die aktuelle Änderung
        nicht direkt relevant sind
  → SWS enthält Rauschen
  → Schnitt schärfer setzen

SIGNAL: Wiederholte ContextGaps auf demselben Begriff
  → Begriff fehlt strukturell im Glossar
  → kein Schnitt-Problem — Sprechakt SP7

SIGNAL: Aufgabe wechselt zwischen Produktionscode und Testcode in einer Iteration
  → Iterations-Trennung verletzt (Tests vs. Produktion)
  → schneiden: erst Produktcode, dann Tests, oder umgekehrt
```

---

## 6. Verhältnis zu anderen Regeln

```text
Task-Schnitt vs. Iterations-Trennung:
  Iterations-Trennung: nicht gleichzeitig Testcode und Produktionscode ändern.
  Task-Schnitt:        nicht gleichzeitig mehrere semantische Räume bearbeiten.
  Beide gelten unabhängig. Ein Schnitt kann beide Grenzen ziehen.

Task-Schnitt vs. Sprechakt SP7:
  SP7 löst Task-Schnitt-Prüfung aus.
  Task-Schnitt kann SP7 einschränken:
  wenn Teilung möglich, gilt SP7 nur für den Teilbereich
  der den fehlenden Begriff aktiv braucht.

Task-Schnitt vs. Preflight:
  Preflight ist eine Voraussetzungsprüfung — läuft immer (P1–P10).
  Task-Schnitt ist eine Strukturentscheidung — läuft wenn T1–T5 eintreten.
  Preflight kann Task-Schnitt auslösen (wenn Brüche oder Lücken sichtbar).

Task-Schnitt vs. migration-bridges.md:
  Wenn ein Bridge-Symbol mit do-not-touch-mechanically im SWS liegt
  und mechanisch geändert würde: Aufgabe muss anders geschnitten werden,
  oder Sprechakt SP6.
```

---

## 7. State bei aktivem Schnitt

Wenn eine Iteration wegen Schnitt-Teilung unterbrochen wird:

```markdown
Status:               IN BEARBEITUNG — TEILSCHNITT
Aktive Iteration:     A | B
Zurückgestellt:       [Liste der zurückgestellten Schritte]
Wiedereintrittspunkt: [erster Schritt von Iteration B]
Voraussetzung:        [was Iteration A abschließen muss]
```

---

## 8. Schlussregel

Ein Task-Schnitt ist gut, wenn der SWS nach dem Schnitt
vollständig, klein und scharf ist.

Wenn keine dieser drei Eigenschaften erreicht werden kann:
nicht raten. Sprechakt oder Abbruch.

---

*Vollständige Regeln: `AGENTS.md`*
*Sprechakt-Protokoll: `sprechakt-protokoll.md`*
*Glossar-Ladeprotokoll: `glossar-README.md`*
*Preflight: `preflight-checkliste.md`*

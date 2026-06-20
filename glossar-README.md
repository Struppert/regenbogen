# Glossar-README.md — Ladeprotokoll und Navigation

**Dokumenttyp: Operativ / referenziell**

> Dieses Dokument ist der Einstiegspunkt für das Glossar-System.
> Es beschreibt welches Glossar wann geladen wird und wie die Teile zusammenhängen.
> Kein Inhaltsdokument — Navigationsdokument.

---

## 1. Glossar-Architektur

```text
glossar-domain.md      → Fachdomänenbegriffe
                          Autorität: Domänenexperte (nicht-technisch)
                          Raum: domain/

glossar-system.md      → System-Semantics-Begriffe
                          Autorität: Systemarchitekt
                          Raum: system/

migration-bridges.md   → Symbole mit Migrationsstatus und Bridge-Funktion
                          Nicht nach Bedeutung geordnet — nach Status

package-schema.md      → Raumregeln, Importmatrix, Known Breaches
                          Nicht Begriffe — Räume und ihre Grenzen
```

Diese Dokumente sind **keine Redundanz**. Jedes beantwortet eine andere Frage:

```text
glossar-domain.md:   Was bedeutet dieser Begriff fachlich?
glossar-system.md:   Wie verhält sich das System in diesem Zustand?
migration-bridges.md: Darf dieser Begriff mechanisch angefasst werden?
package-schema.md:   Welche Importe sind in diesem Raum erlaubt?
```

---

## 2. Ladeprotokoll (Preflight P5)

**Schritt 1: Aktive Begriffe bestimmen**

```text
Welche Begriffe werden in dieser Iteration
  - geändert, umbenannt oder verschoben?
  - als Grundlage einer Entscheidung gebraucht?
  - in neuen Namen, Typen, Fehlern oder Tests eingeführt?
```

**Schritt 2: Raum bestimmen**

```text
Für jeden aktiven Begriff:
  domain/   → glossar-domain.md laden
  system/   → glossar-system.md laden
  Beide     → beide laden (Signal für Task-Schnitt T5)
  Unbekannt → Sprechakt SP7 oder Task-Schnitt T1
```

**Schritt 3: Migrationsstatus prüfen**

```text
Für jeden aktiven Begriff:
  Ist er in migration-bridges.md eingetragen?
  → do-not-touch-mechanically: STOPP, Sprechakt SP6
  → allow-read-only: nicht neu einführen
  → canonical: normal fortfahren
```

**Schritt 4: Vollständigkeit prüfen**

```text
Hat jeder aktiv gebrauchte Begriff einen vollständigen Eintrag?
  Ja → fortfahren
  Nein → Task-Schnitt T1 prüfen
         Wenn Begriff danach noch aktiv nötig: Sprechakt SP7
```

---

## 3. Glossar-Eintrag vs. Sprechakt

```text
Wenn ein Begriff fehlt:
  1. Kann die Aufgabe ohne ihn abgeschlossen werden? (Task-Schnitt T1)
     → Ja: enger schneiden, kein Sprechakt
     → Nein: Sprechakt SP7

Wenn ein Begriff vorhanden aber unvollständig ist:
  → Sprechakt SP7 mit Angabe welches Feld fehlt
  → Nicht raten, nicht aus Code ableiten

Wenn ein Begriff vorhanden und vollständig ist:
  → Glossareintrag als Entscheidungsgrundlage verwenden
  → Nicht am Eintrag vorbei implementieren
```

---

## 4. Wann wird das Glossar nicht geladen?

```text
Nicht laden bei:
  - reinen Lint/Format-Fixes
  - Kommentar-Korrekturen ohne Begriffe
  - rein technischen Refactorings ohne neue Begriffe
  - Änderungen ausschließlich in infrastructure/ oder tools/
    (diese Räume brauchen kein Fachdomänenglossar)
```

---

## 5. Glossar und Autonomieregel

Ein Glossareintrag ist operativ wenn er die Autonomieregel erfüllt:

> Ein einzelner Experte kann den Begriff vollständig beurteilen
> ohne andere Räume zu kennen.

Wenn ein Glossareintrag Begriffe aus einem anderen Raum voraussetzt
um verstanden zu werden — ist er kein valider Glossareintrag.
Er ist ein Signal, dass die Grenze falsch gezogen ist.

---

## 6. Verhältnis zu AGENTS.md

```text
AGENTS.md                  → operative Regeln, Schreibrechte, Abbrüche
glossar-domain.md          → Fachbegriffs-Bedeutungen
glossar-system.md          → Betriebsbegriffs-Bedeutungen
package-schema.md          → Raumregeln und Importmatrix
migration-bridges.md       → Symbole mit Migrationsstatus
grundsatz.md               → warum dieses System so aufgebaut ist

Bei Widerspruch: Autoritätsreihenfolge in regelmatrix.md.
```

---

## 7. Schlussregel

Das Glossar ist fertig genug für eine Iteration wenn alle aktiv
gebrauchten Begriffe vollständige Einträge haben.

Es muss nicht vollständig sein — nur vollständig für den aktuellen SWS.

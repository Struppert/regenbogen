# ausfuehrungsmandat-protokoll.md — Arbeitsmodus und Wirkungsgate

> Dieses Dokument regelt, wann ein Agent lesen, planen oder das Repository
> veraendern darf.

---

## 1. Grundregel

Ein Auftrag erlaubt nur den eindeutig ausgesprochenen Arbeitsmodus.

Ohne nachweisbares Ausfuehrungsmandat gilt:

```text
Arbeitsmodus: ANALYSE
```

Schreibrecht, beschreibbare Dateiklasse, Fast-Path, vorhandener Plan,
festgelegter Sprechakt und fehlender Blocker ersetzen kein
Ausfuehrungsmandat.

---

## 2. Arbeitsmodi

```text
ANALYSE
  Erlaubt: lesen, untersuchen, Befunde benennen, Vorschlaege im Chat machen.
  Verboten: Repository-Mutation, Plan-Datei, Evidence-Datei, Codeaenderung.

PLAN
  Erlaubt: ANALYSE, Plan anlegen/aendern, Entscheidungsfragen formulieren,
           offene Sprechakte oder Diagnose-Evidence anlegen.
  Verboten: Produktcode, Tests, Konfiguration, Dependencies, Governance,
            Migrationen ausfuehren.

AUSFUEHRUNG
  Erlaubt: freigegebenen Plan im Mandatsscope umsetzen, interne Phasen
           durchlaufen, Tests/Checks ausfuehren, Planfortschritt an
           Phasengrenzen aktualisieren.
  Voraussetzung: aktives, scope-gueltiges Ausfuehrungsmandat.
```

Wenn der Arbeitsmodus unklar ist: ANALYSE.

---

## 3. Ausfuehrungsmandat

Ein Ausfuehrungsmandat ist die konkrete Erlaubnis, eine benannte Planversion in
einem benannten Scope auszufuehren.

Mindestfelder:

```text
Mandat-ID:
Mandatstatus: nicht erteilt | aktiv | widerrufen | erloschen
Plan-ID:
Freigegebene Plan-Version:
Freigabezeitpunkt:
Freigabetext oder Freigabereferenz:
Freigegebener Scope:
Freigegebene geschuetzte Dateien:
Nicht freigegeben:
Gueltigkeit: bis Abschluss | bis Widerruf | begrenzte Phase
```

Ein Mandat gilt nur fuer die genannte Plan-Version und den genannten Scope.

---

## 4. Gueltige Freigabe

Eine Freigabe muss Handlung, Scope und Ausfuehrungsabsicht positiv benennen.

Gueltige Formen:

```text
AUSFUEHRUNG FREIGEGEBEN
Plan: PLAN-YYYY-MM-DD-<kurzname>
Plan-Version: <n>
Scope: <vollstaendiger Plan | begrenzter Scope>
Autonomie: bis Abschluss oder echter Blocker
```

Oder im initialen Auftrag:

```text
ARBEITSMODUS: AUSFUEHRUNG
Setze den beschriebenen Scope vollstaendig um.
Scope:
Geschuetzte Dateien:
Autonomie:
```

Nicht ausreichend:

```text
ja
genau
passt
weiter
so machen wir es
der Plan sieht gut aus
das muessen wir aendern
```

Solche Aussagen koennen Befund oder Plan bestaetigen. Sie erteilen nur dann ein
Mandat, wenn sie auf eine unmittelbar vorher explizit formulierte Mandatsfrage
mit Plan-ID, Plan-Version und Scope antworten.

---

## 5. Wirkungsgate W0

W0 wird unmittelbar vor der ersten Repository-Mutation geprueft.

```text
1. Welcher Arbeitsmodus gilt?
2. Existiert ein aktives Ausfuehrungsmandat?
3. Passt die freigegebene Plan-Version?
4. Liegt die geplante Mutation im Scope?
5. Ist die Dateiklasse beschreibbar oder geschuetzt?
6. Ist eine geschuetzte Datei ausdruecklich vom Mandat gedeckt?
```

Wenn W0 nicht gruen ist: keine Mutation. In ANALYSE zurueckfallen oder
Mandat/Delta-Freigabe anfordern.

W0 ist kein Preflight-Schritt P0. Die Preflight-Nummern P1-P9 bleiben stabil.

---

## 6. Mandatsreichweite

Ein aktives Mandat deckt den vollstaendigen semantischen Arbeitsschnitt ab:

```text
interne Phasen
Produktcode
zugehoerige Tests
lokale Refactorings im Scope
Imports und Formatierung
Dokumentationsprojektionen
Validierung und Fehlerkorrekturen innerhalb des Zielmodells
```

Eine Phasengrenze ist kein Benutzer-Checkpoint.

Neue Freigabe ist erforderlich bei:

```text
neuer Semantik
neuer Runtime-Dependency
zusaetzlicher oeffentlicher API
zusaetzlichem semantischem Raum ausserhalb des Plans
nicht genannter geschuetzter Datei
neuem Known-Breach-Scope
wesentlich anderem Zielmodell
```

---

## 7. Delta-Freigabe

Wenn ein Mandat zu klein ist, keine Neuplanung erzwingen. Delta dokumentieren:

```markdown
## Benoetigte Mandatserweiterung

Bisheriger Scope:
Neu erkannter Scope:
Warum nicht im urspruenglichen Plan enthalten:
Zusaetzliche Dateien:
Zusaetzliche Semantik:
Zusaetzliche Risiken:
Auswirkung bei Ablehnung:
```

Bis zur Delta-Freigabe keine Wirkung ausserhalb des alten Mandats.

---

## 8. Plan-Version und Mandatsverlust

Jede mandatsrelevante Planaenderung erhoeht `Plan-Version`.

Mandatsrelevant sind Aenderungen an:

```text
Zielzustand
Scope
geschuetzten Dateien
Semantik
Dependencies
oeffentlicher API
Validierungsgrenze
Rollback-Grenze
```

Nach mandatsrelevanter Aenderung gilt das alte Mandat nicht mehr fuer die neue
Plan-Version.

---

## 9. Widerruf und Wiedereinstieg

Ein Mandat kann widerrufen oder erloschen sein.

Bei Kontextwechsel oder neuem Agenten:

```text
Mandat aktiv und Scope unveraendert  -> autonom fortsetzen
Mandat fehlt oder Plan-Version weicht ab -> ANALYSE, keine Wirkung
Mandat widerrufen oder erloschen -> keine Wirkung
```

Der Agent darf sein Mandat nicht selbst aktivieren.

---

## 10. Schlussregel

Analyse ist erlaubt. Planung ist nur im PLAN- oder AUSFUEHRUNGS-Scope erlaubt.
Wirkung ist nur mit aktivem Ausfuehrungsmandat erlaubt.

Innerhalb eines gueltigen Mandats arbeitet der Agent autonom bis zum
vollstaendigen, validierten Arbeitsschnitt.

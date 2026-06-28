# ausfuehrungsmandat-protokoll.md — Arbeitsmodus und Wirkungsgate

> Ebene: PRIMING
> Rolle: normatives Ausfuehrungsprotokoll
> Geltung: jeder Aufgabenlauf
> Autoritative Frage: Wann darf ein Agent planen oder Wirkung erzeugen?
> Nicht zustaendig fuer: lokale Architektur, fachliche Bedeutung, konkrete Aufgabe

> Dieses Dokument regelt, wann ein Agent lesen, planen oder das Repository
> veraendern darf.

---

## 1. Grundregel

Ein Auftrag erlaubt nur den eindeutig ausgesprochenen Arbeitsmodus.

Ohne eindeutig ausgesprochenen Arbeitsmodus gilt:

```text
Arbeitsmodus: ANALYSE
```

PLAN erfordert einen ausdruecklichen Planungsauftrag, aber kein
Ausfuehrungsmandat.

AUSFUEHRUNG erfordert ein aktives, scope-gueltiges Ausfuehrungsmandat.

Schreibrecht, beschreibbare Dateiklasse, Fast-Path, vorhandener Plan,
festgelegter Sprechakt und fehlender Blocker ersetzen kein
Ausfuehrungsmandat.

---

## 2. Arbeitsmodi und Wirkungstypen

Das Protokoll unterscheidet drei Wirkungsklassen:

```text
diagnostische Wirkung
  Plan-, Entscheidungs-, Sprechakt- oder Evidence-Artefakte, die den
  Zustand beschreiben oder eine Entscheidung vorbereiten.

normative Wirkung
  Aenderungen an Bedeutung, Entscheidung, Freigabe, Governance oder
  gueltigem Projektstatus.

projekt-transformative Wirkung
  Aenderungen an Produktcode, Tests, Konfiguration, Dependencies oder
  Migrationszustand.
```

Diagnostisch sind nur Entwurf, Befund, offene Frage, offener Sprechakt,
Planfortschritt oder Abbruch-/Diagnose-Evidence in ausdruecklich dafuer
vorgesehenen Artefaktraeumen.

Normativ oder projekt-transformativ sind insbesondere:

```text
Sprechakt festlegen, widerrufen oder ersetzen
Zielmodellentscheidung materialisieren
Known Breach genehmigen oder erweitern
Plan-Ziel, Scope oder Plan-Version mandatsrelevant aendern
operative Governance aendern
Produkt-, Test-, Konfigurations- oder Migrationszustand aendern
```

```text
ANALYSE
  Erlaubt: lesen, untersuchen, Befunde benennen, Vorschlaege im Chat machen.
  Verboten: Repository-Mutation, Plan-Datei, Evidence-Datei, Codeaenderung.

PLAN
  Erlaubt: ANALYSE, Plan anlegen/aendern, Entscheidungsfragen formulieren,
           Sprechakt-Artefakte mit Status offen anlegen (nicht festlegen),
           Diagnose-Evidence anlegen.
  Verboten: Produktcode, Tests, Konfiguration, Dependencies, Governance,
            Migrationen ausfuehren, Sprechakte festlegen oder normative
            Statusaenderungen vornehmen.

AUSFUEHRUNG
  Erlaubt: freigegebenen Plan oder Direktauftrag im Mandatsscope umsetzen,
           interne Phasen durchlaufen, Tests/Checks ausfuehren,
           Checkpoint an Phasengrenzen aktualisieren.
  Voraussetzung: aktives, scope-gueltiges Ausfuehrungsmandat.
```

PLAN erlaubt diagnostische Wirkung in den dafuer vorgesehenen Artefakten.
PLAN erlaubt keine normative oder projekt-transformative Wirkung.

Wenn der Arbeitsmodus unklar ist: ANALYSE.

---

## 3. Ausfuehrungsmandat

Ein Ausfuehrungsmandat ist die konkrete Erlaubnis, eine benannte Grundlage in
einem benannten Scope auszufuehren.

Die Grundlage ist entweder:

```text
Plan
  Fuer nichttriviale oder mehrphasige Arbeit.

Direktauftrag
  Fuer kleine, vollstaendig bestimmte Fast-Path-Arbeit ohne Planartefakt.
```

Ein nicht materialisiertes Direktmandat gilt nur im aktuellen
zusammenhaengenden Gespraechs- und Agentenkontext. Bei Kontextwechsel, neuem
Agenten oder Wiederaufnahme erlischt es mangels nachweisbarer Grundlage. Fuer
wiederaufnehmbare Arbeit ist ein Plan erforderlich.

Ein Direktauftrag ist unveraenderlich. Aendern sich Ziel, Scope, Schutzklasse
oder Semantik, erlischt das Direktmandat. Dann ist ein neues Direktmandat
oder ein Plan erforderlich.

Mindestfelder:

```text
Mandat-ID:
Mandatstatus: nicht erteilt | aktiv | widerrufen | erloschen
Mandatsgrundlage: Plan | Direktauftrag
Contract-ID:
Run-ID:
Mandatsrevision:
Grundlagen-ID: Plan-ID | Auftragsreferenz
Grundlagen-Version: Plan-Version | 1
Freigabezeitpunkt:
Freigabetext oder Freigabereferenz:
Freigegebener Scope:
Freigegebene geschuetzte Dateien:
Nicht freigegeben:
Gueltigkeit: bis Abschluss | bis Widerruf | begrenzte Phase
```

`Contract-ID` und `Run-ID` sind Pflichtfelder wenn das Laufbindungs-Konzept
aktiv ist. In Projekten ohne Contract-/Run-Infrastruktur darf `—` als
gueltiger Platzhalterwert eingetragen werden.

Ein Mandat gilt nur fuer die genannte Grundlage, Version und den genannten
Scope.

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
Mandatsgrundlage: Direktauftrag
Scope:
Geschuetzte Dateien:
Autonomie:
```

Der Mensch muss nicht alle Verwaltungsfelder formulieren. Der Agent darf sie
mechanisch aus einer eindeutigen Freigabe materialisieren:

```text
Mandat-ID:
  MD-YYYY-MM-DD-<kurzname>

Grundlagen-ID:
  Auftragsreferenz aus Datum, Kurzname und kurzem Freigabezitat

Grundlagen-Version:
  1
```

Der Agent darf dabei keine Reichweite ergaenzen, keine geschuetzten Dateien
hinzuerfinden, keine Gueltigkeit erweitern und keine Mehrdeutigkeit selbst
aufloesen.

Die menschliche Aeusserung aktiviert das Mandat ausserhalb des Repositorys.
Ein Mandatsartefakt dokumentiert nur das bereits erzeugte Mandat. Das Schreiben
dieser getreuen Evidence-Projektion darf keine Reichweite erweitern.

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
mit Grundlage, Version und Scope antworten.

---

## 5. Wirkungsgate WG-MUTATION

WG-MUTATION ist eine fortlaufende Invariante. Es wird vor der ersten
Repository-Mutation geprueft und erneut, sobald Wirkungstyp, Scope,
Schutzklasse, Mandatsstatus oder Grundlagen-Version sich aendern.

WG-MUTATION ist eine semantische Gate-ID, keine positionsabhaengige
Preflight-Nummer.

```text
1. Wirkungstyp bestimmen.

2a. Diagnostische Wirkung:
    - Arbeitsmodus PLAN oder AUSFUEHRUNG?
    - erlaubter diagnostischer Artefaktraum?
    - keine normative Statusaenderung?
    - kein Ausfuehrungsmandat erforderlich.

2b. Normative oder projekt-transformative Wirkung:
    - Arbeitsmodus AUSFUEHRUNG?
    - aktives Ausfuehrungsmandat?
    - Mandat.Contract-ID passt zum aktiven Contract?
    - Mandat.Run-ID passt zum aktiven Run?
    - passende Grundlage und Version?
    - gebundene Priming-Revision unveraendert?
    - gebundene Repository-Vertragsrevision unveraendert oder als geplante
      Zieltransformation im Contract beschrieben?
    - Current HEAD ist Base-Snapshot oder zulaessige Fortsetzung davon?
    - Interaktions-, Recovery- und Arbeitsprofil passen zum Lauf?
    - Mutation im Scope?
    - Schutzklasse gedeckt?
    - geschuetzte Datei ausdruecklich vom Mandat gedeckt?
```

Wenn WG-MUTATION fuer den jeweiligen Wirkungstyp nicht gruen ist: keine
Mutation. In ANALYSE zurueckfallen oder Mandat/Delta-Freigabe anfordern.

WG-MUTATION ist kein Preflight-Schritt. Die Preflight-IDs `PF-*` bleiben
stabil.

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

Ausfuehrungsprofil (dreidimensional):

```text
Interaktionsprofil:
  interaktiv
    Menschliche Rueckfragen sind normal. Checkpoint optional.
  autonom
    Keine planmaessigen Rueckfragen. Checkpointpflicht.

Recovery-Profil:
  normal
    Kein erhoehter Recovery-Bedarf.
  overnight
    Checkpointpflicht plus gesicherter Recovery-Zustand vor laengerem Lauf.

Arbeitsprofil:
  feature
    Normaler Entwicklungslauf.
  brownfield-migration
    Planpflicht, Migrationsevidence, Governance-Rueckflusspruefung.
  governance-migration
    Zusaetzliche Deckung fuer geschuetzte Governance-Dateien erforderlich.
```

Neue Freigabe ist erforderlich bei:

```text
neuer Semantik
neuer Runtime-Dependency
zusaetzlicher oeffentlicher API
zusaetzlichem semantischem Raum ausserhalb der Grundlage
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
Warum nicht in der urspruenglichen Grundlage enthalten:
Zusaetzliche Dateien:
Zusaetzliche Semantik:
Zusaetzliche Risiken:
Auswirkung bei Ablehnung:
```

Bis zur Delta-Freigabe keine Wirkung ausserhalb des alten Mandats.
Eine Mandatserweiterung eines Direktauftrags fuehrt in der Regel in einen Plan.

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

Ein Mandat ist an Contract-ID und Run-ID gebunden. Aendert sich eine gebundene
Priming-, Repository-, Plan-, Scope-, Autorisierungs-, Base-Snapshot- oder
eine der drei Profil-Revisionen (Interaktions-, Recovery-, Arbeitsprofil)
unerwartet, erlischt die bisherige Ausfuehrungsbindung. Fortsetzung erfordert
neuen Preflight, neue Contract-ID und, soweit betroffen, neue Autorisierung.

Eine geplante Governance- oder Repository-Transformation ist keine unerwartete
Revisionaenderung. Sie bleibt an Baseline, Zielmodell, Plan und Mandat des
Contracts gebunden, bis Verify den neuen Zielzustand bestaetigt oder der Lauf
abbricht.

Bei Kontextwechsel oder neuem Agenten:

```text
Mandat aktiv und Scope unveraendert  -> autonom fortsetzen
Mandat fehlt oder Grundlagen-ID/Grundlagen-Version weicht ab -> ANALYSE, keine Wirkung
Mandat widerrufen oder erloschen -> keine Wirkung
```

Der Agent darf sein Mandat nicht selbst aktivieren.

---

## 10. Schlussregel

Analyse ist erlaubt.

Diagnostische Wirkung ist nur in PLAN oder AUSFUEHRUNG und nur in vorgesehenen
diagnostischen Artefaktraeumen erlaubt.

Normative oder projekt-transformative Wirkung ist nur mit aktivem,
scope-gueltigem Ausfuehrungsmandat erlaubt.

Innerhalb eines gueltigen Mandats arbeitet der Agent autonom bis zum
vollstaendigen, validierten Arbeitsschnitt.

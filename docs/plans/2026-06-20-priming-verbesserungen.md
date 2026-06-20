# Plan: Priming-Verbesserungen aus Systemanalyse

Status: abgeschlossen
Datum: 2026-06-20
Freigabe: 2026-06-20 (Dieter Haag)
Bearbeiter: Claude Sonnet 4.6

## Aufgabe

Sieben Schwächen des Agenten-Priming-Systems schliessen, die in
`analysen/priming-analyse.md` identifiziert wurden. Alle Änderungen
betreffen geschützte Dokumente und erfordern daher explizite Freigabe.

Die Verbesserungen sind in zwei Gruppen gegliedert:

**Gruppe A — Regelschärfung ohne neue Begriffe (V1, V2, V5, V6, V7)**
Bestehende Regeln werden präzisiert oder operationalisiert.
Kein neuer semantischer Begriff entsteht.

**Gruppe B — Glossarstruktur (V3, V4)**
Das Glossarformat wird explizit gemacht (V3) und Metasystem-Begriffe werden
ausgelagert (V4). V4 ändert das Ladeprotokoll und ist ein Sprechakt-Kandidat.

## Betroffene Räume

Kein Produktionscode. Alle Änderungen betreffen das Agenten-Metasystem:

```text
migration-bridges.md          V1 — Diff-Prüfverfahren
preflight-checkliste.md       V2 — Fast-Path für SICHER-Tasks
AGENTS.md                     V5 — H10 operationalisieren
learning-matrix.md            V6 — Muster-Schwelle
AGENTS-COMPACT.md             V7 — Platzhalter-Block leserlich
glossar-domain.md             V3 — Minimalformat einführen
glossar-system.md             V3 — Minimalformat; V4 — Metabegriffe auslagern
glossar-README.md             V4 — Ladeprotokoll um glossar-meta.md erweitern
glossar-meta.md               V4 — neu, Metasystem-Begriffe der Agenten-Box
```

## Nicht-Ziele

- kein Produktionscode, keine Tests, keine Domain-Logik
- keine neuen Fachbegriffe (SP1)
- keine neuen Fehlercodes (SP3)
- keine Runtime-Dependency (SP4)
- keine Änderung an `package-schema.md` oder `regelmatrix.md`
- kein Umbau des Sprechakt- oder Abbruch-Systems — nur Schärfung bestehender Regeln
- keine Änderung an `AGENT-SETUP.md` oder `tools/`

## Schreibrechte

Alle betroffenen Dokumente sind geschützt (AGENTS.md Abschnitt 9).

```text
Explizit freigegeben (Freigabe: 2026-06-20, Dieter Haag):
  migration-bridges.md
  preflight-checkliste.md
  AGENTS.md
  learning-matrix.md
  AGENTS-COMPACT.md
  glossar-domain.md
  glossar-system.md
  glossar-README.md
  glossar-meta.md          (neue Datei, Anlage freigegeben)
```

## Erwartete Änderungen

### V1 — migration-bridges.md: Diff-Prüfverfahren

Abschnitt 5 ("Wie ein Agent dieses Dokument verwendet") um aktive
Diff-Prüffragen ergänzen:

- Erscheint das Symbol als neues Vorkommen im geplanten Diff?
- Erweitere ich seinen Geltungsbereich?
- Mache ich aus passiver Kompatibilität wieder aktive Semantik?
- Wenn ja zu einer dieser Fragen: HARD-Abbruch H2.

Zusätzlich: visueller Warnblock über der Bridge-Registry, der klar macht,
dass Einträge keine Arbeitsgrundlage sind.

### V2 — preflight-checkliste.md: Fast-Path für SICHER-Tasks

Neuer Abschnitt 0 ("Risikoklassen-Weiche") vor P1:

- SICHER-Task → Fast-Path: nur P1 (AGENTS-COMPACT), P7 (Checker), P8 (Testpflicht)
- MITTEL oder höher → vollständiger Preflight P1–P11
- Zweifel über Risikoklasse → vollständiger Preflight

Risikoklassen-Definition referenziert AGENTS.md Abschnitt 6 (Safe Tasks).

### V3 — glossar-domain.md und glossar-system.md: Minimalformat

Neues Metafeld `Eintragstiefe: vollständig | minimal` im Eintrag-Format
(Abschnitt 2 beider Glossare).

Definition:
- `minimal`: Bedeutung + Projektionen + Migrationsstatus vorhanden,
  alle anderen Felder bewusst weggelassen
- `vollständig`: alle Formatfelder vorhanden

Alle bestehenden Einträge werden explizit als `minimal` markiert.
Upgrade auf `vollständig` erfordert keinen Sprechakt, nur Pflege.

### V4 — glossar-system.md und glossar-README.md: Metabegriffe auslagern

Abschnitt "Metasystem-Begriffe der Agenten-Box" aus `glossar-system.md`
in neue Datei `glossar-meta.md` auslagern.

`glossar-README.md` erhält neue Laderegel:
- `glossar-meta.md` nur bei Systempflege laden (Preflight für Agenten-Box-Arbeit)
- nicht bei normaler Fach- oder Systemarbeit

`glossar-system.md` enthält danach ausschliesslich Produktbegriffe.

### V5 — AGENTS.md: H10 operationalisieren

H10 erhält konkrete Erkennungsregeln in Abschnitt 10:

- domain-Typ enthält Feld aus Infrastruktur- oder System-Vokabular
  (retry_count, http_status, db_id)
- domain-Funktion gibt Wert zurück, der nur mit Laufzeitprotokoll
  interpretierbar ist
- Invariante eines domain-Begriffs kann nur ein Systemarchitekt,
  nicht ein Domänenexperte beurteilen

Prüfhilfe: Kompetenzfrage des Glossareintrags heranziehen.
Wenn die Antwort ein Systemarchitekt statt ein Domänenexperte liefern muss:
H10 auslösen.

### V6 — learning-matrix.md: Muster-Schwelle

Neuer Abschnitt 1.1 ("Muster-Schwelle"):

Ein Muster gilt als systemic wenn:
- es in mindestens 2 unabhängigen Sessions mit gleichem Kern auftritt, oder
- es einen HARD-Abbruch verursacht hat, oder
- der Mensch es nach einem einzelnen Erfahrungsbericht explizit als systemic markiert.

Systemische Muster werden in der Matrix eingetragen.
Nicht-systemische Einzelbeobachtungen bleiben im Erfahrungsbericht.

### V7 — AGENTS-COMPACT.md: Platzhalter-Block

Den instanziierten Werte-Block (Zeile 10–13) als lesbare Schlüssel-Wert-Tabelle
formatieren. Inhalt bleibt unverändert, nur Darstellung wird korrigiert.

## Sprechakte

### Sicher kein Sprechakt nötig: V1, V2, V5, V6, V7

Diese Änderungen präzisieren bestehende Regeln ohne neue semantische Begriffe.
Sie sind Freigabe-pflichtig, aber kein Sprechakt-Tatbestand.

### Möglicherweise SP2: V4 (Auslagerung glossar-meta.md)

V4 ändert das Ladeprotokoll des Glossarsystems und führt eine neue Datei
mit eigener Ladebedingung ein. Das ist eine neue systemsemantische Arbeitsregel
für das Agenten-Metasystem.

Zu klären: Reicht Freigabe als strukturelle Entscheidung, oder erfordert
die neue Laderegel einen SP2-Sprechakt?

### Möglicherweise SP2: V3 (Eintragstiefe-Feld)

Das neue Metafeld `Eintragstiefe` ist kein Fachbegriff, aber ein neuer
systemsemantischer Begriff im Glossar-Metasystem.

Zu klären: Reicht Freigabe, oder ist SP2 nötig?

## Testpflicht

Kein Produktionscode betroffen. Keine Unit-Tests nötig.

Prüfpflicht nach Umsetzung:

```bash
python tools/check_agent_docs_consistency.py --instantiated
python tools/check_import_layers.py --preflight src tests tools
python tools/resolve_test_obligations.py --selfcheck --instantiated
```

Zusätzlich: manuelle Konsistenzprüfung der geänderten Dokumente gegen
`regelmatrix.md` und `AGENTS.md`.

## Abbruchbedingungen

```text
H1   Geschützte Datei ohne Freigabe geändert
H3   Widerspruch zwischen geänderten Dokumenten und AGENTS.md / regelmatrix.md
H4   Neuer Begriff wird faktisch eingeführt ohne Sprechakt
     (betrifft besonders V3 Eintragstiefe und V4 glossar-meta)
```

## Wiedereinstiegspunkt

Nach Freigabe dieses Plans und Klärung der SP2-Fragen (V3, V4):

1. V7 zuerst — kleinste Änderung, kein semantisches Risiko
2. V6 — Learning-Matrix, keine Regelkollision
3. V2 — Fast-Path Preflight
4. V5 — H10 Erkennungsregeln
5. V1 — Bridge Diff-Prüfverfahren
6. V3 — Glossar Minimalformat (nach SP2-Klärung)
7. V4 — Auslagerung glossar-meta.md (nach SP2-Klärung, zuletzt wegen
        Abhängigkeit zu V3)

Nach jeder Gruppe: `check_agent_docs_consistency.py` ausführen.

## Abschlusskriterien

- `migration-bridges.md` enthält aktives Diff-Prüfverfahren und Warnblock
- `preflight-checkliste.md` enthält Fast-Path für SICHER-Tasks
- `AGENTS.md` enthält operationalisierbare H10-Erkennungsregeln
- `learning-matrix.md` enthält definierte Muster-Schwelle
- `AGENTS-COMPACT.md` Platzhalter-Block ist lesbar formatiert
- alle Glossareinträge tragen explizites `Eintragstiefe`-Feld
- `glossar-meta.md` existiert mit allen Metasystem-Begriffen
- `glossar-system.md` enthält ausschliesslich Produktbegriffe
- `glossar-README.md` enthält aktualisiertes Ladeprotokoll
- `check_agent_docs_consistency.py` läuft grün
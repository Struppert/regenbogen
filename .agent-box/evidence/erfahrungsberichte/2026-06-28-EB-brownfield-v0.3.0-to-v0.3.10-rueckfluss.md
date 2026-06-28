# Erfahrungsbericht: Brownfield-Migration v0.3.0 -> v0.3.10 Rueckfluss

Datum: 2026-06-28
Learning-Matrix-Kandidat: ja
  (ja wenn: HARD-Abbruch verursacht, oder ≥2 Sessions gleiches Muster,
   oder Mensch markiert als systemic — siehe learning-matrix.md §1a)
Vorgeschlagene Musterkennung: Checker-Konvergenz vs. Legacy-Bestand
Session-Typ:  abgeschlossen
Aufgabe:      Brownfield-Migration box-python v0.3.0 -> v0.3.10 ausführen und Rueckfluss-Artefakte nachziehen
Ergebnis:     Governance auf v0.3.10-Stand migriert, Migrationsevidence und Rueckflussbericht angelegt, Validierung bis auf dokumentierten Format-Altbestand grün

---

## Was sich bewährt hat

Die Kombination aus Plan, festgelegten SP-BF-Entscheidungen und nachgelagerten
Tool-Tests hat die Migration kontrollierbar gemacht. Besonders nützlich war,
dass der neue Konsistenzchecker sofort sichtbar gemacht hat, welche Teile
tatsächlich aktive Migrationsfehler sind und welche nur Legacy-Reibung des
Bestands darstellen.

Auch die Trennung zwischen freigegebenem Migrationsscope und nicht freigegebenem
`tools/instantiate/*` hat funktioniert. Statt das Instanziierungswerkzeug
stillschweigend mitzuziehen, konnte die Testprojektion lokal an den gültigen
Toolstand angepasst werden.

---

## Wo das System Reibung gezeigt hat

Der Template-Stand v0.3.10 koppelt neue Governance-Inhalte eng an schärfere
Konformitätsprüfungen. In einem instanziierten Brownfield-Projekt mit
historischen Plänen erzeugt das zuerst Rauschen:

```text
- alte Planinstanzen ohne Plan-Schema-Version
- Template-only-Artefakte
- Tutorial-/AGENTS-COMPACT-Referenzen außerhalb des freigegebenen Scopes
- Tool-Tests, die bereits neuere instantiate-Logik erwarten
```

Das ist kein inhaltlicher Migrationsfehler, aber ohne Einhegung schwer von
echten Fehlern zu unterscheiden.

Zusätzliche Reibung: Die Ausführung startete auf `master`. Der saubere
Feature-Branch wurde vor der ersten Mutation nicht angelegt. Nachträgliches
Abzweigen wäre nur kosmetisch gewesen und hätte die echte Ablaufchronologie
verdeckt.

---

## Was heute nicht geändert werden soll

```text
- historische Pläne nicht rückwirkend auf Plan-Schema-Version v0.3.7 umheben
- tutorial.md nicht in diesem Lauf modernisieren
- tools/instantiate/* nicht außerhalb des Mandats auf neueren Template-Stand ziehen
- den Format-Altbestand in den 5 unveränderten Produktdateien nicht in diesen Rueckfluss-Lauf hineinmischen
```

---

## Offene Fragen

Soll der Template-Checker künftig einen expliziten Brownfield-Legacy-Modus
bekommen, der historische Planinstanzen und template-only-Artefakte sauber als
Warnung statt als potentielle Vollfehler behandelt?

Soll das Template die Tool-Tests für `instantiate_project_box.py` stärker an den
freigegebenen Scope koppeln, damit Brownfield-Migrationen mit bewusst altem
Instanziierungstool nicht sofort Testanpassungen brauchen?

---

## Nicht-Ziel dieses Dokuments

Dieser Bericht ist kein Änderungsauftrag.

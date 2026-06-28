# Erfahrungsbericht: Brownfield-Migration box-python v0.2.7 → v0.3.0

Datum: 2026-06-27
Learning-Matrix-Kandidat: ja
Vorgeschlagene Musterkennung: BF-CHECKER-TERM-PRAEZISION, BF-CHECKER-MERGE-NICHT-REPLACE
Session-Typ: abgeschlossen
Aufgabe: Brownfield Fall B — alle v0.3.0-Neuerungen in bestehendes regenbogen-Projekt migrieren
Ergebnis: Vollständig abgeschlossen. Alle 4 Pflichtchecks grün (consistency OK, import OK, selfcheck OK, 64 tests passed).

---

## Was sich bewährt hat

**Checker als Gate:** Der `check_agent_docs_consistency.py` hat präzise alle Fehler gefunden
und nach jeder Korrektur sofort rückkopplungsfähig validiert. Ohne den Checker wären
ASCII-Umlaut-Fehler (Ausführungsbreite vs. Ausfuehrungsbreite), Genusformen (bindende vs.
bindender Router) und veraltete Referenzen (AGENTS-COMPACT.md) unentdeckt geblieben.

**Brownfield-Merge statt Replace:** Das Prinzip "lokal als Basis, semantisch mergen" hat verhindert,
dass projekt-spezifische Anpassungen (MODELL-README-Schritt, 23-Sektions-AGENTS.md-Struktur)
durch Template-Standard überschrieben wurden.

**Datei-Aktionsmatrix:** Die vorab erstellte Matrix (add/merge/replace/inspect/forbidden) hat
den Migrationslauf strukturiert und verhindert, dass Dateien versehentlich blind ersetzt wurden.

---

## Wo das System Reibung gezeigt hat

**Checker-Term-Präzision:** Der Checker prüft exakte Zeichenketten, nicht Bedeutungen.
`bindender Router` (Nominativ) vs. `bindende Router` (Genitiv-Adverbial) oder
`Ausfuehrungsbreite` (ASCII) vs. `Ausführungsbreite` (Umlaut) führen zu Fehlern,
die semantisch identisch wirken aber maschinell nicht passen.
→ Fehlerquelle: beim Schreiben neuen Textes aus Gedächtnis statt Copy-Paste aus Checker-Anforderungen.

**P-Nummerierung Kaskadeneffekt:** Die Entscheidung, MODELL-README als projekt-spezifischen
Schritt in P4 zu integrieren, erzwang Renummerierung aller folgenden P-Schritte in
drei Dateien (AGENTS.md, preflight-checkliste.md, task-schnitt.md). Der Kaskadenaufwand
war vorhersehbar aber zeitintensiv.

**Kontext-Unterbrechung:** Die Migration überspannte Kontextfenster-Grenzen. Nach der
automatischen Komprimierung musste der aktuelle Fehlerzustand durch direkte Datei-Lektüre
rekonstruiert werden. Das Checker-Output als direkte Validierungsquelle war entscheidend
für die korrekte Wiederaufnahme.

**Instabile Referenzen (AGENTS.md §N):** Mehrere Dateien enthielten numerische AGENTS.md-Abschnittsverweise
(§2, §9, §10, §17). Alle mussten auf semantische Namen oder andere autoritative Dokumente
umgestellt werden. Betroffen: 5 Dateien + 2 Tools. Dieser Änderungsaufwand ist systemisch
vorhersagbar bei jeder AGENTS.md-Restrukturierung.

---

## Was heute nicht geändert werden soll

- Keine Änderung an der Checker-Architektur: Das exakte Term-Matching ist gewollt und korrekt.
- Keine Entscheidung über kompakteres AGENTS.md-Format (local truth: 23 Sektionen bleiben).
- Kein automatisches MODELL-README-Protokoll (projekt-spezifisch, bewusste Abweichung).

---

## Offene Fragen

- Soll die Learning-Matrix das Muster "Checker-Term-Präzision" als eigenständigen Eintrag erhalten?
- Soll eine Konvention entstehen, dass Checker-Pflichtterme beim Schreiben neuer Abschnitte
  direkt aus REQUIRED_TERMS_BY_FILE kopiert werden (statt aus Gedächtnis formuliert)?

---

## Nicht-Ziel dieses Dokuments

Dieser Bericht ist kein Änderungsauftrag.

# Sprechakt: Basis v0.3.11 und Verbleib der lokalen Zusätze

Aufgabe:          Brownfield-Migration box-python v0.3.10 auf v0.3.11 (PLAN-2026-11-16-migration-v0.3.11)
Zeitpunkt:        2026-11-16
Sprechakt-Klasse: SP2 — Neuer systemsemantischer Steuerwert würde entstehen
Betroffener Begriff / Grenze: Dokumentrollen der lokalen Box; Verbleib lokaler Regel-Zusätze; Pflichtstatus lokaler Dokumente
Status: festgelegt
Folgeartefakte:
- AGENTS.md
- REGELN-UND-TOOLS.md
- PROJEKT.md
- tools/check_agent_docs_consistency.py
- regelmatrix.md
Ersetzt: docs/sprechakte/2026-11-16-dokumentstruktur-und-begriffsindex.md (teilweise: nur Punkt 1, die Dokumentrollen von AGENTS.md und REGELN-UND-TOOLS.md; die übrigen Punkte bleiben gültig)
Ersetzt durch:
Widerruft:
Freigabequelle: Dieter Haag, 2026-11-16 ("1. wir nehmen die v0.3.11 und arbeiten von dort aus", "2. einverstanden", "zu den D 1 und 3 einverstanden", "ja setze den Plan aktiv")

## Was festgelegt wurde

```text
1. Basis: Das Template box-python v0.3.11 (agent-templates, Commit 97f13ac) ist die Basis.
   AGENTS.md ist der Router des Templates. Eigene AGENTS.md-Strukturen entfallen.

2. Index: Der Begriffsindex bleibt ein lokaler Pilot (eigene Tabelle). Er gilt als
   Rückfluss-Beobachtung, nicht als Template-Änderung. Die Freigabe des Index-Entwurfs
   durch den Menschen steht aus.

3. D1: Die lokalen Zusätze aus der früheren langen AGENTS.md (Invarianten I1 bis I11 mit
   Beispielen, H10-Erkennungsregeln, Safe-Task-Listen mit Freigabeliste, Python- und
   Git-Sperren) stehen gebündelt in REGELN-UND-TOOLS.md als lokale Ergänzung
   (Ebene REPOSITORY, Rückfluss-Kandidat). Der Template-Router bleibt unverändert,
   ausser einer Hinweiszeile auf die lokalen Dokumente im Ladeprotokoll.

4. D3: PROJEKT.md und REGELN-UND-TOOLS.md sind im Konsistenzchecker optionale lokale
   Dateien (OPTIONAL_FILES), nicht Pflichtdateien. Die Pflichtliste entspricht dem Template.

5. D2, D4, D5 gelten wie im Plan beschrieben: check_begriffsindex, das Entwurfstool und
   PROJEKT.md bleiben; Rückfluss-Kandidaten kommen in die Migrationsevidence;
   tools/instantiate/* bleibt unberührt.

6. Das Projekt dient als Brownfield-Test für das Template.
```

## Was der Agent danach tut

Phasen 3 bis 8 des Plans im Mandatsscope ausführen: add und replace, AGENTS.md aus dem
Template, Merges der Regeldokumente, Drei-Wege-Merge der Tools, Verify, Migrationsevidence
und Erfahrungsbericht.

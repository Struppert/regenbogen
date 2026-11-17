# Sprechakt: Dokumentstruktur der Agenten-Box und Begriffsindex

Aufgabe:          Dokumentstruktur neu ordnen und Begriffsindex einführen (PLAN-2026-11-16-dokumentstruktur-und-index)
Zeitpunkt:        2026-11-16
Sprechakt-Klasse: SP2 — Neuer systemsemantischer Steuerwert würde entstehen
Betroffener Begriff / Grenze: Dokumentrollen der Agenten-Box (Kern, Projektbeschreibung, Regeln und Tools, Begriffsindex, Task-Dokument); Meta-Begriffe Begriffsindex, Task-Dokument, Meta-Index
Status: festgelegt
Folgeartefakte:
- AGENTS.md
- glossar-meta.md
- regelmatrix.md
- package-schema.md
- preflight-checkliste.md
- glossar-README.md
Ersetzt:
Ersetzt durch:
Widerruft:
Freigabequelle: Dieter Haag, 2026-11-16 (Gespräch; "AGENTS.md muss aufgeteilt werden", "Glossar ... bildet von Namen auf Dateien ab", "menschenlesbar ist das Konzept. KI muss dem folgen", "1. ja / 2. nur semantisch relevante / 3. Tool erzeugt den Entwurf und Mensch gibt ihn frei oder ändert ihn", Hook: "Weglassen", "setze diesen Plan aktiv: PLAN-2026-11-16-dokumentstruktur-und-index")

## Was festgelegt wurde

```text
1. Dokumentrollen (je ein Zweck, jede Aussage nur an einem Ort):
   AGENTS.md            Sicherheitskern und Ladeprotokoll
   PROJEKT.md           Architektur und "was liegt wo"
   BEGRIFFSINDEX.md     Name -> Raum, Ort im Code, Test, Eintrag, Status, Aliase
   REGELN-UND-TOOLS.md  allgemeine Regeln und Tool-Katalog, mit Meta-Index
   Task-Dokument        Beschreibung der jeweiligen Aufgabe (Folgeplan B)

2. Dateinamen PROJEKT.md und REGELN-UND-TOOLS.md sowie ein eigener Ordner
   für template-eigene Dokumente: ja. Der Ordnerumzug ist Folgeplan C und
   nicht Teil von Plan A.

3. Begriffsindex: nur semantisch relevante Begriffe.
   Kriterium laut Plan (mit Planfreigabe unverändert angenommen):
   Fachbegriffe und Typen mit Invarianten, Ports, Use Cases, Fehlerklassen,
   Policies und Konstanten mit Bedeutung, Adapter-/Infrastruktur-Klassen mit
   eigener Rolle, Einstiegspunkte. Nicht: reine Hilfsfunktionen, Formatierer,
   GUI-Bausteine. Öffentliche Symbole ohne Indexzeile meldet der Checker nur
   als Hinweis.

4. Pflege des Index: Ein Tool erzeugt einen Entwurf, der Mensch gibt ihn
   frei oder ändert ihn. Kein automatisches Schreiben des freigegebenen Index.

5. Prinzip: menschenlesbar ist das Konzept, die KI folgt dem. Werkzeuge
   lesen Markdown mit stabilen Köpfen und melden Befunde; sie bestimmen
   weder Format noch Entscheidung.

6. Kein Hook zur Durchsetzung.

7. Neue Meta-Begriffe (Eintrag in glossar-meta.md):
   Begriffsindex, Task-Dokument, Meta-Index.
```

## Was der Agent danach tut

Phasen 1 bis 7 des Plans im Mandatsscope ausführen: Checker-Tests und Checker
anpassen, Index-Entwurfstool bauen, Entwurf zur Freigabe vorlegen, PROJEKT.md
und REGELN-UND-TOOLS.md anlegen, AGENTS.md verschlanken, Glossar bereinigen,
validieren. Der freigegebene Begriffsindex entsteht erst nach menschlicher
Freigabe des Entwurfs.

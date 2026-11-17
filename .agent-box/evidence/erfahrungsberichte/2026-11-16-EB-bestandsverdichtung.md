# Erfahrungsbericht: Bestandsverdichtung der Pläne (erste Anwendung der Kurzform)

Datum: 2026-11-17 (Plan vom 2026-11-16)
Learning-Matrix-Kandidat: ja
  (ja wenn: HARD-Abbruch verursacht, oder ≥2 Sessions gleiches Muster,
   oder Mensch markiert als systemic — siehe learning-matrix.md §1a)
Vorgeschlagene Musterkennung: Altbestand an Aufgaben-Artefakten braucht einen einmaligen Aufräumpunkt
Session-Typ:  abgeschlossen
Aufgabe:      PLAN-2026-11-16-kurz-bestandsverdichtung (Kurzform, Abschlussdokument dieses Plans)
Ergebnis:     15 Pläne verdichtet, Aufgabenindex mit 15 Zeilen, Eingabeplan nach docs/rueckfluss/ verschoben

---

## Zahlen

```text
                          vorher        nachher
Dateien in docs/plans     22            6        (davon 2 Vorlagen)
Bytes                     162.104       67.357   (minus 94,7 KB, minus 58 Prozent)
Zeilen                    4.266         1.618
Konsistenzcheck           16 Warnungen zu Altplänen, 1 Hinweis    nur der Hinweis zu SonnenscheinAnteil
```

Es blieben vier Pläne: die zwei Branch-Pläne (Entscheidung E5), Plan B und dieser Plan. Sie gehen am
Merge-Gate. Sprechakte, Erfahrungsberichte und Migrationsevidence blieben unverändert (kein geänderter
Eintrag unter `docs/sprechakte/`, `.agent-box/`).

---

## Was sich bewährt hat

Der Ablauf Entwurf, Mensch-Entscheidung, Ausführung funktionierte: Das Entwurfstool lieferte
Kandidaten, Zustände und die Zahl der Verweise, der Mensch entschied fünf Punkte, die Ausführung war
danach mechanisch. Der Check "Abschlussdokument existiert und ist nicht leer" lief ohne Befund.
Die Kurzform trug den Plan in einer Datei, inklusive Mandat, Scope, Korrespondenzsatz und den fünf
Entscheidungen.

---

## Wo das System Reibung gezeigt hat

1. **Altformat.** 13 der 15 Pläne haben keine Plan-ID und führen `Status:` und `Aufgabe:` als Felder.
   Das Entwurfstool musste dafür dreimal nachgebessert werden (Altformat-Status und Plan-ID über den
   Dateinamen, Aufgabe als Feld, Satzende in Befehlen mit Punkt). Diese Fälle fand erst der Lauf an
   echten Daten, nicht die ersten Tests.
2. **Ergebnis-Spalte.** Nur wenige Abschlussdokumente führen eine Zeile `Ergebnis:`. Für die übrigen
   steht in der Indexzeile "abgeschlossen (Ergebnis im Abschlussdokument)". Das ist korrekt, aber
   informationsarm. Die eigentliche Auskunft liegt im Bericht.
3. **Fehlendes Abschlussdokument.** `priming-verbesserungen` hatte keinen Erfahrungsbericht. Der Bericht
   wurde nachträglich aus Plan, Repository-Stand und Template-Changelog verfasst (im Bericht vermerkt).
   Ein nachträglich verfasster Bericht ist schwächer als einer aus der Sitzung.
4. **Abschlussdokument beschreibt die Ursache.** Für `format-altbestand-bereinigung` existiert nur der
   Abbruchbericht, der die Ursache beschreibt. Das Ergebnis (Commit 99f4e3a) steht in der Indexzeile.
5. **Veralteter Status.** Der Plan stand auf Vertrag `active`, obwohl er ausgeführt war. Die
   Statuskorrektur (Vertrag completed, Mandat erloschen) wurde vor der Entfernung gemacht. Weil die
   Datei danach entfernt wurde, steht sie nur in diesem Bericht. `git rm` brauchte dafür `-f`.
6. **Verweise.** 13 Dateien nennen entfernte Pläne per Dateiname (12 versiegelte Dokumente, die
   Projektkopie `tutorial.md`). Sie bleiben stehen. Die Plan-ID im Aufgabenindex löst sie auf.
7. **Rückfluss-Status.** Zwölf Zeilen stehen auf UNKNOWN. Für Feature-Aufgaben (GUI, Sonnenstand,
   Blickrichtung, PLZ, Tagesprognose u. a.) ist offen, ob sie als Tutorial-Sessions ins Template
   zurückgehören. Das ist eine Entscheidung des Menschen.

---

## Was heute nicht geändert werden soll

```text
- Aufgabenindex: Ergebnisse nur mit Beleg verfeinern, nicht aus dem Gedächtnis
- Die verbleibenden vier Pläne nicht jetzt verdichten (Merge-Gate)
- Entfernte Pläne nicht aus der Historie wiederherstellen, außer ein Mensch verlangt es
```

---

## Offene Fragen

Soll das Merge-Gate für Altformate einen Legacy-Weg bekommen (Plan-ID über Dateinamen, Status über
`Status:`), oder gilt das nur für diesen einmaligen Bestand? Sollen die Feature-Aufgaben als
Tutorial-Sessions ins Template zurückgehen? Reicht eine generische Ergebniszeile, oder verlangt der
Aufgabenindex ein konkretes Ergebnis je Zeile?

---

## Governance-Rueckfluss

Lokale Governance geaendert: ja

```text
1. Aufgabenindex und Verdichtung am Altbestand erprobt: 15 Pläne, minus 58 Prozent Planbytes.
   Rückflussstatus: TEMPLATE-CANDIDATE (Beobachtung zum Lebenszyklus, siehe Plan B)
2. Verdichtungswerkzeug braucht ein Altformat-Verständnis (Plan-ID, Status, Aufgabe als Feld).
   Rückflussstatus: TOOLING-CANDIDATE
3. Verweise versiegelter Dokumente auf entfernte Pläne, aufgelöst über den Aufgabenindex.
   Rückflussstatus: TEMPLATE-CANDIDATE
```

---

## Nicht-Ziel dieses Dokuments

Dieser Bericht ist kein Änderungsauftrag.

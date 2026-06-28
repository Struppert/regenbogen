# grundsatz.md — Warum dieses System so gebaut ist

> Ebene: PRIMING
> Rolle: Theorie und Begruendung
> Geltung: projektuebergreifender Hintergrund
> Autoritative Frage: Warum sind Abbruch, Evidence und Semantikgrenzen noetig?
> Nicht zustaendig fuer: operative Detailentscheidung, konkrete Ausfuehrung

**Dokumenttyp: Theorie / Hintergrund**

> Dieses Dokument ist kein Regelwerk und kein Änderungsauftrag.
> Es erklärt, warum die Regeln die richtige Form für dieses Problem sind.
> Ein Agent der nur `AGENTS.md` kennt, arbeitet an der Oberfläche.
> Ein Agent der dieses Dokument kennt, versteht warum Abbruch besser ist als Plausibilität.

---

## 1. Das eigentliche Problem: Semantik liegt nie vollständig vor

Die Semantik eines Softwaresystems ist kein Artefakt unter anderen.
Sie ist das, was aus vielen Artefakten, Erinnerungen und Praktiken rekonstruiert wird.
Sie liegt nie vollständig vor — nur in Projektionen:

```text
Code, Kommentare, Dokumentation, Glossar, Tests,
Commit-Messages, Architekturentscheidungen,
Erinnerung der Beteiligten, Betriebserfahrung
```

Keine dieser Projektionen ist die Semantik selbst.
Jede enthält Ausschnitte, Verzerrungen, historische Spuren, Irrtümer und Auslassungen.
Auch ihre Summe ist kein exakter semantischer Zustand — sondern ein zufällig entstandenes Sediment.

**Das ist der entscheidende Punkt: Semantik ist nicht einfach unvollständig dokumentiert.
Sie ist in realen Systemen nur indirekt, verteilt und kontingent gegeben.**

Daraus folgt die gefährliche Konsequenz:

> Das Problem ist nicht nur, dass der Agent etwas nicht weiß.
> Das Problem ist, dass auch das System seine eigene Semantik nicht vollständig besitzt —
> es besitzt nur Spuren davon.

---

## 2. Menschen und Agenten kompensieren anders

```text
Menschliche Arbeit:
  Artefaktspur + Erinnerung + Urteil + Rückfrage

Agentische Arbeit:
  Artefaktspur + Plausibilität + Werkzeugprüfung

Agentenfähiger Artefaktraum:
  Artefaktspur + reifizierte Semantik + Evidence
```

Menschen kompensieren fehlende explizite Semantik durch Erinnerung, Erfahrung und Rückfragen.
Agenten kompensieren es durch Plausibilität.

**Plausibilität ist kein semantischer Zustand.**

Ein Syntaxfehler stoppt.
Plausible falsche Semantik läuft weiter — durch Review, Tests und Dokumentation hindurch.

---

## 3. Warum Reifizierung die Antwort ist

Reifizierung ist der Versuch, semantische Erinnerung aus Personen herauszulösen
und als überprüfbare Struktur in den Artefaktraum zurückzuführen.

Nicht vollständig. Aber so weit, dass kontrollierte Transformation möglich wird.

```text
1. KI macht Syntax billig.
2. Dadurch wird Semantik zum Engpass.
3. Semantik liegt aber nicht vollständig vor.
4. Sie existiert nur in Projektionen.
5. Diese Projektionen sind historisch zufällig, partiell und verzerrt.
6. Menschen kompensieren durch Erinnerung und Erfahrung.
7. Agenten kompensieren durch Plausibilität.
8. Plausibilität ist kein semantischer Zustand.
9. Deshalb brauchen wir reifizierte, kontrollierte, evidenzfähige Semantik:
   Glossar, Räume, Binding, Preflight, Evidence.
```

---

## 4. Was Bedeutung ist — operativ

Bedeutung ist in diesem Modell nicht Satzwahrheit.
Bedeutung ist die Aktivierung eines Bedingungsraums.

Ein Begriff aktiviert einen Bedingungsraum: welche Invarianten gelten,
welche Operationen erlaubt sind, welche Experten urteilen können,
welche Tests prüfen.

**Wenn ein Begriff in einem Modulpfad steht, behauptet er diesen Bedingungsraum.**
Wenn der Bedingungsraum nicht explizit ist, ist die Behauptung leer.

Ein leerer Modulpfad ist kein semantischer Adressraum — er ist ein syntaktisches Silo.

---

## 5. Semantischer Adressraum — G(PKG)

Ein Paket ist erst dann ein semantischer Adressraum, wenn es vier Fragen beantworten kann:

```text
G(PKG) = (Members, Invariants, Projections, SubspaceMap)

Members:      Welches Kriterium entscheidet Zugehörigkeit? Nicht Ordner — Grund.
Invariants:   Was gilt für ALLE Mitglieder ohne Ausnahme?
              Wer kann eine Verletzung erkennen?
Projections:  Wo ist die Zugehörigkeit sichtbar und prüfbar?
              Tests, Docs, Checker, öffentliche API, Glossar.
SubspaceMap:  Welche Unterräume existieren und warum?
              Kein Unterraum aus Bequemlichkeit.
```

Wenn ein Paket diese Fragen nicht beantworten kann, ist es kein stabiler semantischer Adressraum.
Dann ist jede Transformation riskant — weil die Reichweite nicht bestimmbar ist.

---

## 6. Die Autonomieregel — was kein Compiler prüfen kann

Die schärfste Invariante ist epistemisch, nicht strukturell:

> Ein semantischer Raum ist gültig, wenn ein einzelner Experte ihn
> vollständig prüfen kann ohne die anderen Räume zu kennen.

```text
domain/customer:
  Domänenexperte kann urteilen ohne HTTP, Retry, Datenbank zu kennen: ✓
  → Autonomie erhalten → gültig

domain/customer mit retry_count:
  Domänenexperte kann nicht urteilen ohne Retry-Semantik zu kennen: ✗
  → Autonomie verletzt → semantischer Fehler
  → kein Compilerfehler — aber trotzdem falsch
```

Der Compiler schweigt hier prinzipiell — nicht aus Trägheit,
sondern weil die Frage außerhalb seiner Zuständigkeit liegt.
Nur Mensch oder Agent mit Glossar-Zugang kann sie beantworten.

**Das ist der Grund warum ein Checker allein nicht ausreicht.
Das ist der Grund warum Preflight, Sprechakt und Abbruch nötig sind.**

---

## 7. Warum das Glossar operative Infrastruktur ist — nicht Dokumentation

Klassisch (DDD): Glossar als Kommunikationsbrücke zwischen Entwickler und Domänenexperte.

In diesem System: Glossar als operativer Sortierraum.

```text
Vorher (klassisch):
  Glossar als Brücke zum gegenseitigen Verstehen.
  Faktisch: beide Seiten bleiben in ihrer Welt,
  glauben aber sie verstünden die andere.

Jetzt (operativ):
  Glossar als Werkzeug-Eingabe.
  Der Domänenexperte prüft das Glossar — nicht den Code.
  Der Entwickler baut gegen das Glossar — nicht gegen implizites Domänenwissen.
  Agenten konsultieren das Glossar — ohne Verständnisanspruch.
```

Das Glossar wird zum **geteilten operativen Artefakt** auf dem alle Akteure
ihre jeweilige Operation durchführen können — ohne vorgeben zu müssen
die andere Welt zu kennen.

Das ist der Grund warum SP7 (fehlender Glossareintrag) ein Sprechakt-Trigger ist
und nicht ein "bitte ergänzen"-Hinweis.

---

## 8. Warum Abbruch besser ist als Plausibilität

Wenn ein Agent eine Lücke in der expliziten Semantik findet,
hat er zwei Optionen:

```text
Option A: Plausibel weitermachen
  → schnell
  → falsche Semantik läuft durch Review und Tests
  → Fehler werden spät und teuer sichtbar
  → Drift akkumuliert sich

Option B: Abbrechen mit Evidence
  → kostet eine Iteration
  → Lücke wird sichtbar und kann geschlossen werden
  → Semantik bleibt kontrolliert
  → System lernt durch Erfahrungsbericht
```

**Ein gültiger Abbruch ist besser als eine erfundene Lösung.**

Das ist nicht Vorsicht als Selbstzweck.
Das ist die strukturelle Konsequenz daraus, dass Plausibilität kein semantischer Zustand ist.

---

## 9. Warum natürliche Sprache der primäre Bedeutungsträger bleibt

Neue Semantik entsteht nicht im Code.
Sie entsteht in natürlicher Sprache: in Gesprächen, Glossareinträgen, Sprechakten.

Code ist Projektion von Semantik, nicht ihr Ursprung.

Deshalb:
- Neue Begriffe entstehen durch Sprechakt, nicht durch Implementierung.
- Invarianten werden explizit formuliert, bevor sie implementiert werden.
- Tests prüfen Verhalten — sie definieren keine neue Bedeutung.

Der Sprechakt ist die formale Struktur für: "hier entsteht neue Semantik,
ein Mensch muss sie festlegen."

---

## 10. Leitsatz

```text
Frei arbeiten.
Explizit formulieren.
Automatisch prüfen.
Kontrolliert committen.
```

Frei arbeiten bedeutet: innerhalb der expliziten Semantik ist maximale Freiheit erlaubt.
Explizit formulieren bedeutet: neue Semantik entsteht nur an definierten Stellen.
Automatisch prüfen bedeutet: Checker, Preflight, Invarianten — nicht Vertrauen.
Kontrolliert committen bedeutet: jeder Commit hat ableitbare Testpflicht und Evidence.

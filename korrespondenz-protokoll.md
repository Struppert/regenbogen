# korrespondenz-protokoll.md — Modelltreue, Validierung und Evidence

> Ebene: MIXED-TRANSITION
> Primaerer Anteil: PRIMING
> Sekundaere Projektion: PLAN/RUN
> Rolle: Pruefvertrag zwischen Modell, Artefakt und Evidence
> Autoritative Frage: Wie wird nachgewiesen, dass eine Implementierung und ihre Validierung der benannten Bedeutung entsprechen?
> Nicht zustaendig fuer: neue Produktsemantik, Testbefehle, Ausfuehrungsfreigabe

## 1. Zweck

Dieses Protokoll trennt zwei Pruefklassen, die nicht vermischt werden duerfen:

```text
Kohaerenz:
  Widerspruchsfreiheit innerhalb eines Artefakts oder formalen Systems.
  Beispiele: Syntax, Typen, Importlayer, Schemafelder.

Korrespondenz:
  Belegte Beziehung zwischen einer normativen Quelle, ihrer Projektion,
  ihrer Validierung und gegebenenfalls einer Aussenbeobachtung.
```

Ein gruener Compiler oder Checker ist Kohaerenzevidence. Er beweist keine
Modelltreue. Ein gruener Test ist nur Korrespondenzevidence, wenn sein Oracle
auf eine bestehende normative Quelle zurueckfuehrbar ist.

## 2. Korrespondenzkette

```text
Normative Quelle
  -> Implementierungsprojektion
  -> Validierungsprojektion
  -> Evidence
```

Normative Quellen sind ausschliesslich bereits geltende Glossareintraege,
Invarianten, Sprechakte, API-Vertraege oder andere zustaendige
Projektartefakte. Code, Tests, Checker und Messergebnisse erzeugen keine neue
Produktsemantik.

## 3. Korrespondenzsatz

Jede nichttriviale Verhaltensaenderung hat fuer jede betroffene Invariante
mindestens einen Korrespondenzsatz im Plan. Mehrere Sätze duerfen dieselbe
Quelle referenzieren, wenn sie unterschiedliche Projektionen oder
Validierungsgrenzen haben.

```markdown
Korrespondenzsatz-ID: K-<Plan-ID>-<Nr>

Normative Quelle:
  <Glossarbegriff | Invariante | Sprechakt | API-Vertrag, Revision>

Behauptung:
  <Was muss gelten?>

Implementierungsprojektion:
  <Codepfade, Schnittstellen oder Adaptergrenzen>

Validierungsprojektion:
  <Test, Checker, Review oder Messvorgang>

Korrespondenzklasse:
  Modelltreue | Oracle-Treue | Ausfuehrungsverhalten | Aussenkorrespondenz

Evidence:
  <Befehl, Review-Befund oder Messung>
  Ergebnis:
  Geltungsgrenze:

Status:
  bestaetigt | teilweise bestaetigt | widerlegt | offen
```

Die Geltungsgrenze ist Pflicht, sobald die Evidence keine allgemeine Aussage
belegt. Sie verhindert, dass ein kontrollierter Test als Nachweis fuer die
unbeobachtete Aussenwelt ausgegeben wird.

## 4. Korrespondenzklassen

```text
Modelltreue:
  Deckt die Implementierung die benannte Behauptung ab, ohne sie umzudeuten?

Oracle-Treue:
  Prueft ein Test oder Checker eine bereits entschiedene Invariante,
  statt selbst neue Semantik einzufuehren?

Ausfuehrungsverhalten:
  Zeigt die Implementierung unter benannten kontrollierten Bedingungen
  das erwartete Verhalten?

Aussenkorrespondenz:
  Stuetzt eine kalibrierte Beobachtung oder Messung die fachliche Aussage
  ueber die Aussenwelt? Sie ist nie allein durch einen Unit-Test bestaetigt.
```

## 5. Modellreview

Modellreview ist vom Qualitaetsreview getrennt.

```text
Qualitaetsreview:
  Wartbarkeit, Sicherheit, Lesbarkeit, Performance und technische Guete.

Modellreview:
  Quelle, Behauptung, Implementierung, Testoracle und Evidence eines
  Korrespondenzsatzes gegeneinander pruefen.
```

Der Modellreview kann durch einen Menschen oder eine getrennte Pruefinstanz
erfolgen. Er beantwortet fuer jeden Satz mindestens:

```text
- Ist die normative Quelle zustaendig und aktuell?
- Deckt die Implementierung die Behauptung ab?
- Prueft die Validierung dieselbe Behauptung?
- Ist das Ergebnis innerhalb seiner Geltungsgrenze korrekt eingeordnet?
```

Ein offener oder widerlegter Satz ist kein Abschlusszustand. Fehlt die
normative Quelle: Task-Schnitt pruefen, dann Sprechakt SP7. Ist die passende
Validierung nicht ableitbar: HARD-Abbruch H6.

## 6. Evidence und Automatisierung

Checker duerfen Struktur und Vollstaendigkeit von Korrespondenzsaetzen pruefen.
Sie duerfen keine semantische Modelltreue behaupten. Die Beurteilung der
Relation bleibt Modellreview und geeigneter Validierung vorbehalten.

Korrespondenzsaetze werden im Plan gefuehrt. Checkpoints referenzieren nur
Satz-ID, Ergebnis und offene Grenzen; sie erzeugen keine zweite Wahrheit.

## 7. Schlussregel

Eine nichttriviale Verhaltensaenderung ist erst abgeschlossen, wenn ihre
betroffenen Invarianten, Implementierungs- und Validierungsprojektionen sowie
deren Evidence als Korrespondenzsaetze nachvollziehbar gebunden sind.

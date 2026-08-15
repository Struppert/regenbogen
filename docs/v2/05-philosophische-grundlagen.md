# Philosophische Grundlagen: Warum das Modell funktioniert

**Zielgruppe:** Agenten-Architekten, Implementierer  
**Zweck:** Erklärt das epistemische Modell hinter dem System.

---

## 1. Strukturelles Verständnis statt psychologisches

**Das Problem:** "Versteht ein Agent einen Glossar-Begriff wirklich?"

Antwort: Nicht psychologisch. Aber **strukturell**:

Ein Glossar-Begriff ist strukturell verstanden, wenn:

1. **Abhängigkeiten erhalten sind** (A hängt von B im Glossar → Code respektiert das)
2. **Invarianten geprüft sind** (Assertions im Code validieren Glossar-Grenzen)
3. **Komposition funktioniert** (A → B → C im Glossar → A transitiv mit C im Code)

Das ist:
- **Nachprüfbar** (Checker zeigt Verletzungen)
- **Testbar** (Oracle-Tests prüfen Invarianten)
- **Messbar** (strukturelle Metrik, nicht Glaube)

**Konsequenz für Glossare:** Struktur-Dokumentation ist nicht optional — sie ist die einzige "Verstehens"-Garantie, die es gibt.

---

## 2. Korrespondentz, nicht Kohärenz

**Falsch:** "Code ist wahr, wenn er konsistent in sich ist."

**Richtig:** "Code ist wahr, wenn er die Glossar-Struktur respektiert."

Beispiel:
```
Glossar:  RegenbogenWahrscheinlichkeit ∈ [0, 100]
Code (kohärent):  value = value % 101  // Mathematisch korrekt, aber falsch
Code (korrespondent): assert 0 <= value <= 100  // Glossar-Struktur erhalten
```

Der zweite Code ist wahr, weil er dem Glossar *entspricht*. Der erste Code ist kohärent in sich, verletzt aber die Entsprechung.

**Konsequenz für Checker:** Ein Checker muss nicht nur auf interne Konsistenz prüfen (Syntax, Typen), sondern auf Entsprechung zum Glossar (Struktur, Invarianten, Morphismen).

---

## 3. Der Glossar hat Intention, der Agent nicht

**Searles Chinese Room Argument (1980):** Ein System, das nach Regeln manipuliert, versteht nicht.

**Unsere Antwort:** Das stimmt. Aber der **Glossar** selbst kodifiziert Intention:

```
Glossar-Begriff:
  Bedeutung:      "Die Wahrscheinlichkeit eines Regenbogens"
  Invarianten:    0 ≤ value ≤ 100
  Abhängigkeiten: → Wetterzustand, → Sonnenstand
```

Ein Agent, der diese Struktur respektiert, respektiert die Intention des Glossars — nicht weil er sie innerlich versteht, sondern weil die Struktur *die Intention codifiziert*.

**Konsequenz für Agent-Priming:** Der Agent braucht nicht zu verstehen, was RegenbogenWahrscheinlichkeit "bedeutet". Er muss nur die Struktur erhalten: Abhängigkeiten ↔ Imports, Invarianten ↔ Assertions, Morphismen ↔ Code-Pfeile.

---

## 4. Vorbedingungen für das System

Damit das Modell funktioniert, müssen diese Bedingungen erfüllt sein:

1. **Glossare müssen explizit sein** — Definition + Invarianten + Morphismen dokumentieren
2. **Abhängigkeiten müssen kodifizierbar sein** — nicht nur Prosa, sondern strukturelle Pfeile
3. **Invarianten müssen testbar sein** — jede Glossar-Invariante muss in Code als Assertion prüfbar sein
4. **Komposition muss erhalten bleiben** — wenn A von B abhängt und B von C, muss A transitiv mit C verknüpft sein
5. **Checker müssen diese Regeln durchsetzen** — automatisch, nicht manuell per Code-Review

Fehlt eine dieser Bedingungen, funktioniert das System nicht. Das ist keine philosophische Eleganz, sondern praktische Notwendigkeit.

**Konsequenz für Glossar-Design:** Bevor man einen Begriff anlegt, muss klar sein: Kann ich seine Morphismen beschreiben? Kann ich seine Invarianten in Code ausdrücken? Werde ich einen Test schreiben, der prüft, dass der Code diese Invarianten respektiert?

---

## Zusammenfassung

Das Framework funktioniert, weil es nicht auf Psychologie baut, sondern auf **strukturelle Nachprüfbarkeit**.

Ein Agent versteht einen Begriff strukturell, wenn er dessen Abhängigkeiten, Invarianten und Kompositionen respektiert — nicht weil er ihn "innerlich versteht", sondern weil die Struktur explizit und automatisch prüfbar ist.

Das ist nicht elegant, aber es funktioniert.

---

**Erstellt:** 2026-08-15  
**Version:** 0.2 (gekürzt: nur werkzeugtragende Abschnitte)

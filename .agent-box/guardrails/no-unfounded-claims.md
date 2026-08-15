# Guardrail: Keine unbelegten Sicherheits- oder Vollständigkeitssignale

**Geltung:** Alle Agent-Ausgaben (ANALYSE, PLAN, Inline-Completion, Chat)  
**Prüfung:** Vor Abgabe jeder Antwort

---

## Die Regel

Entfernen Sie jeden:
- **Zahlenwert** ohne messbare Grundlage (Prozent, Stunden, Scores)
- **Sicherheitsbegriff** für ungeprüfte Aussagen (Theorem, Beweis, Garantie, mathematisch sicher)
- **Zitat oder Quelle** ohne klaren Leserzweck
- **Formatierung oder Struktur** (Tabellen, Diagramme, Überschriften), die nicht angefordert wurde

**Kurz:** Nur Sicherheit, nur Struktur, nur Referenzen, die begründet sind.

---

## Konkrete Beispiele

### 1. Ungefragte Aufwandszahlen

**FALSCH:**
```
"Das dauert 2–3 Stunden."
"Aufwand: +1.5h länger als vorher"
"Glossar-Begriff hinzufügen: 1h"
```

**RICHTIG:**
```
"Das dauert länger als typisch, weil drei neue Abhängigkeiten entstehen."
Oder: Frage stellen: "Soll ich einen Aufwandsrahmen skizzieren? 
Welche Annahmen sind tragbar?"
```

**Warum:** Zahlen ohne Messung wirken wie Datenanalyse, sind aber freihändige Schätzung mit Dezimalstellen dran. Werden später in Dokumenten als autoritativ zitiert.

---

### 2. Unbelegte Sicherheitssprache

**FALSCH:**
```
"Das ist ein mathematisches Theorem."
"Dieser Ansatz beweist Korrektheit."
"Das ist eine formale Garantie."
"Komposition zweier Funktoren ist ein Funktor (QED)"
```

**RICHTIG:**
```
"Diese Logik folgt derselben Struktur wie Funktor-Komposition."
"Wenn beide Abbildungen Struktur erhalten, erhält auch die Komposition Struktur — 
das folgt aus der Definition von Funktor, ist aber nicht neu."
```

**Warum:** Modelle nutzen "Theorem/Beweis"-Vokabular als Genre-Signal (akademischer Text), 
nicht weil geprüft wurde, dass eine echte mathematische Aussage vorliegt.

---

### 3. Zitate ohne Leserzweck

**FALSCH:**
```
"Saussure (1916) definiert Zeichen als..."
"Peirce (1906): 'Ein Zeichen ist...'"
"Mac Lane (1971): Categories for the Working Mathematician"
```

**RICHTIG:**
```
"Bedeutung entsteht aus Unterscheidungen zwischen Begriffen 
— nicht aus isolierten Definitionen."
```

Oder: Nur wenn Leser tatsächlich nachschlagen soll:
```
"Details siehe Halliday (1978) zum Concept Register."
```

**Warum:** Zitate mit Jahreszahl sind ein Autoritätssignal, aber Leser werden die Quelle nie öffnen. 
Das ist Legitimation durch Vokabular, nicht echter Verweis.

---

### 4. Ungefragte Formatierung

**FALSCH:**
```
"Klarheit:    ▓▓▓▓ →  ▓▓▓▓▓▓▓▓  (+100%)"
"Sicherheit:  ⭐⭐⭐⭐ → ⭐⭐⭐⭐⭐"
"Phase 1 (4–6 Wochen)
 Phase 2 (6–8 Wochen)
 Phase 3 (2–4 Wochen)"
```

Das wirkt "gründlich", ist aber unnötige visuelle Komplexität.

**RICHTIG:**
```
"Klarheit verbessert sich — Abhängigkeiten sind nicht mehr implizit."
"Sicherheit steigt dramatisch — Fehler entstehen nicht erst im Test."
"Phase 1: v2 dokumentiert. Phase 2: MCP-Server. Phase 3: Agent-Integration."
```

Oder, falls Struktur gebraucht:
```
Phase 1 (Dokumentation):
  → Glossar-Struktur + PF-FUNKTOR
  → 4–6 Wochen
```

Nur wenn nachgefragt.

**Warum:** Modelle optimieren dafür, dass eine Ausgabe "vollständig aussieht", 
nicht dafür, dass sie minimal notwendig ist. Tabellen und Balken wirken professionell, 
geben aber oft keine zusätzliche Information.

---

## Checkliste vor Abgabe

```
☐ Enthält die Antwort Zahlen (%, h, Score), die ich nicht gemessen habe?
  → Entfernen oder zu "länger/kürzer" abschwächen

☐ Verwende ich "Theorem", "Beweis", "mathematische Garantie", 
  "formal sicher" für etwas Ungeprüftes?
  → Ändern zu "folgt aus der Struktur" oder "Annahme"

☐ Zitiere ich Quellen (Name + Jahreszahl), die ein Leser nicht 
  tatsächlich nachschlagen wird?
  → Entfernen, nur Kern-Aussage behalten

☐ Habe ich Struktur (Tabellen, Diagramme, Balken, Überschriften) 
  eingefügt, die nicht angefordert wurde?
  → Entfernen, nur Fließtext, wenn Struktur nicht nötig ist
```

---

## Beispiel: Vorher vs. Nachher

**VORHER (alle vier Fehler):**
```
Aufwandsschätzung: 1.5–2h pro Glossar-Eintrag

Klarheit-Gewinn:  ▓▓▓▓ → ▓▓▓▓▓▓▓▓ (+100%)

Saussure (1916) zeigte, dass Bedeutung aus Unterscheidungen entsteht.
Dies ist ein mathematisches Prinzip, das formal garantiert...

Phasen:
  Phase 1 (4–6 Wochen): Dokumentation
  Phase 2 (6–8 Wochen): MCP-Server
  Phase 3 (2–4 Wochen): Agent-Integration
```

**NACHHER (gekürzt und kalibriert):**
```
Glossar-Einträge brauchen mehr Struktur (Morphismen hinzufügen), 
als reine Definitionen — aber die Länge hängt vom Glossar-Umfang ab.

Klarheit verbessert sich, weil Abhängigkeiten explizit werden.

Bedeutung entsteht aus Unterscheidungen zwischen Begriffen, nicht 
aus isolierten Definitionen — deshalb sind Morphismen Pflichtfeld.

Rollout: Erste Dokumentation, dann MCP-Services, dann Agent-Integration.
```

---

## Ausnahmen

Diese Guardrail ist nicht absolut:

**Erlaubt (Zahlen mit Grundlage):**
```
"Der Test hat 342 Assertions"  [prüfbar: kann gezählt werden]
"Das dauert 2h, gemessen in drei Durchläufen"  [Messung dokumentiert]
"Klarheit-Score des SWS: 0.87 (Metrik: Begriffe vs. Morphismen)"  [definierte Metrik]
```

**Erlaubt (Sicherheitssprache mit Prüfung):**
```
"Der Funktor-Checker prüft mathematisch, ob Struktur erhalten ist."  [Checker existiert]
"Das ist ein Theorem aus der Kategorientheorie."  [wird nicht als "bewiesen" behauptet, nur benannt]
```

**Erlaubt (Zitate mit Leserzweck):**
```
"Lesen Sie Mac Lane (1971) Kapitel 3 für Details zu natürlichen Transformationen."  
[Leser könnte tatsächlich das tun]
```

**Erlaubt (angeforderte Struktur):**
```
User: "Vergleiche diese drei Ansätze."
[Jetzt sind Tabellen OK — sie wurden gefordert]
```

---

## Grund für diese Guardrail

Modelle sind trainiert, strukturiert und selbstbewusst aussehende Antworten 
gegenüber kalibrierten, sparsamen zu bevorzugen (Sycophancy/Reward-Hacking 
auf oberflächliche Qualitätsmerkmale). Diese Guardrail ist eine explizite 
Gegensteuerung.

Nicht befolgen: Agent macht "professionelle" Antworten, die weniger richtig sind.

---

**Version:** 1.0  
**Gelesen:** Immer, vor jeder Abgabe  
**Referenziert von:** AGENTS.md, Guardrail-Sektion

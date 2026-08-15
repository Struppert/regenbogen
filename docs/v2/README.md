# Agent-Priming v2: Semiotik + Kategorietheorie

**Zweck:** Formales Rahmenwerk für die Abbildung von Glossar-Begriffen in Code mit mathematischen Garantien.

**Status:** Konzept / Pilotphase (August 2026)

---

## 🎯 Das Problem

Das aktuelle System (v1) hat ein Lücke:

```
Glossar/Ontologie (was bedeuten die Begriffe?)
    ↓ [Implizit, informell]
Code (wie werden sie kodiert?)
    ↓ [Hoffnung, dass es passt]
Tests (wurden die Invarianten verletzt?)
```

**Fehlendes Stück:** Wie wird die **Struktur** von Glossar zu Code abgebildet? Und wie wird das validiert?

---

## 💡 Die Lösung: Funktoren zwischen Kategorien

Statt informale Abbildung → **formale, strukturelle Abbildung mittels Funktoren**:

```
Glossar-Kategorie G
  (Begriffe + Abhängigkeiten)
       ↓ Funktor F (struktur-erhaltend)
Code-Kategorie K
  (Symbole + Imports)
       ↓ Funktor T (Validierung)
Validierungs-Kategorie V
  (Tests/Oracles)
```

**Wichtig:** Funktoren **erhalten Struktur** — wenn A → B im Glossar, dann F(A) → F(B) im Code.

---

## 📚 Dokumente in dieser Serie

### 1. **01-konzept-kategorietheorie-priming.md** – Die Theorie

**Zielgruppe:** Entwickler, Architekten, theoretisch Interessierte

**Inhalte:**
- Semiotik (Peirce): Zeichen und Bedeutung innerhalb einer Domäne
- Kategorietheorie: Strukturen und Pfeile zwischen Kategorien
- Funktoren: struktur-erhaltende Abbildungen
- Die drei Kategorien: Glossar | Code | Tests
- Semiotische Klassifikation (ikonisch, indexikalisch, symbolisch)
- Integration in das Projekt

**Zeitaufwand:** 30–60 Minuten zum Verstehen

**Kernfrage:** Wie bildet man Struktur formal ab?

---

### 2. **02-beispiel-regenbogenwahrscheinlichkeit.md** – Die Praxis

**Zielgruppe:** Agenten, Entwickler (hands-on learning)

**Inhalte:**
- Vollständiges Durchbeispiel: RegenbogenWahrscheinlichkeit
- Glossar-Kategorie: Objekte + Morphismen (Abhängigkeiten)
- Funktor F: Glossar → Code (mit vollständigem Code-Beispiel)
- Funktor T: Code → Tests (mit vollständigen Tests)
- Funktor-Komposition: die komplette Validierungskette
- PF-FUNKTOR-Checkliste angewendet
- Fehler-Szenarien: Was schiefgehen kann
- Semiotische Klassifikation auf das Beispiel angewendet

**Zeitaufwand:** 1–2 Stunden zum Durcharbeiten + Experimentieren

**Kernfrage:** Wie sieht das konkret aus?

---

## 🚀 Schnelleinstieg für Agenten

### Wenn du einen Glossar-Begriff in Code abbildest:

```markdown
## Checkliste: Funktor-Respekt

### 1. GLOSSAR-STRUKTUR VERSTEHEN
  ☐ Welche Abhängigkeiten hat dieser Begriff?
  ☐ Welche Invarianten gelten?
  ☐ Welche Morphismen (Pfeile) sind im Glossar?

### 2. FUNKTOR F DEFINIEREN (Glossar → Code)
  ☐ Code-Symbol eindeutig benennen
  ☐ Kommentar: @functor_source("glossar:Begriff")
  ☐ Alle Glossar-Pfeile → Code-Pfeile abgebildet?
  ☐ Struktur erhalten? (if A → B, dann F(A) → F(B))

### 3. TESTS ALS FUNKTOR T SCHREIBEN
  ☐ Test für jede Glossar-Invariante
  ☐ Markierung: @pytest.mark.oracle("glossar.invariant")
  ☐ Test validiert Glossar-Invariante direkt

### 4. KOMPOSITION PRÜFEN (T ∘ F)
  ☐ Glossar-Invariante → Code-Assertion → Test?
  ☐ Wenn Test fehlschlägt → Glossar verletzt?
  ☐ Validierungskette vollständig?

### 5. PF-FUNKTOR BESTANDEN?
  Alle Struktur-Erhaltungs-Anforderungen erfüllt?
  → JA: Code ist korrekt
  → NEIN: Sprechakt oder Abbruch
```

---

## 🔍 Wichtige Konzepte (Kurzreferenz)

| Konzept | Was es tut | Beispiel |
|---------|---|---|
| **Kategorie** | Sammlung von Objekten + Pfeilen | Glossar-Kategorie: Begriffe + Abhängigkeiten |
| **Morphismus** | Pfeil zwischen Objekten | A → B bedeutet "A hängt von B ab" |
| **Funktor** | struktur-erhaltende Abbildung zwischen Kategorien | F: Glossar → Code |
| **Struktur-Erhaltung** | Pfeile bleiben erhalten | wenn A → B, dann F(A) → F(B) |
| **Komposition** | Pfeile hintereinander | A → B → C ist eine Komposition |
| **Ikonisch** | Form-ähnlich | Name gleich: "RegenbogenWahrscheinlichkeit" |
| **Indexikalisch** | direkt wirksam | Assertion durchgesetzt: assert 0 ≤ value ≤ 100 |
| **Symbolisch** | konventionell | Pattern-Gebunden: "Domain-Entity hat __init__ assertion" |

---

## 📋 Integration in dein Projekt

### Dateien die aktualisiert werden müssen:

```
glossar-meta.md
  └─ Neue Sektion: "## 4. Funktor-Mapping"
     └─ Für jeden Begriff: Funktor F dokumentieren

glossar-domain.md, glossar-system.md
  └─ Neue Felder:
     ├─ Morphismen: [Liste von Abhängigkeiten]
     ├─ Funktor F: Zielort im Code
     ├─ Semiotischer Typ: ikonisch/indexikalisch/symbolisch
     └─ Test-Oracle: Zielort im Tests

package-schema.md
  └─ Neue Sektion: "## 9. Funktor-Mapping und Validierung"
     └─ Conventions für jeden semantischen Raum

preflight-checkliste.md
  └─ Neuer Schritt: "PF-FUNKTOR"
     └─ Struktur-Erhaltung vor Code-Änderung

AGENTS.md
  └─ Neue Instruktion: "Funktoren respektieren"
```

### Neue Tools:

```python
# tools/check_funktor_structure.py
# Checker, der prüft:
#   - Sind alle Glossar-Pfeile im Code erhalten?
#   - Ist Komposition erhalten?
#   - Gibt es Code-Pfeile ohne Glossar-Quelle?
```

---

## 🎓 Lernpfad

### Anfänger (Glossar-Nutzer)

1. Lese: **02-beispiel-regenbogenwahrscheinlichkeit.md** (Teile 1–3)
2. Tu: Wende PF-FUNKTOR-Checkliste auf einen Begriff an
3. Frage: Agenten um Review ("Ist der Funktor korrekt?")

### Fortgeschrittene (Agenten/Architekten)

1. Lese: **01-konzept-kategorietheorie-priming.md** vollständig
2. Lese: **02-beispiel-regenbogenwahrscheinlichkeit.md** vollständig
3. Tu: Durcharbeite ein neues Beispiel (z.B. Wetterzustand)
4. Implement: Schreibe einen Checker für Funktor-Struktur

### Experten (Theory)

1. Lese: beide Dokumente mit allen Details
2. Extend: Überlege Erweiterungen (z.B. Natural Transformations)
3. Research: Verknüpfe mit anderen Theorie-Ansätzen

---

## ⚡ Schnelle Verweisung für Agenten

**Frage: "Wie bilde ich einen Glossar-Begriff in Code ab?"**

→ Siehe: **02-beispiel-regenbogenwahrscheinlichkeit.md, Phase 1–3**

**Frage: "Was ist ein Funktor?"**

→ Siehe: **01-konzept-kategorietheorie-priming.md, § 2.3**

**Frage: "Wie prüfe ich Struktur-Erhaltung?"**

→ Siehe: **02-beispiel-regenbogenwahrscheinlichkeit.md, Phase 5** (PF-FUNKTOR)

**Frage: "Was sind ikonische vs. indexikalische Korrespondenzen?"**

→ Siehe: **02-beispiel-regenbogenwahrscheinlichkeit.md, Phase 6**

---

## 🔗 Verknüpfung mit bestehendem System

Dieses Framework ist **komplementär**, nicht ersetzend:

```
Bestehendes System (v1):
  ├─ Glossare (Semiotik auf einzelne Begriffe)
  ├─ Semantische Räume (domain, system, infrastructure)
  ├─ Import-Checker (Layer-Durchsetzung)
  ├─ Tests (Verhalten prüfen)
  └─ Evidence-System (Nachweise dokumentieren)

Neues Framework (v2):
  ├─ Funktoren (Struktur zwischen Glossar und Code)
  ├─ Korrespondenzmapping (explizite Abbildung)
  ├─ Funktor-Checker (Struktur-Erhaltung prüfen)
  ├─ Oracle-Tests (Invarianten validieren)
  └─ Peirce-Klassifikation (semiotische Typen)

Integration:
  Glossar + Funktor = vollständiges Priming-System
```

---

## 📖 Literatur-Verweise (für Tiefergehendes)

### Semiotik
- **Charles Sanders Peirce** (1896): The Definition of Pragmatic Sign
- **Umberto Eco** (1976): A Theory of Semiotics
- Kernidee: Zeichen = Signifikant + Signifikat + Referent

### Kategorietheorie
- **Saunders Mac Lane** (1971): Categories for the Working Mathematician
- **Steve Awodey** (2010): Category Theory
- Kernidee: Struktur liegt in Morphismen, nicht Objekten

### Funktoren
- **Definition:** Funktor F: C → D erhält Objekt- und Morphismus-Struktur
- **Struktur-Erhaltung:** F(A → B) = F(A) → F(B)
- **Komposition:** (T ∘ F)(X) = T(F(X))

---

## 🎯 Nächste Schritte für dein Projekt

1. **Pilot:** Wende v2-Framework auf 1–2 Begriffe an (2–4 Std)
2. **Checklisten:** Integriere PF-FUNKTOR in preflight-checkliste.md
3. **Werkzeuge:** Schreibe `tools/check_funktor_structure.py`
4. **Glossare:** Füge Funktor-Felder zu glossar-domain.md hinzu
5. **Agent-Priming:** Aktualisiere AGENTS.md mit Funktor-Instruktionen
6. **Learning:** Dokumentiere Lessons in learning-matrix.md

---

## 📞 Fragen? Probleme?

**Im Projekt:**
- Sprechakt: Neue Funktor-Fragen → SP7 oder neue Kategorie?
- Glossar: Sind Morphismus-Felder für alle Begriffe nötig?
- Checker: Soll Funktor-Struktur-Prüfung mandatory sein?

**Erfahrungsbericht:**
- EB bei Pilot-Anwendung schreiben
- Muster identifizieren (welche Funktoren sind häufig?)
- Learning-Matrix aktualisieren

---

**Erstellt:** 2026-08-15  
**Version:** 0.1 (Pilotphase)  
**Autor:** Claude + Dieter (Kategorietheorie-Forschung)  

---

**Viel Erfolg bei der Anwendung! 🚀**

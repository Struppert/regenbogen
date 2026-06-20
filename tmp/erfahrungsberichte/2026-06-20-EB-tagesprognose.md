# Erfahrungsbericht: Tagesprognose

Zeitpunkt: 2026-06-20
Bezug auf Plan: `docs/plans/2026-06-20-tagesprognose.md`

## Kontext

Neue Feature-Erweiterung: stündliche Tagesprognose mit Spitzenstunde.
Fünf Sprechakt-Entscheidungen vor Implementierung, dann vollständige Umsetzung
über Domain → Port → Infrastructure → Use Case → CLI → Tests.

## Beobachtungen

### 1. Schichtverletzung cli → domain

`gui_format.py` wollte `TagesPrognose` aus `domain/` importieren.
Der Checker behandelt `cli → domain` als explizit verboten
(nicht nur als `decision` wie im package-schema beschrieben).
Lösung: Typannotation entfernt — duck typing. Die Funktion ist einfach
genug, dass das akzeptabel ist.

Das zeigt eine strukturelle Spannung: CLI-Formatierungsfunktionen arbeiten
natürlich auf Domain-Objekten, können sie aber im cli/-Raum nicht benennen.
Eine sauberere Lösung wäre ein Protokoll-Typ in system/, aber der würde
seinerseits PrognoseStunde (domain) referenzieren müssen.

### 2. Neue abstrakte Port-Methode bricht vorhandene Fakes

`hole_stundliche_messungen()` als neue abstractmethod auf `WetterApiPort`
hat die handgeschriebene `FakeWetterApi` in `test_logging.py` gebrochen.
`MagicMock(spec=WetterApiPort)` war davon nicht betroffen — es mockt
abstrakte Methoden automatisch.

Regel: Beim Erweitern einer abstrakten Klasse immer alle handgeschriebenen
Fake-Implementierungen im Test-Raum prüfen.

### 3. ZoneInfo('UTC') ≠ timezone.utc

`ZoneInfo('UTC')` und `datetime.timezone.utc` sind beide UTC, aber
nicht `==` als Objekte. Ein Test der `tzinfo == timezone.utc` prüfte,
schlug fehl. Korrekte Prüfung: `utcoffset().total_seconds() == 0`.

### 4. mypy: Gemeinsame Variable für inkompatible Typen

```python
use_case = create_tagesprognose_use_case()    # TagesPrognoseUseCase
...
use_case = create_regenbogen_use_case()        # RegenbogenWahrscheinlichkeitUseCase
```

mypy lehnte das ab — Typinferenz bindet die Variable an den ersten Typ.
Lösung: Keine gemeinsame Variable, Factory-Funktionen direkt inline nutzen.

### 5. TYPE_CHECKING-Guard hilft nicht beim Layer-Checker

Der Checker nutzt `ast.walk()` — er sieht alle Import-Knoten,
auch solche in `if TYPE_CHECKING:` Blöcken. Das ist kein Umgehungspfad.

### 6. Sprechakt-Prozess hat funktioniert

Alle fünf SP-Entscheidungen (SP1-A bis SP3-A) wurden vor Implementierung
getroffen. Keine Implementierungsentscheidung musste nachträglich zurückgedreht
werden. Die Mondbögen-Frage (SP1-A) hat einen klaren Scope-Ausschluss
produziert, der sich in der Nicht-Ziele-Liste niederschlägt.

## Was gut funktioniert hat

- Schrittweise Umsetzung (Domain → Port → Infra → UseCase → CLI → Tests)
  ohne Rückschritte.
- Import-Checker hat die cli→domain-Verletzung sofort und präzise gemeldet.
- Retry-Logik aus dem bestehenden Use Case 1:1 übertragbar — eigene Klasse
  war die richtige Entscheidung (SP2-A).
- 54 Tests grün nach erstem Durchlauf abgesehen von zwei kleinen Nachbesserungen.

## Reibungspunkte

- cli → domain ist strukturell schwierig für Formatierungsfunktionen.
  Kein Blocker in diesem Schnitt, aber ein wiederkehrendes Muster.
- ruff format benötigte einen separaten Lauf nach der Hauptimplementierung —
  kleine Verzögerung, kein Problem.

## Lernwert für das Priming

Der `cli → domain` Import-Konflikt bei Formatierungsfunktionen ist kein
Einzelfall. Er wird bei jeder neuen Domain-Type-basierten Ausgabe auftreten.
Das Muster ist: CLI-Formatierfunktion arbeitet auf Domain-Typ, CLI darf
Domain aber nicht direkt importieren. Die Lösung (duck typing) funktioniert,
ist aber undeklariert. Wenn das Projekt mypy-typed bleiben soll, braucht
es langfristig eine explizite Klassenantwort (Protocol in system? Known Breach
KB-x? cli→domain als `decision` statt forbidden im Checker?).

## Nachträgliche Reflexion

Erfahrungsbericht wurde vergessen — nicht geschrieben nach Plan-Abschluss.
Grund: Nach Abschluss der Vollvalidierung kein expliziter Abschritt
im Preflight der daran erinnert. Der "Abbruchregel"-Block am Ende des Plans
enthält keinen Hinweis, keinen Pflichtschritt für den Erfahrungsbericht.

Mögliche Massnahme: Schritt "Erfahrungsbericht schreiben" in
Abschlusskriterien des Plan-Templates ergänzen oder im Preflight P11
erwähnen.

Learning-Matrix-Kandidat:     ja
Muster-ID:                    leer (neues Muster: Erfahrungsbericht nach Plan vergessen)
Übernommen in Learning-Matrix: nein

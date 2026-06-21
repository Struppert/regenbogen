# migration-bridges.md — Python-Projekt: Symbolsperren und Bridge-Begriffe

> Dieses Dokument klassifiziert Symbole und Begriffe, die nicht mechanisch angefasst
> werden dürfen — auch wenn sie in keiner geschützten Datei stehen.
>
> Geschützte Dateien: `AGENTS.md` Abschnitt 9.
> Symbolsperren: dieses Dokument.

---

## 1. Warum Symbolsperren?

Die Schreibrechte in `AGENTS.md` schützen Dateien.
Dieses Dokument schützt Bedeutungen.

Ein Symbol kann in einer frei beschreibbaren Datei stehen
und trotzdem nicht mechanisch umbenannt, ersetzt oder entfernt werden dürfen —
weil es eine Bridge-Funktion trägt, eine laufende Migration begleitet
oder ein bekannter Bruch bewusst bestehen bleibt.

Ohne dieses Dokument existiert dieses Wissen nur im Kopf des Entwicklers.
Ein Agent der es nicht explizit lesen kann, handelt blind.

---

## 2. Migrationsstatus-Klassen

```text
canonical
  Das ist der aktuelle, bevorzugte Begriff.
  Neuer Code verwendet diesen Begriff.
  Bestehender Code soll in diese Richtung migriert werden.

legacy-bridge
  Der Begriff ist noch aktiv im Einsatz, aber auf dem Weg heraus.
  Darf gelesen, aber nicht neu eingeführt werden.
  Mechanisches Umbenennen ist VERBOTEN — Folgeeffekte sind nicht lokal.
  Ablaufplan muss existieren.

deprecated
  Der Begriff soll nicht mehr verwendet werden.
  Bestehende Verwendungen sind bekannte Brüche.
  Neuer Code darf ihn nicht einführen.
  Darf nur im Rahmen eines expliziten Migrationsplans entfernt werden.

do-not-touch
  Dieser Begriff oder dieses Symbol darf ohne explizite Freigabe
  weder umbenannt, verschoben, ersetzt noch entfernt werden.
  Kein Anlass rechtfertigt eine mechanische Änderung.
  Änderungsauftrag erfordert Sprechakt SP6.
```

---

## 3. Agent-Aktionsregeln

```text
prefer
  Dieser Begriff ist kanonisch. Verwende ihn für neuen Code.

allow-read-only
  Darf gelesen und referenziert werden.
  Darf nicht neu eingeführt werden.

do-not-introduce
  Dieser Begriff darf in neuem Code nicht verwendet werden.
  Bestehendes ist Legacy — nicht anfassen außer im Rahmen eines Plans.

do-not-touch-mechanically
  Keine Find-Replace, keine Batch-Umbenennung, keine automatische Refactoring-Operation.
  Jede Änderung erfordert manuellen Review und Sprechakt SP6.
```

---

## 4. Bridge-Registry

> **ACHTUNG FÜR AGENTEN:** Einträge hier sind KEINE Arbeitsgrundlage.
> Sie beschreiben semantische Altlasten oder laufende Migrationen.
> Ein Bridge-Symbol ist kein Kandidat für neuen Code — auch wenn es
> technisch vorhanden und dokumentiert ist.
> Jede aktive Nutzung eines Bridge-Symbols in neuem Code ist
> standardmäßig ein HARD-Abbruch H3, außer die `Änderungsregel`
> des Eintrags erlaubt sie explizit.
> Dokumentiert = bekannt, nicht = erlaubt.

Bekannte Bridge-Begriffe dieses Projekts eintragen.

Format:

```text
BR-<NR>:
  Symbol:             <Name des Symbols, Schlüssels, Typnamens, Funktionsnamens>
  Ort:                <Dateipfad oder Modulpfad>
  Migrationsstatus:   canonical | legacy-bridge | deprecated | do-not-touch
  Bevorzugter Nachfolger: <neuer kanonischer Begriff, oder "—">
  Agent-Aktion:       prefer | allow-read-only | do-not-introduce | do-not-touch-mechanically
  Änderungsregel:     <was ein Agent konkret tun oder lassen muss>
  Ablaufplan:         <docs/plans/YYYY-MM-DD-... oder "—">
  Begründung:         <warum dieser Status>
```

Kein aktiver Bridge-Eintrag nach Instanziierung.

---

## 5. Wie ein Agent dieses Dokument verwendet

Vor jeder Änderung, die einen Begriff aus der Bridge-Registry berührt:

```text
1. Symbol in BR-Registry suchen.
2. Migrationsstatus lesen.
3. Agent-Aktion prüfen.
4. Bei do-not-touch-mechanically: STOPP.
   Änderung nur mit explizitem Auftrag und Sprechakt SP6.
5. Bei allow-read-only: lesen erlaubt, nicht neu einführen.
6. Bei do-not-introduce: aktiv prüfen —
   a) Erscheint dieses Symbol im geplanten Diff als neu eingeführtes Vorkommen?
   b) Erweitere ich seinen Geltungsbereich (neue Funktion, neuer Modulpfad,
      neues Argument, neuer Rückgabetyp, neue Klasse)?
   c) Mache ich aus passiver Kompatibilität wieder aktive Semantik?
   Wenn ja zu einer dieser Fragen: HARD-Abbruch H3.
7. Bei allow-read-only oder do-not-introduce:
   Ein Bridge-Begriff ist keine Lösung für einen fehlenden kanonischen Begriff.
   Wenn kein kanonischer Begriff verfügbar ist: Task-Schnitt T1, dann SP7.
```

**Warum dieser Diff-Check nötig ist:**
Ein Bridge-Eintrag ist explizit vorhanden, dokumentiert und liegt oft genau
dort, wo neue Arbeit stattfindet. Das macht ihn für ein Modell attraktiv als
scheinbar akzeptierte Lösung. Ohne aktive Prüfung ("führe ich es gerade ein?")
ist die Textwarnung allein nicht ausreichend.

---

## 6. Verhältnis zu anderen Dokumenten

```text
AGENTS.md Abschnitt 9     → schützt Dateien
migration-bridges.md       → schützt Bedeutungen / Symbole aus domain, system und meta
package-schema.md          → klassifiziert Modulräume
sprechakt-protokoll.md SP6  → regelt Umklassifizierungen von Known Breaches

Bei Widerspruch:
  AGENTS.md > migration-bridges.md > package-schema.md
  (Autoritätsreihenfolge nach regelmatrix.md)
```

---

## 7. Pflege

```text
- Neue Bridge-Begriffe werden hier eingetragen, bevor Code geändert wird.
- Abgeschlossene Migrationen werden als "canonical" markiert — nicht gelöscht.
- Migrationsstatus-Änderung ist Sprechakt SP6.
- Dieses Dokument ist geschützt (AGENTS.md Abschnitt 9).
```

---

## 8. Schlussregel

Ein Symbol das in `glossar-domain.md`, `glossar-system.md`, `glossar-meta.md`
oder im Code als Bridge-Begriff bekannt ist,
aber nicht in dieser Registry steht, ist ein Drift-Signal.

Wenn ein Agent unsicher ist, ob ein Symbol eine Bridge-Funktion trägt:
nicht raten. Task-Schnitt prüfen. Sprechakt SP6 auslösen.

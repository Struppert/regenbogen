from regenbogen.domain.tagesprognose import TagesPrognose
from regenbogen.system.core.wahrscheinlichkeit_use_case import WetterErgebnis


def formatiere_wetter(ergebnis: WetterErgebnis) -> str:
    """Menschenlesbarer Wettertext aus WetterErgebnis."""
    teile = []
    if ergebnis.zustand.sonnenschein:
        teile.append(
            "Sonnenscheinanteil "
            f"({round(ergebnis.zustand.sonnenschein_intensitaet * 100)} % der Stunde)"
        )
    if ergebnis.zustand.regen:
        teile.append(f"Regen ({round(ergebnis.zustand.regen_intensitaet * 100)} %)")
    wetter_text = ", ".join(teile) if teile else "Bedeckt, kein Niederschlag"

    zeilen = [
        f"Wetter: {wetter_text}",
        f"Regenbogen: {ergebnis.wahrscheinlichkeit} %",
        f"Sichtbarkeit: {ergebnis.sichtbarkeit} %",
    ]
    if ergebnis.blickrichtung:
        zeilen.append(f"Blickrichtung: {ergebnis.blickrichtung}")
    return "\n".join(zeilen)


def formatiere_tagesprognose(prognose: TagesPrognose) -> str:
    """Stündliche Tagesprognose als kompakte Tabelle."""
    kopf = f"Regenbogen-Prognose für {prognose.ort}"
    if not prognose.hat_regenbogen_chance:
        return f"{kopf}\nHeute kein Regenbogen zu erwarten."

    spitze = prognose.spitzenstunde
    zeilen = []
    for stunde in prognose.stunden:
        markierung = "   ← Spitze" if stunde is spitze else ""
        zeilen.append(
            f"  {stunde.stunde:02d}:00"
            f"  Wahrscheinlichkeit {stunde.wahrscheinlichkeit:3d} %"
            f"  Sichtbarkeit {stunde.sichtbarkeit:3d} %"
            f"{markierung}"
        )
    if prognose.blickrichtung and spitze is not None:
        zeilen.append(
            f"Beste Chance: {spitze.stunde:02d}:00 — schau nach {prognose.blickrichtung}"
        )
    if prognose.hat_sekundaerbogen_chance:
        s_stunden = [
            s for s in prognose.stunden if s.sekundaerbogen_wahrscheinlichkeit > 0
        ]
        fruehste = min(s_stunden, key=lambda s: s.stunde)
        spaetste = max(s_stunden, key=lambda s: s.stunde)
        if fruehste.stunde == spaetste.stunde:
            zeilen.append(f"Sekundaerbogen moeglich: {fruehste.stunde:02d}:00")
        else:
            zeilen.append(
                f"Sekundaerbogen moeglich: {fruehste.stunde:02d}:00–{spaetste.stunde:02d}:00"
            )
    return kopf + "\n" + "\n".join(zeilen)

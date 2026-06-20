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

    return (
        f"Wetter: {wetter_text}\n"
        f"Regenbogen: {ergebnis.wahrscheinlichkeit} %\n"
        f"Sichtbarkeit: {ergebnis.sichtbarkeit} %"
    )


def formatiere_tagesprognose(prognose) -> str:
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
    return kopf + "\n" + "\n".join(zeilen)

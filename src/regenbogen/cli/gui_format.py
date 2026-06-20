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

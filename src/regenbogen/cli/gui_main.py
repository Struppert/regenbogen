import tkinter as tk
from tkinter import messagebox

from regenbogen.adapters.wiring import create_regenbogen_use_case
from regenbogen.cli.ausgabe_fenster import AusgabeFenster
from regenbogen.cli.config_dialog import KonfigurationsDialog
from regenbogen.system.ports.standort_port import PostleitzahlUnbekannt
from regenbogen.system.ports.wetterapi_port import (
    OrtNichtGefunden,
    WetterApiNichtErreichbar,
)


def main() -> int:
    root = tk.Tk()
    root.withdraw()

    dialog = KonfigurationsDialog(root)
    konfiguration = dialog.zeige()
    if konfiguration is None:
        root.destroy()
        return 0

    use_case = create_regenbogen_use_case()

    try:
        ergebnis = use_case.berechne_vollstaendig(
            konfiguration.ortsname,
            konfiguration.postleitzahl or None,
        )
    except OrtNichtGefunden:
        messagebox.showerror(
            "Ort nicht gefunden",
            f"Der Ort '{konfiguration.ortsname}' ist unbekannt.",
        )
        root.destroy()
        return 1
    except PostleitzahlUnbekannt:
        messagebox.showerror(
            "Postleitzahl unbekannt",
            "Die eingegebene Postleitzahl ist unbekannt.",
        )
        root.destroy()
        return 1
    except WetterApiNichtErreichbar:
        messagebox.showerror(
            "Verbindungsfehler",
            "Der Wetterdienst ist nicht erreichbar.\nBitte spaeter erneut versuchen.",
        )
        root.destroy()
        return 2

    ausgabe = AusgabeFenster(root)
    ausgabe.zeige(ergebnis, ortsanzeige=konfiguration.anzeige_name())
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

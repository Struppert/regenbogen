import tkinter as tk
from tkinter import ttk

from regenbogen.cli.gui_format import formatiere_wetter
from regenbogen.system.core.wahrscheinlichkeit_use_case import WetterErgebnis


class AusgabeFenster:
    """Zeigt WetterErgebnis in einem eigenen Fenster an."""

    def __init__(self, root: tk.Tk) -> None:
        self._root = root

    def zeige(self, ergebnis: WetterErgebnis, ortsanzeige: str | None = None) -> None:
        titel = ortsanzeige or ergebnis.ort
        fenster = tk.Toplevel(self._root)
        fenster.title(f"Regenbogen - {titel}")
        fenster.resizable(False, False)

        frame = ttk.Frame(fenster, padding=20)
        frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame, text=titel, font=("", 14, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )

        farbe = "#1a7a1a" if ergebnis.wahrscheinlichkeit >= 30 else "#555555"
        ttk.Label(
            frame,
            text=formatiere_wetter(ergebnis),
            foreground=farbe,
            justify="left",
        ).grid(row=1, column=0, sticky="w")

        ttk.Button(frame, text="Schliessen", command=fenster.destroy).grid(
            row=2, column=0, sticky="e", pady=(16, 0)
        )

import tkinter as tk
from dataclasses import dataclass
from tkinter import messagebox, ttk


@dataclass
class OrtKonfiguration:
    """Ergebnis des Konfigurationsdialogs."""

    ortsname: str
    postleitzahl: str

    def anzeige_name(self) -> str:
        if not self.postleitzahl:
            return self.ortsname
        return f"{self.ortsname} ({self.postleitzahl})"


class KonfigurationsDialog:
    """Modaler Dialog zur Ortsauswahl."""

    def __init__(self, root: tk.Tk) -> None:
        self._root = root
        self._ergebnis: OrtKonfiguration | None = None

    def zeige(self) -> OrtKonfiguration | None:
        dialog = tk.Toplevel(self._root)
        dialog.title("Ort konfigurieren")
        dialog.resizable(False, False)
        dialog.grab_set()

        frame = ttk.Frame(dialog, padding=16)
        frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame, text="Ortsname:").grid(row=0, column=0, sticky="w", pady=4)
        ortsname_var = tk.StringVar(value="Berlin")
        ttk.Entry(frame, textvariable=ortsname_var, width=24).grid(
            row=0, column=1, pady=4, padx=(8, 0)
        )

        ttk.Label(frame, text="Postleitzahl (optional):").grid(
            row=1, column=0, sticky="w", pady=4
        )
        plz_var = tk.StringVar()
        ttk.Entry(frame, textvariable=plz_var, width=24).grid(
            row=1, column=1, pady=4, padx=(8, 0)
        )

        def bestaetigen() -> None:
            name = ortsname_var.get().strip()
            if not name:
                messagebox.showwarning(
                    "Fehlende Eingabe",
                    "Bitte einen Ortsnamen eingeben.",
                    parent=dialog,
                )
                return
            self._ergebnis = OrtKonfiguration(
                ortsname=name,
                postleitzahl=plz_var.get().strip(),
            )
            dialog.destroy()

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(12, 0))
        ttk.Button(btn_frame, text="OK", command=bestaetigen).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Abbrechen", command=dialog.destroy).pack(
            side="left", padx=4
        )

        self._root.wait_window(dialog)
        return self._ergebnis

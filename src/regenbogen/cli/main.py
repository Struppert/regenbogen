import argparse
import sys

from regenbogen.adapters.wiring import create_regenbogen_use_case
from regenbogen.system.ports.standort_port import PostleitzahlUnbekannt
from regenbogen.system.ports.wetterapi_port import (
    OrtNichtGefunden,
    WetterApiNichtErreichbar,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Berechnet die Regenbogen-Wahrscheinlichkeit fuer einen Ort."
    )
    parser.add_argument("ort", help="Ortsname, z. B. Berlin")
    parser.add_argument("--plz", help="Optionale Postleitzahl", default=None)
    args = parser.parse_args()

    use_case = create_regenbogen_use_case()

    try:
        wahrscheinlichkeit = use_case.berechne(args.ort, args.plz)
    except OrtNichtGefunden:
        print(f"Fehler: Ort {args.ort!r} nicht gefunden.", file=sys.stderr)
        return 1
    except PostleitzahlUnbekannt:
        print("Fehler: Postleitzahl unbekannt.", file=sys.stderr)
        return 1
    except WetterApiNichtErreichbar:
        print("Fehler: Wetterdienst nicht erreichbar.", file=sys.stderr)
        return 2

    print(f"Regenbogen-Wahrscheinlichkeit in {args.ort}: {wahrscheinlichkeit}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# BEGRIFFSINDEX.md — Name zu Raum, Ort, Test und Glossareintrag

> Ebene: REPOSITORY
> Rolle: Nachschlagewerk: Name zu Raum, Ort im Code, Test und Glossareintrag
> Geltung: dieses Projekt
> Autoritative Frage: In welcher Datei steht ein Begriff und welcher Glossareintrag erklaert ihn?
> Nicht zustaendig fuer: Bedeutung (Glossar), Regeln, Importmatrix (package-schema.md)

> Lokaler Pilot (Sprechakt `docs/sprechakte/2026-11-16-migration-v0.3.11-entscheidungen.md`).
> Menschenlesbare Tabelle. Der Checker liest sie und meldet Befunde, er entscheidet nichts.
> Neue Begriffe entstehen durch Sprechakt und werden erst danach hier aufgenommen.
> Der Index enthaelt keine Bedeutung. Die steht im Glossar.

Spalten: **Art** ist `Symbol` (steht als Klasse oder Funktion im Code) oder `Konzept`
(Fachbegriff ohne eigenes Symbol). **Raum** ist der semantische Raum des Begriffs. **Ort**
nennt Datei und Symbol (`pfad::Symbol`). **Glossar** verweist auf den Eintrag.

Bekannte Auffaelligkeit: `SonnenscheinAnteil` ist ein Fachbegriff (Raum domain), seine
Umsetzung liegt aber im System-Use-Case. Der Checker meldet das als Hinweis.

| Name | Art | Raum | Ort | Test | Glossar | Status | Aliase |
|---|---|---|---|---|---|---|---|
| create_regenbogen_use_case | Symbol | adapters | `src/regenbogen/adapters/wiring.py::create_regenbogen_use_case` | — | — | canonical |  |
| create_tagesprognose_use_case | Symbol | adapters | `src/regenbogen/adapters/wiring.py::create_tagesprognose_use_case` | — | — | canonical |  |
| AusgabeFenster | Symbol | cli | `src/regenbogen/cli/ausgabe_fenster.py::AusgabeFenster` | — | — | canonical |  |
| OrtKonfiguration | Symbol | cli | `src/regenbogen/cli/config_dialog.py::OrtKonfiguration` | — | — | canonical |  |
| KonfigurationsDialog | Symbol | cli | `src/regenbogen/cli/config_dialog.py::KonfigurationsDialog` | — | — | canonical |  |
| formatiere_wetter | Symbol | cli | `src/regenbogen/cli/gui_format.py::formatiere_wetter` | `tests/cli/test_gui_format.py` | — | canonical |  |
| formatiere_tagesprognose | Symbol | cli | `src/regenbogen/cli/gui_format.py::formatiere_tagesprognose` | `tests/cli/test_gui_format.py` | — | canonical |  |
| main | Symbol | cli | `src/regenbogen/cli/gui_main.py::main` | — | — | canonical |  |
| main | Symbol | cli | `src/regenbogen/cli/main.py::main` | — | — | canonical |  |
| berechne_regenbogen_wahrscheinlichkeit | Symbol | domain | `src/regenbogen/domain/regenbogen.py::berechne_regenbogen_wahrscheinlichkeit` | `tests/domain/test_regenbogen.py` | — | canonical |  |
| Sonnenstand | Symbol | domain | `src/regenbogen/domain/regenbogen_geometrie.py::Sonnenstand` | `tests/cli/test_gui_format.py`, `tests/domain/test_regenbogen.py`, `tests/domain/test_regenbogen_geometrie.py` | `glossar-domain.md#Sonnenstand` | canonical |  |
| berechne_regenbogen_azimut | Symbol | domain | `src/regenbogen/domain/regenbogen_geometrie.py::berechne_regenbogen_azimut` | `tests/domain/test_regenbogen_geometrie.py` | — | canonical |  |
| azimut_zu_himmelsrichtung | Symbol | domain | `src/regenbogen/domain/regenbogen_geometrie.py::azimut_zu_himmelsrichtung` | `tests/domain/test_regenbogen_geometrie.py` | — | canonical |  |
| berechne_sonnenstands_faktor | Symbol | domain | `src/regenbogen/domain/regenbogen_geometrie.py::berechne_sonnenstands_faktor` | `tests/domain/test_regenbogen_geometrie.py` | — | canonical |  |
| berechne_sonnenstands_faktor_sekundaerbogen | Symbol | domain | `src/regenbogen/domain/regenbogen_geometrie.py::berechne_sonnenstands_faktor_sekundaerbogen` | `tests/domain/test_regenbogen_geometrie.py` | — | canonical |  |
| RegenbogenOptikFaktoren | Symbol | domain | `src/regenbogen/domain/regenbogen_optik.py::RegenbogenOptikFaktoren` | `tests/domain/test_regenbogen_optik.py` | — | canonical |  |
| berechne_regenbogen_sichtbarkeit | Symbol | domain | `src/regenbogen/domain/regenbogen_optik.py::berechne_regenbogen_sichtbarkeit` | `tests/domain/test_regenbogen_optik.py` | — | canonical |  |
| PrognoseStunde | Symbol | domain | `src/regenbogen/domain/tagesprognose.py::PrognoseStunde` | `tests/cli/test_gui_format.py`, `tests/domain/test_tagesprognose.py`, `tests/system/test_tagesprognose_use_case.py` | `glossar-domain.md#PrognoseStunde` | canonical |  |
| TagesPrognose | Symbol | domain | `src/regenbogen/domain/tagesprognose.py::TagesPrognose` | `tests/cli/test_gui_format.py`, `tests/domain/test_tagesprognose.py`, `tests/system/test_tagesprognose_use_case.py` | `glossar-domain.md#TagesPrognose` | canonical |  |
| Wetterzustand | Symbol | domain | `src/regenbogen/domain/wetter.py::Wetterzustand` | `tests/cli/test_gui_format.py`, `tests/domain/test_regenbogen.py` | `glossar-domain.md#Wetterzustand` | canonical |  |
| configure_logging | Symbol | infrastructure | `src/regenbogen/infrastructure/event_logger.py::configure_logging` | — | — | canonical |  |
| StdlibEventLogger | Symbol | infrastructure | `src/regenbogen/infrastructure/event_logger.py::StdlibEventLogger` | — | — | canonical |  |
| OpenMeteoClient | Symbol | infrastructure | `src/regenbogen/infrastructure/open_meteo_client.py::OpenMeteoClient` | `tests/infrastructure/test_open_meteo_client.py` | — | canonical |  |
| PlzStandortLookup | Symbol | infrastructure | `src/regenbogen/infrastructure/plz_lookup.py::PlzStandortLookup` | `tests/infrastructure/test_plz_lookup.py` | — | canonical |  |
| OptischeBedingungen | Symbol | system | `src/regenbogen/system/core/optische_bedingungen.py::OptischeBedingungen` | — | — | canonical |  |
| leite_optische_bedingungen_ab | Symbol | system | `src/regenbogen/system/core/optische_bedingungen.py::leite_optische_bedingungen_ab` | `tests/system/test_optische_bedingungen.py` | — | canonical |  |
| berechne_sonnenstand | Symbol | system | `src/regenbogen/system/core/sonnenstand.py::berechne_sonnenstand` | — | — | canonical |  |
| TagesPrognoseUseCase | Symbol | system | `src/regenbogen/system/core/tagesprognose_use_case.py::TagesPrognoseUseCase` | `tests/system/test_tagesprognose_use_case.py` | — | canonical |  |
| WetterErgebnis | Symbol | system | `src/regenbogen/system/core/wahrscheinlichkeit_use_case.py::WetterErgebnis` | `tests/cli/test_gui_format.py` | `glossar-system.md#WetterErgebnis` | canonical |  |
| RegenbogenWahrscheinlichkeitUseCase | Symbol | system | `src/regenbogen/system/core/wahrscheinlichkeit_use_case.py::RegenbogenWahrscheinlichkeitUseCase` | `tests/system/test_logging.py`, `tests/system/test_use_case.py`, `tests/system/test_winkelmodell.py` | — | canonical |  |
| LogLevel | Symbol | system | `src/regenbogen/system/ports/logging_port.py::LogLevel` | — | — | canonical |  |
| LogEvent | Symbol | system | `src/regenbogen/system/ports/logging_port.py::LogEvent` | `tests/system/test_logging.py` | `glossar-system.md#LogEvent` | canonical |  |
| EventLogger | Symbol | system | `src/regenbogen/system/ports/logging_port.py::EventLogger` | `tests/system/test_logging.py` | `glossar-system.md#EventLogger` | canonical |  |
| NullEventLogger | Symbol | system | `src/regenbogen/system/ports/logging_port.py::NullEventLogger` | — | — | canonical |  |
| StandortKoordinaten | Symbol | system | `src/regenbogen/system/ports/standort_port.py::StandortKoordinaten` | `tests/infrastructure/test_open_meteo_client.py`, `tests/system/test_logging.py`, `tests/system/test_tagesprognose_use_case.py` | — | canonical |  |
| PostleitzahlUnbekannt | Symbol | system | `src/regenbogen/system/ports/standort_port.py::PostleitzahlUnbekannt` | `tests/infrastructure/test_plz_lookup.py` | `glossar-system.md#PostleitzahlUnbekannt` | canonical |  |
| StandortPort | Symbol | system | `src/regenbogen/system/ports/standort_port.py::StandortPort` | `tests/system/test_logging.py` | — | canonical |  |
| WetterApiMessung | Symbol | system | `src/regenbogen/system/ports/wetterapi_port.py::WetterApiMessung` | `tests/system/test_logging.py`, `tests/system/test_optische_bedingungen.py`, `tests/system/test_tagesprognose_use_case.py` | — | canonical |  |
| StundlicheWetterApiMessung | Symbol | system | `src/regenbogen/system/ports/wetterapi_port.py::StundlicheWetterApiMessung` | `tests/system/test_logging.py`, `tests/system/test_tagesprognose_use_case.py` | `glossar-system.md#StundlicheWetterApiMessung` | canonical |  |
| WetterApiNichtErreichbar | Symbol | system | `src/regenbogen/system/ports/wetterapi_port.py::WetterApiNichtErreichbar` | `tests/system/test_tagesprognose_use_case.py`, `tests/system/test_use_case.py` | `glossar-system.md#WetterApiNichtErreichbar` | canonical |  |
| OrtNichtGefunden | Symbol | system | `src/regenbogen/system/ports/wetterapi_port.py::OrtNichtGefunden` | `tests/system/test_tagesprognose_use_case.py`, `tests/system/test_use_case.py` | `glossar-system.md#OrtNichtGefunden` | canonical |  |
| WetterApiPort | Symbol | system | `src/regenbogen/system/ports/wetterapi_port.py::WetterApiPort` | `tests/system/test_logging.py`, `tests/system/test_tagesprognose_use_case.py`, `tests/system/test_use_case.py` | — | canonical |  |
| SonnenscheinAnteil | Konzept | domain | `src/regenbogen/system/core/wahrscheinlichkeit_use_case.py`, `src/regenbogen/cli/gui_format.py` | `tests/cli/test_gui_format.py` | `glossar-domain.md#SonnenscheinAnteil` | canonical |  |
| RegenbogenWahrscheinlichkeit | Konzept | domain | `src/regenbogen/domain/regenbogen.py` | `tests/domain/test_regenbogen.py` | `glossar-domain.md#RegenbogenWahrscheinlichkeit` | canonical |  |
| SonnenstandsFaktor | Konzept | domain | `src/regenbogen/domain/regenbogen_geometrie.py` | `tests/domain/test_regenbogen_geometrie.py` | `glossar-domain.md#SonnenstandsFaktor` | canonical |  |
| RegenbogenSichtbarkeit | Konzept | domain | `src/regenbogen/domain/regenbogen_optik.py` | `tests/domain/test_regenbogen_optik.py` | `glossar-domain.md#RegenbogenSichtbarkeit` | canonical |  |
| TropfenQualitaet | Konzept | domain | `src/regenbogen/domain/regenbogen_optik.py` | `tests/domain/test_regenbogen_optik.py` | `glossar-domain.md#TropfenQualitaet` | canonical |  |
| Sekundaerbogen | Konzept | domain | `src/regenbogen/domain/regenbogen_geometrie.py` | `tests/cli/test_gui_format.py`, `tests/domain/test_regenbogen_geometrie.py`, `tests/system/test_tagesprognose_use_case.py` | `glossar-domain.md#Sekundaerbogen` | canonical |  |
| SonnenstandsFaktorSekundaerbogen | Konzept | domain | `src/regenbogen/domain/regenbogen_geometrie.py` | `tests/domain/test_regenbogen_geometrie.py` | `glossar-domain.md#SonnenstandsFaktorSekundaerbogen` | canonical |  |
| SekundaerbogenDaempfung | Konzept | domain | `src/regenbogen/domain/regenbogen_geometrie.py` | `tests/domain/test_regenbogen_geometrie.py` | `glossar-domain.md#SekundaerbogenDaempfung` | canonical |  |
| SekundaerbogenWahrscheinlichkeit | Konzept | domain | `src/regenbogen/domain/tagesprognose.py`, `src/regenbogen/system/core/tagesprognose_use_case.py` | — | `glossar-domain.md#SekundaerbogenWahrscheinlichkeit` | canonical |  |

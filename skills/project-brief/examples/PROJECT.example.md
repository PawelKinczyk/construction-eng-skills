---
# Fictional example. Names, companies and numbers are invented.
project_name: "Biurowiec Zabłocie B2"
project_number: "2026-014"
client: "Zabłocie Office Sp. z o.o."
location: "Kraków, PL"
phase: detailed design
jurisdiction: pl
disciplines: [hvac, plumbing]
role: designer
units: SI
deliverable_language: pl
last_updated: 2026-10-11
---

# Project brief

## Scope

Projekt wykonawczy instalacji HVAC i wod-kan dla budynku biurowego B2: 6 kondygnacji nadziemnych, 1 podziemna (garaż), ok. 9 800 m² PUM.

W zakresie:
- wentylacja mechaniczna z odzyskiem ciepła,
- chłodzenie (VRF),
- ogrzewanie z węzła cieplnego MPEC,
- woda zimna i ciepła,
- kanalizacja sanitarna i deszczowa wewnętrzna.

Poza zakresem:
- instalacje tryskaczowe (osobny projektant),
- sieci zewnętrzne poza budynkiem,
- BMS (tylko punkty i wymagania dla automatyki).

Kluczowe terminy: projekt wykonawczy 15.12.2026, przedmiary 20.12.2026.

## Documents

| Document | Location (path or link) | Revision / date |
|---|---|---|
| Contract / agreement | `01_Umowa/Umowa_2026-014.pdf` | 02.09.2026 |
| Drawings | `03_Rysunki/ARCH/` (podkłady architektury) | rev. C, 30.09.2026 |
| Specifications | `02_Wytyczne/PFU_B2.pdf` | 15.08.2026 |
| Models (IFC / RVT / DWG) | `04_Modele/B2_ARCH.ifc` | 30.09.2026 |
| Correspondence | `06_Korespondencja/` | |
| Pozwolenie na budowę | `01_Umowa/PnB_B2.pdf` | wniosek złożony 12.03.2026 |

## Project standards

- File naming: ISO 19650, `ZB2-PKS-B2-XX-DR-M-0001` (projekt-autor-budynek-poziom-typ-branża-numer)
- Layer / family / object naming: standard warstw inwestora, `02_Wytyczne/Standard_CAD.pdf`
- BEP or CAD standard document: `02_Wytyczne/BEP_B2_v2.pdf`
- Drawing numbering: wg BEP, numer 4-cyfrowy w branży
- Revision convention: P01, P02… robocze; C01… zatwierdzone
- Other rules: rysunki PDF + DWG, eksport IFC4 co 2 tygodnie

## People

| Role | Name | Company | Contact |
|---|---|---|---|
| Inwestor, kierownik projektu | Anna Przykładowa | Zabłocie Office | via email |
| Generalny projektant (ARCH) | Jan Testowy | Pracownia Testowa | via email |
| Projektant prowadzący HVAC | (my) | | |

## Watch-outs

- Wniosek o PnB złożony 12.03.2026: obowiązują WT w brzmieniu sprzed nowych WT. Sprawdzić przy każdej weryfikacji przepisów.
- Inwestor wymaga certyfikacji BREEAM Very Good: SFP central ≤ 1,6 kW/(m³/s), filtry ISO ePM1 50%.
- Garaż: wentylacja oddymiająca strumieniowa. Uzgodnić z rzeczoznawcą ppoż. przed rozpoczęciem rysunków.
- Szachty na kondygnacjach 3–6 ciasne. Każda zmiana tras wymaga potwierdzenia z architekturą.

## Decisions

| Date | Decision | Source |
|---|---|---|
| 25.09.2026 | Chłodzenie VRF zamiast wody lodowej | protokół spotkania nr 3 |
| 01.10.2026 | Centrale na dachu, nie w piwnicy | e-mail od inwestora |

## Open questions

- [ ] Moc zamówiona z MPEC: brak warunków przyłączenia w folderze.
- [ ] Wymagany standard akustyczny pomieszczeń biurowych (dB(A))?
- [x] ~~Lokalizacja central~~: dach (decyzja 01.10.2026).

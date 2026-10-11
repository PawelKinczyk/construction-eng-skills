# Karta doboru: P1 pompa obiegowa c.o.

Projekt: Biurowiec Zabłocie B2 (2026-014), przykład fikcyjny   Data: 2026-10-11   Przygotował: agent, do weryfikacji przez projektanta
Status: wersja robocza do weryfikacji

## 1. Podsumowanie
Pompa obiegowa c.o. dla obiegu grzejnikowego 120 kW, 70/50 °C. Punkt pracy: 5,25 m³/h przy 6,7 m. Model nie został wybrany: brak danych katalogowych w projekcie. Poniżej specyfikacja do zapytania ofertowego.

## 2. Parametry projektowe
| Parametr | Wartość | Jednostka | Źródło |
|---|---|---|---|
| Moc cieplna obiegu | 120 | kW | obliczenia OZC wg EN 12831-1, rew. B (przykład) |
| Temperatury zasilania / powrotu | 70 / 50 | °C | założenie projektowe |
| Przepływ | 5,25 | m³/h | `hvac_calc.py water-flow --load-kw 120 --dt 20 --temp 60` |
| Opory obiegu najniekorzystniejszego | 59,0 | kPa | tabela w p. 3 |
| Wysokość podnoszenia z zapasem | 6,7 | m | 6,1 m + 10 % |

## 3. Obliczenia
| Odcinek / element | Przepływ [m³/h] | Wymiar | Δp [kPa] | Źródło |
|---|---|---|---|---|
| Rury, odcinek główny, 120 m, ζ = 6,5 | 5,25 | DN50 (dw 53,1 mm) | 12,0 | `hvac_calc.py pipe-dp` |
| Wymiennik węzła, strona wtórna | 5,25 | | 15,0 | karta węzła (przykład) |
| Zawór regulacyjny (autorytet ≥ 0,5) | 5,25 | | 15,0 | założenie |
| Grzejnik najniekorzystniejszy z zaworem termostatycznym | | | 10,0 | założenie |
| Licznik ciepła, filtr | 5,25 | | 7,0 | założenie |
| **Razem** | | | **59,0** | ≈ 6,1 m H₂O przy 60 °C |

Zapas 10 % na wysokość podnoszenia. Powód: opory kształtek i armatury przyjęte szacunkowo. Pompa z regulacją obrotów, więc zapas jest umiarkowany. Moc hydrauliczna ok. 0,09 kW (`hvac_calc.py pump-power --flow-m3h 5.25 --head-m 6.7 --temp 60`).

## 4. Wymagania
| Wymaganie | Wartość | Źródło |
|---|---|---|
| Ekoprojekt, pompy bezdławnicowe | EEI ≤ 0,23 | Rozporządzenie (WE) nr 641/2009, EUR-Lex. Do weryfikacji: aktualne brzmienie |
| Regulacja | Δp-zmienne, sygnał do BMS (Modbus RTU) | BEP / wytyczne BMS (przykład) |
| Zasilanie | 1~230 V | PROJECT.md (przykład) |
| Wykonanie | pompa podwójna (praca/rezerwa) | wymaganie inwestora (przykład) |
| Przyłącze | kołnierzowe DN40 lub DN50 | do potwierdzenia z trasą |

## 5. Wybrane urządzenie
| Pozycja | Wartość |
|---|---|
| Producent / model | do wybrania |
| Punkt pracy na charakterystyce | do sprawdzenia: 5,25 m³/h / 6,7 m w zakresie wysokiej sprawności |
| Pobór mocy | do wybrania |
| Wymiary / masa | do wybrania |
| Źródło danych | brak; potrzebna karta katalogowa lub wydruk z programu doboru |

## 6. Alternatywy
| Opcja | Model | Różnica | Kompromis |
|---|---|---|---|
| A | pompa podwójna, regulacja Δp-zmienne | rezerwa w jednym korpusie | mniejsze miejsce, wspólny korpus |
| B | dwie pompy pojedyncze, praca/rezerwa | niezależny serwis | więcej miejsca i armatury |

## 7. Założenia
- Opory wymiennika, zaworu regulacyjnego, grzejnika i licznika przyjęte szacunkowo (p. 3).
- Woda bez glikolu, 60 °C średnio.
- Rura stalowa, chropowatość 0,045 mm.

## 8. Źródła
- Rozporządzenie Komisji (WE) nr 641/2009, eur-lex.europa.eu.
- PN-EN 12831-1, wydanie do potwierdzenia, metoda obliczania obciążenia cieplnego.
- Obliczenia: `scripts/hvac_calc.py`.

## 9. Do weryfikacji
- [ ] Rzeczywisty opór wymiennika z karty węzła.
- [ ] Dobór zaworu regulacyjnego i jego Δp.
- [ ] Model pompy i punkt pracy na charakterystyce.
- [ ] Aktualne brzmienie wymagań ekoprojektu dla pomp bezdławnicowych.

# Karta doboru: P3 podgrzewacz ciepłej wody (zbiornik) + obieg cyrkulacyjny

Projekt: Budynek mieszkalny Wielicka 12 (2026-021), przykład fikcyjny   Data: 2026-10-12   Przygotował: agent, do weryfikacji przez projektanta
Status: wersja robocza do weryfikacji

## 1. Podsumowanie
Zasobnik c.w.u. dla 10 mieszkań (przyjęto 25 osób) z kotłem o mocy c.w.u. 30 kW. Największy rozbiór: 400 l wody zmieszanej 45 °C w 15 min. Wymagana pojemność zasobnika: 151 l przy 60 °C. Proponowany zasobnik 200 l. Model nie wybrany: brak danych katalogowych w projekcie.

## 2. Parametry projektowe
| Parametr | Wartość | Jednostka | Źródło |
|---|---|---|---|
| Liczba mieszkań / osób | 10 / 25 | – | projekt architektoniczny (przykład) |
| Największy rozbiór c.w.u. | 400 l / 15 min, 45 °C | – | założenie projektowe (profil rozbioru) |
| Temperatura w zasobniku | 60 | °C | wymaganie higieniczne (Legionella) |
| Temperatura wody zimnej | 10 | °C | założenie dla lokalizacji |
| Moc ciągła kotła na c.w.u. | 30 | kW | dane kotła (przykład) |
| Objętość wody o temp. 60 °C na 400 l / 45 °C | 280 | l | `plumbing_calc.py dhw-mix --v-mix 400 --t-mix 45 --t-hot 60 --t-cold 10` |
| Woda podgrzana w czasie rozbioru | 129 | l | `plumbing_calc.py dhw-store --v-peak 400 --t-store 60 --t-cold 10 --t-mix 45 --continuous-kw 30 --draw-time-min 15` |
| Pojemność zasobnika (minimum) | 151 | l | ten sam przebieg `dhw-store` (280 − 129) |

## 3. Obliczenia
| Pozycja | Wartość | Jednostka | Źródło / komentarz |
|---|---|---|---|
| Energia rozbioru | 16,26 | kWh | 400 l × 4,18 × (45 − 10) / 3600; `plumbing_calc.py dhw-demand --volume-l 400 --t-hot 45 --t-cold 10 --draw-time-min 15` |
| Średnia moc rozbioru | 65 | kW | 16,26 kWh / 0,25 h (ten sam przebieg `dhw-demand`) |
| Moc szczytowa chwilowa | do weryfikacji | kW | z profilu rozbioru, nie z wartości średniej |
| Cyrkulacja – strata ciepła pętli | 350 | W | oszacowanie: 60 m rury, izolacja 20 mm |
| Cyrkulacja – przepływ przy ΔT 5 K | 0,017 (60) | l/s (l/h) | `plumbing_calc.py dhw-circ --heat-loss-w 350 --dt 5` |
| Woda zimna – przepływ obliczeniowy | 2,23 | l/s | `plumbing_calc.py peak-flow --fixture basin:20 --fixture wc:12 --fixture shower:10 -f 0.5` |
| Kanalizacja – przepływ obliczeniowy | 3,08 | l/s | `plumbing_calc.py stack --du 38 --k 0.5`; przepustowość pionu DN110 do weryfikacji z normą lub od producenta rur |

Uwaga: dobór 200 l wynika z 151 l + zapas na strefę zmieszania w zasobniku. Zapasu procentowego nie dodano: objętość wynika wprost z profilu rozbioru i mocy kotła. Moc średnia 65 kW jest większa od mocy ciągłej kotła 30 kW, dlatego zasobnik pokrywa deficyt 35 kW przez 15 min (129 l odpowiada mocy kotła, 151 l zasobnik); przy dłuższym szczycie trzeba zwiększyć moc kotła, nie pojemność.

## 4. Wymagania
| Wymaganie | Wartość | Źródło |
|---|---|---|
| Ekoprojekt, podgrzewacze wody i zasobniki | klasa i karta produktu | Rozporządzenie (UE) nr 814/2013, EUR-Lex. Do weryfikacji: aktualne brzmienie i klasa |
| Higiena c.w.u. | zasobnik ≥ 60 °C, dystrybucja ≥ 55 °C, woda zimna < 20 °C | wymaganie higieniczne; przepisy krajowe do sprawdzenia |
| Zabezpieczenie przed poparzeniem | zawór termostatyczny (TMV) na wyjściu | wymaganie BHP |
| Ochrona przed przepływem zwrotnym | kategoria płynu i typ zabezpieczenia | PN-EN 1717 |
| Grupa bezpieczeństwa | zawór bezpieczeństwa, naczynie wzbiorcze | dobór wg danych producenta |
| Cyrkulacja | praca czasowa, zawory równoważące na pionach | wytyczne projektu |
| Materiał | stal emaliowana lub stal nierdzewna, aprobata do wody pitnej | wymaganie higieniczne |
| Zasilanie / miejsce | do potwierdzenia z architekturą | – |

## 5. Wybrane urządzenie
| Pozycja | Wartość |
|---|---|
| Producent / model | do wybrania |
| Pojemność / typ | 200 l, stojący, ogrzewany wężownicą z kotła, wg PN-EN 12897 (sprawdzić wydanie) |
| Moc wężownicy (podgrzewanie) | do sprawdzenia: ciągłe ≥ 30 kW przy 60/10 °C |
| Wydajność c.w.u. (trwała i szczytowa) | do sprawdzenia w danych producenta |
| Klasa energetyczna | do sprawdzenia (ekoprojekt 814/2013) |
| Wymiary / masa | do sprawdzenia z miejscem w kotłowni |
| Źródło danych | brak; potrzebna karta katalogowa |

## 6. Alternatywy
| Opcja | Układ | Różnica | Kompromis |
|---|---|---|---|
| A | kocioł 30 kW c.w.u. + zasobnik 200 l z wężownicą | niska moc chwilowa kotła, pokrywa zasobnik | dłuższy czas nagrzewania zasobnika |
| B | kocioł z zasobnikiem warstwowym 200 l, wyższa moc chwilowa | lepszy komfort przy szczycie | wyższa cena, większa masa |
| C | zasobnik 300 l przy mocy kotła 24 kW | większy zapas objętości, mniejsza moc | większe miejsce i straty postojowe |

## 7. Założenia
- Profil rozbioru (400 l / 45 °C / 15 min) przyjęty przez projektanta jako szczyt poranny; do potwierdzenia.
- Przepływy jednostkowe przyborów przyjęte jako typowe (EN 806-3) i wymagają potwierdzenia.
- Szybkość odbioru c.w.u. w zasobniku nie jest jeszcze znana, stąd „do weryfikacji" dla mocy szczytowej.
- Suma jednostek wypływowych kanalizacji 38 DU i współczynnik K = 0,5 przyjęte z tabeli EN 12056-2; do potwierdzenia z normą. Przepustowość pionu DN110 nie jest podana: tabela jest w licencjonowanej normie, brak jej w repozytorium; sprawdzenie pionu pozostaje „do weryfikacji".

## 8. Źródła
- Rozporządzenie Komisji (UE) nr 814/2013 (podgrzewacze wody i zasobniki), eur-lex.europa.eu.
- PN-EN 806-3, PN-EN 1717, PN-EN 12056-2, PN-EN 12897: numery i wydania do potwierdzenia w PKN.
- Obliczenia: `scripts/plumbing_calc.py`, `scripts/hvac_calc.py`.

## 9. Do weryfikacji
- [ ] Rzeczywisty profil rozbioru c.w.u. i moc szczytowa.
- [ ] Moc wężownicy i wydajność zasobnika z karty producenta.
- [ ] Aktualne brzmienie ekoprojektu 814/2013 i klasa energetyczna.
- [ ] Przepisy krajowe: temperatura c.w.u. i zasady ochrony przed Legionellą.
- [ ] Zabezpieczenie przed przepływem zwrotnym (kategoria płynu).
- [ ] Suma DU i współczynnik K z EN 12056-2 oraz pozostałe przybory na pionach.
- [ ] Przepustowość pionu DN110 (norma lub producent rur) i uruchomienie `stack --capacity`.

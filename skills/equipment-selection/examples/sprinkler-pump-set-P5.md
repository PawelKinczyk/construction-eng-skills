# Karta doboru: P5 zestaw pompowy instalacji tryskaczowej

Projekt: Budynek magazynowo-biurowy Wielicka 12 (2026-021), przykład fikcyjny   Data: 2026-10-12   Przygotował: agent, do weryfikacji przez projektanta i rzeczoznawcę
Status: wersja robocza do weryfikacji

## 1. Podsumowanie
Zestaw pompowy tryskaczy: pompa główna, pompa podtrzymująca (jockey) i rezerwa wody. Gęstość projektowa 5 mm/min, powierzchnia obliczeniowa 216 m², dodatek na hydranty 900 l/min. Przepływ obliczeniowy 1980 l/min przy wysokości podnoszenia 62 m. Rezerwa wody 118,8 m³ przy założonym czasie 60 min. Model pompy: do wybrania.

## 2. Parametry projektowe
| Parametr | Wartość | Jednostka | Źródło |
|---|---|---|---|
| Klasa zagrożenia / gęstość projektowa | 5 | mm/min | **do potwierdzenia: PN-EN 12845, tabela klas — podać klauzulę** |
| Powierzchnia obliczeniowa | 216 | m² | **do potwierdzenia: norma dla klasy i typu stropu** |
| Przepływ tryskaczy | 1080 | l/min | `fire_calc.py sprinkler-flow --density 5 --area-m2 216` |
| Dodatek na hydranty (hose allowance) | 900 | l/min | **do potwierdzenia: norma, wartość zależna od klasy** |
| Przepływ całkowity | 1980 | l/min (33 l/s, 118,8 m³/h) | `fire_calc.py sprinkler-flow` |
| Wysokość podnoszenia | 62 | m | dobór do potwierdzenia: obliczenie hydrauliczne + ciśnienie na zaworze |
| Czas zasilania wodą | 60 | min | **do potwierdzenia: norma lub uzgodnienie** |
| Rezerwa wody | 118,8 | m³ | `fire_calc.py water-reserve --flow-l-min 1980 --duration-min 60` |

## 3. Obliczenia
| Pozycja | Wartość | Jednostka | Źródło / komentarz |
|---|---|---|---|
| Przepływ tryskaczy (5 × 216) | 1080 | l/min | wzór Q = gęstość × powierzchnia |
| Dodatek na hydranty | 900 | l/min | do potwierdzenia z normą |
| Przepływ całkowity | 1980 | l/min | suma powyżej |
| Opór rurociągu zasilającego, DN150, 120 m, ζ = 12 | 40,0 | kPa (4,1 m) | `hvac_calc.py pipe-dp --flow-m3h 118.8 --id-mm 154 --length-m 120 --zeta 12` |
| Pozostałe opory (tryskacze, zawory, różnica wysokości) | ok. 58 | m | **do policzenia: hydrauliczne obliczenie najniekorzystniejszego obszaru** |
| Moc hydrauliczna / wału pompy przy 62 m | 20,0 / 30,8 | kW | `hvac_calc.py pump-power --flow-m3h 118.8 --head-m 62 --eff 0.65`, sprawność do potwierdzenia z krzywej |

Zapasu procentowego nie dodano: gęstość, powierzchnia i dodatek na hydranty pochodzą wprost z normy lub koncepcji. Wysokość podnoszenia jest sumą oporów; różnica wysokości i ciśnienie resztowe do potwierdzenia po obliczeniu hydraulicznym.

## 4. Wymagania
| Wymaganie | Wartość | Źródło |
|---|---|---|
| Redundancja pomp | pompa główna + jockey + rezerwa, zasilanie z rezerwy | norma i koncepcja, do potwierdzenia |
| Źródło zasilania wodą | zbiornik 118,8 m³ + napełnianie, niezawodność | warunki wodociągowe i norma |
| Charakterystyka pompy | punkt pracy przy przepływie obliczeniowym; sprawdzić nadwyżkę przy 1,5 × Q | norma: max ciśnienie przy 1,5 × przepływ |
| Napęd pompy | elektryczny lub diesel, zasilanie niezawodne | koncepcja i wymagania zasilania |
| Klasa odporności ogniowej kabli zasilania | obwód pożarowy | PN-HD 60364 i przepisy ppoż. (z `electrical.md`) |
| Aprobata wyrobów | pompa, zawory, tryskacze | **CNBOP-PIB lub CE, do potwierdzenia** |
| Wskaźniki i próby | zawory, manometry, przepływomierze, próba odbiorowa | norma, protokół do ustalenia |

## 5. Wybrane urządzenie
| Pozycja | Wartość |
|---|---|
| Zestaw pompowy | do wybrania: pompa główna + jockey |
| Punkt pracy | do sprawdzenia: 1980 l/min przy 62 m, na krzywej producenta |
| Sprawność w punkcie pracy | do sprawdzenia (przyjęto 0,65) |
| Moc silnika | do sprawdzenia: ≥ 30,8 kW wału przy sprawności z krzywej |
| Zbiornik rezerwy wody | 118,8 m³ użytkowe, do potwierdzenia z geometrią i napełnianiem |
| Źródło danych | brak; potrzebne karty katalogowe zestawu i zbiornika |

## 6. Alternatywy
| Opcja | Układ | Różnica | Kompromis |
|---|---|---|---|
| A | jedna pompa elektryczna + jockey, zbiornik 120 m³ | prosty układ | brak rezerwy na awarię zasilania |
| B | pompa elektryczna + pompa diesel (rezerwa) | niezależność od zasilania | większe pomieszczenie, paliwo, obsługa |
| C | pompownia z dwiema pompami elektrycznymi na dwóch zasilaniach | rezerwa zasilania z sieci | wymaga dwóch niezależnych przyłączy |

## 7. Założenia
- Gęstość 5 mm/min, powierzchnia 216 m² i dodatek na hydranty 900 l/min przyjęte roboczo — **wymagają potwierdzenia z normą i koncepcją**.
- Czas zasilania 60 min przyjęty roboczo.
- Sprawność pompy 0,65 przyjęta; do zastąpienia wartością z krzywej producenta.
- Woda bez dodatków, 20 °C w obliczeniu oporów.

## 8. Źródła
- PN-EN 12845 (instalacje tryskaczowe): wydanie i klauzule do potwierdzenia w PKN.
- PN-EN 12101, PN-EN 54, PN-EN 15650: do potwierdzenia w PKN.
- Rozporządzenie MSWiA z 24 lipca 2009 r. (przeciwpożarowe zaopatrzenie w wodę) i Rozporządzenie MSWiA z 7 czerwca 2010 r.: brzmienie do sprawdzenia w ISAP.
- Obliczenia: `scripts/fire_calc.py`, `scripts/hvac_calc.py`.

## 9. Do weryfikacji
- [ ] Gęstość projektowa, powierzchnia obliczeniowa i dodatek na hydranty z normy (klauzula).
- [ ] Obliczenie hydrauliczne najniekorzystniejszego obszaru i ciśnienie na zaworze.
- [ ] Czas zasilania i rezerwa wody; sposób napełniania zbiornika.
- [ ] Charakterystyka pompy przy 1,5 × przepływie (limit ciśnienia wg normy).
- [ ] Aprobata (CNBOP-PIB / CE) pomp, zaworów i tryskaczy.
- [ ] Wymagania zasilania elektrycznego i klasa kabli pożarowych.
- [ ] Uzgodnienie z rzeczoznawcą ds. zabezpieczeń przeciwpożarowych.

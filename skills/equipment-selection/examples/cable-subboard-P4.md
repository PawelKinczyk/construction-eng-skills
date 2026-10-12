# Karta doboru: P4 kabel zasilający rozdzielnicę oddziałową TK-1

Projekt: Biurowiec Zabłocie B2 (2026-014), przykład fikcyjny   Data: 2026-10-12   Przygotował: agent, do weryfikacji przez projektanta
Status: wersja robocza do weryfikacji

## 1. Podsumowanie
Kabel zasilający rozdzielnicę techniczną TK-1 (wentylacja i klimatyzacja). Moc przyłączona 60 kW, współczynnik jednoczesności 0,75, obciążenie obliczeniowe 45 kW, prąd obliczeniowy 70,6 A przy cos φ = 0,92. Wybrano kabel 5×35 mm² Cu, zabezpieczenie 80 A. Ograniczeniem jest obciążalność prądowa po korekcji, nie spadek napięcia. Model i producent: do potwierdzenia.

## 2. Parametry projektowe
| Parametr | Wartość | Jednostka | Źródło |
|---|---|---|---|
| Moc przyłączona TK-1 | 60 | kW | bilans mocy, rew. B (przykład) |
| Współczynnik jednoczesności | 0,75 | – | założenie projektowe (do potwierdzenia) |
| Obciążenie obliczeniowe | 45 | kW | `electrical_calc.py diversity --load-kw 60 --factor 0.75` |
| cos φ | 0,92 | – | dane odbiorników (silniki z falownikami) |
| Napięcie / układ | 400 / TN-S | V | warunki przyłączenia (przykład) |
| Prąd obliczeniowy Ib | 70,6 | A | `electrical_calc.py load-current --power-kw 45 --voltage 400 --cos-phi 0.92 --phases 3` |
| Długość trasy | 90 | m | trasa w korytku kablowym (przykład) |
| Zapas na rozbudowę | 15 | % | oddzielnie od jednoczesności, wymaganie inwestora |

## 3. Obliczenia
| Pozycja | Wartość | Jednostka | Źródło / komentarz |
|---|---|---|---|
| Spadek napięcia, 35 mm², cos φ 0,92 | 6,85 (1,71 %) | V | `electrical_calc.py cable-drop --section-mm2 35` |
| Wymagany przekrój od spadku napięcia, limit 5 % | 11,39 → 16 | mm² | `cable-drop --max-drop-percent 5 --size` (reaktancja pominięta) |
| Obciążalność 35 mm², sposób C (korytko) | 110 | A | tabela producenta kabla, do potwierdzenia |
| Korekcja: temperatura 40 °C 0,87 × zgrupowanie 3 obwody 0,90 | 0,783 | – | `electrical_calc.py correction --iz 110 --factor 0.87 --factor 0.90` |
| Obciążalność po korekcji Iz | 86,1 | A | powyżej |
| Zestawienie | Ib 70,6 ≤ In 80 ≤ Iz 86,1 | A | warunek spełniony |
| Zs dla Ia = 480 A (charakterystyka MCCB, czas 0,4 s) | 0,455 | Ω | `electrical_calc.py zs-max --u0 230 --ia-a 480`, do porównania z Zs obwodu |

Spadek napięcia 1,71 % jest poniżej limitu 5 %. Przekrój 16 mm² spełniałby spadek napięcia, ale nie obciążalność: 16 mm² (sposób C) po korekcji daje ok. 59 A, poniżej zabezpieczenia 80 A. Dlatego wybrano 35 mm². Zapasu procentowego na obciążalność nie dodano — korekcja jest zapasem.

## 4. Wymagania
| Wymaganie | Wartość | Źródło |
|---|---|---|
| Zabezpieczenie nadprądowe | MCCB 3P, 80 A, nastawa zwarciowa do potwierdzenia | obliczenia, dobór do potwierdzenia |
| Odporność zwarciowa | prąd zwarciowy z warunków przyłączenia, do potwierdzenia | warunki przyłączenia |
| Reakcja na ogień kabla | klasa wg PN-EN 50575, wymagana dla trasy w budynku | PN-EN 50575, klasa do ustalenia z projektem |
| Ochrona przeciwprzepięciowa | SPD typu 2 w TK-1 | ocena ryzyka wg PN-EN 62305 |
| Uziemienie | przewód ochronny w kablu, Zs ≤ 0,455 Ω, do zmierzenia | PN-HD 60364 |
| Rozdzielnica | obudowa IP wymagana dla pomieszczenia, Icw od prądu zwarciowego | PN-EN 61439, do potwierdzenia |
| Ekoprojekt (odbiorniki) | silniki i napędy wg Rozporządzenia (UE) 2019/1781 | EUR-Lex |

## 5. Wybrane urządzenie / wyrób
| Pozycja | Wartość |
|---|---|
| Kabel | 5×35 mm² Cu, 0,6/1 kV, klasa reakcji na ogień do ustalenia |
| Producent / typ | do wybrania |
| Obciążalność z karty producenta | do potwierdzenia: ≥ 110 A w sposobie C |
| Zabezpieczenie | do wybrania: MCCB 80 A, Icu ≥ prąd zwarciowy |
| Źródło danych | brak; potrzebna karta katalogowa kabla i aparatu |

## 6. Alternatywy
| Opcja | Układ | Różnica | Kompromis |
|---|---|---|---|
| A | 5×35 mm² Cu, MCCB 80 A, jedna trasa 90 m | spełnia oba warunki | większy przekrój niż od spadku napięcia |
| B | 4×16 mm² Cu + żyła PE, zabezpieczenie 63 A | mniejszy kabel i aparat | brak rezerwy na rozbudowę, większe spadki przy wzroście obciążenia |
| C | 2 równoległe kable 5×16 mm² | mniejszy przekrój jednego kabla | dwa kable, większa liczba zabezpieczeń i miejsca |

## 7. Założenia
- Współczynnik jednoczesności 0,75 przyjęty przez projektanta; do potwierdzenia z bilansem mocy.
- Temperatura otoczenia 40 °C i zgrupowanie 3 obwodów w korytku przyjęte; współczynniki z tabeli PN-HD 60364-5-52 do potwierdzenia.
- Rezystywność miedzi 0,0225 Ω·mm²/m (temperatura pracy), reaktancja 0,08 Ω/km przyjęte.
- Brak danych prądu zwarciowego z warunków przyłączenia, stąd „do weryfikacji" dla Icu i Icw.

## 8. Źródła
- PN-HD 60364 (instalacje niskiego napięcia) i PN-HD 60364-5-52 (dobór przewodów): numery i wydania do potwierdzenia w PKN.
- PN-EN 50575, PN-EN 61439, PN-EN 62305: do potwierdzenia w PKN.
- Rozporządzenie Komisji (UE) 2019/1781 (silniki i napędy), eur-lex.europa.eu.
- Obliczenia: `scripts/electrical_calc.py`.

## 9. Do weryfikacji
- [ ] Prąd zwarciowy i moc zwarciowa z warunków przyłączenia (dobór Icu, Icw).
- [ ] Współczynniki korekcji z tabeli PN-HD 60364-5-52 dla rzeczywistego sposobu ułożenia.
- [ ] Obciążalność 35 mm² z karty producenta dla sposobu C.
- [ ] Zs obwodu i czas wyłączenia wg PN-HD 60364 (zabezpieczenie i charakterystyka).
- [ ] Klasa reakcji na ogień kabla wymagana przepisami dla tej trasy.
- [ ] Współczynnik jednoczesności i zapas na rozbudowę z inwestorem.
- [ ] Dobór SPD i ocena ryzyka wg PN-EN 62305.

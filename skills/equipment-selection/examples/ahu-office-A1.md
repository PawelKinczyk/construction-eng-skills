# Karta doboru: A1 centrala wentylacyjna nawiewno-wywiewna, biura

Projekt: Biurowiec Zabłocie B2 (2026-014), przykład fikcyjny   Data: 2026-10-12   Przygotował: agent, do weryfikacji przez projektanta
Status: wersja robocza do weryfikacji

## 1. Podsumowanie
Centrala nawiewno-wywiewna z odzyskiem ciepła obrotowym dla biur, kondygnacje 1-6. Strumienie: 2400 m³/h nawiew i 2400 m³/h wywiew. Opór zewnętrzny (ESP) 250 Pa na stronie nawiewu i 250 Pa na stronie wywiewu, z zapasem 15 % na każdej stronie. Model nie wybrany: brak danych katalogowych. Punkt sporny: zgodność SFPint wymaga deklaracji producenta.

## 2. Parametry projektowe
| Parametr | Wartość | Jednostka | Źródło |
|---|---|---|---|
| Strumień nawiewu / wywiewu | 2400 / 2400 | m³/h | 80 osób × 30 m³/h·os. (założenie z WT, do potwierdzenia) |
| Kontrola strumienia od obciążenia cieplnego | 4462 | m³/h | `hvac_calc.py air-flow --load-kw 12 --dt 8`; większe niż strumień higieniczny, więc o chłodzeniu decyduje klimatyzacja |
| ESP, strona nawiewu | 250 | Pa | obliczenie instalacji, rew. P02 |
| ESP, strona wywiewu | 250 | Pa | obliczenie instalacji, rew. P02 |
| Sprawność odzysku ciepła | 78 | % (sucha) | **do potwierdzenia: WT, załącznik nr 2, klauzula** |
| Filtry | nawiew ISO 16890 ≥ ePM1 50 %, wywiew ≥ ISO coarse 60 % | klasa | założenie projektowe, do potwierdzenia |
| Nagrzewnica / chłodnica | do potwierdzenia: moc z bilansu cieplnego pomieszczeń | kW | obliczenia OZC, rew. B |
| Wymagany czas pracy | 12 h/d, 250 d/rok | – | wymaganie inwestora (przykład) |

## 3. Obliczenia
| Pozycja | Wartość | Jednostka | Źródło / komentarz |
|---|---|---|---|
| ESP z zapasem, strona nawiewu | 287,5 | Pa | `hvac_calc.py margin --value 250 --percent 15` |
| Moc wentylatora nawiewu, 2400 m³/h przy 287,5 Pa, η = 0,60 | 0,320 (SFP 0,480) | kW (kW/(m³/s)) | `hvac_calc.py fan-power --flow-m3h 2400 --dp-pa 288 --eff 0.6` |
| Moc wentylatora wywiewu, analogicznie | ~0,320 (SFP 0,480) | kW | przyjęto symetrię; do potwierdzenia po doborze |
| SFP centrali (suma obu wentylatorów) | ~0,96 | kW/(m³/s) | suma powyżej, przy założonej sprawności 0,60 |
| Opór przewodu głównego 500×300, 30 m, ζ = 3 | 54,5 (0,63 Pa/m) | Pa | `hvac_calc.py duct-dp --a-mm 500 --b-mm 300 --length-m 30 --zeta 3` |
| Prędkość w przewodzie głównym | 4,44 | m/s | powyżej, w zakresie 4-6 m/s dla biur |

Zapas 15 % zastosowano raz, tylko na ESP, z powodu niepewności oporów kształtek i tłumików. Nie dodano zapasu na strumień: różnicę pokrywa nieszczelność instalacji liczona wg EN 16798-3, nie procent. Sprawność 0,60 przyjęta jako całkowita dla wentylatora z silnikiem; do zastąpienia wartością z karty producenta.

## 4. Wymagania
| Wymaganie | Wartość | Źródło |
|---|---|---|
| Ekoprojekt central | SFPint wg etapu 2018 | Rozporządzenie (UE) nr 1253/2014, EUR-Lex. Do weryfikacji: aktualne brzmienie i wartość dopuszczalna |
| Silniki i napędy | klasa sprawności wg ekoprojektu | Rozporządzenie (UE) 2019/1781, EUR-Lex |
| Sprawność odzysku ciepła | 78 % (sucha) | WT, załącznik nr 2 (do odczytania z ISAP) |
| Klapy ppoż. i odporność przewodów | klasa wg przejść przez oddzielenia ppoż. | WT, dział VI; PN-EN 15650 (wyrób). Zgodność sprawdzić w `code-compliance` |
| Izolacja przewodów | grubość wg tabeli | WT, załącznik nr 2 (do odczytania z ISAP) |
| Higiena | dostęp do filtrów i czyszczenie, klasa filtrów | projekt (wymaganie inwestora), VDI 6022 tylko gdy wymagane |
| Akustyka | do potwierdzenia: poziom w pomieszczeniu i przy granicy działki | wymaganie inwestora / WT |
| Sterowanie | sterownik zintegrowany, Modbus RTU do BMS | wytyczne BMS (przykład) |
| Lokalizacja i dostęp | dach, wymiary transportowe i serwisowe | projekt architektury, do potwierdzenia |

## 5. Wybrane urządzenie
| Pozycja | Wartość |
|---|---|
| Producent / model | do wybrania |
| Punkt pracy | do sprawdzenia: 2400 m³/h przy 287,5 Pa po każdej stronie, w zakresie regulacji |
| SFPint z deklaracji | do sprawdzenia: zgodność z Rozp. (UE) 1253/2014 |
| Moc pobierana | do sprawdzenia (przyjęto ~0,64 kW dla obu wentylatorów) |
| Filtry | nawiew ePM1 50 %, wywiew coarse 60 %, do potwierdzenia |
| Wymiary / masa / przyłącza | do sprawdzenia z transportem na dach |
| Źródło danych | brak; potrzebna karta katalogowa, rew. i data |

## 6. Alternatywy
| Opcja | Model | Różnica | Kompromis |
|---|---|---|---|
| A | odzysk obrotowy, sprawność sucha 78 % | wysoka sprawność, wilgoć przenoszona | możliwe przenoszenie zapachów między nawiewem i wywiewem |
| B | odzysk przeciwprądowy płytowy, sprawność 70-75 % | brak przenoszenia zanieczyszczeń | niższa sprawność, większy opór, ryzyko szronu |
| C | dwa odzyski z obejściem (bypass) na chłodzenie nocne | mniejsze zużycie energii w lecie | wyższy koszt, więcej miejsca |

## 7. Założenia
- 30 m³/h na osobę dla biur przyjęte jako strumień higieniczny; wymaganie z WT do odczytania z tekstu jednolitego.
- Sprawność wentylatorów 0,60 i symetria obu stron przyjęte.
- Opory kształtek i tłumików ujęte w ζ = 3 dla przewodu głównego i w zapasie 15 % na ESP.
- Filtry, mocę nagrzewnicy i chłodnicy oraz poziomy akustyczne przyjęto roboczo.

## 8. Źródła
- Rozporządzenie Komisji (UE) nr 1253/2014 (centrale wentylacyjne), eur-lex.europa.eu.
- Rozporządzenie Komisji (UE) 2019/1781 (silniki i napędy), eur-lex.europa.eu.
- Rozporządzenie w sprawie warunków technicznych: tekst jednolity, isap.sejm.gov.pl (załącznik nr 1 i nr 2, do odczytania).
- PN-EN 16798-3, PN-EN 13053, ISO 16890, PN-EN 15650: numery i wydania do potwierdzenia w PKN.
- Obliczenia: `scripts/hvac_calc.py`.

## 9. Do weryfikacji
- [ ] Strumień higieniczny i sprawność odzysku: wartości z WT (załącznik nr 2) odczytane z ISAP.
- [ ] SFPint producenta i zgodność z Rozp. (UE) 1253/2014 dla tego etapu.
- [ ] Moce nagrzewnicy i chłodnicy z bilansu cieplnego oraz warunki zewnętrzne projektowe.
- [ ] Klasy filtrów i dostęp serwisowy; wpływ filtrów na opór końcowy.
- [ ] Poziomy akustyczne w pomieszczeniach i przy granicy działki.
- [ ] Wymiary, masa i droga transportu na dach; obciążenie dachu z konstruktorem.
- [ ] Klapy ppoż. i klasa odporności ogniowej przewodów na przejściach.

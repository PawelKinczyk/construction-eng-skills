# Analiza DXF: liczba klimakonwektorów i porównanie rewizji, arkusz A-101

Przykład fikcyjny pokazujący format i wynik działania skryptu. Pliki, wartości i numery są wymyślone. Skrypt: `scripts/dxf_report.py` (wymaga `ezdxf`).

## 1. Podsumowanie
Pliki: `A-101_revB.dxf` (2026-10-05) i `A-101_revC.dxf` (2026-10-09), instalacje sanitarne, model space.
Jednostki: metry (`$INSUNITS` = 6). Zasięg rew. C: 30,0 × 20,0 m; w rew. B rozciągnięty do 900 × 900 m przez jedną linię poza obszarem rysunku.
Wynik: **4 klimakonwektory typu FCU-4PIPE w rew. C** (3 w rew. B). Różnica: dodany FCU-04.
Uwaga: policzono wstawienia bloków, nie symbole widoczne na wydruku. Etykieta FCU-03 ma puste pole przepływu.

## 2. Warunki odczytu
| Parametr | Wartość | Źródło |
|---|---|---|
| Plik | A-101_revC.dxf | plik |
| Narzędzie | ezdxf 1.4.4 | `dxf_report.py` |
| Jednostki rysunku | metry (`$INSUNITS` = 6) | nagłówek pliku |
| Zasięg | 30,0 × 20,0 m | `dxf_report.py summary` |
| Zakres zliczania | model space; paper space raportowany osobno | skrypt |
| Bloki anonimowe | 0 (wymiary i kreskowania nie występują w tym pliku) | skrypt |
| Xrefy | brak | skrypt |
| Obiekty proxy | 0 | skrypt |

## 3. Warstwy
| Warstwa | Liczba obiektów | Stan | Zgodność ze standardem |
|---|---|---|---|
| S-PIPE-WC | 4 | włączona | do sprawdzenia w `project-standards` |
| A-WALL | 1 | włączona | do sprawdzenia |
| A-TEXT | 1 | włączona | do sprawdzenia |
| 0 | 0 | włączona | warstwa domyślna, pusta — OK |
| Defpoints | 0 | włączona | warstwa systemowa, pusta — OK |

## 4. Bloki i atrybuty
| Blok | Liczba wstawień | Warstwy | Znaczniki atrybutów |
|---|---|---|---|
| FCU-4PIPE | 4 | S-PIPE-WC | TAG, FLOW |

| Blok | Warstwa | Pozycja [m] | TAG | FLOW |
|---|---|---|---|---|
| FCU-4PIPE | S-PIPE-WC | 5,0 / 4,0 | FCU-01 | 450 |
| FCU-4PIPE | S-PIPE-WC | 9,0 / 4,0 | FCU-02 | 450 |
| FCU-4PIPE | S-PIPE-WC | 13,0 / 4,0 | FCU-03 | **(puste)** |
| FCU-4PIPE | S-PIPE-WC | 17,0 / 4,0 | FCU-04 | 600 |

Pole FLOW w FCU-03 jest puste w pliku. Do zestawienia klimakonwektorów potrzebne jest uzupełnienie w projekcie — nie wolno go przyjąć z sąsiedniego urządzenia.

## 5. Teksty na warstwach
| Tekst | Warstwa | Pozycja [m] | Wartość znaczenia |
|---|---|---|---|
| WENTYLACJA MECHANICZNA BIUR | A-TEXT | 1,0 / 18,0 | opis zakresu arkusza |

## 6. Porównanie rewizji (rew. B → rew. C)
Baza porównania: zawartość plików, model space. Bez paper space i bez xrefów.

```
== DXF comparison ==  A-101_revB.dxf -> A-101_revC.dxf
units: metres (code 6) -> metres (code 6)
extents old: min [0,0] max [900,900]  size [900,900]
extents new: min [0,0] max [30,20]    size [30,20]

Layers added (0): -
Layers removed (0): -
Layer entity count changes (2):
  A-WALL        2 -> 1
  S-PIPE-WC     3 -> 4
Blocks added (0): -
Blocks removed (0): -
Block count changes (1):
  FCU-4PIPE     3 -> 4
Entity type changes (2):
  INSERT        3 -> 4
  LINE          1 -> 0
```

Interpretacja do potwierdzenia przez projektanta:
| Zmiana w pliku | Prawdopodobne znaczenie | Wymaga odczytu rysunku |
|---|---|---|
| FCU-4PIPE 3 → 4 | dodany klimakonwektor FCU-04, przepływ 600 m³/h | tak — potwierdzić w zestawieniu |
| LINE 1 → 0, zasięg 900 → 30 m | usunięta linia konstrukcyjna poza obszarem rysunku | nie — to nie jest zmiana projektowa |
| S-PIPE-WC 3 → 4 | nowy klimakonwektor na warstwie instalacji | tak |

Zmiany liczby obiektów nie mówią, co się zmieniło projektowo. Wiersz z linią konstrukcyjną jest tego przykładem: liczba zmieniła się, projekt nie.

## 7. Do weryfikacji
- [ ] Zestawienie klimakonwektorów: potwierdzić 4 sztuki i typy z rysunków i z projektu.
- [ ] FCU-03: uzupełnić przepływ w projekcie.
- [ ] Zgodność nazw warstw i bloków ze standardem projektu — `project-standards`.
- [ ] Czy plik rew. B zawiera inne elementy poza obszarem rysunku (poza jedną linią).
- [ ] Jednostki: potwierdzić, że projekt prowadzony jest w metrach (zgodnie z konwencją w `PROJECT.md`).
- [ ] Liczby nie są podstawą zamówienia ani wyceny — przekazać do `equipment-selection` i `cost-estimate` po potwierdzeniu.

## 8. Źródła
- Pliki DXF A-101 rew. B i rew. C (przykład fikcyjny).
- Narzędzie i wersja: `ezdxf` 1.4.4, skrypt `scripts/dxf_report.py`.
- Standard warstw i bloków: `PROJECT.md` → `project-standards`.
- Skrypt tylko czyta pliki; nie modyfikuje, nie czyści i nie zapisuje plików użytkownika.

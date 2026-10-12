# Analiza IFC: liczby elementów, ilości i kontrola wymagań, model rew. C

Przykład fikcyjny pokazujący format i wynik działania skryptu. Model zbudowany na potrzeby przykładu; wartości i GUID-y nie są z żadnego realnego projektu. Skrypt: `scripts/ifc_report.py` (wymaga `ifcopenshell`).

## 1. Podsumowanie
Plik: `model_revC.ifc`, schemat IFC4, narzędzie ifcopenshell 0.9.0.
Jednostki: długość **milimetry** (MILLI METRE), powierzchnia m², objętość m³ — uwaga: ilości w pliku są w milimetrach, nie w metrach.
Kondygnacje: 1 (`Level 1`). Elementy: 8 produktów, 0 przestrzeni (`IfcSpace`).
Znaleziska: brak jakichkolwiek przestrzeni (analiza per pomieszczenie niemożliwa); 1 pompa bez mocy znamionowej; 3 elementy (Site, Building, Storey) nieprzypisane do kondygnacji, co jest normalne dla struktury, ale musi być świadome w zestawieniach per kondygnacja.

## 2. Liczby elementów
| Typ | Liczba | Uwaga |
|---|---|---|
| IfcPump | 3 | występowania, nie obiekty typu |
| IfcWall | 1 | – |
| IfcAirTerminal | 1 | – |
| IfcSite / IfcBuilding / IfcBuildingStorey | 1 / 1 / 1 | struktura przestrzenna |

```
Level 1: IfcPump 3, IfcWall 1, IfcAirTerminal 1
(not assigned): IfcBuilding 1, IfcBuildingStorey 1, IfcSite 1
```

Liczby to występowania (`IfcPump`), nie obiekty typu (`IfcPumpType`). Nie sumować jednych z drugimi.

## 3. Ilości z modelu
| Element | GUID | Kondygnacja | Zbiór ilości | Ilość | Wartość | Jednostka |
|---|---|---|---|---|---|---|
| W1 (IfcWall) | 31fYQR3i95g98D0GIoVz8i | Level 1 | Qto_WallBaseQuantities | Length | 6,0 | mm (jak w modelu) |
| W1 | jak wyżej | Level 1 | Qto_WallBaseQuantities | Height | 3,0 | mm |
| W1 | jak wyżej | Level 1 | Qto_WallBaseQuantities | Width | 0,25 | mm |
| W1 | jak wyżej | Level 1 | Qto_WallBaseQuantities | NetVolume | 3,2 | m³ wg deklaracji jednostki objętości |

Każda wartość podana ze zbiorem ilości i nazwą ilości — bez tego nie da się jej sprawdzić. Zbiór `Qto_WallBaseQuantities` jest jedynym zbiorem ilości w modelu: pompy i nawiewnik nie mają żadnego `IfcElementQuantity`, więc ich ilości nie są zerowe, tylko nieobecne.

Uwaga o jednostkach: wartość `NetVolume` = 3,2 pochodzi z deklaracji objętości w m³, natomiast wymiary liniowe (6,0 i 3,0) są w milimetrach zgodnie z deklaracją długości. Przed użyciem w wycenie przeliczyć spójnie i pokazać współczynnik.

## 4. Zestawienie pomp
| GUID | Nazwa | Kondygnacja | Reference | RatedPower [kW] |
|---|---|---|---|---|
| 2quGbbHXL6hOX_kgp0DNW3 | P-01 | Level 1 | P-01 | 5,5 |
| 3XP6CWv7nCK9fcN824kxg6 | P-02 | Level 1 | P-02 | 11,0 |
| 22n5wYAH5E0uBsN6hqiqfZ | P-03 | Level 1 | P-03 | **(puste)** |

Eksport: `ifc_report.py schedule --type IfcPump --props Reference,RatedPower`.
Pole `Tag` jest puste we wszystkich pompach — znacznik (`Tag`) jest używany w zestawieniach odbiorczych, więc to znalezisko, nie kosmetyka.

## 5. Kontrola wymagań
Wymagania z pliku `requirements.json` (lista projektowa, nie IDS — IDS nie został uruchomiony):

| Reguła | Liczba naruszeń | Opis |
|---|---|---|
| Pset_PumpTypeCommon.RatedPower | 1 | brak wartości (puste pole) w P-03 |
| IfcValve | 1 | typu `IfcValve` nie ma w modelu, choć wymagany |

Wynik grupowany po regule, nie tylko po elemencie: projektant modelu poprawia regułę, nie pojedynczy element.

## 6. Porównanie rewizji B → C
```
products: 7 -> 8
added: 8   removed: 7   changed properties: 0
```

Wynik jest **nieużyteczny jako porównanie projektowe** i właśnie dlatego jest tu pokazany: oba pliki pochodzą z niezależnych eksportów, więc wszystkie GUID-y są nowe. Model widzi 7 elementów usuniętych i 8 dodanych, mimo że jedyną realną zmianą jest dodanie pompy P-03.

Wniosek do raportu: porównanie po GUID ma sens tylko dla tego samego modelu pochodzącego z tego samego narzędzia i z zachowaniem GUID-ów. W innym wypadku porównywać należy po atrybutach (typ + nazwa + kondygnacja) i tak to zaznaczyć.

## 7. Znaleziska modelu
| Znalezisko | Waga | Uwaga |
|---|---|---|
| Brak `IfcSpace` | wysoka | analizy per pomieszczenie i ilości pomieszczeniowe niemożliwe |
| `Tag` puste na wszystkich pompach | średnia | zestawienia odbiorcze i etykietowanie |
| Brak `IfcElementQuantity` na pompach i nawiewniku | średnia | brak ilości w modelu; nie wolno przyjmować zera |
| Jednostka długości w milimetrach | średnia | ryzyko przeliczenia; podać jednostkę w każdym zestawieniu |
| Elementy bez przypisania do kondygnacji | niska | dotyczy Site, Building, Storey — normalne, ale do świadomego wyłączenia w zestawieniach |

## 8. Do weryfikacji
- [ ] P-03: uzupełnić moc znamionową w modelu i w projekcie.
- [ ] `Tag` na urządzeniach: ustalić konwencję z projektem i uzupełnić w modelu.
- [ ] Jednostki: potwierdzić z modelerem, że długość w milimetrach jest zamierzona.
- [ ] Brak przestrzeni: czy model ma zawierać `IfcSpace` (wymaganie BEP).
- [ ] `IfcValve`: czy wymaganie dotyczy tego modelu (zakres eksportu).
- [ ] Ilości nie są podstawą zamówienia ani wyceny — po potwierdzeniu przekazać do `cost-estimate` i `equipment-selection`.
- [ ] Kontrola wymagań to lista projektowa, nie wynik IDS; jeżeli projekt wymaga IDS, uruchomić `ifc_report.py ids --spec <plik>` (wymaga `ifctester`).

## 9. Źródła
- Model: `model_revC.ifc` (przykład fikcyjny), schemat IFC4.
- Narzędzie: ifcopenshell 0.9.0, skrypt `scripts/ifc_report.py`.
- Wymagania: `requirements.json` (lista projektowa, przykład).
- Wymagania modelu: `PROJECT.md` → `project-standards` (BEP / wymagania informacyjne zamawiającego).
- Skrypt tylko czyta model; nie edytuje, nie naprawia i nie eksportuje ponownie plików użytkownika.

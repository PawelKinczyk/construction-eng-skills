# Rejestr rysunków i porównanie rewizji: pakiet sanitarny, rew. B i C

Przykład fikcyjny pokazujący format i wynik działania skryptu. Nazwy plików, numery arkuszy i daty są wymyślone. Skrypt: `scripts/pdf_register.py`, reguły: `rules.json` projektu.

## 1. Podsumowanie
Zakres: pakiet instalacji sanitarnych, wydanie rew. B (2026-10-05) i rew. C (2026-10-09), 6 arkuszy w każdym wydaniu.
Wynik porównania: dodany arkusz S-203 (kanalizacja deszczowa), usunięty arkusz S-202 (przeniesiony do pakietu drogowego), 2 arkusze ze zmienioną rewizją (S-201, S-204).
Problemy w metrykach: 1 arkusz bez pola status, 1 plik z nazwą niezgodną z numerem arkusza w metryce.
Wszystkie arkusze wektorowe (tekst czytelny). Ekstrakcja: `pypdf`.

## 2. Rejestr arkuszy (wydanie rew. C)
| Nr arkusza | Tytuł | Dyscyplina | Rew | Status | Data | Skala | Format | Plik | Uwaga |
|---|---|---|---|---|---|---|---|---|---|
| S-201 | Rzut parteru, instalacje sanitarne | S | C | S3 | 09.10.2026 | 1:50 | A1 | S-201_revC.pdf | zmiana wobec rew. B |
| S-202 | — | S | — | — | — | — | — | — | **usunięty w rew. C**, zakres do pakietu drogowego |
| S-203 | Kanalizacja deszczowa, rzut dachu | S | A | S1 | 09.10.2026 | 1:100 | A1 | S-203_revA.pdf | **nowy w rew. C** |
| S-204 | Węzeł c.w.u., schemat | S | C | S3 | 09.10.2026 | NTS | A3 | S-204_revC.pdf | zmiana wobec rew. B |
| S-205 | Zestawienie przyborów i zaworów | S | B | S3 | 05.10.2026 | NTS | A3 | S-205_revB.pdf | bez zmian |
| S-206 | Profil kanalizacji, osie A-C | S | B | — | 05.10.2026 | 1:50 | A1 | profil_kanalizacji_osie_AC.pdf | **brak pola status w metryce**; nazwa pliku niezgodna z numerem arkusza |

Wiersze pochodzą z wyniku skryptu: `pdf_register.py scan --dir drawings --recursive --rules rules.json --csv register-revC.csv`.

## 3. Dane wyciągnięte z arkuszy
| Wartość | Arkusz | Rew | Miejsce odczytu |
|---|---|---|---|
| Średnica przewodu głównego kanalizacji deszczowej dn160 | S-203 | A | tabelka na rzucie dachu, lewy górny róg |
| Wydajność węzła c.w.u. 60 kW | S-204 | C | metryka schematu, pole „moc" |
| Liczba przyborów: 128 (umywalki 62, WC 40, natryski 26) | S-205 | B | zestawienie, kolumna „ilość" |

Wartości odczytane z plików wektorowych. Wartości z arkuszy skanowanych oznaczyć jako odczyt wizualny i poprosić o potwierdzenie.

## 4. Porównanie rewizji (rew. B → rew. C)
Baza porównania: kod rewizji i pole statusu z metryki, potwierdzone otwarciem arkusza.

```
== Register comparison ==  register-revB.csv -> register-revC.csv
Added (1): S-203
Removed (1): S-202
Changed (1):
  S-201   rev: 'B' -> 'C'; status: 'S2' -> 'S3'; date: '05.10.2026' -> '09.10.2026'
  S-204   rev: 'B' -> 'C'; status: 'S2' -> 'S3'; date: '05.10.2026' -> '09.10.2026'
```

Zmiany w treści (po otwarciu obu rewizji, do uzupełnienia przez projektanta):
| Arkusz | Co się zmieniło | Zakres nieporównany |
|---|---|---|
| S-201 | zmiana trasy pionu W2 w osi B; nowa średnica dn63 | instalacja w pomieszczeniach 1.04-1.06 nie porównana (skan) |
| S-204 | dodany zawór równoważący na powrocie; zmieniony schemat węzła | cały arkusz porównany |
| S-203 | arkusz nowy: kanalizacja deszczowa, dn160 | – |

Uwaga: sam kod rewizji nie mówi, co się zmieniło. Wiersze w tabeli pochodzą z porównania arkuszy, nie z rejestru.

## 5. Kontrola kompletności pakietu
Wymagana lista arkuszy: **nie przekazana**, więc kompletności nie oceniano. Poniżej stan pakietu.

| Kontrola | Wynik |
|---|---|
| Liczba arkuszy w pakiecie | 6 |
| Arkusze z aktualną rewizją | 5 z 6 (S-205 w rew. B, wydane wcześniej — potwierdzić, czy obowiązuje) |
| Arkusze przestarzałe w pakiecie | brak |
| Pola metryki kompletne | 5 z 6 (S-206 bez statusu) |
| Nazwy plików zgodne ze standardem projektu | 5 z 6 (`profil_kanalizacji_osie_AC.pdf` niezgodna) |
| Zgodność listy przewodniej z zawartością folderu | do sprawdzenia po otrzymaniu listy przewodniej |

## 6. Do weryfikacji
- [ ] S-202: potwierdzić u zamawiającego, że zakres przeniesiono do pakietu drogowego.
- [ ] S-206: brak pola status w metryce; nazwa pliku niezgodna z numerem arkusza — poprawka po stronie biura projektowego.
- [ ] S-205: czy rew. B jest aktualna dla tego wydania.
- [ ] Treść zmian na S-201 w pomieszczeniach 1.04-1.06 (obszar nieporównany).
- [ ] Wymagana lista arkuszy do oceny kompletności pakietu.

## 7. Źródła
- Pliki PDF pakietu instalacji sanitarnych, wydania rew. B i rew. C (przykład fikcyjny).
- Reguły odczytu metryki: `rules.json` projektu (przykład).
- Rejestr: `pdf_register.py scan`, porównanie: `pdf_register.py compare`.
- Standard nazewnictwa i kodów rewizji: `PROJECT.md` → `project-standards` (ISO 19650 albo BEP projektu).
- Skrypt nie zmienia, nie zmienia nazw i nie zapisuje plików rysunków — praca wyłącznie na odczycie.

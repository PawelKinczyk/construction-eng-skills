# Lista usterek: skrzydło A, poziom 0, przegląd przed odbiorem

Przykład fikcyjny pokazujący format i wynik działania skryptu. Projekt, usterki, osoby i terminy są wymyślone. Rejestr: `punch.json` (przykład).

Stan na dzień: 2026-10-16 (przegląd 2026-10-12; zamknięcie U-001 w tym samym rejestrze 2026-10-16). Liczby zgodne z `punch_list.py summary --date 2026-10-16`.

## 1. Podsumowanie
Zakres przeglądu: skrzydło A, poziom 0, pomieszczenia 1.01-1.06 oraz korytarz. Data przeglądu: 2026-10-12, zgłoszenie B2-SV-007.
Wynik: 6 pozycji — 4 otwarte, 1 w toku, 1 zamknięta. Zaległe: 1 (U-003, sanitarne, 7 dni). Bez zdjęcia: 1 (U-006). Bez odpowiedzialnego: 1 (U-005, do ustalenia z umowy).
Odbiór częściowy 2026-10-26: blokują pozycje U-002 i U-003 (waga B, otwarte; U-001 zamknięta 2026-10-16).

## 2. Widok roboczy (wg branż)

### Sanitarne — 3 pozycje
| ID | Lokalizacja | Element | Opis | Waga | Zdjęcie | Odpowiedzialny | Termin | Status |
|---|---|---|---|---|---|---|---|---|
| U-001 | skrz. A, poz. 0, pom. 1.04 | izolacja przewodu c.w.u. | Izolacja zakończona 300 mm przed zaworem odcinającym | B | SV-007/4-5 | Wykonawca / M. Lis | 2026-10-15 | zamknięta |
| U-003 | skrz. A, poz. 0, korytarz | przewód kanalizacji | Przewód podwieszony w odległości 1,45 m od płyty stropowej | B | SV-007/6 | Wykonawca / P. Zieliński | 2026-10-09 | **otwarta, zaległa 7 dni** |
| U-004 | skrz. A, poz. 0, pom. 1.02 | otulina kolana | Otulina przewężona opaską na kolanie c.w.u. | C | SV-007/7 | Wykonawca / M. Lis | 2026-10-24 | w toku |

Wymaganie dla U-003: specyfikacja techniczna, tom 3, p. 4.7 (maksymalny rozstaw podwieszeń przewodu dn110). Wymaganie dla U-001 i U-004: instrukcja producenta otuliny, p. 3 (izolacja ciągła na całej długości, bez przewężeń).

### Elektryczne — 2 pozycje
| ID | Lokalizacja | Element | Opis | Waga | Zdjęcie | Odpowiedzialny | Termin | Status |
|---|---|---|---|---|---|---|---|---|
| U-002 | skrz. A, poz. 0, pom. 1.05 | oprawa oświetleniowa | Oprawa nie działa po próbie napięciowej | B | SV-007/8 | Wykonawca elektryczny / R. Kmita | 2026-10-20 | otwarta |
| U-006 | skrz. A, poz. 0, pom. 1.06 | puszka podtynkowa | Puszka osadzona 8 mm poza licem tynku | C | **brak** | Wykonawca elektryczny / R. Kmita | 2026-10-26 | otwarta |

U-006 bez zdjęcia — uzupełnić przy najbliższej wizycie. Bez zdjęcia pozycja jest pierwsza do zakwestionowania przy odbiorze.

### Ogólnobudowlane — 1 pozycja
| ID | Lokalizacja | Element | Opis | Waga | Zdjęcie | Odpowiedzialny | Termin | Status |
|---|---|---|---|---|---|---|---|---|
| U-005 | skrz. A, poz. 0, pom. 1.01 | tynk wewnętrzny | Rysa skurczowa na ścianie w osi A, długość ok. 400 mm | C | SV-007/9 | **do ustalenia** | 2026-10-26 | otwarta |

U-005: odpowiedzialność do ustalenia z umowy (roboty tynkarskie wykonawcy generalnego czy podwykonawcy). Wpisanie „wykonawca" bez wskazania podmiotu nie jest przypisaniem odpowiedzialności.

## 3. Widok odbiorowy (wg pomieszczeń)
| Pomieszczenie | ID | Branża | Opis | Waga | Status |
|---|---|---|---|---|---|
| 1.01 | U-005 | ogólnobudowlane | Rysa skurczowa, oś A | C | otwarta |
| 1.02 | U-004 | sanitarne | Otulina przewężona na kolanie | C | w toku |
| 1.04 | U-001 | sanitarne | Izolacja przed zaworem | B | zamknięta |
| 1.05 | U-002 | elektryczne | Oprawa nie działa | B | otwarta |
| 1.06 | U-006 | elektryczne | Puszka poza licem tynku | C | otwarta |
| korytarz | U-003 | sanitarne | Rozstaw podwieszeń przewodu | B | otwarta, zaległa |

Widok wygenerowany: `punch_list.py export --view room`. Do odbioru: podać datę przeglądu, zakres zbadany (skrzydło A, poziom 0) i zakres niezbadany (skrzydło B, poziomy 1-6, dach).

## 4. Zaległe
| ID | Opis | Odpowiedzialny | Termin | Dni po terminie |
|---|---|---|---|---|
| U-003 | Rozstaw podwieszeń przewodu kanalizacji | Wykonawca / P. Zieliński | 2026-10-09 | 7 |

U-003 to pozycja wagi B w kanale widokowym korytarza: opóźnienie blokuje zamknięcie stropu podwieszanego i odbiór częściowy korytarza.

## 5. Rejestr zdjęć
| Zdjęcie | Pozycja | Temat |
|---|---|---|
| SV-007/4, SV-007/5 | U-001 | zakończenie izolacji przed zaworem, ujęcie szerokie i zbliżenie |
| SV-007/6 | U-003 | przewód i podwieszenie na tle płyty stropowej |
| SV-007/7 | U-004 | otulina na kolanie z opaską |
| SV-007/8 | U-002 | oprawa po próbie napięciowej |
| SV-007/9 | U-005 | rysa na ścianie, ujęcie z linijką |
| — | U-006 | brak zdjęcia, do wykonania |

Zamknięcie U-001: zweryfikowane 2026-10-16 przez inspektora (T. Wrona), zamknięte 2026-10-16 z notatką i zdjęciem 23. Weryfikacja nie mogła być wykonana przez M. Lisa — osoba, która usuwa usterkę, nie potwierdza jej usunięcia.

## 6. Kontrola pozycji
| Sprawdzenie | Wynik |
|---|---|
| Pozycje z lokalizacją, branżą, opisem faktu, wagą | 6 z 6 |
| Pozycje z odpowiedzialnym | 5 z 6 (U-005 do ustalenia) |
| Pozycje z terminem | 6 z 6 |
| Pozycje ze zdjęciem | 5 z 6 (U-006 brak) |
| Pozycje z wymaganiem źródłowym | 4 z 6 (U-002 i U-005: opis faktu bez odwołania do tolerancji — do uzupełnienia po sprawdzeniu specyfikacji) |
| Pytania projektowe w liście | brak (osobno do projektanta) |
| Pozycje zamknięte bez weryfikatora | 0 |

## 7. Do weryfikacji
- [ ] U-003: potwierdzić wykonanie i rozstaw podwieszeń pomiarem; termin przekroczony.
- [ ] U-005: ustalić odpowiedzialny podmiot z umowy (wykonawca generalny / podwykonawca tynków).
- [ ] U-006: wykonać zdjęcie, potwierdzić tolerancję lica tynku ze specyfikacją.
- [ ] U-002 i U-005: dopisać wymaganie źródłowe (specyfikacja, punkt) albo pozostawić jako opis faktu.
- [ ] Zakres niezbadany: skrzydło B, poziomy 1-6, dach — dopisać do kolejnego przeglądu.
- [ ] Pozycje otwarte na dzień odbioru 2026-10-26: U-002, U-003, U-005, U-006 — podać plan i terminy w protokole odbioru.

## 8. Uwagi
- Lista jest rejestrem faktów i odpowiedzialności wynikającej z umowy. Nie jest roszczeniem, zawiadomieniem, wyceną ani potwierdzeniem odbioru robót.
- Opisy podają fakt, nie ocenę; tolerancja tylko z podaniem dokumentu i punktu.
- Wszystkie zmiany statusu mają datę i notatkę — to odpowiada na pytanie „kiedy to naprawiono i kto sprawdził".

# Przegląd przetargu: modernizacja instalacji sanitarnej, budynek szpitalny

Przykład fikcyjny pokazujący format. Dokumenty, kwoty, ryzyka i odpowiedzi zamawiającego są wymyślone. Rejestr ryzyk pochodzi z pliku `risks-example.json`, ceny z przykładu `cost-estimate`.

## 1. Podsumowanie
Postępowanie: przetarg nieograniczony, zamówienie publiczne, modernizacja instalacji wodno-kanalizacyjnej w czynnym budynku szpitalnym.
Forma umowy: wzór zamawiającego na podstawie ustawy Pzp, bez wzorca FIDIC/NEC; umowa i SWZ w załączeniu.
Zakres w jednym zdaniu: wymiana pionów wod-kan w 4 skrzydłach, nowy węzeł c.w.u., kanalizacja podposadzkowa, roboty w czynnym obiekcie.
Rekomendacja: **składać ofertę z odstępstwami** — 3 z 6 ryzyk kwantyfikowalnych są nieakceptowalne w obecnym brzmieniu umowy (brak limitu kar, gwarancja 60 miesięcy, obmiar weryfikowany przy zaniżonym przedmiarze).
Trzy największe ryzyka: R3 przedmiar zaniżony przy weryfikowanym obmiarze (186 000 zł), R1 warunki gruntowe (147 000 zł), R2 uzgodnienia z gestorem sieci (90 000 zł).
Pytania do zamawiającego: 5 otwartych. Rekomendacja: złożyć pytania do 2026-10-05, termin ofert 2026-10-20.

## 2. Przegląd zakresu
| Pozycja | Stan | Uwaga |
|---|---|---|
| Piony wod-kan w 4 skrzydłach | do wyceny | ilości z przedmiaru, do kontroli z rzutami rew. S-04 |
| Węzeł c.w.u. z zasobnikiem | do wyceny | zakres i moc do potwierdzenia (PFU p. 4.2) |
| Kanalizacja podposadzkowa | do wyceny | brak rzutu podposadzkowej w zestawie dokumentów — **pytanie 1** |
| Odbudowa wykończeń po wymianie pionów | nie w przedmiarze | **pytanie 2** — kto odtwarza wykończenia |
| Praca w czynnym obiekcie | ujęte w PFU p. 3.2 | ograniczenia godzinowe, dezynfekcja, śluzy |
| Próby, dezynfekcja, odbiory | częściowo w przedmiarze | **pytanie 3** — zakres badań bakteriologicznych |
| Zasilanie placu i media na potrzeby robót | brak w dokumentach | **pytanie 4** |
| Utylizacja odpadów z demontażu | w SWZ p. 5.9 | karty przekazania, opłaty do potwierdzenia |

Sprzeczność znaleziona: przedmiar poz. 2.14 podaje 480 m² izolacji, rysunek S-04 rew. B pozwala obmiarować ok. 640 m². Rozstrzygnięcie zależy od odpowiedzi na pytanie 5; przy obmiarze weryfikowanym (umowa par. 11.3) ryzyko ilości ponosi wykonawca (**R3**).

## 3. Rejestr ryzyk
| # | Ryzyko | Kategoria | Kto ponosi | Skutek | Postępowanie | Kwota w ryzyku [zł] |
|---|---|---|---|---|---|---|
| R3 | Przedmiar zaniżony, obmiar weryfikowany | zakres | wykonawca | 310 000, umowa par. 11.3 | wycena w ryzyku + pytanie 5 | 186 000,00 |
| R1 | Warunki gruntowe gorsze niż w dokumentacji | plac budowy | wykonawca | 420 000, umowa par. 4.2 | wycena w ryzyku, badanie geotechniczne przed ofertą | 147 000,00 |
| R2 | Przedłużenie uzgodnień z gestorem sieci | pozwolenia | zamawiający | 180 000, PFU p. 6.4 | pytanie do zamawiającego | 90 000,00 |
| R4 | Praca w czynnym obiekcie, ograniczenia godzinowe | harmonogram | wykonawca | 95 000, PFU p. 3.2 | wycena w koszcie bezpośrednim | 76 000,00 |
| R5 | Kary umowne bez limitu | umowa | wykonawca | 500 000, umowa par. 15.1 | odstępstwo w ofercie (limit 10 % wartości) | 75 000,00 |
| R6 | Gwarancja 60 miesięcy na urządzenia | umowa | wykonawca | 120 000, SWZ p. 4.7 | potwierdzenie u producentów przed ofertą | 48 000,00 |
| R7 | Zmiana zakresu corrigendum nr 2 | zakres | zamawiający | do skwantyfikowania | do skwantyfikowania po odpowiedzi na pytania | nieujęte |

Suma wartości oczekiwanej: **622 000,00 zł** (`bid_calc.py risk --file risks-example.json`).
R7 nie wchodzi do sumy — brak prawdopodobieństwa i skutku. Zostanie wycenione po odpowiedzi na pytania albo przeniesione do odstępstw.

## 4. Przegląd umowy
| # | Zmiana wobec praktyki rynkowej | Klauzula | Skutek |
|---|---|---|---|
| 1 | Brak limitu kar umownych | umowa par. 15.1 | nieograniczona ekspozycja; żądać limitu 10 % wartości umowy |
| 2 | Gwarancja 60 miesięcy na urządzenia | SWZ p. 4.7 | ponad standard producentów (24-36 miesięcy); potwierdzić u dostawców lub wycenić serwis |
| 3 | Zapłata 60 dni od zatwierdzenia protokołu odbioru | umowa par. 12.4 | finansowanie własne na ok. 3 miesiące; ujęte w cashflow |
| 4 | Zabezpieczenie należytego wykonania 10 % na 60 miesięcy | umowa par. 13.1 | koszt gwarancji przez cały okres gwarancyjny, do kalkulacji |
| 5 | Brak klauzuli waloryzacyjnej przy umowie na 14 miesięcy | umowa par. 12.1 | ryzyko wzrostu cen materiałów po stronie wykonawcy; żądać klauzuli waloryzacyjnej |
| 6 | Obmiar weryfikowany przez zamawiającego | umowa par. 11.3 | ryzyko ilości po stronie wykonawcy, patrz R3 |

## 5. Pytania do zamawiającego (RFI)
| # | Pytanie | Dokument / klauzula | Co zmienia odpowiedź | Termin |
|---|---|---|---|---|
| 1 | Czy zamawiający przekaże rzut kanalizacji podposadzkowej i inwentaryzację istniejącej kanalizacji? | PFU p. 4.5, wykaz załączników | ilość i ryzyko kolizji, R3 | pytać do 2026-10-05 |
| 2 | Kto odtwarza wykończenia (posadzki, glazura, sufity) po wymianie pionów i na jakiej podstawie? | przedmiar, brak pozycji | zakres i cena, ok. 120 000 zł | pytać do 2026-10-05 |
| 3 | Jaki zakres badań bakteriologicznych po robotach i kto je wykonuje? | PFU p. 7.3 | próby i odbiór, R2 | pytać do 2026-10-05 |
| 4 | Czy zasilanie placu budowy i media na potrzeby robót są w naszym zakresie, w którym miejscu? | brak w dokumentach | koszty bezpośrednie | pytać do 2026-10-05 |
| 5 | Który obmiar izolacji jest wiążący: przedmiar poz. 2.14 (480 m²) czy rysunek S-04 rew. B (ok. 640 m²)? | przedmiar poz. 2.14, rysunek S-04 rew. B | 160 m², ok. 4 000 zł + ryzyko obmiaru | pytać do 2026-10-05 |

## 6. Odstępstwa i zastrzeżenia
| # | Dokument / klauzula | Jak w dokumentach | Propozycja | Skutek |
|---|---|---|---|---|
| 1 | umowa par. 15.1 | brak limitu kar umownych | limit kar 10 % wartości umowy | ograniczenie nieograniczonej ekspozycji |
| 2 | SWZ p. 4.7 | gwarancja 60 miesięcy | 36 miesięcy na urządzenia, 60 miesięcy na instalację | zgodne z gwarancją producentów, mniejszy koszt rezerwy |
| 3 | umowa par. 12.1 | brak waloryzacji | klauzula waloryzacji materiałów wg indeksu GUS publikowanego | przeniesienie ryzyka wzrostu cen |

Odstępstwa 1-3 są przedmiotem pytań; jeśli zamawiający ich nie przyjmie, rekomendacja: nie składać oferty albo wycenić R5 i R6 ostrożniej (podwyżka ceny o ok. 100-150 tys. zł).

## 7. Budowa ceny
| Składnik | Źródło | Wartość [zł] |
|---|---|---|
| Koszt bazowy | kosztorys robót (skrypt `cost-estimate`) | 4 200 000,00 |
| Rezerwa na ryzyka | rejestr ryzyk, suma wartości oczekiwanej | 622 000,00 |
| Narzut kosztów ogólnych 6 % | założenie firmy | 252 000,00 |
| **Razem** | | **5 074 000,00** |
| Marża 8 % od kosztu | założenie ofertowe | 405 920,00 |
| **Cena ofertowa netto** | (`bid_calc.py price`) | **5 479 920,00** |
| VAT 23 % | stawka dla tego zakresu, do potwierdzenia | 1 260 381,60 |
| **Cena brutto** | | **6 740 301,60** |

Marża 8 % od kosztu to 7,41 % ceny netto — podać jedną wartość i wskazać podstawę.
Koszt finansowania z warunków płatności: 7 763,22 zł (0,14 % wartości umowy) przy założeniach: 14 miesięcy, zaliczka 5 %, zatrzymanie (retencja) 5 %, płatność 30 dni, oprocentowanie 8,5 %. **Koszt finansowania to koszt, nie rezerwa na ryzyka** — do doliczenia w kosztach, jeśli nie jest już ujęty.

## 8. Struktura oferty
1. Pismo przewodnie: znak sprawy, cena netto i brutto, termin realizacji, okres gwarancji, podpis.
2. Formularz cenowy zamawiającego (zał. 1) — kompletny, bez pustych pozycji.
3. Oświadczenia i dokumenty podmiotowe wymagane w SWZ rozdz. 6.
4. Rejestr odstępstw i zastrzeżeń — w formie załącznika do oferty, z powołaniem w formularzu.
5. Harmonogram rzeczowo-finansowy wg wymaganego wzoru.
6. Dokumenty techniczne: karty urządzeń, programy prób, plan jakości, plan BIOZ.
7. Wykaz robót i referencje, kadra z uprawnieniami.

## 9. Kontrola przed złożeniem
- [ ] Odpowiedzi na pytania 1-5 wprowadzone do wyceny i do odstępstw.
- [ ] R7 skwantyfikowane albo przeniesione do odstępstw.
- [ ] Ceny materiałów potwierdzone u dostawców na dzień ofertowy.
- [ ] Limit kar i waloryzacja — stanowisko zamawiającego z odpowiedzi.
- [ ] Formularz cenowy zgodny z zał. 1, jednostki i waluta jak w SWZ.
- [ ] Podpisy, pełnomocnictwa, dokumenty podmiotowe aktualne.
- [ ] Decyzja o cenie i zatwierdzenie wg limitów firmowych.

## 10. Źródła
- Dokumenty postępowania: SWZ z 2026-09-10, umowa wzór (zał. 4), PFU, przedmiar, rysunki rew. S-04, corrigendum nr 2 z 2026-09-28. **Wszystkie dokumenty fikcyjne w tym przykładzie.**
- Rejestr ryzyk: `examples/risks-example.json` (przykład).
- Obliczenia: `scripts/bid_calc.py risk|price|cashflow`.
- Prawo zamówień publicznych: isap.sejm.gov.pl — brzmienie i tryb do potwierdzenia dla tego postępowania.
- Ustawa o podatku od towarów i usług (stawka VAT): isap.sejm.gov.pl — stan aktualny do odczytania.

## 11. Do weryfikacji
- [ ] Kompletność zestawu dokumentów (rozdz. 2, poz. 3 i 7).
- [ ] Wpływ corrigendum nr 2 na zakres i termin (R7).
- [ ] Warunki geotechniczne — badanie własne przed ofertą (R1).
- [ ] Realność gwarancji 60 miesięcy u producentów (R6).
- [ ] Koszt gwarancji ubezpieczeniowej i zabezpieczenia na 60 miesięcy (rozdz. 4, poz. 4).
- [ ] Klauzula waloryzacyjna i limit kar — stanowisko zamawiającego.
- [ ] Zgodność wyceny z przedmiarem zamawiającego pozycja po pozycji przed złożeniem.

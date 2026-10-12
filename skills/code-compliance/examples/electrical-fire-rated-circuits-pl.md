# Sprawdzenie zgodności: obwody elektryczne dla urządzeń przeciwpożarowych i kable na drogach ewakuacyjnych

Przykład fikcyjny pokazujący format. Wymagania oznaczone DO WERYFIKACJI nie zostały odczytane ze źródła w tym przykładzie i nie są cytatami przepisów.

## 1. Podsumowanie
Zakres: zasilanie wentylatorów oddymiających, pomp tryskaczowych, DSO i oświetlenia ewakuacyjnego oraz kable ogólne przebiegające przez drogę ewakuacyjną, budynek B2.
Wyniki: OK 2, FAIL 1, DO WERYFIKACJI 3, NIE DOTYCZY 1.
Najważniejsze: kabel zasilający wentylator oddymiający nie ma wymaganej klasy odporności ogniowej — trasa przez strefę pożarową bez zabezpieczenia.
To sprawdzenie pomocnicze, nie opinia prawna ani uzgodnienie. W sprawach spornych decyduje rzeczoznawca i organ.

## 2. Podstawa
- Klasyfikacja: budynek użyteczności publicznej, średniowysoki, kategoria ZL III (projekt architektury rew. C).
- Wybór wersji przepisów: data wniosku o PnB 12.03.2026; okres przejściowy wg ustawy z 31.07.2026 (Dz.U. poz. 1161).
- Dokumenty: schemat zasilania rew. E-02, trasa kabli rew. E-03, zestawienie kabli rew. E-01, projekt oddymiania rew. P-04.

## 3. Lista kontrolna
| # | Temat | Wymaganie | Źródło | Wartość projektowa | Źródło projektu | Wynik | Uwagi |
|---|---|---|---|---|---|---|---|
| 1 | Zasilanie wentylatora oddymiającego | kabel o określonej odporności ogniowej na czas działania | przepisy ppoż. dla urządzeń służących bezpieczeństwu pożarowemu; klauzula do odczytania w ISAP | kabel YKY bez klasy ogniowej, trasa przez strefę ZL III | schemat E-02, trasa E-03 | FAIL | zastosować kabel o wymaganej klasie (np. PH 90 wg PN-EN 50200 / PN-EN 13501-3) lub zmienić trasę |
| 2 | Zasilanie zestawu tryskaczowego | niezawodność zasilania i kabel o wymaganej klasie | przepisy ppoż. i norma tryskaczowa; klauzula do odczytania | dwa zasilania z rozdzielni głównej, kabel bez klasy | schemat E-02 | FAIL | zależnie od wymagań: kabel o klasie ogniowej lub dwa niezależne zasilania |
| 3 | Reakcja na ogień kabli ułożonych w budynku | klasa wg wymagań dla lokalizacji | PN-EN 50575 (klasyfikacja), wymagania krajowe do odczytania | deklarowane Eca, brak potwierdzenia dla tras w drogach ewakuacyjnych | zestawienie E-01 | DO WERYFIKACJI | odczytać wymaganą klasę dla lokalu/drogi ewakuacyjnej i porównać z deklaracją |
| 4 | DSO i oświetlenie ewakuacyjne | zasilanie i czas działania | przepisy ppoż.; PN-EN 1838, PN-EN 50172 | zasilanie z rozdzielni z baterią centralną, 1 h | opis projektu | DO WERYFIKACJI | odczytać wymagany czas i sposób zasilania dla kategorii ZL III |
| 5 | Przejścia przez oddzielenia ppoż. | uszczelnienie o klasie ściany | przepisy ppoż. | uszczelnienia przewidziane, karta wyrobu w projekcie | opis techniczny | DO WERYFIKACJI | potwierdzić klasę uszczelnienia równą klasie elementu |
| 6 | Uziemienie i ochrona przeciwporażeniowa | warunki ochrony dla obwodów bezpieczeństwa | PN-HD 60364 | Zs i czas wyłączenia policzone dla obwodów ogólnych | obliczenia E-05 | OK | rozszerzyć obliczenia na obwody ppoż. i potwierdzić przy odbiorze |
| 7 | Instalacja odgromowa | ocena ryzyka i klasa LPS | PN-EN 62305 | nie dotyczy zakresu | | NIE DOTYCZY | osobne sprawdzenie wraz z konstrukcją |

## 4. Niezgodności i propozycje
**#1 Wentylator oddymiający.** Kabel zasilający przechodzi przez strefę pożarową bez odporności ogniowej, więc po zadziałaniu strefy zasilanie może zostać utracone przed zakończeniem oddymiania. Propozycja: kabel o wymaganej klasie odporności ogniowej (klasa do potwierdzenia w przepisach i w projekcie oddymiania) albo trasa poza strefą pożarową. Zakres potwierdzić z rzeczoznawcą.

**#2 Zestaw tryskaczowy.** Brak kabla o klasie ogniowej i brak potwierdzonej niezależności dwóch zasilających rozdzielni. Propozycja: kabel o klasie ogniowej albo dwa rzeczywiście niezależne zasilania, zgodnie z wymaganiami normy i przepisów.

## 5. Do weryfikacji
- [ ] #1, #2: wymagane klasy kabli i wymagania zasilania dla urządzeń ppoż. — odczytać z aktu w ISAP.
- [ ] #3: wymagana klasa reakcji na ogień kabli dla tras w drogach ewakuacyjnych.
- [ ] #4: wymagany czas działania i sposób zasilania DSO oraz oświetlenia ewakuacyjnego.
- [ ] #5: klasy uszczelnień przejść z kart wyrobów.
- [ ] Dodatkowo: interfejs pożarowy (zwolnienie drzwi, klapy ppoż., wyłączenia) — sprawdzić macierz przyczynowo-skutkową.

## 6. Źródła
- Rozporządzenie w sprawie warunków technicznych, tekst jednolity: isap.sejm.gov.pl.
- Rozporządzenie MSWiA z 7 czerwca 2010 r. w sprawie ochrony przeciwpożarowej budynków: isap.sejm.gov.pl (brzmienie do potwierdzenia).
- PN-HD 60364, PN-EN 50575, PN-EN 50200, PN-EN 13501-3, PN-EN 1838, PN-EN 50172: tylko numery i wydania do potwierdzenia w PKN.
- Komunikat MRiT z 18.09.2026, gov.pl.

# Protokół z narady koordynacyjnej nr 2026-011

Przykład fikcyjny pokazujący format. Projekt, osoby, decyzje i terminy są wymyślone. Rejestr działań: `actions.json` (przykład).

```
Projekt: Biurowiec Zabłocie B2 (2026-014)          Data: 2026-10-12   Godz.: 10:00-11:20
Miejsce: budowa, biuro kierownika budowy
Przewodniczący: Inżynier kontraktu / M. Wiśniewski
Obecni:
  M. Wiśniewski - Inżynier kontraktu - przewodniczący
  J. Kowalski - Zamawiający - przedstawiciel inwestora
  A. Nowak - Projektant instalacji sanitarnych
  P. Zieliński - Wykonawca instalacji - kierownik robót
  K. Adamczyk - Wykonawca generalny - koordynator
Nieobecni: inspektor nadzoru sanitarnego (usprawiedliwiony)
Do wiadomości: inspektor nadzoru sanitarnego, rzeczoznawca ppoż.
Załączniki:
  1. Zestawienie działań A-001 do A-004 (PDF, 1 str.)
  2. Rysunek S-201 rew. C (PDF)
Status: wersja robocza do zatwierdzenia przez przewodniczącego. Uwagi do M. Wiśniewskiego do 2026-10-16.
```

## 1. Sprawy z poprzedniego protokołu (nr 2026-010)

| # | Działanie | Odpowiedzialny | Termin | Status | Uwaga |
|---|---|---|---|---|---|
| A-001 | Przekazać rzut kanalizacji podposadzkowej | Zamawiający / J. Kowalski | 2026-10-09 | **zaległe** | rzut przekazany 09.10.2026 jako ZAM-DOK-118, ale bez fragmentu osi C-D; działanie przeniesione na A-004 |
| A-002 | Uzgodnić z gestorem zakres przekładki instalacji ciepłowniczej | Wykonawca / P. Zieliński | 2026-10-05 | zamknięte | potwierdzenie gestora z 06.10.2026, pismo GC-77/2026 |
| A-003 | Uzupełnić moc wężownicy w karcie zasobnika | Projektant / A. Nowak | 2026-10-08 | **nie zgłoszono** | brak informacji w materiale na naradę; do wyjaśnienia na naradzie 2026-012 |

## 2. Punkty porządku obrad

**2.1 Postęp robót (P. Zieliński)**
Zgłoszono: wymiana pionów wod-kan zakończona w skrzydle A (100 %), w skrzydle B zaawansowanie 40 % (przód robót na pionie W2). Brak opóźnień wobec harmonogramu na 2026-10-12.

**2.2 Kolizja z niezinwentaryzowaną instalacją ciepłowniczą (K. Adamczyk)**
Zgłoszono: kolizja w osi C-D, poziom 0, zgłoszona pismem B2-NOT-001 z 2026-10-06. Gestor potwierdził przebieg instalacji w osi C-D na głębokości 0,75 m.
Decyzja: przekładka instalacji ciepłowniczej poza obrys kanalizacji podposadzkowej, wg rozwiązania projektanta; roboty wstrzymane do czasu przekazania rysunku (D-001).
Działanie: A-005.

**2.3 Obmiar izolacji (J. Kowalski)**
Zgłoszono: pytanie wykonawcy (B2-RFI-003) o wiążący obmiar izolacji: 480 m² z przedmiaru poz. 2.14 wobec ok. 640 m² z rysunku S-04 rew. B.
Decyzja: **brak decyzji na tej naradzie** — zamawiający zobowiązał się do pisemnej odpowiedzi do 2026-10-16 (umowa par. 11.3, obmiar weryfikowany).
Działanie: A-006.

**2.4 Zmiana trasy pionu W2 (A. Nowak)**
Zgłoszono: trasa pionu W2 w skrzydle B skorygowana wobec kolizji, rysunek S-201 rew. C przekazany 2026-10-09.
Decyzja: zaakceptowano trasę pionu W2 wg rysunku S-201 rew. C (D-002). Wykonawca potwierdza brak wpływu na pozostałe instalacje.
Działanie: A-007.

**2.5 Wentylacja poziomu 1 — zapotrzebowanie informacji (M. Wiśniewski)**
Zgłoszono: brak zestawienia klimakonwektorów z mocami dla poziomu 1; wpływ na zamówienie urządzeń (termin dostawy 6 tygodni).
Decyzja: projektant przekazuje zestawienie do 2026-10-19 (D-003).
Działanie: A-008.

## 3. Podjęte decyzje

| ID | Decyzja | Kto podjął | Data | Czego dotyczy | Odniesienie |
|---|---|---|---|---|---|
| D-001 | Przekładka instalacji ciepłowniczej poza obrys kanalizacji, osie C-D | Inżynier kontraktu / M. Wiśniewski | 2026-10-12 | zakres, koszt | pismo B2-NOT-001, zgłoszenie dziennika 214 |
| D-002 | Akceptacja trasy pionu W2 wg rysunku S-201 rew. C | Projektant / A. Nowak | 2026-10-12 | projekt | rys. S-201 rew. C |
| D-003 | Projektant przekazuje zestawienie klimakonwektorów poziomu 1 | Inżynier kontraktu / M. Wiśniewski | 2026-10-12 | projekt, termin | zgłoszenie wykonawcy z narady |

Decyzja D-001 zmienia zakres i koszt. **Protokół nie jest poleceniem zmiany ani zawiadomieniem** — przekazać do `project-correspondence` (polecenie zmiany oraz zawiadomienie z zastrzeżeniem praw wg umowy par. 9.2 i 14.1).

## 4. Zestawienie działań z tej narady

| ID | Punkt | Działanie | Odpowiedzialny | Termin | Status |
|---|---|---|---|---|---|
| A-004 | 2.2 | Przekazać rzut kanalizacji podposadzkowej w osi C-D wraz z przebiegiem instalacji ciepłowniczej | Zamawiający / J. Kowalski | 2026-10-16 | otwarte |
| A-005 | 2.2 | Przekazać rozwiązanie przekładki instalacji ciepłowniczej (rysunek) | Projektant / A. Nowak | 2026-10-19 | otwarte |
| A-006 | 2.3 | Pisemna odpowiedź w sprawie wiążącego obmiaru izolacji | Zamawiający / J. Kowalski | 2026-10-16 | otwarte |
| A-007 | 2.4 | Potwierdzić brak kolizji pozostałych instalacji w skrzydle B po zmianie trasy W2 | Wykonawca generalny / K. Adamczyk | 2026-10-23 | otwarte |
| A-008 | 2.5 | Przekazać zestawienie klimakonwektorów poziomu 1 z mocami | Projektant / A. Nowak | 2026-10-19 | otwarte |

Rejestr działań (`actions.py`): `A-001` przeniesione (zastąpione przez A-004), `A-002` zamknięte (pismo GC-77/2026), `A-003` **nie zgłoszono** — bez statusu na kolejną naradę.

## 5. Ryzyka i sprawy zgłoszone

| # | Sprawa | Zgłosił | Do zrobienia |
|---|---|---|---|
| R1 | Brak obmiaru izolacji blokuje zamówienie materiału (dostawa ok. 3 tygodni) | P. Zieliński | odpowiedź zamawiającego do 2026-10-16, w przeciwnym razie ryzyko przestoju izolowania w skrzydle B od 2026-11-02 |
| R2 | Brak zestawienia klimakonwektorów poziomu 1 opóźnia zamówienie urządzeń (6 tygodni dostawy) | K. Adamczyk | zestawienie do 2026-10-19; przy braku — zamówienie przesunięte poza 2026-11-09 |
| R3 | Instalacja ciepłownicza nieujęta w inwentaryzacji przekazanej przez zamawiającego | P. Zieliński | zgłoszono pismem B2-NOT-001, zastrzeżenie praw; kwantyfikacja po przekazaniu rysunku |

## 6. Następna narada

Termin: 2026-10-26, godz. 10:00, budowa, biuro kierownika budowy.
Punkty przeniesione: status A-003 (moc wężownicy), status A-004 i A-006 (odpowiedzi zamawiającego), zamówienie urządzeń po zestawieniu klimakonwektorów.

## 7. Uwagi do protokołu

- Terminy podane jako daty bezwzględne, nie „w przyszłym tygodniu".
- Odpowiedzialny zawsze jako osoba w firmie; „wykonawca" nie jest odpowiedzialnym.
- Czynności zamknięte mają dowód (numer pisma, data). Działanie A-003 pozostaje otwarte jako „nie zgłoszono" — nie zamykamy go bez informacji.
- Decyzje D-001 i D-003 mają skutek w zakresie i terminie, dlatego wskazano przekazanie do `project-correspondence`.
- Dane osobowe ograniczone do imienia, nazwiska, firmy i roli projektowej.

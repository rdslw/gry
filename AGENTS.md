# Zasady pracy w repozytorium gier
## Cel i układ repozytorium

- Repo zawiera niezależne, statyczne gry przeglądarkowe publikowane przez GitHub Pages.
- Każda gra zajmuje własny katalog bezpośrednio w katalogu głównym, np. `literkowa-kraina/`.
- Nie twórz pośredniego katalogu `games/` ani pojedynczych plików `<nazwa-gry>.html` w root.
- `README.md` opisuje repo ludziom, `AGENTS.md` określa workflow, a główny `index.html` jest katalogiem gier.
- Katalogi techniczne, takie jak `scripts/` i `.github/`, nie są grami.

## Kontrakt pojedynczej gry

- Wymagane pliki gry to `<slug>/index.html` oraz `<slug>/game.json`.
- Slug zapisuj małymi literami ASCII, z wyrazami rozdzielonymi myślnikami; nie zmieniaj go po publikacji bez migracji linków.
- Zasoby trzymaj wewnątrz katalogu gry, najlepiej w `<slug>/assets/`; nie odwołuj się do zasobów innej gry.
- Używaj względnych URL-i, aby gra działała pod ścieżką `/gry/<slug>/` i przez lokalny serwer.
- Domyślnie twórz rozwiązania client-side bez backendu, procesu budowania i sekretów.
- Klucze `localStorage` poprzedzaj slugiem gry, aby uniknąć kolizji między grami.
- Interfejs ma działać dotykiem na iPhonie i iPadzie oraz nie może wymagać precyzyjnego hovera.

## Metadane `game.json`

Każda opublikowana gra używa tego minimalnego formatu:

```json
{
  "title": "Literkowa Kraina",
  "description": "Gra edukacyjna do nauki i rozpoznawania polskich liter.",
  "age": "4–8 lat",
  "status": "published",
  "created": "2026-07-29",
  "updated": "2026-07-29"
}
```

- Daty zapisuj jako `YYYY-MM-DD`; `created` pozostaje stałe, a `updated` zmieniaj przy widocznej zmianie gry.
- Dozwolone statusy to `draft` i `published`; główny katalog pokazuje tylko gry opublikowane.
- Nie zapisuj w metadanych ścieżki ani URL-a gry — wynikają z nazwy katalogu.
- Opcjonalne pola, np. `featured`, `thumbnail` lub `thread`, dodawaj tylko wtedy, gdy obsługuje je katalog.

## Katalog i publikacja

- Główny `index.html` ma być generowany z plików `*/game.json` przez `scripts/build-index.py`, nie edytowany ręcznie.
- Po dodaniu gry lub zmianie metadanych uruchom generator i dołącz zaktualizowany indeks do tego samego commita.
- Jeśli generator udostępnia `--check`, uruchom `python3 scripts/build-index.py --check` przed wysłaniem zmian.
- Nie dodawaj automatycznych commitów z CI ani dokumentacji generowanej przez płatny LLM.

## Workflow i weryfikacja

- Domyślnie pracuj w orb, sprawdź zmianę przez portal Amp, a po akceptacji użyj Ship do `main`.
- Commit powinien obejmować jedną spójną grę lub zmianę; nie modyfikuj innych gier bez potrzeby.
- Dla zmian wspólnej infrastruktury, ryzykownych przebudów lub równoległej pracy użyj brancha i Pull Requesta zamiast bezpośredniego Ship.
- Przed Ship sprawdź ładowanie bez błędów konsoli, start, główną interakcję, restart i osiągalny stan końcowy.
- Dla zmian UI sprawdź mały ekran, orientację mobilną, obsługę dotyku i czytelne cele dotykowe.

## Świadome ograniczenia

- Nie wprowadzaj frameworka, bundlera, wspólnej biblioteki UI ani backendu bez konkretnej potrzeby gry.
- Nie przenoś powtarzalnego kodu do `shared/`, dopóki co najmniej dwie gry nie potrzebują stabilnego wspólnego rozwiązania.
- Nie używaj portalu Amp jako hostingu produkcyjnego; publiczną wersję zapewnia GitHub Pages.
- Nigdy nie umieszczaj tokenów, kluczy API ani prywatnych danych w kodzie publikowanym przez Pages.

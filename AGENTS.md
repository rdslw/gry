# Zasady pracy w repozytorium gier
## Cel i układ repozytorium
- Repo zawiera niezależne, statyczne gry przeglądarkowe publikowane przez GitHub Pages.
- Każda gra zajmuje własny katalog bezpośrednio w root; nie twórz `games/` ani rootowych plików `<slug>.html`.
- `README.md` jest dla ludzi, `AGENTS.md` definiuje workflow, a główny `index.html` jest generowanym katalogiem.
- Katalogi techniczne, np. `scripts/` i `.github/`, nie są grami.
## Kontrakt pojedynczej gry
- Wymagane pliki to `<slug>/index.html` i `<slug>/game.json`; slug zapisuj małymi literami ASCII z myślnikami.
- Zasoby trzymaj w katalogu gry i używaj względnych URL-i działających pod `/gry/<slug>/` oraz lokalnym serwerem.
- Domyślnie twórz client-side bez backendu; klucze `localStorage` poprzedzaj slugiem.
- Interfejs ma działać dotykiem na iPhonie i iPadzie bez wymagania precyzyjnego hovera.
- Dodawaj stabilne hooki smoke testu: `[data-game-root]`, `[data-smoke-action="start"]` i `data-game-state`.
## Python i narzędzia
- Do środowisk i zależności Pythona używaj `uv`; nigdy nie instaluj pakietów przez czyste `pip`.
- Skrypty uruchamiaj przez `uv run`, a jednorazowe narzędzia przez `uvx` z przypiętą wersją.
- Często używane CLI instaluj przez `uv tool install`; Rodney ma być przypięty do wersji `0.4.0`.
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
- Daty zapisuj jako `YYYY-MM-DD`; `created` jest stałe, a `updated` zmieniaj przy widocznej zmianie.
- Status to `draft` lub `published`; katalog pokazuje tylko opublikowane gry.
- Nie zapisuj ścieżki ani URL-a; pola opcjonalne dodawaj tylko, gdy obsługuje je generator.
## Katalog i publikacja
- Generuj główny `index.html` z `*/game.json` przez `scripts/build-index.py`; nie edytuj go ręcznie.
- Po zmianie gry uruchom `uv run python scripts/build-index.py` i dołącz indeks do tego samego commita.
- Przed Ship uruchom `uv run python scripts/build-index.py --check` i napraw nieaktualny katalog.
- Nie dodawaj automatycznych commitów z CI ani dokumentacji generowanej przez płatny LLM.
## Workflow
- Domyślnie pracuj w orb; po testach pokaż portal, a dopiero po akceptacji użyj Ship do `main`.
- Commit obejmuje jedną spójną zmianę; dla infrastruktury, ryzykownych przebudów lub kolizji użyj brancha i PR.
## Smoke test przed Ship
- Testuj przez lokalny serwer HTTP, nigdy `file://`; zacznij od `curl --fail` oczekującego na URL gry.
- Jeśli brak Rodney, zainstaluj go przez `uv tool install rodney==0.4.0`, nigdy przez `pip`.
- Używaj `rodney start --local` i zawsze wykonaj `rodney stop`; zachowaj ignorowany `.rodney/`, aby ponownie używać profilu.
- Otwórz URL, poczekaj na `[data-game-root]`, sprawdź tytuł, kliknij start i potwierdź oczekiwany `data-game-state`.
- Przy błędzie zapisz screenshot w `.amp/in/artifacts/`; rutynowych screenshotów nie commituj.
- Rodney nie zbiera wstecz błędów konsoli; jeśli to istotne, dodaj `window.__smokeErrors` albo mocniejszy test.
- Niezerowy wynik blokuje Ship; po każdej późniejszej zmianie powtórz test, następnie pokaż portal użytkownikowi.
## Decyzje i odłożone rozszerzenia
- Zachowuj czytelne commity i trailer `Amp-Thread` łączący zmianę z wątkiem.
- Każda gra wymaga smoke testu; pełne E2E dodawaj dla zachowań istotnych lub podatnych na regresje.
- Nie dodawaj frameworka, bundlera, wspólnej biblioteki UI ani backendu bez konkretnej potrzeby.
- Nie twórz `shared/`, dopóki co najmniej dwie gry nie potrzebują stabilnego wspólnego rozwiązania.
- Portal Amp nie jest hostingiem produkcyjnym; zapewnia go GitHub Pages.
- Nigdy nie publikuj tokenów, kluczy API ani prywatnych danych.

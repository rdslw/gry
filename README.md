# Gry

Zbiór prostych gier przeglądarkowych tworzonych z pomocą Amp.

Katalog gier będzie dostępny przez GitHub Pages pod adresem <https://rdslw.github.io/gry/>.

Każda gra znajduje się we własnym katalogu bezpośrednio w repozytorium i ma własny plik `index.html`, na przykład:

```text
literkowa-kraina/
  index.html
  game.json
memory/
  index.html
  game.json
```

Główny `index.html` jest generowany z metadanych gier poleceniem:

```bash
python3 scripts/build-index.py
```

## Codzienny workflow tworzenia gry

1. Utwórz nowy wątek w projekcie Amp `gry` i wskaż katalog nowej gry oraz jej wymagania.
2. Amp tworzy grę i `game.json` w osobnym katalogu, bez modyfikowania innych gier.
3. Agent uruchamia generator katalogu, testy i lokalny serwer w orb.
4. Obejrzyj grę przez portal Amp; zgłoś poprawki przed publikacją.
5. Po akceptacji użyj Ship, aby utworzyć spójny commit i wypchnąć go do `main`.
6. GitHub Actions sprawdza aktualność katalogu, a GitHub Pages publikuje nową wersję.

Przed wysłaniem równoległego wątku należy zsynchronizować go z aktualnym `origin/main`. Branch i Pull Request są alternatywą dla zmian wspólnej infrastruktury, ryzykownych przebudów lub prac mogących wejść ze sobą w konflikt.

Szczegółowy kontrakt gry, format `game.json` i zasady weryfikacji znajdują się w [`AGENTS.md`](AGENTS.md).

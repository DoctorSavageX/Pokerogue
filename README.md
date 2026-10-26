# PokéRogue — single HTML file

`PokeRogue.html` is the whole game in one file. Open it in a browser (Chrome, Edge or Firefox) and play.

- **Needs internet.** All of the game code is inside the file, but images, music and text are loaded from GitHub
  (`raw.githubusercontent.com`, from the `pokerogue-assets` and `pokerogue-locales` repos).
- **Guest/offline saves.** There is no login. Progress is saved in your browser's local storage, separate from any
  pokerogue.net account. Clearing browser data erases it.
- Daily runs, leaderboards and anything that needs the official server won't work.

## How it was built

Built from [pagefaultgames/pokerogue](https://github.com/pagefaultgames/pokerogue) at commit
`3368c11f9bc2061a1e52f3c2e2f38f8db0f0ed6e` (AGPL-3.0), with `single-file-build.patch` applied:

- locale files load from the `pokerogue-locales` repo on GitHub
- the whole bundle is built as one chunk (`inlineDynamicImports`)
- the loader requests assets with CORS, so GitHub-hosted images and videos can be drawn in WebGL
- move animations accept GitHub's `text/plain` content type for JSON

```sh
git clone https://github.com/pagefaultgames/pokerogue && cd pokerogue
git checkout 3368c11f9bc2061a1e52f3c2e2f38f8db0f0ed6e
git clone https://github.com/pagefaultgames/pokerogue-locales locales  # build reads locale namespaces
git apply ../single-file-build.patch
pnpm install --frozen-lockfile --ignore-scripts
VITE_BYPASS_LOGIN=1 npx vite build --mode production   # the static-shell plugin errors at the end; dist/ is still written
python3 ../assemble.py dist ../PokeRogue.html
```

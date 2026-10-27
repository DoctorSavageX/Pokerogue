# PokéRogue — single HTML file

Download `PokeRogue.html`, open it in a browser (Chrome, Edge or Firefox) and play.

- **Auto-updates.** Each time you open it, the page checks this repo for the newest build and downloads it if
  there is one. A GitHub Action (`.github/workflows/build.yml`) rebuilds the game every day from the latest
  PokeRogue release and commits it to `latest/`. The last download is kept, so the game still starts if the check fails.
- **Needs internet.** Images, music and text load from GitHub (`raw.githubusercontent.com`), from the
  `pokerogue-assets` and `pokerogue-locales` repos.
- **This repo must be public**, or the page can't download the builds.
- **Guest saves only.** There is no login. Progress is saved in your browser, separate from any pokerogue.net
  account, and survives updates. Clearing browser data erases it. The official server only accepts requests from
  pokerogue.net itself, so logging in from this file isn't possible.
- Daily runs, leaderboards and anything else that needs the official server won't work.

## How it's built

From [pagefaultgames/pokerogue](https://github.com/pagefaultgames/pokerogue) (AGPL-3.0), `main` branch.
`build/patch.py` makes these changes before building:

- locale files load from the `pokerogue-locales` repo on GitHub
- the whole game is built as one JS file
- the loader requests assets with CORS, so GitHub-hosted images and videos can be drawn in WebGL
- move animations accept GitHub's `text/plain` content type for JSON

`build/assemble.py` then writes `latest/game.js`, `game.css`, `shell.html` and `version.json`.

To rebuild right away instead of waiting for the daily run: Actions → Build PokeRogue → Run workflow
(tick "force" to rebuild the same version).

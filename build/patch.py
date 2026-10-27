"""Patch a PokeRogue checkout so it can run from a single local HTML file.

Usage: python3 build/patch.py <pokerogue-dir> <locales-commit-sha>

Every replacement must match exactly once, so an upstream change that breaks
one of them fails the build loudly instead of shipping a broken game.
"""

import sys
from pathlib import Path

src = Path(sys.argv[1])
locales_sha = sys.argv[2]

PATCHES = [
    # Locale files load from the pokerogue-locales repo instead of the page's own folder
    (
        "src/i18n.ts",
        "return getCachedUrl(`./locales/${lng}/${fileName}.json`);",
        "return `https://raw.githubusercontent.com/pagefaultgames/pokerogue-locales/"
        + locales_sha
        + "/${lng}/${fileName}.json`;",
    ),
    # GitHub serves JSON as text/plain, which the move animation loader rejected
    (
        "src/data/battle-anims.ts",
        'if (!response.ok || contentType?.indexOf("application/json") === -1) {',
        'if (!response.ok || !(contentType?.includes("json") || contentType?.includes("text/plain"))) {',
    ),
    # Cross-origin images and videos need CORS requests before WebGL can draw them
    (
        "src/main.ts",
        "    type: Phaser.WEBGL,\n",
        '    type: Phaser.WEBGL,\n    loader: { crossOrigin: "anonymous" },\n',
    ),
    (
        "src/loading-scene.ts",
        'intro.loadURL("images/intro_dark.mp4", true);',
        'intro.loadURL("images/intro_dark.mp4", true, "anonymous");',
    ),
    # The static shell loader expects a hosted site; drop it since the launcher loads the bundle itself
    (
        "vite.config.ts",
        '      (await import("./plugins/vite/static-shell-plugin.ts")).staticShellPlugin(),\n',
        "",
    ),
    # Build everything into one JS file
    (
        "vite.config.ts",
        "          keepNames: true,\n",
        "          keepNames: true,\n          inlineDynamicImports: true,\n",
    ),
]

for rel, old, new in PATCHES:
    path = src / rel
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        sys.exit(f"patch.py: expected 1 match in {rel}, found {count}:\n  {old!r}")
    path.write_text(text.replace(old, new), encoding="utf-8")
    print(f"patched {rel}")

"""Turn a Vite build of PokeRogue into the files PokeRogue.html loads.

Usage: python3 build/assemble.py <dist-dir> <out-dir> <pokerogue-commit> <assets-commit> <version>

Writes game.js, game.css, shell.html (fonts and touch controls markup) and version.json.
"""

import glob
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

dist, out = Path(sys.argv[1]), Path(sys.argv[2])
commit, assets_sha, version = sys.argv[3], sys.argv[4], sys.argv[5]

html = (dist / "index.html").read_text(encoding="utf-8")
js_files = glob.glob(str(dist / "assets" / "index-*.js"))
css_files = glob.glob(str(dist / "assets" / "index-*.css"))
if len(js_files) != 1 or len(css_files) != 1:
    sys.exit(f"assemble.py: expected one JS and one CSS bundle, got {js_files} {css_files}")

head = html.split("</head>", 1)[0]
body = html.split("<body>", 1)[1].split("</body>", 1)[0]
styles = "\n".join(re.findall(r"<style[^>]*>.*?</style>", head, flags=re.S))
body = re.sub(r"<script.*?</script>", "", body, flags=re.S).strip()

out.mkdir(parents=True, exist_ok=True)
(out / "game.js").write_text(Path(js_files[0]).read_text(encoding="utf-8"), encoding="utf-8")
(out / "game.css").write_text(Path(css_files[0]).read_text(encoding="utf-8"), encoding="utf-8")
(out / "shell.html").write_text(styles + "\n" + body + "\n", encoding="utf-8")
(out / "version.json").write_text(
    json.dumps(
        {
            "version": version,
            "pokerogueCommit": commit,
            "builtAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "assetsBase": f"https://raw.githubusercontent.com/pagefaultgames/pokerogue-assets/{assets_sha}/",
        },
        indent=2,
    )
    + "\n",
    encoding="utf-8",
)
print(f"wrote {out}")

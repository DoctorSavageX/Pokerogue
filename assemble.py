import glob, re, sys
d = sys.argv[1]; out = sys.argv[2]
html = open(f"{d}/index.html", encoding="utf-8").read()
js = open(glob.glob(f"{d}/assets/index-*.js")[0], encoding="utf-8").read()
css = open(glob.glob(f"{d}/assets/index-*.css")[0], encoding="utf-8").read()
assert "</script" not in js.lower()
BASE = "https://raw.githubusercontent.com/pagefaultgames/pokerogue-assets/6f31bac89b31f95d9697e48fac87bbd599a4b1b6/"
# drop service worker block, manifest link, and external entry tags
html = re.sub(r'\s*<script>\s*if \("serviceWorker".*?</script>', "", html, flags=re.S)
html = re.sub(r'\s*<link rel="manifest"[^>]*>', "", html)
html = re.sub(r'\s*<script type="module" crossorigin src="[^"]*"></script>', "", html)
html = re.sub(r'\s*<link rel="stylesheet" crossorigin href="[^"]*">', "", html)
html = html.replace('<meta charset="UTF-8" />', '<meta charset="UTF-8" />\n\t<base href="' + BASE + '" />', 1)
head_add = "\n\t<style>\n" + css + "\n\t</style>\n"
html = html.replace("</head>", head_add + "</head>", 1)
body_add = "\n<script type=\"module\">\n" + js + "\n</script>\n"
html = html.replace("</body>", body_add + "</body>", 1)
for bad in ("serviceWorker.register", "manifest.webmanifest", "./assets/index-"):
    assert bad not in html.replace(js, ""), bad
open(out, "w", encoding="utf-8").write(html)
print(len(html))

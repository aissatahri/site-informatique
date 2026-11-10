"""Génère le site statique dans docs/ à partir de cours/*.md et exercices/*.md.

Usage : python build.py
Dépendance : pip install markdown
"""
import html
import json
import re
import shutil
import struct
import unicodedata
import zlib
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"
SITE_TITLE = "Informatique - Tronc Commun"
SCHOOL = "Lycée Qadi Ibn Arabi"
TEACHER = "Aissa Tahri"
YEAR = "2026-2027"

# ---------------------------------------------------------------------------
# CONFIGURATION DU CONTENU
# Pour chaque module : son titre et ses chapitres (liste vide = module « Bientôt »).
# Pour chaque chapitre : le nom (sans .md) du fichier dans cours/, exercices/, tp/.
#   - "cours" est obligatoire ; "exercices" et "tp" sont optionnels (omis ou None).
# Un module est actif s'il a au moins un chapitre.
# ---------------------------------------------------------------------------
MODULES = [
    {
        "title": "Généralités sur les systèmes informatiques",
        "chapters": [
            {"cours": "ch1-definitions", "exercices": "ch1-exercices"},
            {"cours": "ch2-structure-ordinateur", "exercices": "ch2-exercices"},
            {"cours": "ch3-logiciels", "exercices": "ch3-exercices"},
        ],
    },
    {
        "title": "Les logiciels",
        "chapters": [
            {
                "cours": "m2-ch1-systeme-exploitation",
                "exercices": "m2-ch1-exercices",
                "tp": "m2-ch1-tp",
            },
        ],
    },
    {"title": "Algorithme et programmation", "chapters": []},
    {"title": "Réseaux et internet", "chapters": []},
]

# Types de pages : (clé, dossier, libellé, classe du bouton d'accueil)
KINDS = [
    ("cours", "cours", "Cours", "btn"),
    ("exercices", "exercices", "Exercices", "btn btn-alt"),
    ("tp", "tp", "TP", "btn btn-alt"),
]

# Livre ouvert simple, utilisé comme logo (si assets/logo.png n'existe pas) et comme favicon
LOGO_SVG_INNER = (
    '<rect width="64" height="64" rx="14" fill="#1F3A5F"/>'
    '<path d="M32 19c-5-3-12-4-20-3v28c8-1 15 0 20 3 5-3 12-4 20-3V16c-8-1-15 0-20 3z" fill="#fff"/>'
    '<path d="M32 19v28" stroke="#C8962E" stroke-width="3" fill="none"/>'
)
LOGO_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="44" height="44" '
    f'aria-hidden="true" focusable="false">{LOGO_SVG_INNER}</svg>'
)
FAVICON_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
    f"{LOGO_SVG_INNER}</svg>\n"
)

def make_favicon_ico(size=64, ss=4):
    """Dessine le livre ouvert du logo (sans dépendance) et l'encode en .ico (PNG intégré)."""

    def bezier(p0, p1, p2, p3, n=16):
        return [
            tuple(
                (1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t**2 * c + t**3 * d
                for a, b, c, d in zip(p0, p1, p2, p3)
            )
            for t in (i / n for i in range(1, n + 1))
        ]

    book = [(32, 19)]
    book += bezier((32, 19), (27, 16), (20, 15), (12, 16))
    book += [(12, 44)]
    book += bezier((12, 44), (20, 43), (27, 44), (32, 47))
    book += bezier((32, 47), (37, 44), (44, 43), (52, 44))
    book += [(52, 16)]
    book += bezier((52, 16), (44, 15), (37, 16), (32, 19))

    def inside(poly, x, y):
        c = False
        for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
            if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
                c = not c
        return c

    def in_round_rect(x, y, r=14):
        cx, cy = min(max(x, r), 64 - r), min(max(y, r), 64 - r)
        return (x - cx) ** 2 + (y - cy) ** 2 <= r * r

    navy, white, gold = (0x1F, 0x3A, 0x5F), (255, 255, 255), (0xC8, 0x96, 0x2E)
    k = 64 / (size * ss)
    raw = bytearray()
    for py in range(size):
        raw.append(0)  # filtre PNG : aucun
        for px in range(size):
            r = g = b = a = 0
            for sy in range(ss):
                for sx in range(ss):
                    x, y = (px * ss + sx + 0.5) * k, (py * ss + sy + 0.5) * k
                    if not in_round_rect(x, y):
                        continue
                    if 30.5 <= x <= 33.5 and 19 <= y <= 47:
                        col = gold
                    elif inside(book, x, y):
                        col = white
                    else:
                        col = navy
                    r, g, b, a = r + col[0], g + col[1], b + col[2], a + 255
            n = ss * ss
            cnt = a // 255
            raw += bytes((r // cnt, g // cnt, b // cnt, a // n) if cnt else (0, 0, 0, 0))

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data))

    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + chunk(b"IEND", b"")
    )
    header = struct.pack("<HHH", 0, 1, 1)
    entry = struct.pack("<BBBBHHII", size, size, 0, 0, 1, 32, len(png), 22)
    return header + entry + png


PAGE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="icon" href="{root}favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="{root}favicon.svg">
<link rel="stylesheet" href="{root}style.css">
</head>
<body id="haut">
<header class="site-header">
<a class="brand" href="{root}index.html">
{logo}
<span class="brand-text"><strong>{school}</strong><span>{site_title}</span></span>
</a>
<nav class="site-nav" aria-label="Navigation principale">
<a href="{root}index.html">Accueil</a>
<a href="{root}entrainement.html">Entraînement</a>
<a href="{root}jeux/index.html">Jeux</a>
</nav>
</header>
<main>
{body}
</main>
<footer class="site-footer">
<p>Enseignant : {teacher}</p>
<p>Année scolaire {year}</p>
</footer>
<a class="to-top" href="#haut" aria-label="Retour en haut">↑ <span>Retour en haut</span></a>
<script>
// Impression : ouvre toutes les corrections
window.addEventListener("beforeprint", function () {{
  document.querySelectorAll("details").forEach(function (d) {{ d.open = true; }});
}});
</script>
</body>
</html>
"""

LABELS = {
    "Définition": "definition",
    "Exemple": "exemple",
    "Remarque": "remarque",
    "À retenir": "retenir",
    "Attention": "attention",
}


def convert(text):
    md = markdown.Markdown(extensions=["tables", "fenced_code"])
    return md.convert(text)


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "section"


def add_heading_ids(out):
    """Ajoute un id aux titres h2 et retourne (html, [(id, texte)])."""
    toc, used = [], set()

    def repl(m):
        text = html.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip()
        base = slug = slugify(text)
        n = 2
        while slug in used:
            slug, n = f"{base}-{n}", n + 1
        used.add(slug)
        toc.append((slug, text))
        return f'<h2 id="{slug}">{m.group(2)}</h2>'

    return re.sub(r"<h2(\s[^>]*)?>(.*?)</h2>", repl, out, flags=re.S), toc


def style_quotes(out):
    """Classe les citations Définition / Exemple / Remarque d'après leur libellé."""

    def repl(m):
        return f'<blockquote class="note note-{LABELS[m.group(1)]}"><p><strong>{m.group(1)}</strong>'

    return re.sub(
        r"<blockquote>\s*<p><strong>(Définition|Exemple|Remarque|À retenir|Attention)</strong>",
        repl,
        out,
    )


def render(md_text):
    # Les blocs <details> restent du HTML brut, mais leur contenu Markdown est converti
    blocks = []

    def keep(m):
        summary, body = m.group(1), m.group(2)
        blocks.append(f"<details>\n{summary}\n{convert(body)}\n</details>")
        return f"\n\nDETAILSBLOCK{len(blocks) - 1}X\n\n"

    md_text = re.sub(
        r"<details>\s*(<summary>.*?</summary>)(.*?)</details>", keep, md_text, flags=re.S
    )
    out = convert(md_text)
    for i, block in enumerate(blocks):
        out = out.replace(f"<p>DETAILSBLOCK{i}X</p>", block)
    out = style_quotes(out)
    # Tableaux dans un conteneur à défilement horizontal
    out = out.replace("<table>", '<div class="table-wrap"><table>')
    out = out.replace("</table>", "</table></div>")
    return add_heading_ids(out)


def title_of(md_text, fallback):
    m = re.search(r"^#\s+(.+)$", md_text, re.M)
    return m.group(1).strip() if m else fallback


def load_all():
    """Lit la configuration MODULES et retourne une liste de modules.

    Chaque module : {"title", "chapters": [{kind: (fichier, titre, html, sommaire)}]}.
    Un fichier optionnel absent du disque est simplement ignoré.
    """
    modules = []
    for mod in MODULES:
        chapters = []
        for conf in mod["chapters"]:
            chapter = {}
            for kind, folder, _label, _cls in KINDS:
                stem = conf.get(kind)
                if not stem:
                    continue
                path = ROOT / folder / f"{stem}.md"
                if not path.exists():
                    if kind == "cours":
                        raise SystemExit(f"Fichier obligatoire introuvable : {path}")
                    continue
                text = path.read_text(encoding="utf-8")
                body, toc = render(text)
                chapter[kind] = (stem, title_of(text, stem), body, toc)
            chapters.append(chapter)
        modules.append({"title": mod["title"], "chapters": chapters})
    return modules


def logo_html():
    if (ROOT / "assets" / "logo.png").exists():
        return '<img class="logo" src="{root}assets/logo.png" alt="" width="44" height="44">'
    return LOGO_SVG


def breadcrumb(mod_idx, num):
    return (
        '<nav class="breadcrumb" aria-label="Fil d\'Ariane"><ol>'
        '<li><a href="../index.html">Accueil</a></li>'
        f'<li><a href="../index.html#module-{mod_idx + 1}">Module {mod_idx + 1}</a></li>'
        f'<li aria-current="page">Chapitre {num}</li>'
        "</ol></nav>"
    )


def switcher(kind, chapter):
    items = []
    for k, folder, label, _cls in KINDS:
        if k not in chapter:
            continue
        if k == kind:
            items.append(f'<span class="tab current" aria-current="page">{label}</span>')
        else:
            items.append(f'<a class="tab" href="../{folder}/{chapter[k][0]}.html">{label}</a>')
    return '<div class="tabs">' + "".join(items) + "</div>" if len(items) > 1 else ""


def toc_html(toc):
    if len(toc) < 2:
        return ""
    lis = "".join(f'<li><a href="#{i}">{html.escape(t)}</a></li>' for i, t in toc)
    return f'<nav class="toc" aria-label="Table des matières"><h2>Table des matières</h2><ol>{lis}</ol></nav>'


def pager(kind, num, chapters):
    """Précédent / Suivant limités aux chapitres du module qui ont une page de ce type."""
    pages = {n: ch[kind] for n, ch in enumerate(chapters, 1) if kind in ch}
    nums = sorted(pages)
    i = nums.index(num)
    prev = nxt = '<span></span>'
    if i > 0:
        p = pages[nums[i - 1]]
        prev = f'<a class="btn btn-ghost" href="{p[0]}.html">← Précédent<small>{html.escape(p[1])}</small></a>'
    if i < len(nums) - 1:
        n = pages[nums[i + 1]]
        nxt = f'<a class="btn btn-ghost next" href="{n[0]}.html">Suivant →<small>{html.escape(n[1])}</small></a>'
    return f'<nav class="pager" aria-label="Navigation entre chapitres">{prev}{nxt}</nav>'


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def make_page(title, description, root, body):
    return PAGE.format(
        title=html.escape(title),
        description=html.escape(description, quote=True),
        root=root,
        logo=logo_html().replace("{root}", root),
        school=html.escape(SCHOOL),
        site_title=html.escape(SITE_TITLE),
        body=body,
        teacher=html.escape(TEACHER),
        year=html.escape(YEAR),
    )


def index_page(modules, n_series):
    intro = (
        "Bienvenue sur le site de cours d'informatique : retrouvez ici les cours "
        "et les exercices corrigés de l'année."
    )
    parts = [
        '<section class="hero">',
        f"<h1>{html.escape(SITE_TITLE)}</h1>",
        f"<p>{html.escape(intro)}</p>",
        "</section>",
        '<h2 class="section-title">Les modules</h2>',
        '<div class="modules">',
    ]
    for i, mod in enumerate(modules):
        name = mod["title"]
        count = len(mod["chapters"])
        active = count > 0
        if count == 0:
            count_txt = "Chapitres à venir"
        else:
            count_txt = f"{count} chapitre{'s' if count > 1 else ''}"
        tag = (
            '<span class="badge badge-ok">Disponible</span>'
            if active
            else '<span class="badge">Bientôt</span>'
        )
        anchor = f'<a href="#module-{i + 1}">{html.escape(name)}</a>' if active else html.escape(name)
        parts.append(
            f'<article class="card{"" if active else " soon"}">'
            f'<span class="card-num">Module {i + 1}</span>'
            f"<h3>{anchor}</h3>"
            f'<p class="card-meta">{count_txt}</p>{tag}</article>'
        )
    parts.append("</div>")

    parts.append('<h2 class="section-title">Entraînement</h2>')
    parts.append('<div class="modules">')
    parts.append(
        '<article class="card">'
        '<span class="card-num">Entraînement</span>'
        '<h3><a href="entrainement.html">Séries d\'entraînement</a></h3>'
        f'<p class="card-meta">{n_series} séries, notées sur 20</p>'
        '<span class="badge badge-ok">Disponible</span></article>'
    )
    parts.append(
        '<article class="card">'
        '<span class="card-num">Jeux</span>'
        '<h3><a href="jeux/index.html">Souris et clavier</a></h3>'
        '<p class="card-meta">3 activités : clics, glisser-déposer, clavier</p>'
        '<span class="badge badge-ok">Disponible</span></article>'
    )
    parts.append("</div>")

    for i, mod in enumerate(modules):
        if not mod["chapters"]:
            continue
        parts.append(f'<section class="chapters" id="module-{i + 1}">')
        parts.append(f"<h2>Module {i + 1} : {html.escape(mod['title'])}</h2>")
        for chapter in mod["chapters"]:
            parts.append('<div class="chapter">')
            parts.append(f"<h3>{html.escape(chapter['cours'][1])}</h3>")
            parts.append('<p class="buttons">')
            for kind, folder, label, cls in KINDS:
                if kind in chapter:
                    parts.append(
                        f'<a class="{cls}" href="{folder}/{chapter[kind][0]}.html">{label}</a>'
                    )
            parts.append("</p></div>")
        parts.append("</section>")
    return make_page(
        f"{SITE_TITLE} - {SCHOOL}",
        f"{SITE_TITLE} au {SCHOOL} : cours et exercices corrigés, année scolaire {YEAR}.",
        "",
        "\n".join(parts),
    )


def chapter_page(kind, mod_idx, num, chapters):
    chapter = chapters[num - 1]
    stem, title, body, toc = chapter[kind]
    label = next(l for k, _f, l, _c in KINDS if k == kind)
    inner = (
        breadcrumb(mod_idx, num)
        + switcher(kind, chapter)
        + '<div class="layout">'
        + toc_html(toc)
        + f'<article class="content">{body}</article></div>'
        + pager(kind, num, chapters)
    )
    return make_page(
        f"{title} - {SITE_TITLE}",
        f"{label} d'informatique, Tronc Commun : {title}. {SCHOOL}, {YEAR}.",
        "../",
        inner,
    )


TRAINING_BODY = """<nav class="breadcrumb" aria-label="Fil d'Ariane"><ol>
<li><a href="index.html">Accueil</a></li>
<li aria-current="page">Entraînement</li>
</ol></nav>
<h1>Entraînement</h1>
<section id="step-choice">
<p>Choisis une série, puis clique sur « Commencer ». Les questions sont tirées au hasard à chaque début. La note est calculée sur 20, directement dans ton navigateur : rien n'est envoyé ni enregistré.</p>
<div id="series" class="series"></div>
<p class="buttons"><button type="button" class="btn" id="start">Commencer</button></p>
</section>
<section id="step-result" hidden>
<div class="result">
<h2 id="result-title"></h2>
<p class="big-note" id="result-note"></p>
<div class="table-wrap" id="result-table"></div>
<p class="buttons">
<button type="button" class="btn" id="restart">Recommencer (nouveau tirage)</button>
<button type="button" class="btn btn-ghost" id="change">Changer de série</button>
</p>
<p class="legend"><span class="lg ok">Bonne réponse</span> <span class="lg ko">Mauvaise réponse ou sans réponse</span></p>
</div>
</section>
<section id="step-exam" hidden>
<h2 id="exam-title" class="exam-title"></h2>
<div id="exam-root"></div>
<p class="buttons"><button type="button" class="btn btn-alt" id="finish">Terminer et voir la correction</button></p>
</section>
<script>var TRAINING = __DATA__;</script>
<script src="exam.js"></script>
<script src="entrainement.js"></script>"""


def training_page(training):
    data = json.dumps(training, ensure_ascii=False).replace("</", "<\\/")
    return make_page(
        f"Entraînement - {SITE_TITLE}",
        f"Séries d'entraînement corrigées et notées sur 20. {SCHOOL}, {YEAR}.",
        "",
        TRAINING_BODY.replace("__DATA__", data),
    )


def main():
    modules = load_all()
    src = ROOT / "entrainement"
    training = json.loads((src / "source" / "training.json").read_text(encoding="utf-8"))

    # Pages HTML régénérées ; assets recopiés (les liens ../assets/ restent valides)
    for _k, sub, _l, _c in KINDS:
        shutil.rmtree(DOCS / sub, ignore_errors=True)
    shutil.rmtree(DOCS / "assets", ignore_errors=True)
    shutil.copytree(ROOT / "assets", DOCS / "assets")
    # Jeux souris / clavier : pages autonomes recopiées telles quelles
    shutil.rmtree(DOCS / "jeux", ignore_errors=True)
    shutil.copytree(ROOT / "jeux", DOCS / "jeux")

    write(DOCS / "favicon.svg", FAVICON_SVG)
    (DOCS / "favicon.ico").write_bytes(make_favicon_ico())
    shutil.copy(src / "source" / "exam.js", DOCS / "exam.js")
    shutil.copy(src / "entrainement.js", DOCS / "entrainement.js")
    write(DOCS / "entrainement.html", training_page(training))
    write(DOCS / "index.html", index_page(modules, len(training)))
    counts = {k: 0 for k, *_ in KINDS}
    for mod_idx, mod in enumerate(modules):
        for num, chapter in enumerate(mod["chapters"], 1):
            for kind, folder, _l, _c in KINDS:
                if kind in chapter:
                    write(
                        DOCS / folder / f"{chapter[kind][0]}.html",
                        chapter_page(kind, mod_idx, num, mod["chapters"]),
                    )
                    counts[kind] += 1
    print(
        f"Site généré dans {DOCS} ({counts['cours']} cours, "
        f"{counts['exercices']} exercices, {counts['tp']} TP)"
    )


if __name__ == "__main__":
    main()

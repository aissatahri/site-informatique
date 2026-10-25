"""Génère le site statique dans docs/ à partir de cours/*.md et exercices/*.md.

Usage : python build.py
Dépendance : pip install markdown
"""
import html
import re
import shutil
import unicodedata
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"
SITE_TITLE = "Informatique - Tronc Commun"
SCHOOL = "Lycée Qadi Ibn Arabi"
TEACHER = "Aissa Tahri"
YEAR = "2026-2027"

MODULES = [
    "Généralités sur les systèmes informatiques",
    "Les logiciels",
    "Algorithme et programmation",
    "Réseaux et internet",
]
ACTIVE_MODULE = 0

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

PAGE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="icon" type="image/svg+xml" href="{root}favicon.svg">
<link rel="stylesheet" href="{root}style.css">
</head>
<body id="haut">
<header class="site-header">
<a class="brand" href="{root}index.html">
{logo}
<span class="brand-text"><strong>{school}</strong><span>{site_title}</span></span>
</a>
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

LABELS = {"Définition": "definition", "Exemple": "exemple", "Remarque": "remarque"}


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
        r"<blockquote>\s*<p><strong>(Définition|Exemple|Remarque)</strong>", repl, out
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


def load(folder):
    """Retourne {numéro de chapitre: (fichier, titre, html, sommaire)}."""
    pages = {}
    for path in sorted((ROOT / folder).glob("*.md")):
        m = re.match(r"ch(\d+)", path.name)
        if not m:
            continue
        text = path.read_text(encoding="utf-8")
        body, toc = render(text)
        pages[int(m.group(1))] = (path.stem, title_of(text, path.stem), body, toc)
    return pages


def logo_html():
    if (ROOT / "assets" / "logo.png").exists():
        return '<img class="logo" src="{root}assets/logo.png" alt="" width="44" height="44">'
    return LOGO_SVG


def breadcrumb(num):
    return (
        '<nav class="breadcrumb" aria-label="Fil d\'Ariane"><ol>'
        '<li><a href="../index.html">Accueil</a></li>'
        '<li><a href="../index.html#module-1">Module 1</a></li>'
        f'<li aria-current="page">Chapitre {num}</li>'
        "</ol></nav>"
    )


def switcher(kind, num, cours, exercices):
    items = []
    for k, label, pages in (("cours", "Cours", cours), ("exercices", "Exercices", exercices)):
        if num not in pages:
            continue
        if k == kind:
            items.append(f'<span class="tab current" aria-current="page">{label}</span>')
        else:
            items.append(f'<a class="tab" href="../{k}/{pages[num][0]}.html">{label}</a>')
    return '<div class="tabs">' + "".join(items) + "</div>" if len(items) > 1 else ""


def toc_html(toc):
    if len(toc) < 2:
        return ""
    lis = "".join(f'<li><a href="#{i}">{html.escape(t)}</a></li>' for i, t in toc)
    return f'<nav class="toc" aria-label="Table des matières"><h2>Table des matières</h2><ol>{lis}</ol></nav>'


def pager(kind, num, pages):
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


def index_page(cours, exercices):
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
    for i, name in enumerate(MODULES):
        active = i == ACTIVE_MODULE
        count = len(cours) if active else 0
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

    parts.append(f'<section class="chapters" id="module-{ACTIVE_MODULE + 1}">')
    parts.append(
        f"<h2>Module {ACTIVE_MODULE + 1} : {html.escape(MODULES[ACTIVE_MODULE])}</h2>"
    )
    for num in sorted(cours):
        stem, title, _, _ = cours[num]
        parts.append('<div class="chapter">')
        parts.append(f"<h3>{html.escape(title)}</h3>")
        parts.append('<p class="buttons">')
        parts.append(f'<a class="btn" href="cours/{stem}.html">Cours</a>')
        if num in exercices:
            parts.append(
                f'<a class="btn btn-alt" href="exercices/{exercices[num][0]}.html">Exercices</a>'
            )
        parts.append("</p></div>")
    parts.append("</section>")
    return make_page(
        f"{SITE_TITLE} - {SCHOOL}",
        f"{SITE_TITLE} au {SCHOOL} : cours et exercices corrigés, année scolaire {YEAR}.",
        "",
        "\n".join(parts),
    )


def chapter_page(kind, num, cours, exercices):
    pages = cours if kind == "cours" else exercices
    stem, title, body, toc = pages[num]
    label = "Cours" if kind == "cours" else "Exercices"
    inner = (
        breadcrumb(num)
        + switcher(kind, num, cours, exercices)
        + '<div class="layout">'
        + toc_html(toc)
        + f'<article class="content">{body}</article></div>'
        + pager(kind, num, pages)
    )
    return make_page(
        f"{title} - {SITE_TITLE}",
        f"{label} d'informatique, Tronc Commun : {title}. {SCHOOL}, {YEAR}.",
        "../",
        inner,
    )


def main():
    cours, exercices = load("cours"), load("exercices")

    # Pages HTML régénérées ; assets recopiés (les liens ../assets/ restent valides)
    for sub in ("cours", "exercices"):
        shutil.rmtree(DOCS / sub, ignore_errors=True)
    shutil.rmtree(DOCS / "assets", ignore_errors=True)
    shutil.copytree(ROOT / "assets", DOCS / "assets")

    write(DOCS / "favicon.svg", FAVICON_SVG)
    write(DOCS / "index.html", index_page(cours, exercices))
    for kind, pages in (("cours", cours), ("exercices", exercices)):
        for num, (stem, *_rest) in pages.items():
            write(DOCS / kind / f"{stem}.html", chapter_page(kind, num, cours, exercices))
    print(f"Site généré dans {DOCS} ({len(cours)} cours, {len(exercices)} exercices)")


if __name__ == "__main__":
    main()

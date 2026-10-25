"""Génère le site statique dans docs/ à partir de cours/*.md et exercices/*.md.

Usage : python build.py
Dépendance : pip install markdown
"""
import html
import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"
SITE_TITLE = "Informatique - Tronc Commun"

MODULES = [
    "Généralités sur les systèmes informatiques",
    "Les logiciels",
    "Algorithme et programmation",
    "Réseaux et internet",
]
ACTIVE_MODULE = 0

PAGE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{root}style.css">
</head>
<body>
{nav}
<main>
{body}
</main>
</body>
</html>
"""


def convert(text):
    md = markdown.Markdown(extensions=["tables", "fenced_code"])
    return md.convert(text)


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
    # Tableaux dans un conteneur à défilement horizontal
    out = out.replace("<table>", '<div class="table-wrap"><table>')
    return out.replace("</table>", "</table></div>")

def title_of(md_text, fallback):
    m = re.search(r"^#\s+(.+)$", md_text, re.M)
    return m.group(1).strip() if m else fallback


def load(folder):
    """Retourne {numéro de chapitre: (fichier, titre, html)}."""
    pages = {}
    for path in sorted((ROOT / folder).glob("*.md")):
        m = re.match(r"ch(\d+)", path.name)
        if not m:
            continue
        text = path.read_text(encoding="utf-8")
        pages[int(m.group(1))] = (path.stem, title_of(text, path.stem), render(text))
    return pages


def nav_bar(kind, num, cours, exercices):
    pages = cours if kind == "cours" else exercices
    nums = sorted(pages)
    i = nums.index(num)
    items = ['<a href="../index.html">Accueil</a>']
    other = exercices if kind == "cours" else cours
    if num in other:
        other_kind = "exercices" if kind == "cours" else "cours"
        label = "Exercices" if kind == "cours" else "Cours"
        items.append(f'<a href="../{other_kind}/{other[num][0]}.html">{label}</a>')
    if i > 0:
        p = pages[nums[i - 1]][0]
        items.append(f'<a href="{p}.html">← Précédent</a>')
    if i < len(nums) - 1:
        n = pages[nums[i + 1]][0]
        items.append(f'<a href="{n}.html">Suivant →</a>')
    return '<nav class="topnav">' + "".join(items) + "</nav>"


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def index_page(cours, exercices):
    parts = [f"<h1>{html.escape(SITE_TITLE)}</h1>", '<div class="modules">']
    for i, name in enumerate(MODULES):
        parts.append('<section class="module%s">' % ("" if i == ACTIVE_MODULE else " soon"))
        parts.append(f"<h2>Module {i + 1} : {html.escape(name)}</h2>")
        if i == ACTIVE_MODULE:
            for num in sorted(cours):
                stem, title, _ = cours[num]
                parts.append('<div class="chapter">')
                parts.append(f"<h3>{html.escape(title)}</h3>")
                parts.append('<p class="buttons">')
                parts.append(f'<a class="btn" href="cours/{stem}.html">Cours</a>')
                if num in exercices:
                    parts.append(
                        f'<a class="btn btn-alt" href="exercices/{exercices[num][0]}.html">Exercices</a>'
                    )
                parts.append("</p></div>")
        else:
            parts.append('<p><span class="badge">Bientôt</span></p>')
        parts.append("</section>")
    parts.append("</div>")
    return PAGE.format(title=SITE_TITLE, root="", nav="", body="\n".join(parts))


def main():
    cours, exercices = load("cours"), load("exercices")

    # Pages HTML régénérées ; assets recopiés (les liens ../assets/ restent valides)
    for sub in ("cours", "exercices"):
        shutil.rmtree(DOCS / sub, ignore_errors=True)
    shutil.rmtree(DOCS / "assets", ignore_errors=True)
    shutil.copytree(ROOT / "assets", DOCS / "assets")

    write(DOCS / "index.html", index_page(cours, exercices))
    for kind, pages in (("cours", cours), ("exercices", exercices)):
        for num, (stem, title, body) in pages.items():
            page = PAGE.format(
                title=f"{html.escape(title)} - {SITE_TITLE}",
                root="../",
                nav=nav_bar(kind, num, cours, exercices),
                body=body,
            )
            write(DOCS / kind / f"{stem}.html", page)
    print(f"Site généré dans {DOCS} ({len(cours)} cours, {len(exercices)} exercices)")


if __name__ == "__main__":
    main()


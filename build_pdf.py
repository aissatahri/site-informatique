#!/usr/bin/env python3
"""Génère les PDF téléchargeables (cours et TP) : filigrane au nom de l'enseignant
et mot de passe à l'ouverture.

Usage :  python build_pdf.py     (nécessite : pip install pymupdf markdown)
         puis python build.py    (ajoute les liens de téléchargement dans les pages)

Le mot de passe n'est jamais écrit dans le dépôt (public) : il est lu dans la
variable d'environnement PDF_PASSWORD ou dans le fichier pdf_password.txt (ignoré par git).
Les PDF sont écrits dans docs/pdf/.
"""

import os
import re
import secrets
import sys
import tempfile
from pathlib import Path

import build  # même rendu Markdown que le site

try:
    import pymupdf as fitz
except ImportError:  # anciennes versions
    import fitz

ROOT = build.ROOT
OUT = build.DOCS / "pdf"
KINDS_PDF = ("cours", "tp")  # les exercices n'ont pas de PDF

CSS = """
body { font-family: sans-serif; font-size: 10.5pt; line-height: 1.35; color: #1E2430; }
h1 { font-size: 19pt; color: #1F3A5F; margin: 4pt 0 6pt 0; }
h2 { font-size: 14pt; color: #1F3A5F; margin: 14pt 0 4pt 0; border-bottom: 1.5pt solid #C8962E; }
h3 { font-size: 12pt; color: #1F3A5F; margin: 10pt 0 3pt 0; }
h4 { font-size: 11pt; color: #1F3A5F; margin: 8pt 0 2pt 0; }
p { margin: 3pt 0; }
ul, ol { margin: 3pt 0; }
li { margin: 1.5pt 0; }
table { border-collapse: collapse; width: 100%; margin: 5pt 0; }
th { background-color: #1F3A5F; color: #ffffff; border: 0.5pt solid #1F3A5F; padding: 3pt; text-align: left; }
td { border: 0.5pt solid #aab3c0; padding: 3pt; vertical-align: top; }
tr { page-break-inside: avoid; }
blockquote { margin: 6pt 0; padding: 4pt 8pt; background-color: #eef0f3; border-left: 3pt solid #9aa3b0; }
.note-definition { background-color: #e8f0fb; border-left: 3pt solid #5b8fd6; }
.note-exemple { background-color: #fff8dc; border-left: 3pt solid #e0b73a; }
.note-retenir { background-color: #e9f7ee; border-left: 3pt solid #4caf72; }
.note-attention { background-color: #fff1e0; border-left: 3pt solid #f0993a; }
img { max-width: 100%; }
code { font-family: monospace; background-color: #eceff2; }
.meta { color: #5b6573; font-size: 9pt; margin: 0 0 6pt 0; }
"""


def password():
    pw = os.environ.get("PDF_PASSWORD", "").strip()
    if not pw:
        f = ROOT / "pdf_password.txt"
        if f.exists():
            pw = f.read_text(encoding="utf-8").strip()
    if not pw:
        raise SystemExit(
            "Mot de passe introuvable : définir PDF_PASSWORD ou créer pdf_password.txt "
            "(fichier ignoré par git)."
        )
    return pw


def to_pdf_html(body):
    """Adapte le HTML du site au moteur HTML de PyMuPDF."""
    body = body.replace("../assets/", "")  # images résolues depuis le dossier assets/
    body = re.sub(r'<h2 id="[^"]*"', "<h2", body)
    # petit espace après chaque tableau (évite qu'un titre suivant soit recouvert)
    body = body.replace('<div class="table-wrap">', "").replace(
        "</table></div>", '</table><p style="margin:0; font-size:4pt">&nbsp;</p>'
    )
    # liens relatifs vers les autres pages du site : texte seul
    body = re.sub(r'<a href="\.\./[^"]*">(.*?)</a>', r"\1", body, flags=re.S)
    return body


def flatten_gradients(svg_text):
    """MuPDF ne rend pas les dégradés SVG (fond noir) : on les remplace par la couleur moyenne."""
    grads = {}
    for m in re.finditer(r'<(?:linear|radial)Gradient[^>]*\bid="([^"]+)"[^>]*>(.*?)</(?:linear|radial)Gradient>', svg_text, re.S):
        cols = re.findall(r'stop-color="#([0-9a-fA-F]{6})"', m.group(2))
        if cols:
            rgb = [[int(c[i:i + 2], 16) for i in (0, 2, 4)] for c in cols]
            avg = [sum(v[k] for v in rgb) // len(rgb) for k in range(3)]
            grads[m.group(1)] = "#%02x%02x%02x" % tuple(avg)
    for gid, color in grads.items():
        svg_text = svg_text.replace(f"url(#{gid})", color)
    # Règles CSS de type .classe{...} : recopiées en attribut style (MuPDF ignore <style>)
    for m in re.finditer(r"\.([\w-]+)\s*\{([^}]*)\}", svg_text.split("</style>")[0] if "</style>" in svg_text else ""):
        cls, decls = m.group(1), m.group(2).strip()
        svg_text = re.sub(rf'class="{cls}"', f'class="{cls}" style="{decls}"', svg_text)
    return svg_text


def rasterize_svgs(html_text, folder):
    """Les schémas SVG sont convertis en PNG (le moteur HTML les rend mal)."""
    for m in set(re.findall(r'src="([^"]+\.svg)"', html_text)):
        src = ROOT / "assets" / m
        if not src.exists():
            continue
        text = src.read_text(encoding="utf-8")
        text = flatten_gradients(text)
        svg = fitz.open(stream=text.encode("utf-8"), filetype="svg")
        pdf = fitz.open("pdf", svg.convert_to_pdf())
        png = folder / (m[:-4] + ".png")
        png.parent.mkdir(parents=True, exist_ok=True)
        pdf[0].get_pixmap(dpi=170, alpha=False).save(str(png))
        svg.close()
        pdf.close()
        html_text = html_text.replace(m, m[:-4] + ".png")
    return html_text


def build_one(title, body, dest, pw):
    meta = f"{build.SITE_TITLE} · {build.SCHOOL} · {build.TEACHER} · {build.YEAR}"
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        html_doc = rasterize_svgs(f'<p class="meta">{meta}</p>' + to_pdf_html(body), Path(tmp))
        archive = fitz.Archive(str(ROOT / "assets"))
        archive.add(fitz.Archive(tmp))
        story = fitz.Story(html=html_doc, user_css=CSS, archive=archive)
        mediabox = fitz.paper_rect("a4")
        where = mediabox + (48, 48, -48, -56)
        raw = Path(tmp) / "raw.pdf"
        writer = fitz.DocumentWriter(str(raw))
        more = 1
        while more:
            dev = writer.begin_page(mediabox)
            more, _ = story.place(where)
            story.draw(dev)
            writer.end_page()
        writer.close()

        doc = fitz.open(str(raw))
        n = len(doc)
        for i, page in enumerate(doc, 1):
            r = page.rect
            # Filigrane diagonal : nom de l'enseignant
            page.insert_text(
                fitz.Point(r.width * 0.16, r.height * 0.62),
                build.TEACHER,
                fontsize=64,
                fontname="helv",
                color=(0.55, 0.6, 0.7),
                fill_opacity=0.2,
                morph=(fitz.Point(r.width / 2, r.height / 2), fitz.Matrix(-38)),
                overlay=True,
            )
            # Pied de page
            foot = f"© {build.TEACHER} - {build.SCHOOL} - Document réservé aux élèves"
            page.insert_text(fitz.Point(48, r.height - 30), foot, fontsize=8, fontname="helv", color=(0.35, 0.4, 0.45))
            page.insert_text(fitz.Point(r.width - 100, r.height - 30), f"Page {i} / {n}", fontsize=8, fontname="helv", color=(0.35, 0.4, 0.45))
        doc.set_metadata({"title": title, "author": build.TEACHER, "subject": build.SITE_TITLE})
        dest.parent.mkdir(parents=True, exist_ok=True)
        doc.save(
            str(dest),
            encryption=fitz.PDF_ENCRYPT_AES_256,
            user_pw=pw,                      # mot de passe d'ouverture (donné aux élèves)
            owner_pw=secrets.token_hex(16),  # propriétaire : jamais conservé
            permissions=fitz.PDF_PERM_PRINT | fitz.PDF_PERM_ACCESSIBILITY,
            garbage=3,
            deflate=True,
        )
        doc.close()
    return n


def main():
    pw = password()
    modules = build.load_all()
    OUT.mkdir(parents=True, exist_ok=True)
    wanted = set()
    for mod in modules:
        for chapter in mod["chapters"]:
            for kind in KINDS_PDF:
                if kind not in chapter:
                    continue
                stem, title, body, _toc = chapter[kind]
                wanted.add(f"{stem}.pdf")
                n = build_one(title, body, OUT / f"{stem}.pdf", pw)
                print(f"  {stem}.pdf ({n} pages)")
    # PDF devenus inutiles
    for old in OUT.glob("*.pdf"):
        if old.name not in wanted:
            old.unlink()
            print(f"  supprimé : {old.name}")
    print(f"PDF générés dans {OUT}")


if __name__ == "__main__":
    sys.exit(main())

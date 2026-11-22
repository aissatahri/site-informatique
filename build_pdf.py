#!/usr/bin/env python3
"""Génère les PDF téléchargeables (cours et TP) : filigrane au nom de l'enseignant
et mot de passe à l'ouverture.

Principe : les pages du site (docs/cours, docs/tp) sont imprimées en PDF par Microsoft Edge
(ou Chrome) en mode « sans fenêtre », avec la feuille de style d'impression du site ; puis
PyMuPDF ajoute le filigrane, le pied de page et le chiffrement.

Usage :  python build.py          (génère les pages HTML)
         python build_pdf.py      (nécessite : pip install pymupdf ; Edge ou Chrome installé)
         python build.py          (ajoute les boutons de téléchargement)

Le mot de passe n'est jamais écrit dans le dépôt (public) : il est lu dans la
variable d'environnement PDF_PASSWORD ou dans le fichier pdf_password.txt (ignoré par git).
Navigateur : détecté automatiquement, ou chemin donné dans la variable BROWSER.
Les PDF sont écrits dans docs/pdf/.
"""

import os
import secrets
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import build  # constantes et configuration du site

try:
    import pymupdf as fitz
except ImportError:  # anciennes versions
    import fitz

ROOT = build.ROOT
OUT = build.DOCS / "pdf"
KINDS_PDF = ("cours", "tp")  # les exercices n'ont pas de PDF

BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]


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


def find_browser():
    env = os.environ.get("BROWSER", "").strip()
    candidates = ([env] if env else []) + BROWSERS
    for name in ("msedge", "chrome", "google-chrome", "chromium"):
        found = shutil.which(name)
        if found:
            candidates.append(found)
    for c in candidates:
        if c and Path(c).exists():
            return c
    raise SystemExit("Edge ou Chrome introuvable : installer l'un des deux ou définir BROWSER.")


def print_to_pdf(browser, page_html, dest):
    """Imprime une page HTML en PDF avec le navigateur (feuille de style @media print du site)."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        dest.unlink()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as profile:
        cmd = [
            browser, "--headless", "--disable-gpu", "--no-pdf-header-footer",
            "--print-to-pdf-no-header", f"--user-data-dir={profile}",
            f"--print-to-pdf={dest}", page_html.resolve().as_uri(),
        ]
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            proc.wait(timeout=90)
        except subprocess.TimeoutExpired:
            pass  # le PDF est parfois déjà écrit alors que le navigateur ne se ferme pas
        time.sleep(1)
        if proc.poll() is None:
            proc.kill()
            proc.wait()
    if not dest.exists() or dest.stat().st_size == 0:
        raise SystemExit(f"Échec de l'impression PDF : {page_html}")


def protect(raw, dest, title, pw):
    """Ajoute filigrane, pied de page, métadonnées, puis chiffre le PDF."""
    doc = fitz.open(str(raw))
    n = len(doc)
    foot = f"© {build.TEACHER} - {build.SCHOOL} - Document réservé aux élèves"
    for i, page in enumerate(doc, 1):
        r = page.rect
        page.insert_text(  # filigrane diagonal : nom de l'enseignant
            fitz.Point(r.width * 0.16, r.height * 0.62),
            build.TEACHER,
            fontsize=64,
            fontname="helv",
            color=(0.55, 0.6, 0.7),
            fill_opacity=0.2,
            morph=(fitz.Point(r.width / 2, r.height / 2), fitz.Matrix(-38)),
            overlay=True,
        )
        page.insert_text(fitz.Point(40, r.height - 24), foot, fontsize=8, fontname="helv", color=(0.35, 0.4, 0.45))
        page.insert_text(fitz.Point(r.width - 92, r.height - 24), f"Page {i} / {n}", fontsize=8, fontname="helv", color=(0.35, 0.4, 0.45))
    doc.set_metadata({"title": title, "author": build.TEACHER, "subject": build.SITE_TITLE})
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
    browser = find_browser()
    modules = build.load_all()
    OUT.mkdir(parents=True, exist_ok=True)
    wanted = set()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        for mod in modules:
            for chapter in mod["chapters"]:
                for kind in KINDS_PDF:
                    if kind not in chapter:
                        continue
                    stem, title, _body, _toc = chapter[kind]
                    page = build.DOCS / kind / f"{stem}.html"
                    if not page.exists():
                        raise SystemExit(f"{page} introuvable : lancer d'abord python build.py")
                    raw = Path(tmp) / f"{stem}.pdf"
                    print_to_pdf(browser, page, raw)
                    n = protect(raw, OUT / f"{stem}.pdf", title, pw)
                    wanted.add(f"{stem}.pdf")
                    print(f"  {stem}.pdf ({n} pages)")
    for old in OUT.glob("*.pdf"):  # PDF devenus inutiles
        if old.name not in wanted:
            old.unlink()
            print(f"  supprimé : {old.name}")
    print(f"PDF générés dans {OUT}")


if __name__ == "__main__":
    sys.exit(main())

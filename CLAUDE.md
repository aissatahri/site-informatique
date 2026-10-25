# Site de cours d'informatique - Tronc Commun

## Contexte
Site web pour mes élèves de Tronc Commun (Maroc).
Module 1 : Généralités sur les systèmes informatiques.
Langue : français. Les élèves consultent surtout sur téléphone.

## Structure
- /ressources : PDF originaux (ne pas modifier)
- /cours : chapitres en Markdown
- /exercices : exercices et corrections
- /assets : images et CSS
- Créer ces dossiers s'ils n'existent pas.

## Commandes
- `python build.py` : régénère le site (nécessite `pip install markdown`).
- Le site est dans docs/, ne jamais éditer docs/*.html à la main
  (modifier cours/ ou exercices/ puis relancer la commande).
- Aperçu local : `python -m http.server 8000 --directory docs` puis http://localhost:8000

## Règles
- Site statique : HTML et CSS simples, sans framework.
- Ne jamais changer le contenu pédagogique sans me le demander.
- Chaque exercice a un bouton « Afficher la correction ».
- Travailler une petite tâche à la fois et attendre ma validation.
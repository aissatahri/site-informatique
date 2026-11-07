# Site de cours d'informatique - Tronc Commun

## Contexte
Site web pour mes élèves de Tronc Commun (Maroc).
Module 1 : Généralités sur les systèmes informatiques.
Langue : français. Les élèves consultent surtout sur téléphone.

## Structure
- /ressources : PDF originaux (ne pas modifier)
- /cours : chapitres en Markdown
- /exercices : exercices et corrections
- /tp : travaux pratiques en Markdown (pages générées dans docs/tp/)
- /assets : images et CSS
- Créer ces dossiers s'ils n'existent pas.

## Ajouter un chapitre
1. Déposer les fichiers Markdown dans cours/ (obligatoire), exercices/ et tp/ (optionnels).
2. Dans build.py, section CONFIGURATION (MODULES), ajouter le chapitre au module voulu :
   {"cours": "nom", "exercices": "nom", "tp": "nom"} (noms sans .md).
3. Lancer `python build.py` : accueil, navigation et Précédent/Suivant sont mis à jour.

## Commandes
- `python build.py` : régénère le site (nécessite `pip install markdown`).
- Le site est dans docs/, ne jamais éditer docs/*.html à la main
  (modifier cours/ ou exercices/ puis relancer la commande).
- Aperçu local : `python -m http.server 8000 --directory docs` puis http://localhost:8000

## Règles
- Site statique : HTML et CSS simples, sans framework.
- Ne jamais changer le contenu pédagogique sans me le demander.
- Chaque exercice a un bouton « Afficher la correction ».
- entrainement/source/ = données de la page d'entraînement ;
  ne jamais copier exams.json ni les corrigés de contrôle dans ce projet.
- Travailler une petite tâche à la fois et attendre ma validation.
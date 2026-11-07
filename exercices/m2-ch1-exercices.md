# Exercices du chapitre 1 : Système d'exploitation

## Exercice 1 : Questions de cours

**1.** Définir un système d'exploitation.

<details>
<summary>Afficher la correction</summary>

Le système d'exploitation est l'ensemble des programmes qui gèrent les ressources matérielles et logicielles de l'ordinateur et servent d'intermédiaire entre l'utilisateur, les applications et le matériel.

</details>

**2.** Citer quatre fonctions principales d'un système d'exploitation.

<details>
<summary>Afficher la correction</summary>

Gestion du processeur, de la mémoire, des périphériques, des fichiers ; interface utilisateur ; sécurité. (Quatre au choix.)

</details>

**3.** Citer trois systèmes d'exploitation pour ordinateur et deux pour smartphone.

<details>
<summary>Afficher la correction</summary>

Ordinateur : Windows 11, Linux (Ubuntu), macOS.<br>
Smartphone : Android, iOS.

</details>

**4.** Quelle est la différence entre une interface graphique et une interface en ligne de commande ?

<details>
<summary>Afficher la correction</summary>

Interface graphique : on utilise la souris, les fenêtres et les icônes.<br>
Ligne de commande : on tape des commandes au clavier (cmd, PowerShell, Terminal).

</details>

**5.** Qu'est-ce qu'un pilote (driver) ?

<details>
<summary>Afficher la correction</summary>

Un pilote est un petit programme qui permet au système d'exploitation de communiquer avec un périphérique (imprimante, carte graphique…).

</details>

## Exercice 2 : Vrai ou Faux

Répondre par **Vrai** ou **Faux** et corriger les affirmations fausses.

**1.** Word est un système d'exploitation.

<details>
<summary>Afficher la correction</summary>

**Faux.** Word est un logiciel d'application (traitement de texte).

</details>

**2.** Le système d'exploitation est chargé en mémoire au démarrage de l'ordinateur.

<details>
<summary>Afficher la correction</summary>

**Vrai.**

</details>

**3.** Windows 11 est un système multitâche.

<details>
<summary>Afficher la correction</summary>

**Vrai.**

</details>

**4.** Supprimer un raccourci supprime le programme associé.

<details>
<summary>Afficher la correction</summary>

**Faux.** Un raccourci ne fait que pointer vers le programme ; celui-ci reste installé.

</details>

**5.** Un fichier supprimé d'une clé USB peut être restauré depuis la Corbeille.

<details>
<summary>Afficher la correction</summary>

**Faux.** Les fichiers supprimés d'une clé USB sont supprimés définitivement.

</details>

**6.** L'extension .xlsx correspond à un classeur Excel.

<details>
<summary>Afficher la correction</summary>

**Vrai.**

</details>

**7.** Le raccourci Windows + E ouvre les Paramètres.

<details>
<summary>Afficher la correction</summary>

**Faux.** Windows + E ouvre l'Explorateur de fichiers ; les Paramètres s'ouvrent avec Windows + I.

</details>

## Exercice 3 : QCM

Choisir la (ou les) bonne(s) réponse(s).

**1.** Le bouton Démarrer de Windows 11 se trouve : a) en haut à gauche ; b) sur la barre des tâches ; c) dans la Corbeille.

<details>
<summary>Afficher la correction</summary>

**b)**

</details>

**2.** Pour afficher le menu contextuel, on fait : a) un double-clic ; b) un clic droit ; c) un glisser-déposer.

<details>
<summary>Afficher la correction</summary>

**b)**

</details>

**3.** Le raccourci pour renommer un fichier est : a) F2 ; b) F5 ; c) Ctrl + R.

<details>
<summary>Afficher la correction</summary>

**a)**

</details>

**4.** Lequel de ces noms de fichier est incorrect ? a) cours_TC.docx ; b) note?.txt ; c) photo 1.jpg.

<details>
<summary>Afficher la correction</summary>

**b)** Le caractère « ? » est interdit dans un nom de fichier.

</details>

**5.** Pour sélectionner des fichiers non contigus, on maintient : a) Maj ; b) Alt ; c) Ctrl.

<details>
<summary>Afficher la correction</summary>

**c)**

</details>

**6.** Le Gestionnaire des tâches s'ouvre avec : a) Ctrl + Maj + Échap ; b) Alt + F4 ; c) Windows + D.

<details>
<summary>Afficher la correction</summary>

**a)**

</details>

## Exercice 4 : Associer

Associer chaque extension (colonne A) au type de fichier correspondant (colonne B).

| A : Extension | B : Type de fichier |
|---|---|
| 1. .mp3 | a. Présentation |
| 2. .pptx | b. Image |
| 3. .png | c. Programme exécutable |
| 4. .exe | d. Musique |
| 5. .pdf | e. Document portable |

<details>
<summary>Afficher la correction</summary>

1 → d ; 2 → a ; 3 → b ; 4 → c ; 5 → e.

</details>

## Exercice 5 : Arborescence et chemins

Ahmed a organisé son disque D: de la façon suivante :

```
D:
├── Lycee
│   ├── Maths
│   │   └── equations.docx
│   └── Informatique
│       ├── Cours
│       │   └── windows11.pdf
│       └── TP
│           └── tp1.docx
└── Loisirs
    └── Photos
        └── plage.jpg
```

**1.** Quelle est la racine de cette arborescence ?

<details>
<summary>Afficher la correction</summary>

La racine est **D:**.

</details>

**2.** Citer les sous-dossiers du dossier Informatique.

<details>
<summary>Afficher la correction</summary>

**Cours** et **TP**.

</details>

**3.** Écrire le chemin d'accès complet du fichier windows11.pdf.

<details>
<summary>Afficher la correction</summary>

`D:\Lycee\Informatique\Cours\windows11.pdf`

</details>

**4.** Écrire le chemin d'accès complet du fichier plage.jpg.

<details>
<summary>Afficher la correction</summary>

`D:\Loisirs\Photos\plage.jpg`

</details>

**5.** Ahmed déplace tp1.docx dans le dossier Cours. Donner son nouveau chemin.

<details>
<summary>Afficher la correction</summary>

`D:\Lycee\Informatique\Cours\tp1.docx`

</details>

**6.** Combien y a-t-il de dossiers (sans compter la racine) ? Combien de fichiers ?

<details>
<summary>Afficher la correction</summary>

**7 dossiers** (Lycee, Maths, Informatique, Cours, TP, Loisirs, Photos) et **4 fichiers**.

</details>

## Exercice 6 : Les éléments de l'interface

Compléter le tableau en indiquant le nom de l'élément de Windows 11 décrit.

| Description | Nom de l'élément |
|---|---|
| Bande en bas de l'écran contenant les icônes des applications ouvertes et épinglées | ……………………… |
| Zone à droite de la barre des tâches affichant l'heure, le volume et le réseau | ……………………… |
| Endroit où sont placés les fichiers supprimés du disque dur | ……………………… |
| Application qui regroupe tous les réglages de Windows | ……………………… |
| Bouton qui permet de placer la fenêtre dans la barre des tâches sans la fermer | ……………………… |

<details>
<summary>Afficher la correction</summary>

Barre des tâches ; Zone de notification ; Corbeille ; Paramètres ; Réduire.

</details>

## Exercice 7 : Situation-problème

Salma a enregistré son exposé « exposé_SVT.docx » sur le bureau. Elle souhaite le ranger dans un dossier « SVT » situé dans Documents, tout en gardant une copie sur sa clé USB (lecteur E:).

**1.** Décrire les étapes pour créer le dossier SVT dans Documents.

<details>
<summary>Afficher la correction</summary>

Ouvrir l'Explorateur (Windows + E) › Documents › clic droit dans une zone vide › Nouveau › Dossier › taper SVT › Entrée.

</details>

**2.** Quelle opération (copier ou déplacer) doit-elle utiliser pour ranger l'exposé dans SVT ? Justifier.

<details>
<summary>Afficher la correction</summary>

**Déplacer** (Couper/Coller) : elle veut ranger le fichier, il ne doit plus rester sur le bureau.

</details>

**3.** Quelle opération doit-elle utiliser pour la clé USB ? Donner les raccourcis clavier correspondants.

<details>
<summary>Afficher la correction</summary>

**Copier** : le fichier doit rester dans SVT et exister aussi sur la clé. Ctrl + C puis, dans E:, Ctrl + V.

</details>

**4.** Par erreur, elle supprime l'exposé du dossier SVT. Comment peut-elle le récupérer ?

<details>
<summary>Afficher la correction</summary>

Ouvrir la Corbeille, faire un clic droit sur exposé_SVT.docx › Restaurer. (Ctrl + Z fonctionne aussi juste après la suppression.)

</details>

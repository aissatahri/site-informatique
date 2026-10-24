# Chapitre 1 : Définition et vocabulaire de base

*Module 1 : Généralités sur les systèmes informatiques — TAHRI Aissa*

## I. Définition de l’information

Une information est une connaissance ou donnée ayant un sens, que l'on peut traiter, stocker et transmettre.

- L’information prend plusieurs formes : texte, image, son
- On peut dire que « *une information est un support de connaissance* »

## II. Traitement de l’information

### 1. Définition

- Un traitement est l’ensemble des techniques permettant de stocker, d’élaborer, de modifier, de manipuler… les informations.
- *Exemple : Traitement de texte(s) : ensemble des techniques informatiques qui permettent la saisie, la mémorisation, la correction, l'actualisation, la mise en page et la diffusion de textes.*

### 2. Le schéma de traitement

[SCHÉMA : trois cases reliées. Une case « Donnée (entrée) » à gauche et une case « Résultat (sortie) » à droite, reliées par une grosse flèche horizontale allant de la donnée vers le résultat. Une case « Traitement » au-dessus, avec une petite flèche vers le bas pointant sur la grosse flèche.]

**Exemple**

[SCHÉMA : même disposition. À gauche la case « What’s your name ? » (entrée), à droite la case « Quel est votre nom ? » (sortie), reliées par une grosse flèche horizontale. Au-dessus, la case « Traduction » avec une flèche vers le bas pointant sur la grosse flèche.]

### 3. Traitement automatique

- Un traitement automatique est un traitement effectué par un système informatique (exemple : l’ordinateur)
- ► Un traitement automatique = Traitement effectué sans intervention humaine ; ≠ traitement manuel

## III. Informatique

- **Définition** : l’informatique est la science de traitement automatique de l’information par ordinateur
- **Remarque** : le terme « informatique » vient de la contraction de deux mots « information » et « Automatique » – Informatique = information + automatique

## IV. Système informatique

a) **Le matériel (Hardware)** : est l’ensemble des éléments physiques d'un système informatique (il est tous les éléments qu’on peut voir ou toucher)

b) **Le logiciel (Software)** : (abstrait) c’est l’ensemble des programmes, des procédés et des règles relatifs au fonctionnement d'un ensemble de traitement de l'information.

c) **Système informatique** : c’est un ensemble de moyens matériels (hardware) et logiciels (software) permettant d’assurer le traitement automatique de l’information

Exemples : calculatrice programmable, téléphone portable, ordinateur portable, tablette, console de jeux …

## V. Codage de l’information

### 1. Chiffres binaires

Le codage de l’information est la Transcription (d'une information) dans un langage utilisable par un ordinateur, et comme toutes les communications à l’intérieur d’un ordinateur sont faites par des signaux électriques, magnétiques ou optiques, Ces signaux ont deux états seulement :

- 0 → éteint, ouvert, sud…
- 1 → allumé, fermé, nord …

Les chiffres 0 et 1 dites : chiffres binaires

### 2. Information binaire

Une information binaire est une suite composée des chiffres binaires (0 et 1 : base binaire)

### 3. Le bit (de l’anglais : binary digit) :

C’est la plus petite unité d’information (0 ou 1) manipulable par une machine numérique

### 4. Représentation de l’information

- Avec 1 bit on peut représenter 2 = 2<sup>1</sup> informations possibles 0 ou 1.
- Avec 2 bit on peut représenter 4 = 2<sup>2</sup> informations possibles 00, 01, 10 ou 11.
- …
- En général, avec n bits on peut représenter 2<sup>n</sup> informations possibles

**Représentation des nombres**

| Nombre | Représentation sur 8 bits |
|---|---|
| 0 | 0 0 0 0 0 0 0 0 |
| 1 | 0 0 0 0 0 0 0 1 |
| 2 | 0 0 0 0 0 0 1 0 |
| 3 | 0 0 0 0 0 0 1 1 |
| 4 | 0 0 0 0 0 1 0 0 |
| 5 | 0 0 0 0 0 1 0 1 |
| …. | |
| 255 | 1 1 1 1 1 1 1 1 |

**Exercice :** convertir en décimale les nombres suivants :

- 10011 = ……………………
- 110101 = …………………..

Convertir en binaire les nombres suivants :

- 59 = ……………………
- 171 = ……………………

**Représentation des caractères**

| Nombre | Représentation sur 8 bits |
|---|---|
| ‘A’ | 0 1 0 0 0 0 0 1 |
| ‘a’ | 0 1 1 0 0 0 0 1 |
| ‘0’ | 0 0 1 1 0 0 0 0 |
| ‘?’ | 0 0 1 1 1 1 1 1 |
| ‘&’ | 0 0 1 0 0 1 1 0 |
| ‘@’ | 0 1 0 0 0 0 0 0 |
| …. | |

### 5. L’octet (en anglais : Byte) :

L’Octet est la plus petite unité de **mesure** de l’information, il est composé de 8 bits.

➔ Avec 1 octet (= 8bits) on peut représenter 2<sup>8</sup> = 256 informations

### 6. Les unités de mesure multiples de l’octet

- Kilo-octet : ➔ 1ko = 2<sup>10</sup> octets ≈ 1000 octet
- Méga-octet : ➔ 1Mo = 2<sup>10</sup> Ko ≈ 1000 Ko
- Giga-octet : ➔ 1Go = 2<sup>10</sup> Mo ≈ 1000 Mo
- Téraoctet : ➔ 1To = 2<sup>10</sup> Go ≈ 1000 Go

**Remarque :**

Pour convertir un nombre de la base binaire à la base décimale on utilise la méthode suivante :

(a<sub>n</sub> a<sub>n-1</sub> ... a<sub>1</sub> a<sub>0</sub>)<sub>2</sub> = a<sub>n</sub>×2<sup>n</sup> + a<sub>n-1</sub>×2<sup>n-1</sup> + … + a<sub>1</sub>×2<sup>1</sup> + a<sub>0</sub>×2<sup>0</sup>

**Exemple :** (1001)<sub>2</sub> = 1×2<sup>3</sup> + 0×2<sup>2</sup> + 0×2<sup>1</sup> + 1×2<sup>0</sup> = (9)<sub>10</sub>

Pour convertir un nombre de la base décimale à la base binaire on divise le nombre décimal par 2, puis on divise le quotient obtenu par 2 et ainsi de suite jusqu'à l’obtention d'un quotient nul. La suite des restes obtenus correspond aux chiffres dans la base 2.

**Exemple :** (10)<sub>10</sub> = (1010)<sub>2</sub>

[SCHÉMA : divisions successives de 10 par 2. 10 ÷ 2 = 5 reste 0 ; 5 ÷ 2 = 2 reste 1 ; 2 ÷ 2 = 1 reste 0 ; 1 ÷ 2 = 0 reste 1. Une flèche en diagonale indique de lire les restes de bas en haut : 1010.]

**Exercice :**

Représenter en binaire les caractères suivants :

- B : …………………………….
- C : …………………………….
- E : …………………………….
- c : …………………………….
- f : …………………………….

Sachant que : 1 + 1 = 10 et 1 + 0 = 1

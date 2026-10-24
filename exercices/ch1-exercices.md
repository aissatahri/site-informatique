# Chapitre 1 : Exercices

*Module 1 : Généralités sur les systèmes informatiques*

## Exercice 1 : Binaire → décimal

Convertir en décimal les nombres suivants :

1. 10011 = ……………………
2. 110101 = ……………………

<details>
<summary>Afficher la correction</summary>

- 10011 = 16 + 2 + 1 = **19**
- 110101 = 32 + 16 + 4 + 1 = **53**

*Méthode : on additionne les puissances de 2 correspondant aux bits égaux à 1.*

</details>

## Exercice 2 : Décimal → binaire

Convertir en binaire les nombres suivants :

1. 59 = ……………………
2. 171 = ……………………

<details>
<summary>Afficher la correction</summary>

- 59 = 32 + 16 + 8 + 2 + 1 = **111011**, soit **00111011** sur 8 bits
- 171 = 128 + 32 + 8 + 2 + 1 = **10101011**

*Méthode : on décompose le nombre en puissances de 2 (ou par divisions successives par 2, en lisant les restes de bas en haut).*

</details>

## Exercice 3 : Représentation des caractères

Représenter en binaire les caractères suivants :

1. B : …………………………….
2. C : …………………………….
3. E : …………………………….
4. c : …………………………….
5. f : …………………………….

Sachant que : A = 01000001 et a = 01100001

Sachant que : 1 + 1 = 10 et 1 + 0 = 1

<details>
<summary>Afficher la correction</summary>

Sachant que A = 01000001 et a = 01100001 :

- B = **01000010**
- C = **01000011**
- E = **01000101**
- c = **01100011**
- f = **01100110**

*Méthode : B = A + 1 ; C = A + 2 ; E = A + 4 ; c = a + 2 ; f = a + 5 (chaque lettre : code de A ou a + son rang dans l'alphabet moins 1, addition en binaire).*

</details>

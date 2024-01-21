# Platformio

En gros ça vous aide la vie.

## Création d'un projet:

Afin de créer un projet platformio, choisisez un projet qui existe déjà et qui est semblable à votre projet (type de la carte électronique) et dupliquez ce projet. N'oubliez pas de renommer le dosser ainsi que modifier les paramètres dans le menu de platformio.

## Boards et framework

Une board est le type de cartes électroniques, par exemple arduino nano, esp32 ou stm32. Je vous invite à regarder dans le menu platformio toutes les possibilités.
Un framework est la base de programmation de votre projet. Pour simplifier notre boulot, on utilise la framework d'arduino cela veut dire que nos cartes se programme avec le même language de programmation qu'un arduino basique.

## Structure d'un projet Platformio
```
projet/                 - Dossier du projet
├─ .vscode/             - Config de VsCode
├─ include/             - Dossier de vos fichiers .h (en c++)
├─ lib/                 - Librairies privées propre au projet
├─ src/                 - Dossier de vos fichiers sources .c ou .cpp
├─ test/                - Jsp ne l'utilisez pas
├─ .gitignore           - Pour git, recense les dossier à ne pas mettre dans le github
├─ platformio.ini       - Configuration de votre projet
```


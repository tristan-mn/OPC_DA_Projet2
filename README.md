# Projet 2 OPENCLASSROOMS : Utilisez les bases de Python pour l'analyse de marché

## Contexte :  

Dans le cadre de ce projet, j'ai créé un outil de scraping avec le langage Python visant à récupérer des informations sur le site http://books.toscrape.com/.  

Vous pouvez donc trouver ici un fichier de scraping.  

Ce fichier permet de récupérer les informations de tous les livres du site et les écrit dans un fichier csv dédié à chaque catégorie(genre littéraire). 

De plus, il récupère les fichiers image de tous les livres et les enregistre dans un dossier images. 

------------------  

## Installation

* ### 1 - installer Python 3  

  sudo apt-get install python3 python3-venv python3-pip

* ### 2 - mise ne place de l'environnement virtuel  

Accéder au répertoire du projet puis taper cette commande pour créer l'environnement    

    python3 -m venv env

* ### 3 - Ouverture de l'environnement virtuel et ajout des modules 

  source env/bin/activate  

  pip install -r requirements.txt

-----------------  


## Autheur  
    Montemitro Tristan

------------------  

## Utilisation du programme :  

* ### 1 - Lancement

       python3 scrap.py

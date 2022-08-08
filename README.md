# appli_cli_meteo
Application CLI meteo

Application météo en ligne de commande.

Lancer le programme dans le terminal avec : python weather.py <nom_de_la_ville/pays>

## Détails
- Création d'interfaces de ligne de commande à l'aide de argparse
- Lire des données publiques sur Internet avec des API (OpenWeather)
- Intégration des API dans le code Python 
- Travailler avec des données JSON
- Importation de modules et de bibliothèques
- Définir ses propres fonctions
- Gestion des erreurs avec les exceptions Python
- Formater votre texte à l'aide de f-strings
- Utiliser des expressions conditionnelles

## Aperçu
[appli_cli_meteo](images/appli_cli_meteo_references_grande_taille.png)

## Suite du projet
- Personnaliser le style
- Enrichir le bulletin météo avec plus d'informations à partir de données de réponse JSON
- Refactorisez la CLI à l'aide de Typer
-Installez une version supérieure à 3.10 et remplacez le code dans _select_weather_display_params() par une déclaration match...case
- Empaquetez la CLI pour la distribution à l'aide de Python zipapp ou créer un package à publier sur PyPi

## Auteur
Virginie Evrard, mars 2022

## Remerciements
J'ai réalisé mon application météo en suivant les explications d'un article sur Real Python.
Merci à l'auteur Martin Breuss, d'avoir écrit cet article 'Raining Outside? Build a Weather CLI App With Python'
sur le site de Real Python, qui m'aura permis d'améliorer mes compétences en programmation Python.
Lien pour l'aricle : https://realpython.com/build-a-python-weather-app-cli/
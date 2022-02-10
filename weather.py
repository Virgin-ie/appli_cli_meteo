import argparse
import json
import sys
from configparser import ConfigParser
from urllib import error, parse, request

import style

# une constante s'écrit en majuscule
# défini 'BASE_WEATHER_API_URL' comme une constante vu que tous les appels API passerons par cette base de l'url
BASE_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

# codes/ID pour les conditions météorologiques
# plus d'info : https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
THUNDERSTORM = range(200, 300)   # ORAGE
DRIZZLE = range(300, 400)        # BRUINE
RAIN = range(500, 600)           # PLUIE
SNOW = range(600, 700)           # NEIGE
ATMOSPHERE = range(700, 800)     # ATMOSPHERE
CLEAR = range(800, 801)          # CLAIR/DEGAGER
CLOUDY = range(801, 900)         # NUAGEUX


def read_user_cli_args():
    """
    Gère les interactions des utilisateurs CLI.

    terminal :
    python weather.py -h Pour obtenir de l'aide et connaître les options disponibles
                      - i OU --imperial Demander la température en unités impérials (Fahrenheit)
    :return:
        argparse.Namespace: Populated namespace object
    """
    # créer une instance de 'argparse.ArgumentParser', à laquelle on transmet une description facultative de l'analyseur
    # renvoie les résultats d'un appel à '.parse_args()', qui seront les valeurs saisies par l'utilisateur
    parser = argparse.ArgumentParser(
        description="Obtenir des informations sur la météo et la température d'une ville"
    )
    # l'argument 'city' prendra une ou plusieurs entrées séparées par des espaces, en définissant le nombres d'arguments
    # 'nargs' sur '+', on autorise l'utilisateur à transmettre des noms de ville composés de plusieurs mots ex: New York
    # l'argument de mot-clé 'help' définit le texte d'aide qui est ensuite rendu disponible via l'indicateur '-h'
    parser.add_argument(
        "city", nargs="+", type=str, help="Entrer le nom de la ville"
    )
    # définit l'argument booléen facultatif 'imperial'
    # définit l'argument du mot-clé 'action' sur 'store-true', ce qui signifie que la valeur de 'imperial' sera 'True'
    # si les utilisateurs ajoutent l'indicateur facultatif, et 'False' s'ils ne le font pas
    parser.add_argument(
        "-i",
        "--imperial",
        action="store_true",
        help="Afficher la température en unités impériales (Fahrenheit)"
    )
    return parser.parse_args()


def build_weather_query(city_input, imperial=False):
    """
    Construit l'URL d'une demande d'API à l'API météo d'OpenWeather

    :param city_input: (List[str]): Nom d'une ville tel que collecté par 'argparse'
    :param imperial: valeur booléenne qui décidera d'afficher la température en degrés Celsius ou Fahrenheit
                     valeur par défaut pour cet argument = False
    :return:
        str: URL formatée pour un appel au point de terminaison de nom de ville d'OpenWeather
    """
    # appel '_get_api_key' pour récupérer la clé API à partir du fichier de configuration et l'enregistre en tant que
    # 'api_key'
    api_key = _get_api_key()
    # utilise 'str.join()' pour concaténer les mots qui compose un même nom de ville avec un caractère
    # d'espacement (" ") si un nom de ville se compose de plus d'un mot
    city_name = " ".join(city_input)
    # fonction du module 'urllib.parse' pour aider à nettoyer l'entrée de l'utilisateur afin que l'API puisse la
    # consommer en toute sécurité.
    # passe 'city_name' à 'parse.quote_plus()', qui encode la chaîne afin d'envoyer une requête HTTP valide à l'API.
    # Outre la conversion de certains caractères via l'encodage UTF-8, cette fonction convertit également les
    # caractères d'espacement en symboles plus(+), qui est une forme d'encodage d'URL nécessaire pour les appels
    # appropriés à cette API.
    url_encoded_city_name = parse.quote_plus(city_name)
    # utilise une expression conditionnelle pour affecter soit 'imperial' ou 'metric' à 'units, selon que le paramètre
    # imperial est True ou False
    units = "imperial" if imperial else "metric"
    url = (
        f"{BASE_WEATHER_API_URL}?q={url_encoded_city_name}"
        f"&units={units}&appid={api_key}"
    )
    return url


# Créer une fonction non public (commence par _ ) nommée 'get_api_key()', qui encapsule la logique de code pour accéder
# à la clé API OpenWeather
def _get_api_key():
    """
    Récupérer la clé API à partir du fichier de configuration.
    Attend un fichier de configuration nommé 'secrets.ini' avec la structure
    [openweather]
    api_key=<your-openweather-api-key>
    """
    # instancie un objet 'ConfigParser' nommée 'Config'
    # utilise '.read' pour charger les informations enregistrées dans 'secrets.ini'
    # renvoie la valeur de la clé API en accédant à la valeur du dictionnaire à l'aide de la notation entre crochets
    config = ConfigParser()
    config.read("secrets.ini")
    return config["openweather"]["api_key"]


# fonction qui permet d'avoir un affichage dans la console à la place d'avoir le résultat dans le navigateur
def get_weather_data(query_url):
    """
    Envoie une requête API à une URL et renvoie les données sous la forme d'un objet Python

    :arg:
        query_url (str): URL formatée pour le point de terminaison du nom de la ville d'OpenWeather
    :return:
        dict: Informations météorologiques pour une ville spécifique
    """
    # utilise 'urllib.request.urlopen()' pour faire une requête HTTP GET au paramètre 'query_url' et enregistre le
    # résultat sous 'response'
    try:
        response = request.urlopen(query_url)
    except error.HTTPError as http_error:
        if http_error.code == 401:         # 401 Unauthorized / Non autorisé
            sys.exit("Accès refusé. Vérifiez votre clé API.")
        elif http_error.code == 404:       # 404 Not Found / Introuvable
            sys.exit("Impossible de trouver les données météos pour cette ville :(")
        else:
            sys.exit(f"Quelque chose c'est mal passé .. ({http_error.code})")

    # extrait les données de la réponse
    data = response.read()

    # renvoi un appel à 'json.loads()' avec 'data' comme argument. La fonction renvoie un objet Python contenant
    # les informations JSON extraites de query_url. la gestion des erreurs 'try' et 'except' permet de lutter contre le
    # JSON potentiellement malformé que l'API pourrait vous envoyer
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        sys.exit("Impossible de lire la réponse du serveur")


# Créer une fonction d'affichage
def display_weather_info(weather_data, imperial=False):
    """
    Imprime des informations météo formatées sur une ville

    :arg:
        weather_data (dict): Réponse API d'OpenWeather par nom de ville
        imperial (bool): Utiliser ou non les unités impériales pour la température

    Plus d'informations sur http://openweathermap.org/current#name
    """
    # sélectionnent les données pertinentes pour 'city', 'weather_description' et 'temperature' dans le dictionnaire
    # 'weather_data' et les affectent aux variables
    city = weather_data["name"]
    # afficher les conditions météo en couleur en fonction de leurs ID
    weather_id = weather_data["weather"][0]["id"]
    weather_description = weather_data["weather"][0]["description"]
    temperature = weather_data["main"]["temp"]

    # end="", définit le caractère final sur un caractère d'espacement au lieu du caractère de nouvelle ligne par défaut
    # ^{PADDING}, centre le nom de la ville en fonction de sa longueur
    # REVERSE et RESET pour modifier la couleur (surbriance) de sortie du terminal
    style.change_color(style.GREEN)
    print(f"{city:^{style.PADDING}}", end="")
    style.change_color(style.RESET)

    # weather_symbol = emojis
    weather_symbol, color = _select_weather_display_params(weather_id)

    style.change_color(color)
    print(f"\t{weather_symbol}", end=" ")
    print(
        f"{weather_description.capitalize():^{style.PADDING}}",
        end=" "
    )
    style.change_color(style.RESET)

    # imprime les infos. de température, puis utilise une expression conditionnelle qui repose sur la valeur booléenne
    # de 'imperial' pour décider d'imprimer un 'F'  pour Fahrenheit ou un 'C' pour Celsius
    print(f"({temperature}°{'F' if imperial else 'C'})")


# associe une couleur avec l'ID/code de la condition météologique
def _select_weather_display_params(weather_id):
    if weather_id in THUNDERSTORM:
        display_params = ("🌩", style.RED)
    elif weather_id in DRIZZLE:
        display_params = ("☔", style.CYAN)
    elif weather_id in RAIN:
        display_params = ("💧", style.BLUE)
    elif weather_id in SNOW:
        display_params = ("❄", style.WHITE)
    elif weather_id in ATMOSPHERE:
        display_params = ("🌌", style.BLUE)
    elif weather_id in CLEAR:
        display_params = ("☀", style.YELLOW)
    elif weather_id in CLOUDY:
        display_params = ("☁", style.WHITE)
    else:  # Dans le cas où l'API ajoute de nouveaux codes météo
        display_params = ("🌡", style.RESET)
    return display_params


if __name__ == "__main__":
    user_args = read_user_cli_args()
    query_url = build_weather_query(user_args.city, user_args.imperial)
    # appel 'get_weather_data()' en passant le 'query_url' qui est généré avec 'build_weather_query()' puis enregistre
    # le dictionnaire dans 'weather_data'
    weather_data = get_weather_data(query_url)

    display_weather_info(weather_data, user_args.imperial)

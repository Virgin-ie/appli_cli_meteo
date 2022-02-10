# permet de conserver la chaîne de sorti à une longueur cohérente de 20 caractères et de remplir toute chaîne plus
# courte avec des espaces à gauche et à droite
PADDING = 20

# couleurs
RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
YELLOW = "\033[1;33m"
WHITE = "\033[37m"
GREEN = "\033[1;32m"

# Syntaxe : \033 Caractère d'échapement ASCII + [ crochet ouvrant + paramètres SGR (Select Graphic Rendition voir
# Code d'échappement ANSI) : https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters
# \033[;7m Inverse les couleurs d'arrière-plan et d'avant-plan du terminal
REVERSE = "\033[;7m"

# \033[0m Remet tout à sa valeur par défaut
RESET = "\033[0m"


def change_color(color):
    print(color, end="")

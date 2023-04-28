from ursina import *
from snake import Snake
from loadingscreen import LoadingScreen


app = Ursina()


# Initialisation de la fenetre de jeu qui occupe toute la taille de l'écran de l'utilisateur
window.fullscreen = True
window.borderless = False
# Enlève la possibilité d'accéder aux paramètres windows
window.cog_button.disable()
# Enlève le conteur des fps qui apparait normalement avec ursina
window.fps_counter.disable()
# Enlève le bouton windows qui permet de fermer l'application
window.exit_button.disable()

# Importation de la classe 'Snake()' du fichier 'snake.py'
jeu_snake = Snake()

# Importation de la classe 'LoadingScreen()' du fichier 'loadingscreen.py'
loadingscreen = LoadingScreen()

# Affiche le loading screen pendant 8.5 secondes qui est un gif en 2d d'un jeu snake
loadingscreen.afficher()
invoke(loadingscreen.enlever, delay=8.5)

app.run()

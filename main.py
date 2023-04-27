from ursina import *
from snake import Snake 
from loadingscreen import LoadingScreen


app = Ursina()  


#Initialisation de la fenetre de jeu qui occupe toute la taille de l'écran de l'utilisateur    
window.fullscreen = True
window.borderless = False
window.cog_button.disable()
window.fps_counter.disable()
window.exit_button.disable()


jeu_snake = Snake()

#Importation de la classe 'LoadingScreen()' du fichier 'loadingscreen.py'
loadingscreen = LoadingScreen()

#Affiche le loading screen pendant 10 secondes qui est un gif en 2d d'un jeu snake 
loadingscreen.afficher()
invoke(loadingscreen.enlever, delay=8.5)

app.run()

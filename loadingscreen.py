from ursina import *
from ursina import input_handler
import imageio
import time


class LoadingScreen(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui,
                         model='quad',
                         color=color.rgba(0, 0, 0, 0))
    """classe qui créer un loading screen"""

    def afficher(self):
        """fonction qui affiche le loading screen"""
        # Désactive les touches space et escape qui auraient pu créer des beugs si appuyées
        input_handler.unbind('space')
        input_handler.unbind('escape')
        # Gif du snake 2d
        self.loading_snake = Animation(
            'Assets/images/loading_snake.gif', scale=(1.8, 1), parent=self)
        # Png du 'Loading'
        self.loading_sprite = Sprite(
            texture="Assets/images/loading.png", scale=0.15, position=(-0.09, -0.2), parent=self)

        # Les trois points blancs animés du loading
        self.point1 = Entity(model="circle", scale=0.03, position=(
            0.23, -0.2), color=color.rgba(255, 255, 255, 255), parent=self)
        self.point2 = Entity(model="circle", scale=0.03, position=(
            0.28, -0.2), color=color.rgba(255, 255, 255, 0), parent=self)
        self.point3 = Entity(model="circle", scale=0.03, position=(
            0.33, -0.2), color=color.rgba(255, 255, 255, 0), parent=self)

        self.last_time = 0
        # Des valeurs pour que les points s'affichent au bon moment
        self.opacite2 = 0
        self.opacite3 = -2

    def update(self):
        """
        fonction native de la bibliotheque qui s'execute 60 fois par seconde 
        ici, les points blancs du loading sont animés"""
        current_time = time.time()  # Prend le temps de l'instant
        # Soustrait le temps de l'instant avec le temps déja passé
        elapsed_time = current_time - self.last_time
        if elapsed_time >= 0.7:
            # Si le 'a' du rgba vaut 255 alors le point blanc s'affiche
            if self.opacite2 % 3 != 0:
                self.point2.color = color.rgba(255, 255, 255, 255)
            else:
                self.point2.color = color.rgba(255, 255, 255, 0)
            if self.opacite3 % 3 == 0:
                self.point3.color = color.rgba(255, 255, 255, 255)
            else:
                self.point3.color = color.rgba(255, 255, 255, 0)
            self.opacite2 += 1
            self.opacite3 += 1
            self.last_time = current_time  # Met a jour le temps passé

    def enlever(self):
        """fonction qui enlève le loading screen"""
        # Reactive les touches pour pouvoir jouer
        input_handler.bind('space', 'space')
        input_handler.bind('escape', 'escape')
        destroy(self.loading_snake)
        destroy(self.loading_sprite)
        destroy(self.point1)
        destroy(self.point2)
        destroy(self.point3)

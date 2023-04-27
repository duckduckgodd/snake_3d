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
        #Désactive les touches space et escape qui aurait pu créer des beugs si appuyer
        input_handler.unbind('space')
        input_handler.unbind('escape')
        #Gif du snake 2d 
        self.loading_snake = Animation('Assets/images/loading_snake.gif',scale = (1.8, 1),parent = self)
        #Png du 'Loading'
        self.loading_sprite = Sprite(
        texture="Assets/images/loading.png", scale=0.15, position=(-0.09, -0.2), parent = self )

        #Les trois points blancs animés du loading
        self.dot1 = Entity(model="circle", scale=0.03, position=(
            0.23, -0.2), color=color.rgba(255, 255, 255, 255), parent = self)
        self.dot2 = Entity(model="circle", scale=0.03, position=(
            0.28, -0.2), color=color.rgba(255, 255, 255, 0), parent = self)
        self.dot3 = Entity(model="circle", scale=0.03, position=(
            0.33, -0.2), color=color.rgba(255, 255, 255, 0), parent = self)

        self.last_time = 0
        self.opacity2 = 0
        self.opacity3 = -2

    def update(self):
        """fonction qui fait que les points blancs du loading sont animés"""
        current_time = time.time()
        elapsed_time = current_time - self.last_time
        if elapsed_time >= 0.7:
            if self.opacity2 % 3 != 0:
                self.dot2.color = color.rgba(255, 255, 255, 255)
            else:
                self.dot2.color = color.rgba(255, 255, 255, 0)
            if self.opacity3 % 3 == 0:
                self.dot3.color = color.rgba(255, 255, 255, 255)
            else:
                self.dot3.color = color.rgba(255, 255, 255, 0)
            self.opacity2 += 1
            self.opacity3 += 1
            self.last_time = current_time
    
    def enlever(self):
        """fonction qui enlève le loading screen"""
        input_handler.bind('space', 'space')
        input_handler.bind('escape', 'escape')
        destroy(self.loading_snake)
        destroy(self.loading_sprite)
        destroy(self.dot1)
        destroy(self.dot2)
        destroy(self.dot3)
        
         


            



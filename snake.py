from ursina import *
from ursina.shaders import lit_with_shadows_shader, transition_shader
from ursina import input_handler
from player import Toujoursenavant
from map import Map
from menu import Menu, selection
import random


class Snake(Entity):
    def __init__(self):
        super().__init__(model="quad", color=color.rgba(0, 0, 0, 0))
        """classe qui contient les fontions principales du jeu"""

        # Importation de la classe 'Toujoursenavant()' du fichier 'player.py' qui créer un joueur
        # en première personne qui va toujours en avant qui peut être controllé par l'utilisateur
        self.player = Toujoursenavant()

        # Corps serpent:

        # Tête du serpent avec le model 'snakehead.fbx'
        self.snake_head = Entity(parent=self.player, model="Assets/models/snakehead.fbx",
                                 texture="Assets/images/tail.jpg", scale=(0.0021, 0.0021, 0.0021), position=(0, 0, 1.5),
                                 collider="box", shader=lit_with_shadows_shader)

        # Collider de la tête du serpent transparent qui a les mêmes dimensions mais en forme de cube afin d'éviter les bugs
        self.head = Entity(parent=self.player, model="cube", scale=(1.1, 1, 1.3),
                           color=color.rgba(0, 0, 0, 0), position=(0, -0.4, 1.95), collider="box", shader=lit_with_shadows_shader)

        # Les yeux des serpents
        oeil_gauche = Entity(parent=self.player, model="sphere", scale=0.1,
                             color=color.yellow, position=(-0.19, 0.2, 2.4), collider="box", shader=lit_with_shadows_shader)
        oeil_droite = Entity(parent=self.player, model="sphere", scale=0.1,
                             color=color.yellow, position=(0.19, 0.2, 2.4), collider="box", shader=lit_with_shadows_shader)

        # Liste qui va contenir les scripts de la fonction SmoothFollow() de chaque sphere du serpent
        self.smoothfollow = []

        # Variable qui va servir de déterminer dans la fonction 'nouvelle_sphere()' quelle est la sphere qui doit être suivie
        self.num_corps = 1

        # Liste qui va contenir chaque partie du corps ou sphere du serpent
        self.corps = [self.head, Entity(parent=self.head, model="sphere", collider="sphere", texture="Assets/images/tail.jpg", z=-0.5,
                                        scale=0.8, shader=lit_with_shadows_shader)]

        # Initialise les 11 premières spheres du début de chaque partie
        for i in range(10):
            self.nouvelle_sphere()
            self.corps[i+2].position = (0, -0.4, -12.5-i/1.3)
        #self.disable_smoothfollow()

        # Variable qui va vérifier si le serpent est déja mort dans la partie
        self.interaction_mur = False
        self.interaction_corps = False

        # Pomme initiale
        self.pomme = Entity(model="Assets/models/pomme.fbx", texture="Assets/images/apple_texture.jpg",
                            position=(0, -0.1, 8), scale=0.013, collider="mesh", shader=transition_shader)

        # Son pour quand le serpent mange une pomme et meurt
        self.bite_sound = Audio(
            "Assets/audio/Apple_Bite.mp3", loop=False, autoplay=False)

        self.son_mort = Audio("Assets/audio/snakedeath.mp3",
                              loop=False, autoplay=False)

        # Importation de la classe 'Map()' du fichier 'map.py'

        self.map = Map()

        # Importation de la classe 'Menu()' du fichier 'menu.py'
        self.menu = Menu()

        # Score et highscore en haut à gauche de l'écran avec les images de la pomme et du trophée

        self.score = 0
        self.highscores = []

        self.pomme_sprite = Sprite(texture="Assets/images/apple.png", scale=0.05, position=(-0.75, 0.42),
                                   world_parent=camera.ui)
        self.pomme_score = Text(text=f"{self.score}", position=(-0.69, 0.42), origin=(0, 0), scale=1.5,
                                color=color.yellow)

        if len(self.highscores) > 0:
            self.highscore_sprite = Sprite(texture="Assets/images/highscore.png", scale=0.05,
                                           position=(-0.60, 0.42), world_parent=camera.ui)
        self.pomme_highscore = Text(text=f" ", position=(-0.54, 0.42), origin=(0, 0),
                                    scale=1.5, color=color.yellow)

        self.escape_sprite = Sprite(texture="Assets/images/esc.png", scale=0.008, position=(-0.86, 0.475),
                                    world_parent=camera.ui)

        # Map 2d

        map2d_back = Sprite(texture="Assets/images/2dmap_back.png", scale=0.02, position=(0.76, 0.377),
                            world_parent=camera.ui)

        self.apple2d_x = (
            (self.pomme.position[0] - (-13)) / (13 - (-13))) * (0.836 - 0.68) + 0.68
        self.apple2d_y = (
            (self.pomme.position[2] - (-13)) / (13 - (-13))) * (0.446 - 0.297) + 0.297
        self.apple2d = Sprite(texture="Assets/images/apple_pixel.png", scale=0.03, position=(self.apple2d_x, self.apple2d_y),
                              world_parent=camera.ui)

        self.snake2d_x = (
            (self.player.position[0] - (-13)) / (13 - (-13))) * (0.836 - 0.68) + 0.68
        self.snake2d_y = (
            ((self.player.position[2]+1.5) - (-13)) / (13 - (-13))) * (0.446 - 0.297) + 0.297
        self.snake2d = Sprite(texture="Assets/images/bluesnake2d.png", scale=0.009, position=(self.snake2d_x, self.snake2d_y),
                              world_parent=camera.ui)

    def nouvelle_sphere(self):
        """
        fonction qui ajoute une sphere a liste du corps 
        """
        nouvelle_sphere = Entity(model="sphere", collider="sphere", texture="Assets/images/tail.jpg",
                                 scale=0.8, shader=lit_with_shadows_shader, position=self.corps[self.num_corps].position)
        self.num_corps += 1
        self.corps.append(nouvelle_sphere)

    def disable_smoothfollow(self):
        """
        fonction qui enlève la fonction SmoothFollow() du script de chaque sphere.
        """
        for j in range(len(self.smoothfollow)):
            self.corps[j+2].scripts.remove(self.smoothfollow[j])
        self.smoothfollow = []

    def enable_smoothfollow(self):
        """
        fonction qui ajoute la fonction SmoothFollow() au script de chaque sphere.
        """
        for j in range(len(self.corps)-2):
            if len(self.corps[j+2].scripts) == 0:
                sf = self.corps[j+2].add_script(SmoothFollow(
                    target=self.corps[j+1], offset=[0, 0, 0], speed=12))
                self.smoothfollow.append(sf)

    # Pommes

    def spawn_pomme(self):
        """
        fonction qui va spawn une pomme à une position au hasard de la map.
        """
        x = random.uniform(-13, 13)
        z = random.uniform(-13, 13)
        position = (x, -0.1, z)
        self.pomme = Entity(model="Assets/models/pomme.fbx", texture="Assets/images/apple_texture.jpg", scale=0.013,
                            position=position, collider="mesh", shader=transition_shader)
        destroy(self.apple2d)
        self.apple2d_x = (
            (self.pomme.position[0] - (-13)) / (13 - (-13))) * (0.836 - 0.68) + 0.68
        self.apple2d_y = (
            (self.pomme.position[2] - (-13)) / (13 - (-13))) * (0.446 - 0.297) + 0.297
        self.apple2d = Sprite(texture="Assets/images/apple_pixel.png", scale=0.03, position=(self.apple2d_x, self.apple2d_y),
                              world_parent=camera.ui)

    def intersection_pomme(self):
        """
        fonction qui vérifie si la tête du serpent a intersecté avec la pomme et si oui rajoute quatres au bout du serpent et rajoute 1 au score de la partie.
        """
        if self.head.intersects(self.pomme):
            self.bite_sound.play()
            self.pomme.disable()
            self.spawn_pomme()
            self.score += 1
            destroy(self.pomme_score)
            self.pomme_score = Text(text=f"{self.score}", position=(-0.69, 0.42), origin=(0, 0),
                                    scale=1.5, color=color.yellow)
            # Ajoute 4quatres spheres a chaque fois que une pomme est mangé
            for i in range(4):
                self.nouvelle_sphere()
            self.enable_smoothfollow()
            if len(self.highscores) > 0:
                if self.score > self.highscore_actuel:
                    destroy(self.pomme_highscore)
                    self.pomme_highscore = Text(text=f"{self.score}", position=(-0.54, 0.42),
                                                origin=(0, 0), scale=1.5, color=color.yellow)

    # Morts (interaction avec le mur ou le corps)

    def intersection_mur(self):
        """
        fonction qui vérifie si la tête du serpent a intersecté avec un des quatres murs et si oui arrête le serpent et met le menu de fin.
        """
        if (self.head.intersects(self.map.mur_avant) or self.head.intersects(self.map.mur_droit) or self.head.intersects(self.map.mur_gauche) or self.head.intersects(self.map.mur_arriere)) and self.interaction_corps == False:
            self.interaction_corps = True
            self.player.stop()
            self.son_mort.play()
            self.disable_smoothfollow()
            self.highscores.append(self.score)
            self.highscore_actuel = max(self.highscores)
            self.menu.menu_fin.enabled = True
            # Affiche les scores sur l'écran de fin
            self.menu.highscore_fin.text = f"{self.highscore_actuel}"
            self.menu.score_fin.text = f"{self.score}"

    def intersection_corps(self):
        """
        fonction qui vérifie si la tête du serpent a intersecté avec son propre corps et si oui arrête le serpent et met le menu de fin.
        """
        if len(self.corps) > 12:
            for i in range(5, len(self.corps)):
                if (self.head.intersects(self.corps[i])
                        and self.interaction_corps == False):
                    self.interaction_corps = True
                    self.player.stop()
                    self.son_mort.play()
                    self.disable_smoothfollow()
                    self.highscores.append(self.score)
                    self.highscore_actuel = max(self.highscores)
                    # Affiche les scores sur l'écran de fin
                    self.menu.highscore_fin.text = f"{self.highscore_actuel}"
                    self.menu.score_fin.text = f"{self.score}"
                    self.menu.menu_fin.enabled = True

    def update(self):
        """
        fonction qui met a jour la position du serpent sur la map 2d et vérifie a chaque frame si la tête du serpent a intersecté avec une pomme ou un mur ou son propre corps et execute leur code.
        """
        if self.player.always_move_forward == True:
            destroy(self.snake2d)
            self.snake2d_x = (
                (self.player.position[0] - (-13)) / (13 - (-13))) * (0.836 - 0.68) + 0.68
            self.snake2d_y = (
                ((self.player.position[2]+1.5) - (-13)) / (13 - (-13))) * (0.446 - 0.297) + 0.297
            self.snake2d = Sprite(texture="Assets/images/bluesnake2d.png", scale=0.009, position=(self.snake2d_x, self.snake2d_y),
                                  world_parent=camera.ui)
        self.intersection_pomme()
        self.intersection_mur()
        self.intersection_corps()

    # Start player and reset him

    def reset(self):
        """
        fonction qui réinitialise la position du serpent, le corps du serpent, le score, et toutes les valeurs initiales.
        """
        # Met la position du joueur du début
        self.player.position = (0, 0, -13)
        self.player.rotation = (0, 0, 0)
        # Enlève toutes les parties du corps sauf les deux premiers éléments
        for e in range(2, len(self.corps)):
            self.corps[e].disable()
        for entity in self.corps[2:]:
            self.corps.remove(entity)
        self.player.stop()
        self.smoothfollow = []
        self.corps = [self.head, Entity(parent=self.head, model="sphere", collider="sphere", texture="Assets/images/tail.jpg", z=-0.5,
                                        scale=0.8, shader=lit_with_shadows_shader)]
        self.num_corps = 1
        self.highscores.append(self.score)
        self.score = 0
        destroy(self.pomme_score)
        self.pomme_score = Text(text=f"{self.score}", position=(-0.69, 0.42), origin=(0, 0),
                                scale=1.5, color=color.yellow)
        if len(self.highscores) > 0:
            self.highscore_sprite = Sprite(texture="Assets/images/highscore.png", scale=0.05,
                                           position=(-0.60, 0.42), world_parent=camera.ui)
            destroy(self.pomme_highscore)
            self.highscore_actuel = max(self.highscores)
            self.pomme_highscore = Text(text=f"{self.highscore_actuel}", position=(-0.54, 0.42),
                                        origin=(0, 0), scale=1.5, color=color.yellow)
        # Fait que le joueur regarde la direction dans laquelle le serpent est positionné
        self.player.camera.position = (0, 0, 0)
        self.player.camera.rotation = (0, 0, 0)
        destroy(self.pomme)
        for i in range(10):
            self.nouvelle_sphere()
            self.corps[i+2].position = (0, -0.4, -12.5-i/1.3)
        self.enable_smoothfollow()
        self.disable_smoothfollow()
        self.pomme = Entity(model="Assets/models/pomme.fbx", texture="Assets/images/apple_texture.jpg",
                            scale=0.013, position=(0, -0.1, 8), collider="mesh", shader=transition_shader)
        destroy(self.apple2d)
        self.apple2d_x = (
            (self.pomme.position[0] - (-13)) / (13 - (-13))) * (0.836 - 0.68) + 0.68
        self.apple2d_y = (
            (self.pomme.position[2] - (-13)) / (13 - (-13))) * (0.446 - 0.297) + 0.297
        self.apple2d = Sprite(texture="Assets/images/apple_pixel.png", scale=0.03, position=(self.apple2d_x, self.apple2d_y),
                              world_parent=camera.ui)
        destroy(self.snake2d)
        self.snake2d_x = (
            (self.player.position[0] - (-13)) / (13 - (-13))) * (0.836 - 0.68) + 0.68
        self.snake2d_y = (
            ((self.player.position[2]+1.5) - (-13)) / (13 - (-13))) * (0.446 - 0.297) + 0.297
        self.snake2d = Sprite(texture="Assets/images/bluesnake2d.png", scale=0.009, position=(self.snake2d_x, self.snake2d_y),
                              world_parent=camera.ui)
        self.interaction_mur = False
        self.interaction_corps = False

    def input(self, key):
        """
        fonction qui active les menu et fait execute une fonction si une certaine touche est appuyer. 
        """
        # Conditions si aucun menu est activé
        if self.menu.menu_pause.enabled == False and self.menu.menu_fin.enabled == False:
            application.time_scale = 1
            if key == "r":
                self.reset()
            if key == "space":
                self.player.start()
                self.enable_smoothfollow()
            if key == "f":
                
                quit()

        # Conditions si le menu de pause est activé
        elif self.menu.menu_pause.enabled:
            # On arrete le joueur
            self.player.stop()
            application.time_scale = 0
            if key == "enter":
                # On regarde quel bouton est sélectionné et on execute la fonction qui va avec
                if selection(self.menu.reprendre):
                    self.player.start()
                elif selection(self.menu.nouvelle_partie_pause):
                    self.reset()
                elif selection(self.menu.quitter_pause):
                    quit()
            elif key == "escape":
                self.player.start()
            if key == "r":
                self.reset()
            if key == "f":
                quit()

        # Conditions si le menu de fin est activé
        elif self.menu.menu_fin.enabled:
            if key == "enter":
                # On regarde quel bouton est sélectionné et on execute la fonction qui va avec
                if selection(self.menu.rejouer_partie_fin):
                    self.reset()
                elif selection(self.menu.quitter_fin):
                    quit()
            if key == "r":
                self.reset()
            if key == "f":
                quit()

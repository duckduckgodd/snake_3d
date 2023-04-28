from ursina import *
from ursina.shaders import lit_with_shadows_shader


class Map(Entity):
    def __init__(self):
        super().__init__()
        """
        classe qui créer une map pour le jeu avec des ombres et un soleil
        """
        # Sol de la map
        self.sol = Entity(
            model="cube",
            position=(0, -1.7, 0),
            scale=(44, 2, 44),
            texture="grass",
            collider="box",
            shader=lit_with_shadows_shader)

        # Les quatres murs qui se complètent pour former un carré

        self.mur_avant = Entity(
            model="cube",
            texture="brick",
            collider="box",
            scale=(30, 10, 2),
            position=(0, 0, 15),
            color=color.rgb(80, 184, 103),
            shader=lit_with_shadows_shader
        )
        self.mur_droit = Entity(
            model="cube",
            texture="brick",
            collider="box",
            scale=(2, 10, 30),
            position=(15, 0, 0),
            color=color.rgb(80, 184, 103),
            shader=lit_with_shadows_shader
        )
        self.mur_gauche = Entity(
            model="cube",
            texture="brick",
            collider="box",
            scale=(2, 10, 30),
            position=(-15, 0, 0),
            color=color.rgb(80, 184, 103),
            shader=lit_with_shadows_shader
        )
        self.mur_arriere = Entity(
            model="cube",
            texture="brick",
            collider="box",
            scale=(30, 10, 2),
            position=(0, 0, -15),
            color=color.rgb(80, 184, 103),
            shader=lit_with_shadows_shader
        )

        # Foncion de ursina qui crée un ciel pour la map
        self.sky = Sky(collider="box", shader=lit_with_shadows_shader)

        # Foncion de ursina qui créer un soleil pour la map qui va créer des ombres
        self.sun = DirectionalLight()
        self.ombre = self.sun.look_at(Vec3(1, -1, -1))

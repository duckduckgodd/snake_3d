from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina import input_handler


class Toujoursenavant(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        """classe qui crée un joueur allant toujours vers l'avant"""
        self.cursor.enabled = False
        self.gravity = 0
        # Ajuste la sensibilisé de la souris
        self.mouse_sensitivity = Vec2(110, 110)
        self.always_move_forward = False
        self.position = (0, 0, -13)  # Position initiale du joueur
        self.rotation = (0, 0, 0)
        self.speed = 12
        self.collider = "box"

        # Désactive les touches w,a,s,d qui aurait fait que l'utilisateur puisse changer de direction
        input_handler.unbind("w")
        input_handler.unbind("a")
        input_handler.unbind("d")
        input_handler.unbind("s")
        self.spacestart_sprite = Sprite(
            texture="Assets/images/spacetostart.png",
            scale=0.1,
            position=(0, -0.25),
            world_parent=camera.ui,
        )
        # Camera qui est la vue du joueur
        self.camera = Entity(parent=self)

    def update(self):
        """fonction qui fait que le serpent avance toujours"""
        if self.always_move_forward == True:
            self.position += self.forward * self.speed * \
                time.dt  # Avance le joueur vers l'avant
            super().update()

    def start(self):
        """fonction qui commence le serpent"""
        self.always_move_forward = True
        destroy(self.spacestart_sprite)

    def stop(self):
        """fonction qui arrête le serpent"""
        self.always_move_forward = False

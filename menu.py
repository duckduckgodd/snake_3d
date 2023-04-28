from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


couleurH = color.rgb(0, 191, 255)  # Couleur de selection
couleurN = color.rgb(43, 88, 222)  # Couleur de bouton normale


def selection(bouton):
    """Button --> bool
    Permet de savoir quel bouton est sélectionné parl l'utilisateur
    """
    return bouton.color == couleurH


class Menu(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui)
        """
        """
        self.menu_principal = Entity(parent=self, enabled=False)
        self.menu_pause = Entity(parent=self, enabled=False)
        self.menu_fin = Entity(parent=self, enabled=False)

        self.menus = [self.menu_principal, self.menu_pause, self.menu_fin]
        self.index = 0

        # Menu de Pause --> comporte tous les élement de l'interface

        self.pause_background = Sprite(
            parent=self.menu_pause,
            texture="Assets/images/menu_pause_back.png",
                    position=(-0.65, 0), scale=(0.12, 0.11)
        )

        self.reprendre = Button(
            parent=self.menu_pause,
            scale=(0.27, 0.09),
            position=(-0.65, 0.16),
            color=color.rgb(43, 88, 222),
            text="Reprendre       "
        )

        self.reprendre_sprite = Sprite(
            "Assets/images/play.png",
            parent=self.menu_pause,
            scale=(0.008, 0.008),
            position=(-0.58, 0.16),
        )

        self.nouvelle_partie_pause = Button(
            parent=self.menu_pause,
            scale=(0.27, 0.09),
            position=(-0.65, 0),
            color=color.rgb(43, 88, 222),
            text="Recommencer          "
        )

        self.recommencer_sprite = Sprite(
            "Assets/images/replay.png",
            parent=self.menu_pause,
            scale=(0.008, 0.008),
            position=(-0.56, 0),
        )

        self.quitter_pause = Button(
            parent=self.menu_pause,
            scale=(0.27, 0.09),
            position=(-0.65, -0.16),
            color=color.rgb(43, 88, 222),
            text="Quitter       ",
        )

        self.quitter_pause_sprite = Sprite(
            "Assets/images/quitter.png",
            parent=self.menu_pause,
            scale=(0.016, 0.016),
            position=(-0.60, -0.16),
        )

        self.sprite_pause = Sprite(
            "Assets/images/pause.png",
            parent=self.menu_pause,
            scale=(0.05, 0.05),
            position=(0, 0)
        )

        self.fleches_pause = Sprite(
            "Assets/images/arrowkeys.png",
            parent=self.menu_pause,
            position=(-0.814, 0),
            scale=(0.016, 0.016),
        )

        # Liste de boutons de pause pour naviguer dans le menu
        self.boutons_pause = [self.reprendre,
                              self.nouvelle_partie_pause, self.quitter_pause]
        # Lorsque le menu est activé, les boutons sont réinitialisés
        self.menu_pause.on_enable = self.ouverture_menu(self.boutons_pause)

        # Menu et écran de fin lorsque le joueur meurt--> Tous les éléments de l'interface
        self.background_fin = Sprite(
            parent=self.menu_fin,
            texture="Assets/images/menu_back.png",
                    position=(0, -0.04), scale=(0.12, 0.11)
        )

        self.rejouer_partie_fin = Button(
            parent=self.menu_fin,
            scale=(0.15, 0.07),
            position=(-0.1, -0.16),
            color=color.azure,
            text="Rejouer      ",
        )

        self.rejouer_sprite = Sprite(parent=self.menu_fin, texture="Assets/images/replay.png",
                                     scale=0.0055, position=(-0.05, -0.16))

        self.quitter_fin = Button(
            parent=self.menu_fin,
            scale=(0.15, 0.07),
            position=(0.1, -0.16),
            color=color.azure,
            text="Quitter     ",
        )

        self.quitter_sprite = Sprite(parent=self.menu_fin, texture="Assets/images/quitter.png",
                                     scale=0.012, position=(0.15, -0.16))

        self.apple_fin = Sprite(
            "Assets/images/apple.png",
            parent=self.menu_fin,
            position=(-0.1, 0.14),
            scale=(0.07, 0.07),
        )
        self.score_fin = Text(parent=self.menu_fin,
                              position=(-0.11, .05), scale=1.5)
        self.highscore_fin = Text(
            parent=self.menu_fin, position=(0.09, .05), scale=1.5)
        self.trophee_highscore = Sprite(
            "Assets/images/highscore.png",
            parent=self.menu_fin,
            position=(0.1, 0.14),
            scale=(0.07, 0.07),
        )

        self.fleches_fin = Sprite(
            "Assets/images/arrowkeys.png",
            parent=self.menu_fin,
            position=(0.00, -0.16),
            scale=(0.016, 0.016),
        )

        self.son_bouton = Audio(
            "Assets/audio/button.mp3", loop=False, autoplay=False)

        # Liste de boutons du menu de fin pour naviguer
        self.boutons_fin = [self.rejouer_partie_fin, self.quitter_fin]
        # Lorsque le menu est activé, les boutons sont réinitialisés
        self.menu_fin.on_enable = self.ouverture_menu(self.boutons_fin)

    def ouverture_menu(self, liste_menu):
        """ list --> none
        permet de réinitialiser l'affichage des boutons dans la liste pour que le premier soit selectionné"""
        self.index = 0
        for bouton in liste_menu:
            bouton.color = couleurN
        liste_menu[0].color = couleurH

    def input(self, key):
        """
        touche --> action
        fonction native de la bibliotheque ursina qui regarde les touches utilisées et leur associe des actions
        ici, elle permet d'activer les menus et de naviguer dedans à l'aide des fleches
        """
        if self.menu_pause.enabled:
            if key == "down arrow":
                self.son_bouton.play()
                self.index += 1
                if self.index > len(self.boutons_pause) - 1:
                    self.index = len(self.boutons_pause) - 1
                # On attribue la couleur de selection au bouton à la position self.index
                self.boutons_pause[self.index].color = couleurH
                # On attribue la couleur normale aux boutons qui ne sont pas sélectionnés
                for bouton in self.boutons_pause:
                    if bouton != self.boutons_pause[self.index]:
                        bouton.color = couleurN
            if key == "up arrow":
                self.son_bouton.play()
                self.index -= 1
                if self.index < 0:
                    self.index = 0
                self.boutons_pause[self.index].color = couleurH
                for bouton in self.boutons_pause:
                    if bouton != self.boutons_pause[self.index]:
                        bouton.color = couleurN
            # On fait disparaitre le menu lorsque ces touches sont appuyées
            if key == "enter":
                self.son_bouton.play()
                self.menu_pause.enabled = False
            elif key == "escape":
                self.son_bouton.play()
                self.menu_pause.enabled = False
            elif key == "r":
                self.son_bouton.play()
                self.menu_pause.enabled = False

        # Mechanisme identique ici
        elif self.menu_fin.enabled:
            if key == "down arrow":
                self.son_bouton.play()
                self.index += 1
                if self.index > len(self.boutons_fin) - 1:
                    self.index = len(self.boutons_fin) - 1
                self.boutons_fin[self.index].color = couleurH
                for bouton in self.boutons_fin:
                    if bouton != self.boutons_fin[self.index]:
                        bouton.color = couleurN
            if key == "up arrow":
                self.son_bouton.play()
                self.index -= 1
                if self.index < 0:
                    self.index = 0
                self.boutons_fin[self.index].color = couleurH
                for bouton in self.boutons_fin:
                    if bouton != self.boutons_fin[self.index]:
                        bouton.color = couleurN

            if key == "enter":
                self.son_bouton.play()
                self.menu_fin.enabled = False
            elif key == "r":
                self.son_bouton.play()
                self.menu_fin.enabled = False

        else:
            if key == "escape":
                self.son_bouton.play()
                # Activation de l'écran de pause avec la touche esc
                self.menu_pause.enabled = True

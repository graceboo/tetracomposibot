# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : _________
#  Prénom Nom No_étudiant/e : _________
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

from robot import *
import random
import math

# === Nom de l’équipe ===
team_name = "Challenger"

# === Identifiant global de robot (entre 0 et 3 dans une équipe)
nb_robots = 0

class Robot_player(Robot):

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1

        self.memory = 0  # UNE SEULE variable mémoire autorisée
        self.param = [random.randint(-1, 1) for _ in range(8)]  # utile pour robot GA
        self.x_init=x_0
        self.y_init=y_0
        self.best_param = self.param.copy()
        self.best_fitness = -1
        self.iteration = 0

        super().__init__(x_0, y_0, theta_0, name="Robot " + str(self.robot_id), team=team_name)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        """
        Fonction appelée à chaque tick de simulation. Retourne (vitesse_translation, vitesse_rotation, ask_reset)
        """

        if self.robot_id == 0 :
            return self.explorateur_reactif(sensors)
        elif self.robot_id == 1:
            return self.explorateur_agressif(sensors, sensor_robot, sensor_team)
        elif self.robot_id == 2:
            return self.comportement_alterné(sensors)
        elif self.robot_id == 3:
            return self.braitenberg_optimisé(sensors)
        else:
            return 0.5, 0, False
        
    def explorateur_reactif(self, sensors): #meilleur
        """ Comportement réactif de type Braitenberg, amélioré pour meilleure exploration. """
        front = sensors[sensor_front]
        left = sensors[sensor_left]
        right = sensors[sensor_right]
        front_left = sensors[sensor_front_left]
        front_right = sensors[sensor_front_right]

        # Calculer un "niveau de danger" global
        danger = min(front, front_left, front_right)

        # Adapter la vitesse : plus rapide si c'est dégagé
        translation = danger * 0.4 + 0.1  # max vitesse 0.5, minimum 0.1

        # Rotation basée sur les côtés, mais si danger est proche, tourner plus vite
        base_rotation = 0.2 * left + 0.2 * front_left - 0.2 * right - 0.2 * front_right
        rotation = base_rotation * (1.0 / (danger + 0.1))  # tourner plus si danger proche
        rotation += (random.random() - 0.5) * 0.5  # moins de bruit qu'agressif

        return translation, rotation, False

    def explorateur_reactif2(self, sensors): #bien
        "comportement réactif de type Braitenberg. "
        "Ce type de comportement est caractérisé par une réaction immédiate et simple aux entrées "
        "sensorielles, ce qui est le cas ici avec "
        "la gestion de la translation et de la rotation en fonction des capteurs frontaux et latéraux"
        front = sensors[sensor_front]
        left = sensors[sensor_left]
        front_left = sensors[sensor_front_left]
        right = sensors[sensor_right]
        front_right = sensors[sensor_front_right]

        # Toujours avancer doucement
        translation = front * 0.1 + 0.2

        # Rotation contrôlée par capteurs latéraux + gros bruit aléatoire
        rotation = 0.2 * left + 0.2 * front_left - 0.2 * right - 0.2 * front_right + (random.random() - 0.5) * 1.0

        return translation, rotation, False

    def explorateur_agressif(self, sensors, sensor_robot, sensor_team):
        """ Comportement réactif agressif avec évitement d'obstacles plus marqué. """
        # Récupérer les capteurs de distance
        front = sensors[sensor_front]
        left = sensors[sensor_left]
        right = sensors[sensor_right]
        front_left = sensors[sensor_front_left]
        front_right = sensors[sensor_front_right]

        # Vitesse de translation augmentée en fonction de la distance avant (avance plus vite)
        translation = front * 0.2 + 0.3  # Vitesse plus rapide

        # Rotation contrôlée par les capteurs latéraux avec plus de poids pour les obstacles
        rotation = 0.4 * left + 0.4 * front_left - 0.4 * right - 0.4 * front_right
        rotation += (random.random() - 0.5) * 2.0  # Plus de bruit pour une rotation moins prévisible

        # Si un mur est détecté devant, agir de manière plus agressive
        if front < 0.3:
            if left > right:  # Plus de place à gauche
                return 0.0, 1.5, False  # Tourner brusquement à gauche
            else:  # Plus de place à droite ou égal
                return 0.0, -1.5, False  # Tourner brusquement à droite

        # Si pas de mur devant, continuer à avancer et ajuster la direction
        return translation, rotation, False

    def comportement_alterné2(self, sensors): #bien
        """ Change de mode toutes les 20 étapes (exploration vs rotation sur place) omportement de type subsomption """
        """s’apparente à une architecture de subsomption simple où le robot alterne entre deux comportements de base : 
        exploration et rotation. Le changement entre ces comportements est contrôlé par un compteur 
        d'étapes et les capteurs détectant la proximité d'un obstacle. """
        front = sensors[sensor_front]
        if self.memory < 20:
            self.memory += 1
            if front < 0.2:
                return 0.0, 0.5, False  # trop près du mur : tourne
            else:
                return 0.8, 0.0, False  # sinon avance
        elif self.memory < 30:
            self.memory += 1
            return 0.0, 0.5, False  # tourne
        else:
            self.memory = 0
            return 0.8, 0.0, False
    def comportement_alterné(self, sensors): #parfaite
        """ Comportement alterné amélioré avec évitement intelligent et exploration dynamique """

        front = sensors[sensor_front]
        left = sensors[sensor_left]
        front_left = sensors[sensor_front_left]
        right = sensors[sensor_right]
        front_right = sensors[sensor_front_right]

        # Cas spécial : coincé dans un coin
        if front < 0.1 and left < 0.1 and right < 0.1:
            return -0.5, 1.0, False  # recule et tourne vite

        # Comportement alterné classique, mais amélioré
        if self.memory < 20:
            self.memory += 1
            if front < 0.2:
                # Trop près devant, choisir le côté le plus dégagé
                if left > right:
                    rotation = 0.5  # tourne à gauche
                else:
                    rotation = -0.5  # tourne à droite
                return 0.0, rotation, False
            else:
                # Avancer selon l'espace disponible
                if front > 0.5:
                    translation = 1.0
                elif front > 0.2:
                    translation = 0.5
                else:
                    translation = 0.0
                return translation, 0.0, False

        elif self.memory < 30:
            self.memory += 1
            # Phase de rotation : tourner vers l'espace libre
            rotation = (0.5 * left + 0.2 * front_left) - (0.5 * right + 0.2 * front_right)
            rotation += (random.random() - 0.5) * 0.4  # petit bruit aléatoire
            return 0.1, rotation, False  # petite avancée en tournant

        else:
            self.memory = 0
            return 0.8, 0.0, False  # relance l'exploration

    def braitenberg_optimisé(self, sensors):
        """
        Contrôle basé sur des poids optimisés par un algorithme génétique
        Contrôleur linéaire à 8 paramètres
        """

        # Mise à jour plus fréquente des paramètres pour plus de réactivité
        if self.iteration % 50 == 0:  # Mettre à jour tous les 50 ticks pour plus de réactivité
            fitness = math.sqrt((self.x - self.x_init) ** 2 + (self.y - self.y_init) ** 2)

            if fitness > self.best_fitness:
                self.best_param = self.param.copy()
                self.best_fitness = fitness

            # Mutation aléatoire des paramètres pour une nouvelle itération
            self.param = [random.randint(-1, 1) for _ in range(8)]

        # Perceptron sensoriel : calcul de la translation et de la rotation
        front_left = sensors[sensor_front_left]
        front_right = sensors[sensor_front_right]
        front = sensors[sensor_front]

        # Améliorer la gestion de la translation pour une plus grande réactivité
        translation = math.tanh(
            self.param[0] + self.param[1] * front_left +
            self.param[2] * front + self.param[3] * front_right
        )
        
        # Ajuster la rotation en fonction des capteurs latéraux
        rotation = math.tanh(
            self.param[4] + self.param[5] * front_left +
            self.param[6] * front + self.param[7] * front_right
        )

        # Si un obstacle est détecté devant, on ajuste la direction de façon plus rapide
        if front < 0.3:  # Distance seuil pour réagir
            if front_left > front_right:
                # Si plus de place à gauche, tourner à gauche
                rotation = 1.0  # Rotation rapide
            else:
                # Si plus de place à droite, tourner à droite
                rotation = -1.0  # Rotation rapide
            translation = 0.0  # Ne pas avancer si trop proche d'un obstacle

        self.iteration += 1
        return translation, rotation, False
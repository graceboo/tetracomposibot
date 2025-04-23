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

        if self.robot_id == 0:
            return self.explorateur_classique(sensors)
        elif self.robot_id == 1:
            return self.agressif_enemi(sensors, sensor_robot, sensor_team)
        elif self.robot_id == 2:
            return self.comportement_alterné(sensors)
        elif self.robot_id == 3:
            return self.braitenberg_optimisé(sensors)
        else:
            return 0.5, 0, False

    def explorateur_classique(self, sensors):
        """ Comportement Braitenberg simple pour l'exploration """
        front = sensors[sensor_front]
        left = sensors[sensor_front_left]
        right = sensors[sensor_front_right]
        rotation = right - left + (random.random() - 0.5) * 0.05
        translation = front
        return translation, rotation, False

    def agressif_enemi(self, sensors, sensor_robot, sensor_team):
        """ Va vers les ennemis détectés devant, sinon explore """
        if sensor_robot[sensor_front] != -1 and sensor_team[sensor_front] != self.team:
            return 1.0, 0.0, False  # fonce droit sur l'ennemi
        else:
            # exploration braitenberg basique
            left = sensors[sensor_front_left]
            right = sensors[sensor_front_right]
            rotation = right - left + (random.random() - 0.5) * 0.1
            translation = sensors[sensor_front]
            return translation, rotation, False

    def comportement_alterné(self, sensors):
        """ Change de mode toutes les 20 étapes (exploration vs rotation sur place) """
        if self.memory < 20:
            self.memory += 1
            return 0.8, 0.0, False  # avance
        elif self.memory < 30:
            self.memory += 1
            return 0.0, 0.5, False  # tourne
        else:
            self.memory = 0
            return 0.8, 0.0, False

    def braitenberg_optimisé(self, sensors):
        """
        Contrôle basé sur des poids optimisés (ex: via GA ou random search)
        Contrôleur linéaire à 8 paramètres
        """
        if self.iteration % 400 == 0 and self.iteration > 0:
            fitness = math.sqrt((self.x - self.x_init) ** 2 + (self.y - self.y_init) ** 2)
            if fitness > self.best_fitness:
                self.best_param = self.param.copy()
                self.best_fitness = fitness
            self.param = [random.randint(-1, 1) for _ in range(8)]
       
        # Perceptron sensoriel : translation et rotation
        translation = math.tanh(
            self.param[0] + self.param[1] * sensors[sensor_front_left] +
            self.param[2] * sensors[sensor_front] + self.param[3] * sensors[sensor_front_right]
        )
        rotation = math.tanh(
            self.param[4] + self.param[5] * sensors[sensor_front_left] +
            self.param[6] * sensors[sensor_front] + self.param[7] * sensors[sensor_front_right]
        )

        self.iteration += 1
        return translation, rotation, False
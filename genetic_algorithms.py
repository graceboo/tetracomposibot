from robot import * 
import math
import random

nb_robots = 0
debug = False

class Robot_player(Robot):

    team_name = "OptimizerGA"
    robot_id = -1
    iteration = 0

    param = []        # paramètres en cours
    bestParam = []    # meilleur ensemble de paramètres
    it_per_evaluation = 400
    trial = 0         # numéro d'évaluation

    best_fitness = -1
    x_0 = 0
    y_0 = 0

    max_trials = 20  # nombre maximal d'évaluations

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a", evaluations=0, it_per_evaluation=0):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = theta_0
        self.it_per_evaluation = it_per_evaluation

        self.bestParam = [random.randint(-1, 1) for _ in range(8)]
        self.param = self.bestParam.copy()

        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def mutate(self, parent):
        child = parent.copy()
        index = random.randint(0, len(child) - 1)
        values = [-1, 0, 1]
        values.remove(child[index])
        child[index] = random.choice(values)
        return child

    def fitness(self):
        return math.sqrt((self.x - self.x_0) ** 2 + (self.y - self.y_0) ** 2)

    def reset(self):
        super().reset()

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        if self.iteration % self.it_per_evaluation == 0:
            if self.iteration > 0:
                fit = self.fitness()
                with open("results_genetic10.txt", "a") as f:
                    f.write(f"{self.trial}, {fit}, {self.best_fitness}\n")

                print(f"\n--- Évaluation n°{self.trial} ---")
                print(f"Fitness actuelle : {fit:.4f}")
                print(f"Fitness meilleure : {self.best_fitness:.4f}")
                print("Paramètres testés :", self.param)
                print("Meilleurs paramètres :", self.bestParam)

                if fit > self.best_fitness:
                    self.bestParam = self.param.copy()
                    self.best_fitness = fit
                    print("=>  Nouvelle meilleure stratégie trouvée !")
                else:
                    print("=> Moins bon : on garde la stratégie précédente.")

            if self.trial >= self.max_trials:
                print("\n=== Optimisation terminée après", self.trial, "évaluations ===")
                print(">> Meilleure stratégie trouvée :", self.bestParam)
                print(">> Fitness associée            :", round(self.best_fitness, 4))
                print("========================================\n")

            self.param = self.mutate(self.bestParam)
            self.trial += 1
            self.iteration += 1
            return 0, 0, True

        # fonction de contrôle
        translation = math.tanh(self.param[0] + self.param[1] * sensors[sensor_front_left] +
                                self.param[2] * sensors[sensor_front] + self.param[3] * sensors[sensor_front_right])
        rotation = math.tanh(self.param[4] + self.param[5] * sensors[sensor_front_left] +
                             self.param[6] * sensors[sensor_front] + self.param[7] * sensors[sensor_front_right])

        if debug and self.iteration % 100 == 0:
            print("Robot", self.robot_id, "at step", self.iteration)
            print("Sensors =", sensors)

        self.iteration += 1
        return translation, rotation, False

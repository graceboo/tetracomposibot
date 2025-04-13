from robot import * 
import math

nb_robots = 0
debug = False

class Robot_player(Robot):

    team_name = "RandomSearch"
    robot_id = -1
    iteration = 0

    param = []
    bestParam = []
    #evaluations = 500   # nombre total de comportements à tester
    #it_per_evaluation = 400 # chaque comportement est testé pendant 400 itérations
    trial = 0

    x_0 = 0
    y_0 = 0
    theta_0 = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a",evaluations=0,it_per_evaluation=0):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = theta_0
        self.param = [random.randint(-1, 1) for i in range(8)]
        self.evaluations = evaluations
        self.it_per_evaluation = it_per_evaluation

        self.best_score = -math.inf
        self.bestParam = []
        self.best_trial = 0

        self.repeat_count = 0      # combien de fois on a testé le comportement courant
        self.total_score = 0       # la somme des scores des 3 tests

        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def reset(self):
        super().reset()
        self.theta = random.uniform(-math.pi, math.pi)  # orientation aléatoire en radian

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

            # toutes les X itérations: le robot est remis à sa position initiale avec orientation aléatoire
            if self.iteration % self.it_per_evaluation == 0 :
                if self.iteration > 0:
                    score = self.log_sum_of_translation * (1 - abs(self.log_sum_of_rotation))
                    self.total_score += score
                    self.repeat_count += 1
                    print(f"→ Score #{self.repeat_count} = {score}")

                    if self.repeat_count < 3 :
                        print(" Répétition pour la même stratégie")
                        self.iteration += 1
                        return 0, 0, True  # même stratégie, orientation différente

                    else:
                        print(f" Score total = {self.total_score}")
                        with open("random/results_random10.txt", "a") as f:
                            f.write(f"{self.trial}, {self.total_score}, {self.best_score}\n")

                        if self.total_score > self.best_score:
                            self.best_score = self.total_score
                            self.bestParam = self.param.copy()
                            self.best_trial = self.trial
                            print(" Nouveau meilleur score :", self.best_score)
                            print(" Paramètres :", self.bestParam)
                        
    
                        # Si on n’a pas encore fini toutes les evaluations 
                        if self.trial < self.evaluations :
                            self.total_score = 0
                            self.repeat_count = 0
                            self.param = [random.randint(-1, 1) for i in range(8)] # on teste avec de nouveaux paramètres 
                            self.trial = self.trial + 1
                            print ("Trying strategy no.",self.trial)
                            self.iteration = self.iteration + 1
                            return 0, 0, True # ask for reset on passe à la suivante évaluation
                        else:
                            print("best evaluation : ", self.best_trial," de paramètres : ",self.bestParam," et un score : ",self.best_score)
                            self.param = self.bestParam
                            print("Rejoue le meilleur comportement")
                            return 0, 0, True
                # si c'est la première itération
                self.trial = self.trial + 1
                print ("Trying strategy no.",self.trial)
                self.iteration = self.iteration + 1
                return 0, 0, True # ask for reset
            
            # Fonction de contrôle (Perceptron)
            translation = math.tanh(
                self.param[0] + self.param[1] * sensors[sensor_front_left] +
                self.param[2] * sensors[sensor_front] + self.param[3] * sensors[sensor_front_right]
            )
            rotation = math.tanh(
                self.param[4] + self.param[5] * sensors[sensor_front_left] +
                self.param[6] * sensors[sensor_front] + self.param[7] * sensors[sensor_front_right]
            )

            if debug:
                print(f"[{self.iteration}] translation = {translation:.3f}, rotation = {rotation:.3f}")

            self.iteration += 1
            return translation, rotation, False

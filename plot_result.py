import os
import matplotlib.pyplot as plt
import numpy as np

def load_scores(folder, prefix, num_runs=10):
    all_scores = []

    for i in range(1, num_runs + 1):
        file_path = os.path.join(folder, f"{prefix}{i}.txt")
        evals = []
        best_scores = []
        with open(file_path, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 3:
                    evals.append(int(parts[0]))
                    best_scores.append(float(parts[2]))
        all_scores.append(best_scores)
    return np.array(all_scores)

def plot_individual_and_average(all_scores, label, color):
    for run in all_scores:
        plt.plot(run, color=color, alpha=0.2)
    avg = np.mean(all_scores, axis=0)
    plt.plot(avg, color=color, label=label, linewidth=2)
    return avg

# 📁 Dossiers contenant les résultats
random_folder = "random"
genetic_folder = "genetic"

# 📌 Chargement
random_scores = load_scores(random_folder, "results_random")
genetic_scores = load_scores(genetic_folder, "results_genetic")

# 📊 Tracé
plt.figure(figsize=(12, 6))
plot_individual_and_average(random_scores, "Random Search (moyenne)", "blue")
plot_individual_and_average(genetic_scores, "Genetic Algorithm (moyenne)", "green")

plt.title("Comparaison des scores (meilleur score au fil des évaluations)")
plt.xlabel("Évaluation")
plt.ylabel("Score cumulé (meilleur)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("comparison_plot.png")
plt.show()

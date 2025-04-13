import os
import matplotlib.pyplot as plt
import numpy as np

def load_scores(folder, prefix, num_runs=10):
    all_scores = []

    for i in range(1, num_runs + 1):
        file_path = os.path.join(folder, f"{prefix}{i}.txt")
        best_scores = []
        with open(file_path, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 3:
                    best_scores.append(float(parts[2]))
        all_scores.append(best_scores)
    return np.array(all_scores)

def plot_mean_curve(all_scores, label, color):
    min_len = min(len(run) for run in all_scores)
    trimmed_scores = np.array([run[:min_len] for run in all_scores])
    mean_scores = np.mean(trimmed_scores, axis=0)
    plt.plot(mean_scores, label=label, color=color)

# 📁 Dossiers contenant les résultats
random_folder = "random"
genetic_folder = "genetic"

# 📌 Chargement
random_scores = load_scores(random_folder, "results_random")
genetic_scores = load_scores(genetic_folder, "results_genetic")

# Tracé
plt.figure(figsize=(12, 6))
plot_mean_curve(random_scores, "Random Search (moyenne)", "blue")
plot_mean_curve(genetic_scores, "Genetic Algorithm (moyenne)", "green")

plt.title("Comparaison des scores moyens (10 runs chacun)")
plt.xlabel("Évaluation")
plt.ylabel("Score cumulé (moyen)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("comparison_mean.png")
plt.show()

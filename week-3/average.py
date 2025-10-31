import numpy as np

tiny = [4, 5, 2, 3, 1]
distil = [2, 3, 1, 3, 1]
falcon = [4, 5, 3, 5, 3]

models = {"TinyLlama": tiny, "DistilGPT2": distil, "Falcon": falcon}

for model, scores in models.items():
    avg = np.mean(scores)
    print(f"{model} Average Effectiveness: {avg:.2f}/5")

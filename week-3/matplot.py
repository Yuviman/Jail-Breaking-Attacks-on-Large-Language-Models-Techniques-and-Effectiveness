import matplotlib.pyplot as plt
import numpy as np

techniques = ["Direct Prompt", "DAN Persona", "Typoglycemia", "Grandmother", "HTML Injection"]
tiny = [4, 5, 2, 3, 1]
distil = [2, 3, 1, 3, 1]
falcon = [4, 5, 3, 5, 3]

x = np.arange(len(techniques))
width = 0.25

fig, ax = plt.subplots()
ax.bar(x - width, tiny, width, label="TinyLlama-1.1B")
ax.bar(x, distil, width, label="DistilGPT-2")
ax.bar(x + width, falcon, width, label="Falcon-RW-1B")

ax.set_xlabel("Jailbreak Technique")
ax.set_ylabel("Effectiveness (1–5)")
ax.set_title("Model-wise Jailbreak Effectiveness Comparison")
ax.set_xticks(x)
ax.set_xticklabels(techniques, rotation=20)
ax.legend()
plt.tight_layout()
plt.show()

import json
import matplotlib.pyplot as plt
from pathlib import Path
ROOT = Path(__file__).parent
data = json.load(open(ROOT / "results.json"))
# bias counts
counts = {}
for r in data:
    for b in r["predicted"]:
        counts[b] = counts.get(b, 0) + 1
plt.bar(list(counts.keys()), list(counts.values()))
plt.title("Predicted Bias Counts")
plt.savefig(ROOT / "predicted_bias_counts.png")
print("Saved plots to evaluation/predicted_bias_counts.png")

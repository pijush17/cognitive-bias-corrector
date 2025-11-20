import requests
import json
import time
from pathlib import Path

SRC = "http://127.0.0.1:8000/decide"
ROOT = Path(__file__).parent
cases = json.load(open(ROOT / "test_cases.json"))

results = []
for c in cases:
    payload = {"user_id": "eval_user", "text": c["text"]}
    t0 = time.time()
    r = requests.post(SRC, json=payload)
    t1 = time.time()
    try:
        resp = r.json()
    except Exception:
        resp = {"error": r.text}
    results.append({
        "id": c["id"],
        "text": c["text"],
        "ground_truth": c["ground_truth_biases"],
        "predicted": [b.get("bias") for b in resp.get("detected_biases", [])],
        "duration_ms": int((t1 - t0) * 1000)
    })

out = ROOT / "results.json"
open(out, "w", encoding="utf-8").write(json.dumps(results, indent=2))
print(f"Saved evaluation to {out}")

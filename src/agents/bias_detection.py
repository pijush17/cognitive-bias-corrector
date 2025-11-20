import json
import os
from src.tools.llm_client import LLMClient

PROMPT_PATH = os.path.join(os.getcwd(), "prompts", "bias_detection.txt")

# Simple triggers for fallback
TRIGGERS = {
    "scarcity": ["only", "last", "limited", "left", "ends", "sale ends"],
    "recency": ["recently", "just", "today", "yesterday", "last night"],
    "sunk_cost": ["already invested", "wasted", "spent a lot", "paid for"],
    "confirmation": ["i believe", "i know", "obviously", "for sure"],
    "loss_aversion": ["can't lose", "avoid losing", "don't want to lose"]
}

class BiasDetectionAgent:
    def __init__(self):
        self.llm = LLMClient()

    def detect(self, context):
        text = context.get("raw_text", "") or ""
        # Use LLM prompt first
        try:
            with open(PROMPT_PATH, "r", encoding="utf-8") as f:
                prompt_template = f.read()
        except Exception:
            prompt_template = ("System: You are an expert behavioral psychologist.\n"
                               "User: Given the decision JSON: {decision_json}\n"
                               "Identify likely cognitive biases and return a JSON array: "
                               '[{"bias":"name","reason":"...","confidence":0.0}, ...]')

        prompt = prompt_template.replace("{decision_json}", json.dumps(context))
        resp = self.llm.completion(prompt)
        try:
            arr = json.loads(resp.get("text", "[]"))
            if isinstance(arr, list):
                return arr
        except Exception:
            # fallback rule-based
            found = []
            lower = text.lower()
            for name, triggers in TRIGGERS.items():
                for t in triggers:
                    if t in lower:
                        found.append({"bias": name, "reason": f"trigger word '{t}' found", "confidence": 0.8})
                        break
            return found
        return []

import json
import os
from src.tools.llm_client import LLMClient

PROMPT_PATH = os.path.join(os.getcwd(), "prompts", "bias_explain.txt")

class BiasExplanationAgent:
    def __init__(self):
        self.llm = LLMClient()

    def explain(self, context, detected):
        try:
            with open(PROMPT_PATH, "r", encoding="utf-8") as f:
                prompt_template = f.read()
        except Exception:
            prompt_template = ("System: You are a patient teacher.\n"
                               "User: Given the detected biases and the decision, explain each bias briefly.\n"
                               "Input: {input}\nReturn JSON: [{\"bias\":\"...\",\"explanation\":\"...\",\"example\":\"...\"}]")

        payload = {
            "context": context,
            "detected": detected
        }
        prompt = prompt_template.replace("{input}", json.dumps(payload))

        resp = self.llm.completion(prompt)
        try:
            return json.loads(resp.get("text", "[]"))
        except Exception:
            # fallback simple explanation generated locally
            out = []
            for d in detected:
                b = d.get("bias")
                out.append({
                    "bias": b,
                    "explanation": f"Detected {b}. This bias can influence quick decisions.",
                    "example": f"A simple example of {b}...\n"
                })
            return out

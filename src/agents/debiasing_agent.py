import json
import os
from src.tools.llm_client import LLMClient
from src.tools.evidence_fetcher import EvidenceFetcher

PROMPT_PATH = os.path.join(os.getcwd(), "prompts", "debiasing.txt")

class DebiasingAgent:
    def __init__(self):
        self.llm = LLMClient()
        self.evidence = EvidenceFetcher()

    def suggest(self, context, detected):
        # Build prompt and call LLM, then attach evidence via EvidenceFetcher
        try:
            with open(PROMPT_PATH, "r", encoding="utf-8") as f:
                prompt_template = f.read()
        except Exception:
            prompt_template = ("System: You are a pragmatic advisor.\n"
                               "User: Given context {context} and detected biases {detected}, produce 3 alternatives: "
                               "logical, evidence_based, emotion_aware. Return JSON with 'alternatives' list.")

        prompt = prompt_template.replace("{context}", json.dumps(context)).replace("{detected}", json.dumps(detected))
        resp = self.llm.completion(prompt)
        try:
            result = json.loads(resp.get("text","{}"))
        except Exception:
            # fallback simple suggestions
            result = {
                "alternatives": [
                    {"type":"logical","action":"Wait 48 hours and compare options","why":"Cool off and gather info","evidence_query":"best laptop deals 2025"},
                    {"type":"evidence_based","action":"Compare total cost of ownership","why":"See real cost","evidence_query":"laptop total cost ownership calculator"},
                    {"type":"emotion_aware","action":"Set a cooling-off reminder for 2 days","why":"Avoid impulse buy","evidence_query":""}
                ]
            }

        # For any alternative that contains 'evidence_query', call EvidenceFetcher
        for alt in result.get("alternatives", []):
            q = alt.get("evidence_query")
            if q:
                alt["evidence"] = self.evidence.search(q)
        return result

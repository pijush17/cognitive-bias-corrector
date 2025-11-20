import json
import os
from src.tools.llm_client import LLMClient

PROMPT_PATH = os.path.join(os.getcwd(), "prompts", "decision_understanding.txt")

class DecisionUnderstandingAgent:
    def __init__(self):
        self.llm = LLMClient()

    def parse(self, text: str):
        # Try LLM-based parse; fallback to simple heuristics
        try:
            with open(PROMPT_PATH, "r", encoding="utf-8") as f:
                prompt_template = f.read()
        except Exception:
            prompt_template = ("System: You are a concise JSON extractor.\n"
                               "User: Read the user decision: \"{user_text}\"\n"
                               "Return JSON with: summary, domain (purchase|academic|finance|personal|other), "
                               "constraints (list), emotions (calm|anxious|angry|hopeful|other), raw_text.\n")

        prompt = prompt_template.replace("{user_text}", text)
        resp = self.llm.completion(prompt)
        # If llm returns JSON-like text, try to parse
        try:
            obj = json.loads(resp.get("text", "{}"))
            return obj
        except Exception:
            # fallback quick heuristic
            lower = text.lower()
            #domain detection
            domain = "other"
            if any(k in lower for k in ["buy", "price", "sale", "purchase"]):
                domain = "purchase"
            elif any(k in lower for k in ["exam", "score", "grade", "assignment"]):
                domain = "academic"
            elif any(k in lower for k in ["invest", "stocks", "bank", "loan"]):
                domain = "finance"
                
            #emotions detection
            # If urgent keywords appear → emotion = urgent
            if any(w in lower for w in ["now","immediately","asap","must buy","urgent","only", "last"]):
                emotions = "urgent"
            else:    
                emotions = "anxious" if any(w in lower for w in ["worried","afraid","panic","anxious","stressed"]) else "calm"
            return{
                "summary": text if len(text) < 200 else text[:197] + "...",
                "domain": domain,
                "constraints": [],
                "emotions": emotions,
                "raw_text": text
            }
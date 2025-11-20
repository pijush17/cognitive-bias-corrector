import os
import json
try:
 import openai
except Exception:
    openai = None

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if openai and self.api_key:
            openai.api_key = self.api_key

    def completion(self, prompt: str, max_tokens: int = 300):
        """
        If OPENAI_API_KEY is set and openai is installed, call OpenAI completion (text-davinci style).
        Otherwise return a simple stub response to keep local flow working.
        """
        if openai and self.api_key:
            try:
                # Use the simple completion endpoint for compatibility. Adjust for your provider.
                resp = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=max_tokens, temperature=0.3)
                text = resp.choices[0].text.strip()
                return {"text": text}
            except Exception as e:
                return {"text": f"{{\"error\":\"openai_error\",\"message\":\"{str(e)}\"}}"}
        # Stub response: try to return something JSON-like for common prompts
        if "Identify likely cognitive biases" in prompt or "behavioral psychologist" in prompt:
            return {"text": "[{\"bias\":\"scarcity\",\"reason\":\"'only' or 'left' phrasing\",\"confidence\":0.8}]"}
        if "produce 3 alternatives" in prompt or "pragmatic advisor" in prompt:
            return {"text": "{\"alternatives\": [{\"type\":\"logical\",\"action\":\"Wait 48 hours\",\"why\":\"Avoid impulse\",\"evidence_query\":\"\"}]}"}
        # default echo
        return {"text": prompt[:1000]}

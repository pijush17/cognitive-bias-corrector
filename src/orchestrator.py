import time
import json
import logging
from uuid import uuid4
from src.agents.decision_understanding import DecisionUnderstandingAgent
from src.agents.bias_detection import BiasDetectionAgent
from src.agents.bias_explanation import BiasExplanationAgent
from src.agents.debiasing_agent import DebiasingAgent
from src.memory.memory_bank import MemoryBank
logger = logging.getLogger("bias-corrector")
handler = logging.FileHandler("logs/trace.log")
handler.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class Orchestrator:
    def __init__(self):
        self.du = DecisionUnderstandingAgent()
        self.bd = BiasDetectionAgent()
        self.be = BiasExplanationAgent()
        self.db = DebiasingAgent() 
        self.mem = MemoryBank()

    def handle_decision(self, user_id: str, text: str):
        trace_id = str(uuid4())
        t0 = time.time()
        # Step 1: Understand
        context = self.du.parse(text)
        context['raw_text'] = text

        # Step 2: Detect
        detected = self.bd.detect(context)

        # Step 3: Explain
        explanations = self.be.explain(context, detected)

        # Step 4: Debias and gather evidence
        correction = self.db.suggest(context, detected)

        # Save to memory
        self.mem.save(user_id, {
            "trace_id": trace_id,
            "text": text,
            "context": context,
            "detected": detected,
            "correction": correction,
            "timestamp": time.time()
        })

        t1 = time.time()
        duration_ms = int((t1 - t0) * 1000)

        result = {
            "trace_id": trace_id,
            "input_text": text,
            "context": context,
            "detected_biases": detected,
            "explanations": explanations,
            "correction": correction,
            "duration_ms": duration_ms
        }

        # Log trace (JSON line)
        logger.info(json.dumps({
            "trace_id": trace_id,
            "user_id": user_id,
            "duration_ms": duration_ms,
            "num_biases": len(detected),
            "steps": ["understand", "detect", "explain", "debias"]
        }))

        return result

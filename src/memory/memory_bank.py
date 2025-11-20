import json
import os
from datetime import datetime

class MemoryBank:
    def __init__(self, fname="memory.json"):
        self.fname = os.path.join(os.getcwd(), fname)
        self._load()

    def _load(self):
        if os.path.exists(self.fname):
            try:
                self.mem = json.load(open(self.fname, "r", encoding="utf-8"))
            except Exception:
                self.mem = {}
        else:
            self.mem = {}

    def save(self, user_id: str, record: dict):
        user = self.mem.get(user_id, {"records": [], "bias_counts": {}})
        user["records"].append(record)
        # update bias counts
        for b in record.get("detected", []):
            name = b.get("bias")
            if name:
                user["bias_counts"][name] = user["bias_counts"].get(name, 0) + 1
        user["last_updated"] = datetime.utcnow().isoformat()
        self.mem[user_id] = user
        with open(self.fname, "w", encoding="utf-8") as f:
            json.dump(self.mem, f, indent=2)

    def get(self, user_id: str):
        return self.mem.get(user_id, {"records": [], "bias_counts": {}})

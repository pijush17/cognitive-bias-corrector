from fastapi import FastAPI
from pydantic import BaseModel
from src.orchestrator import Orchestrator
import uvicorn

app = FastAPI(title="Cognitive Bias Corrector (Concierge Agent)")

orc = Orchestrator()

class DecisionIn(BaseModel):
    user_id: str
    text: str

@app.post("/decide")
def decide(payload: DecisionIn):
    return orc.handle_decision(payload.user_id, payload.text)

@app.get("/memory/{user_id}")
def get_memory(user_id: str):
    return orc.mem.get(user_id)

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)

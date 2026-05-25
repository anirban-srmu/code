"""Day 6 demo: simple event API server.
Run: uvicorn fastapi_event_server:app --reload --host 0.0.0.0 --port 8000
"""
from datetime import datetime
from typing import List, Dict, Any
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Vision Event Server")
events: List[Dict[str, Any]] = []

class VisionEvent(BaseModel):
    camera_id: str
    event_type: str
    label: str
    confidence: float
    timestamp: float | None = None

@app.post("/events")
def create_event(event: VisionEvent):
    item = event.model_dump()
    item["received_at"] = datetime.utcnow().isoformat()
    events.append(item)
    return {"status": "stored", "count": len(events), "event": item}

@app.get("/events")
def list_events():
    return {"count": len(events), "events": events[-50:]}

@app.get("/health")
def health():
    return {"status": "ok"}

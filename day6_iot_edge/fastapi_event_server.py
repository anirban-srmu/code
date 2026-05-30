"""Day 6 demo: simple event API server.
Run: uvicorn fastapi_event_server:app --reload --host 0.0.0.0 --port 8000
"""
from datetime import datetime
from typing import List, Dict, Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from pydantic import BaseModel,ConfigDict

app = FastAPI(title="AI Vision Event Server")
events: List[Dict[str, Any]] = []

app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

class VisionEvent(BaseModel):
    model_config = ConfigDict(extra="allow")
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

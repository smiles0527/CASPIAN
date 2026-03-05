import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from database import init_db, get_db
from models import Entry
from llm_service import generate_insights

# CORS: use CORS_ORIGINS env var (comma-separated) or default to localhost for dev
_cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
CORS_ORIGINS = [o.strip() for o in _cors_origins.split(",") if o.strip()]


# --- Pydantic schemas ---
class SensorInput(BaseModel):
    sensor_1: Optional[float] = None
    sensor_2: Optional[float] = None
    sensor_3: Optional[float] = None
    sensor_4: Optional[float] = None
    sensor_5: Optional[float] = None
    sensor_6: Optional[float] = None
    sensor_7: Optional[float] = None
    sensor_8: Optional[float] = None
    sensor_9: Optional[float] = None
    sensor_10: Optional[float] = None
    sensor_11: Optional[float] = None
    sensor_12: Optional[float] = None
    sensor_13: Optional[float] = None
    sensor_14: Optional[float] = None
    sensor_15: Optional[float] = None
    sensor_16: Optional[float] = None
    sensor_17: Optional[float] = None
    sensor_18: Optional[float] = None
    sensor_19: Optional[float] = None
    sensor_20: Optional[float] = None
    feelings: Optional[str] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    # cleanup if needed
    pass


app = FastAPI(title="CASPIAN Follow-Up Care", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/entries", response_model=list)
def list_entries(db: Session = Depends(get_db), limit: int = 10):
    entries = db.query(Entry).order_by(Entry.created_at.desc()).limit(limit).all()
    return [e.to_dict() for e in entries]


@app.get("/entries/{entry_id}", response_model=dict)
def get_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(Entry).filter(Entry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry.to_dict()


@app.post("/insights")
def create_insights(input_data: SensorInput, db: Session = Depends(get_db)):
    sensors = [
        getattr(input_data, f"sensor_{i}", None) for i in range(1, 21)
    ]
    feelings = input_data.feelings

    # Fetch last 8 entries (excluding current) for history
    history_rows = (
        db.query(Entry)
        .order_by(Entry.created_at.desc())
        .limit(8)
        .all()
    )
    history_entries = [e.to_dict() for e in history_rows]

    try:
        summary, care_plan = generate_insights(sensors, feelings, history_entries)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate insights: {str(e)}")

    # Save new entry
    entry = Entry(
        sensor_1=input_data.sensor_1,
        sensor_2=input_data.sensor_2,
        sensor_3=input_data.sensor_3,
        sensor_4=input_data.sensor_4,
        sensor_5=input_data.sensor_5,
        sensor_6=input_data.sensor_6,
        sensor_7=input_data.sensor_7,
        sensor_8=input_data.sensor_8,
        sensor_9=input_data.sensor_9,
        sensor_10=input_data.sensor_10,
        sensor_11=input_data.sensor_11,
        sensor_12=input_data.sensor_12,
        sensor_13=input_data.sensor_13,
        sensor_14=input_data.sensor_14,
        sensor_15=input_data.sensor_15,
        sensor_16=input_data.sensor_16,
        sensor_17=input_data.sensor_17,
        sensor_18=input_data.sensor_18,
        sensor_19=input_data.sensor_19,
        sensor_20=input_data.sensor_20,
        feelings=feelings,
        insights=summary,
        care_plan=care_plan,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)

    return {
        "id": entry.id,
        "insights": summary,
        "care_plan": care_plan,
        "created_at": entry.created_at.isoformat() if entry.created_at else None,
    }

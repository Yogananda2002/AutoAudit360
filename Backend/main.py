# main.py

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime
from typing import Optional, List
import os
import shutil

# HuggingFace and PIL
from transformers import pipeline
from PIL import Image

# SQLAlchemy JSON support
from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import JSON

UPLOAD_DIR = "uploads"
DB_URL = "sqlite:///database.db"

# Ensure upload folder exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Database setup
engine = create_engine(DB_URL, echo=False)

# Object detection pipeline (load at startup)
object_detector = pipeline("object-detection", model="facebook/detr-resnet-50")

# Database model
class UploadedFile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    upload_time: datetime
    detections: Optional[list] = Field(default=None, sa_column=Column(JSON))

def init_db():
    SQLModel.metadata.create_all(engine)

app = FastAPI(
    title="AutoAudit360 API",
    description="Backend API for image uploads and compliance audit.",
    version="0.2.0"
)

# Enable CORS for local frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Save the file
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run object detection (Hugging Face)
    try:
        image = Image.open(file_location)
        results = object_detector(image)
        labels = list({result['label'] for result in results})
    except Exception as e:
        labels = []
        print(f"Detection error: {e}")

    # Save to DB
    uploaded = UploadedFile(
        filename=file.filename,
        upload_time=datetime.utcnow(),
        detections=labels
    )
    with Session(engine) as session:
        session.add(uploaded)
        session.commit()
    return {
        "message": "File uploaded and analyzed",
        "filename": file.filename,
        "detections": labels
    }

@app.get("/files")
def list_files():
    with Session(engine) as session:
        files = session.exec(select(UploadedFile)).all()
        return files

@app.get("/uploads/{filename}")
def get_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    return FileResponse(file_path)

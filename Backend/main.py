# main.py

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime
import os
import shutil

UPLOAD_DIR = "uploads"
DB_URL = "sqlite:///database.db"

# Ensure upload folder exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Database setup
engine = create_engine(DB_URL)

class UploadedFile(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    filename: str
    upload_time: datetime

def init_db():
    SQLModel.metadata.create_all(engine)

app = FastAPI(
    title="AutoAudit360 API",
    description="Backend API for image uploads and compliance audit.",
    version="0.1.0"
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
    # Save to DB
    uploaded = UploadedFile(
        filename=file.filename,
        upload_time=datetime.utcnow()
    )
    with Session(engine) as session:
        session.add(uploaded)
        session.commit()
    return {"message": "File uploaded successfully", "filename": file.filename}

@app.get("/files")
def list_files():
    with Session(engine) as session:
        files = session.exec(select(UploadedFile)).all()
        return files

@app.get("/uploads/{filename}")
def get_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    return FileResponse(file_path)


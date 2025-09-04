# AutoAudit360

**AI-Powered Automated Compliance Auditor for Visual and Document Data**

---

## What is AutoAudit360?

AutoAudit360 is an intelligent platform that automates compliance checks from images and documents. Our MVP focuses on uploading images and laying the foundation for integrating AI object detection.

---

## Tech Stack

- Backend: Python (FastAPI)
- Frontend: React.js
- Database: SQLite (for MVP)
- Storage: Local file system (upgradeable to S3)
- Model Integration: HuggingFace (planned)

---

## MVP Workflow

1. User uploads an image via dashboard.
2. Backend stores the image and metadata.
3. Uploaded images are listed in the dashboard.

---


## Getting Started

### Backend Setup

1. Install Python 3.9+
2. `cd backend`
3. `python -m venv venv`
4. `source venv/bin/activate`
5. `pip install -r requirements.txt`
6. `uvicorn main:app --reload`

### Frontend Setup

1. Install Node.js 18+
2. `cd frontend`
3. `npm install`
4. `npm start`

## Backend API Endpoints

- `POST /upload`: Upload an image file. Returns filename and status.
- `GET /files`: List all uploaded files with metadata.
- `GET /uploads/{filename}`: Download a specific file.

See interactive API docs at `/docs`.

## Frontend MVP Features

- Upload images to the backend
- See all uploaded images with thumbnails, filename, upload time
- React.js with Axios, styled for usability

## AI Object Detection

Each uploaded image is automatically analyzed with a Hugging Face DETR object detection model.  
Detected objects are listed in the dashboard for quick compliance review.

---
## Authors

- Yoga Nanda (Product Owner, Tech Lead, documentation)

from fastapi import FastAPI, UploadFile, File
import shutil
import os
from backend.video_compare import compare_videos

app = FastAPI()

UPLOAD_FOLDER = "uploads"
DATASET_VIDEO = "dataset/virat_kohli/cover_drive.mp4"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload")

async def upload_video(video: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_FOLDER, video.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    compare_videos(file_path, DATASET_VIDEO)

    return {"message": "Comparison started"}

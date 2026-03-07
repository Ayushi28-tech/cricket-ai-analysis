from fastapi import FastAPI, UploadFile, File
import shutil
import os
from backend.video_compare import compare_videos

app = FastAPI()

UPLOAD_FOLDER = "uploads"
REFERENCE_VIDEO = "dataset/virat_kohli/cover_drive.mp4"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload")

async def upload_video(video: UploadFile = File(...)):

    file_location = os.path.join(UPLOAD_FOLDER, video.filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    # start comparison
    compare_videos(file_location, REFERENCE_VIDEO)

    return {"message": "Video uploaded and comparison started"}

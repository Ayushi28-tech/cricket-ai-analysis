from fastapi import FastAPI, UploadFile, File
import shutil
import os

app = FastAPI()

UPLOAD_FOLDER = "uploads"

@app.post("/upload")

async def upload_video(video: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_FOLDER, video.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    return {"message": "Video uploaded"}

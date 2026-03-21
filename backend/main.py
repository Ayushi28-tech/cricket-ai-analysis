from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import shutil
import os
from backend.image_compare import compare_images
#from backend.video_compare import compare_videos

app = FastAPI()

#folders
os.makedirs("output", exist_ok=True)

# static for output video only
app.mount("/output", StaticFiles(directory="output"), name="output")
#app.mount("/videos", StaticFiles(directory="dataset/virat_kohli"), name="videos")

#cores
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#home page
@app.get("/")
def home():
    return FileResponse("frontend/index.html")

# upload API
#@app.post("/upload")
#async def upload_video(file: UploadFile = File(...)):

    #file_path = f"uploads/{file.filename}"

    #with open(file_path, "wb") as buffer:
        #shutil.copyfileobj(file.file, buffer)

    #similarity, feedback, phases, output_video = compare_videos(file_path)

    #return {
       # "status": "completed",
        #"similarity": similarity,
       # "feedback": feedback,
        #"phases": phases,
        #"video_url": "/output/result.mp4"}

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    similarity, output_image = compare_images(file_path)

    return {
        "similarity": similarity,
        "image_url": f"/output/result.jpg"
    }
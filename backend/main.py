from fastapi import FastAPI, UploadFile, File
import shutil

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Cricket AI Analysis API Running"}

@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    
    with open(f"uploads/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "Video uploaded successfully"}

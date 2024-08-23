from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse

from math_project.functions import modify_image

app = FastAPI()

IMAGEDIR = "images/"

@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    file.filename = "image.jpg"
    filename = f"{IMAGEDIR}{file.filename}"
    content = await file.read()

    with open(filename, "wb") as f:
        f.write(content)

    modify_image(filename)

    return FileResponse(filename)
    
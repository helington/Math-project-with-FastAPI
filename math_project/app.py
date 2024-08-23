from fastapi import FastAPI, UploadFile, Response

from math_project.schemas import Message, Image

app = FastAPI()

@app.post("/upload/")
async def create_upload_file(file: UploadFile | None = None):
    content = await file.read()
    if not file:
        return {"message": "No upload file sent"}
    else:
        return Response(content=content, media_type="image/png")

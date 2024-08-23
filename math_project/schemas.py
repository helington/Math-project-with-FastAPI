from pydantic import BaseModel, AnyUrl

class Image(BaseModel):
    url: AnyUrl

class Message(BaseModel):
    message: str
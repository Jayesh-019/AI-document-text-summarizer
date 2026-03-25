from pydantic import BaseModel


class TextRequest(BaseModel):
    text: str


class SummaryResponse(BaseModel):
    original_text: str
    summary: str

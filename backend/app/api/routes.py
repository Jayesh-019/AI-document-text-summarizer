from fastapi import APIRouter, File, HTTPException, UploadFile

from app.models.schemas import SummaryResponse, TextRequest
from app.services.summarizer import extract_text_from_file, summarize_text

router = APIRouter()


@router.post("/summarize-text", response_model=SummaryResponse)
def summarize_from_text(payload: TextRequest):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    summary = summarize_text(payload.text)
    return SummaryResponse(original_text=payload.text, summary=summary)


@router.post("/summarize-file", response_model=SummaryResponse)
async def summarize_from_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="File name is missing.")

    content = await file.read()

    try:
        text = extract_text_from_file(file.filename, content)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from file.")

    summary = summarize_text(text)
    return SummaryResponse(original_text=text, summary=summary)

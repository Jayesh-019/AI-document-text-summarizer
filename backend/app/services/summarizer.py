from io import BytesIO

from pypdf import PdfReader
from transformers import pipeline

from app.core.config import MAX_INPUT_WORDS, MODEL_NAME

summarizer = pipeline("summarization", model=MODEL_NAME, device=-1)


def chunk_text(text: str, max_words: int = MAX_INPUT_WORDS) -> list[str]:
    words = text.split()
    return [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]


def summarize_text(text: str) -> str:
    cleaned = " ".join(text.split())
    if not cleaned:
        return ""

    chunks = chunk_text(cleaned)
    partial_summaries = []

    for chunk in chunks:
        result = summarizer(
            chunk,
            max_length=130,
            min_length=30,
            do_sample=False,
            truncation=True,
        )
        partial_summaries.append(result[0]["summary_text"])

    combined = " ".join(partial_summaries)

    if len(partial_summaries) == 1:
        return combined

    final_result = summarizer(
        combined,
        max_length=150,
        min_length=40,
        do_sample=False,
        truncation=True,
    )
    return final_result[0]["summary_text"]


def extract_text_from_file(filename: str, content: bytes) -> str:
    lower_name = filename.lower()

    if lower_name.endswith(".txt"):
        return content.decode("utf-8", errors="ignore")

    if lower_name.endswith(".pdf"):
        reader = PdfReader(BytesIO(content))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)

    raise ValueError("Only .txt and .pdf files are supported.")

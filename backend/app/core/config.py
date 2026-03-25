import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "sshleifer/distilbart-cnn-6-6")
MAX_INPUT_WORDS = int(os.getenv("MAX_INPUT_WORDS", "800"))
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "*")

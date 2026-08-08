import os 
from dotenv import load_dotenv
load_dotenv() 

class Config:
    """Classe pour stocker la configuration globale du projet."""
    API_KEY = os.getenv("API_KEY", "")
    BASE_URL = os.getenv("BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash")

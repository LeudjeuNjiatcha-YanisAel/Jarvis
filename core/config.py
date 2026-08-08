import os 
from dotenv import load_dotenv
load_dotenv() 

class Config:
    """Classe pour stocker la configuration globale du projet."""
    
    # 4. Récupère la clé API de l'environnement (ça peut être Gemini, Groq, etc.)
    API_KEY = os.getenv("API_KEY", "")
    
    # 5. Récupère l'URL de l'API (permet de dire à la librairie OpenAI de parler à Google, Groq, ou Cerebras)
    BASE_URL = os.getenv("BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
    
    # 6. Définit le nom du modèle que Jarvis utilisera par défaut.
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash")

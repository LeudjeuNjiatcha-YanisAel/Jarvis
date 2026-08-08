import os 
from dotenv import load_dotenv
load_dotenv() 

class Config:
    """Classe pour stocker la configuration globale du projet."""
    
    # On récupère TOUTES les clés API, séparées par des virgules
    # Exemple dans .env : API_KEYS=cle1,cle2,cle3
    # On les découpe en une liste Python : ["cle1", "cle2", "cle3"]
    _raw_keys = os.getenv("API_KEYS", "")
    API_KEYS = [k.strip() for k in _raw_keys.split(",") if k.strip()]
    
    # On garde la première clé comme clé "par défaut" pour la compatibilité
    API_KEY = API_KEYS[0] if API_KEYS else ""
    
    # L'URL du serveur d'IA (Google Gemini, Groq, Cerebras...)
    BASE_URL = os.getenv("BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
    
    # Le nom du modèle d'IA à utiliser
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")
    
    # Clé spécifique pour les oreilles (Groq possède Whisper)
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    
    # Clé pour la voix ultra-réaliste ElevenLabs
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")

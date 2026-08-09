import os 
from dotenv import load_dotenv
load_dotenv() 

class Config:
    """Classe pour stocker la configuration globale du projet."""
    
    # On récupère TOUTES les clés API, séparées par des virgules
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

    # Clés optionnelles pour d'autres fournisseurs IA
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY", "")
    
    # Configuration des fournisseurs d'IA disponibles en fallback/spécifique
    PROVIDERS = [
        {
            "name": "default",
            "keys": API_KEYS,
            "base_url": BASE_URL,
            "model": MODEL_NAME
        },
        {
            "name": "groq",
            "keys": [GROQ_API_KEY],
            "base_url": "https://api.groq.com/openai/v1",
            "model": "llama-3.3-70b-versatile"
        },
        {
            "name": "deepseek",
            "keys": [DEEPSEEK_API_KEY],
            "base_url": "https://api.deepseek.com",
            "model": "deepseek-chat"
        },
        {
            "name": "cerebras",
            "keys": [CEREBRAS_API_KEY],
            "base_url": "https://api.cerebras.ai/v1",
            "model": "llama3.1-8b"
        }
    ]

# 1. Importe le module os pour interagir avec le système d'exploitation (lire les variables d'environnement)
import os 
# 2. Importe la fonction load_dotenv pour lire un fichier .env (qui contient nos mots de passe/clés secrètes)
from dotenv import load_dotenv

# 3. Charge les variables définies dans le fichier .env dans la mémoire de notre programme
load_dotenv() 

class Config:
    """Classe pour stocker la configuration globale du projet."""
    
    # 4. Récupère la clé API OpenAI depuis l'environnement. 
    # Si elle n'existe pas, retourne une chaîne vide "" par défaut.
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # 5. Définit le nom du modèle que Jarvis utilisera par défaut.
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

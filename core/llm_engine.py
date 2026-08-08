# 1. Importe le client OpenAI pour communiquer avec l'IA
from openai import OpenAI
# 2. Importe notre configuration (qui contient la clé API et le nom du modèle)
from core.config import Config
# 3. Importe notre outil de log pour suivre ce que fait le cerveau
from utils.logger import setup_logger

# 4. Initialise un logger spécifique pour le module "Cerveau"
logger = setup_logger("Cerveau")

class LLMEngine:
    """Le moteur d'intelligence artificielle (le cerveau) de Jarvis."""
    
    def __init__(self):
        # 5. Vérifie si on a bien une clé API configurée
        if not Config.OPENAI_API_KEY or Config.OPENAI_API_KEY == "votre_cle_api_ici":
            logger.error("Aucune clé API OpenAI valide trouvée. Veuillez vérifier votre fichier .env.")
            
        # 6. Initialise le client OpenAI avec notre clé API
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        
        # 7. Stocke le nom du modèle à utiliser
        self.model = Config.MODEL_NAME
        
        # 8. Définit la personnalité de Jarvis (le "System Prompt"). C'est ce qui dicte son comportement.
        self.system_prompt = (
            "Tu es J.A.R.V.I.S., un assistant virtuel très intelligent, poli et un peu sarcastique, "
            "créé par Tony Stark pour assister l'utilisateur actuel. Tes réponses doivent être concises."
        )
        
    def generate_response(self, user_text: str) -> str:
        """Envoie le texte de l'utilisateur à l'IA et retourne la réponse générée."""
        
        # 9. Affiche dans le terminal ce que le cerveau est en train de faire
        logger.info(f"Je réfléchis à la requête : '{user_text}'")
        
        try:
            # 10. Envoie la requête au serveur de l'IA (OpenAI)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    # 11. Le premier message donne les instructions globales au système (sa personnalité)
                    {"role": "system", "content": self.system_prompt},
                    # 12. Le deuxième message est ce que l'utilisateur vient de dire
                    {"role": "user", "content": user_text}
                ],
                # 13. La "temperature" contrôle la créativité (0 = strict/robotique, 1 = très créatif/imprévisible)
                temperature=0.7 
            )
            
            # 14. Extrait le texte de la réponse depuis le gros objet renvoyé par l'API
            answer = response.choices[0].message.content
            
            # 15. Signale que l'opération a réussi
            logger.info("Réponse générée avec succès.")
            
            # 16. Retourne la réponse trouvée au reste du programme
            return answer
            
        except Exception as e:
            # 17. Si une erreur survient (pas d'internet, clé API invalide...), on l'affiche proprement
            logger.error(f"Erreur lors de la génération de la réponse : {e}")
            return "Désolé Monsieur, mes circuits cognitifs rencontrent un problème technique."

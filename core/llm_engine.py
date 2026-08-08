#Just A Rather Very Intelligent System
from openai import OpenAI
import json # NOUVEAU: Pour lire les paramètres renvoyés par l'IA
from core.config import Config
from utils.logger import setup_logger
from skills.system_control import open_website # NOUVEAU: On importe notre compétence

logger = setup_logger("Cerveau")

class LLMEngine:
    """Le moteur d'intelligence artificielle (le cerveau) de Jarvis."""
    
    def __init__(self):
        if not Config.API_KEY or Config.API_KEY == "votre_cle_ici":
            logger.error("Aucune clé API valide trouvée. Veuillez vérifier votre fichier .env.")
            
        self.client = OpenAI(
            api_key=Config.API_KEY,
            base_url=Config.BASE_URL
        )
        
        self.model = Config.MODEL_NAME
        
        self.system_prompt = (
            "Tu es J.A.R.V.I.S., un assistant virtuel très intelligent, poli et un peu sarcastique. "
            "Tes réponses doivent être concises."
        )
        
        # NOUVEAU : On définit la liste de nos outils (Skills)
        # C'est un format standard JSON compris par Gemini, OpenAI, Groq, etc.
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "open_website",
                    "description": "Ouvre un site web dans le navigateur de l'utilisateur. Utilise cela quand on te demande d'ouvrir YouTube, Google, ou un site spécifique.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "L'URL complète du site à ouvrir, par exemple https://www.youtube.com"
                            }
                        },
                        "required": ["url"]
                    }
                }
            }
        ]
        
    def generate_response(self, user_text: str) -> str:
        """Envoie le texte à l'IA et gère l'exécution des compétences si nécessaire."""
        
        logger.info(f"Je réfléchis à la requête : '{user_text}'")
        
        # On prépare l'historique (ce qu'on va envoyer)
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_text}
        ]
        
        try:
            # 1. On envoie la requête à l'IA, en lui passant nos outils (`tools=self.tools`)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools, 
                temperature=0.7 
            )
            
            message_ia = response.choices[0].message
            
            # 2. On vérifie si l'IA a décidé d'utiliser un outil (tool_calls n'est pas vide)
            if message_ia.tool_calls:
                logger.info("L'IA a décidé d'utiliser une compétence (Skill) !")
                
                # On ajoute la décision de l'IA à l'historique
                messages.append(message_ia)
                
                # 3. On traite tous les outils qu'elle a demandés (parfois elle en demande plusieurs d'un coup)
                for tool_call in message_ia.tool_calls:
                    nom_fonction = tool_call.function.name
                    
                    # L'IA renvoie les paramètres sous forme de texte JSON, on le traduit pour Python
                    arguments = json.loads(tool_call.function.arguments)
                    
                    if nom_fonction == "open_website":
                        url_demandee = arguments.get("url")
                        
                        # 4. On exécute la VRAIE fonction Python de notre ordinateur !
                        resultat_action = open_website(url_demandee)
                        
                        # 5. On renvoie le résultat à l'IA pour qu'elle sache que ça a marché
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": resultat_action
                        })
                        
                # 6. On fait une DEUXIÈME requête à l'IA avec le résultat de l'outil.
                # C'est ce qui lui permet de dire "J'ai bien ouvert Youtube monsieur !"
                logger.info("Analyse du résultat de l'action...")
                seconde_reponse = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7
                )
                
                return seconde_reponse.choices[0].message.content
                
            else:
                # 7. Si elle n'a pas utilisé d'outil, elle a juste parlé normalement
                logger.info("Réponse vocale standard générée.")
                return message_ia.content
                
        except Exception as e:
            logger.error(f"Erreur lors de la génération de la réponse : {e}")
            return "Désolé Monsieur, mes circuits cognitifs rencontrent un problème technique."

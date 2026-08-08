# Just A Rather Very Intelligent System
from openai import OpenAI
# On importe json pour lire les paramètres renvoyés par l'IA quand elle appelle un outil
import json
from core.config import Config
from utils.logger import setup_logger
# On importe notre compétence "ouvrir un site web"
from skills.system_control import open_website

logger = setup_logger("Cerveau")

class LLMEngine:
    """Le moteur d'intelligence artificielle (le cerveau) de Jarvis."""
    
    def __init__(self):
        # On vérifie qu'on a au moins une clé API configurée
        if not Config.API_KEYS:
            logger.error("Aucune clé API valide trouvée. Veuillez vérifier votre fichier .env.")
        else:
            # On affiche combien de clés sont disponibles (comme dans ai.js avec AI_STUDIO)
            logger.info(f"{len(Config.API_KEYS)} clé(s) API disponible(s) pour le cerveau.")
            
        # On stocke l'URL du serveur et le nom du modèle
        self.base_url = Config.BASE_URL
        self.model = Config.MODEL_NAME
        
        # La personnalité de Jarvis
        self.system_prompt = (
            "Tu es J.A.R.V.I.S., un assistant virtuel très intelligent, poli et un peu sarcastique. "
            "Tes réponses doivent être concises."
        )
        
        # Liste des outils (Skills) que Jarvis peut utiliser
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
        
    def _create_client(self, api_key: str) -> OpenAI:
        """Crée un client OpenAI avec une clé spécifique."""
        # Cette fonction permet de créer rapidement un nouveau client
        # quand on veut essayer une autre clé API
        return OpenAI(api_key=api_key, base_url=self.base_url)
    
    def _call_with_fallback(self, messages: list, use_tools: bool = True):
        """Essaie chaque clé API l'une après l'autre jusqu'à ce qu'une fonctionne.
        Inspiré de la boucle for(keys) de ton fichier ai.js !"""
        
        # On boucle sur TOUTES les clés disponibles
        for i, api_key in enumerate(Config.API_KEYS):
            try:
                # On crée un client avec la clé courante
                client = self._create_client(api_key)
                
                # On prépare les paramètres de la requête
                params = {
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.7
                }
                
                # On n'ajoute les outils que si demandé (pas lors de la 2ème requête après un tool_call)
                if use_tools:
                    params["tools"] = self.tools
                
                # On envoie la requête au serveur de l'IA
                response = client.chat.completions.create(**params)
                
                # Si on arrive ici, c'est que la clé a fonctionné !
                logger.info(f"Réponse obtenue avec la clé n°{i + 1}.")
                return response, client
                
            except Exception as e:
                # Si la clé échoue, on affiche l'erreur et on passe à la suivante
                logger.warning(f"❌ Clé n°{i + 1} échouée : {e}")
                continue
        
        # Si TOUTES les clés ont échoué, on lève une erreur
        raise Exception("Toutes les clés API ont échoué.")
        
    def generate_response(self, user_text: str) -> str:
        """Envoie le texte à l'IA et gère l'exécution des compétences si nécessaire."""
        
        logger.info(f"Je réfléchis à la requête : '{user_text}'")
        
        # On prépare l'historique de la conversation
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_text}
        ]
        
        try:
            # 1. On envoie la requête en essayant chaque clé (comme dans ai.js)
            response, client = self._call_with_fallback(messages, use_tools=True)
            
            message_ia = response.choices[0].message
            
            # 2. On vérifie si l'IA a décidé d'utiliser un outil
            if message_ia.tool_calls:
                logger.info("L'IA a décidé d'utiliser une compétence (Skill) !")
                
                # On ajoute la décision de l'IA à l'historique
                messages.append(message_ia)
                
                # 3. On exécute chaque outil demandé
                for tool_call in message_ia.tool_calls:
                    nom_fonction = tool_call.function.name
                    
                    # L'IA renvoie les paramètres sous forme de texte JSON
                    arguments = json.loads(tool_call.function.arguments)
                    
                    if nom_fonction == "open_website":
                        url_demandee = arguments.get("url")
                        # On exécute la VRAIE fonction Python !
                        resultat_action = open_website(url_demandee)
                        
                        # On renvoie le résultat à l'IA
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": resultat_action
                        })
                        
                # 4. Deuxième requête pour que l'IA formule sa réponse finale
                logger.info("Analyse du résultat de l'action...")
                seconde_reponse, _ = self._call_with_fallback(messages, use_tools=False)
                
                return seconde_reponse.choices[0].message.content
                
            else:
                # 5. Pas d'outil utilisé, réponse texte classique
                logger.info("Réponse vocale standard générée.")
                return message_ia.content
                
        except Exception as e:
            logger.error(f"Erreur lors de la génération de la réponse : {e}")
            return "Désolé Monsieur, mes circuits cognitifs rencontrent un problème technique."

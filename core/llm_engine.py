# Just A Rather Very Intelligent System
from openai import OpenAI
import json
from core.config import Config
from utils.logger import setup_logger
# On importe TOUTES nos compétences
from skills.system_control import (
    get_datetime,
    open_application,
    set_volume,
    get_system_info,
    save_note,
    read_notes
)
from skills.web_search import(
    open_website,
    search_web,
    youtube_video
)

logger = setup_logger("Cerveau")

class LLMEngine:
    """Le moteur d'intelligence artificielle (le cerveau) de Jarvis."""
    
    def __init__(self):
        # On vérifie qu'on a au moins une clé API
        if not Config.API_KEYS:
            logger.error("Aucune clé API valide trouvée. Veuillez vérifier votre fichier .env.")
        else:
            logger.info(f"{len(Config.API_KEYS)} clé(s) API disponible(s) pour le cerveau.")
            
        self.base_url = Config.BASE_URL
        self.model = Config.MODEL_NAME
        
        # La personnalité de Jarvis
        self.system_prompt = (
            "Ton nom  est JARVIS., un assistant virtuel très intelligent, poli et un peu sarcastique. "
            "Tu réponds en français. Tes réponses doivent être concises.Capable aussi de faire des suggestion"
        )
        
        # Dictionnaire qui associe le NOM de chaque outil à sa VRAIE fonction Python
        # Quand l'IA demande d'exécuter "open_website", on cherche ici la fonction correspondante
        self.available_functions = {
            "open_website": open_website,
            "get_datetime": get_datetime,
            "open_application": open_application,
            "set_volume": set_volume,
            "get_system_info": get_system_info,
            "save_note": save_note,
            "read_notes": read_notes,
            "search_web": search_web,
            "youtube_video": youtube_video
        }
        
        # Liste des outils (Skills) au format JSON pour l'IA
        # Chaque outil a un nom, une description et ses paramètres
        self.tools = [
            # ── Skill 1 : Ouvrir un site web ──
            {
                "type": "function",
                "function": {
                    "name": "open_website",
                    "description": "Ouvre un site web dans le navigateur. Utilise quand on demande d'ouvrir YouTube, Google, etc.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "L'URL complète, ex: https://www.youtube.com"
                            }
                        },
                        "required": ["url"]
                    }
                }
            },
            # ── Skill 2 : Date et heure ──
            {
                "type": "function",
                "function": {
                    "name": "get_datetime",
                    "description": "Retourne la date et l'heure actuelles. Utilise quand on demande 'quelle heure est-il' ou 'quel jour sommes-nous'.",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            # ── Skill 3 : Ouvrir une application ──
            {
                "type": "function",
                "function": {
                    "name": "open_application",
                    "description": "Ouvre une application sur l'ordinateur (terminal, firefox, vlc, vscode, fichiers, calculatrice, etc.).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "app_name": {
                                "type": "string",
                                "description": "Le nom de l'application à ouvrir, ex: 'firefox', 'terminal', 'vscode', 'fichiers'"
                            }
                        },
                        "required": ["app_name"]
                    }
                }
            },
            # ── Skill 4 : Régler le volume ──
            {
                "type": "function",
                "function": {
                    "name": "set_volume",
                    "description": "Règle le volume du système entre 0 et 100. Utilise quand on demande de monter, baisser ou couper le son.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "level": {
                                "type": "integer",
                                "description": "Le niveau de volume entre 0 (muet) et 100 (maximum)"
                            }
                        },
                        "required": ["level"]
                    }
                }
            },
            # ── Skill 5 : Infos système ──
            {
                "type": "function",
                "function": {
                    "name": "get_system_info",
                    "description": "Donne l'état du système : RAM, CPU, batterie. Utilise quand on demande 'comment va mon PC' ou 'combien de RAM'.",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            # ── Skill 6 : Sauvegarder une note ──
            {
                "type": "function",
                "function": {
                    "name": "save_note",
                    "description": "Sauvegarde une note/rappel. Utilise quand on dit 'note que...', 'rappelle-moi de...', 'enregistre...'.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "Le contenu de la note à sauvegarder"
                            }
                        },
                        "required": ["content"]
                    }
                }
            },
            # ── Skill 7 : Lire les notes ──
            {
                "type": "function",
                "function": {
                    "name": "read_notes",
                    "description": "Lit toutes les notes sauvegardées. Utilise quand on demande 'lis mes notes' ou 'qu'est-ce que j'ai noté'.",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            # ── Skill 8 : Recherche web ──
            {
                "type": "function",
                "function": {
                    "name": "search_web",
                    "description": "Recherche quelque chose sur Google. Utilise quand on dit 'cherche...', 'recherche...'.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "La requête de recherche"
                            }
                        },
                        "required": ["query"]
                    }
                }
            }
            # ── Skill 9 : Ouvre une video youtube specifique ──
            {
                "type": "function",
                "function": {
                    "name": "youtube_video",
                    "description": "Ouvre une video youtube specifique precifque celle la plus apprecie lorsque tu fais des recherche sur le web",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "La requête de recherche"
                            }
                        },
                        "required": ["query"]
                    }
                }
            }
        ]
        
    def _create_client(self, api_key: str) -> OpenAI:
        """Crée un client OpenAI avec une clé spécifique."""
        return OpenAI(api_key=api_key, base_url=self.base_url)
    
    def _call_with_fallback(self, messages: list, use_tools: bool = True):
        """Essaie chaque clé API l'une après l'autre jusqu'à ce qu'une fonctionne."""
        
        for i, api_key in enumerate(Config.API_KEYS):
            try:
                client = self._create_client(api_key)
                
                params = {
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.7
                }
                
                if use_tools:
                    params["tools"] = self.tools
                
                response = client.chat.completions.create(**params)
                logger.info(f"Réponse obtenue avec la clé n°{i + 1}.")
                return response, client
                
            except Exception as e:
                logger.warning(f"❌ Clé n°{i + 1} échouée : {e}")
                continue
        
        raise Exception("Toutes les clés API ont échoué.")
        
    def generate_response(self, user_text: str) -> str:
        """Envoie le texte à l'IA et gère l'exécution des compétences si nécessaire."""
        
        logger.info(f"Je réfléchis à la requête : '{user_text}'")
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_text}
        ]
        
        try:
            # 1. On envoie la requête en essayant chaque clé
            response, client = self._call_with_fallback(messages, use_tools=True)
            message_ia = response.choices[0].message
            
            # 2. On vérifie si l'IA a décidé d'utiliser un ou plusieurs outils
            if message_ia.tool_calls:
                logger.info("L'IA a décidé d'utiliser une compétence (Skill) !")
                messages.append(message_ia)
                
                # 3. On exécute CHAQUE outil demandé (parfois l'IA en demande plusieurs)
                for tool_call in message_ia.tool_calls:
                    nom_fonction = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)
                    
                    logger.info(f"Exécution du skill : {nom_fonction}({arguments})")
                    
                    # On cherche la fonction Python correspondante dans notre dictionnaire
                    if nom_fonction in self.available_functions:
                        # On appelle la vraie fonction avec ses arguments
                        fonction = self.available_functions[nom_fonction]
                        resultat = fonction(**arguments)
                    else:
                        resultat = f"Compétence '{nom_fonction}' non reconnue."
                    
                    # On renvoie le résultat à l'IA
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": resultat
                    })
                        
                # 4. Deuxième requête pour la réponse finale
                logger.info("Analyse du résultat de l'action...")
                seconde_reponse, _ = self._call_with_fallback(messages, use_tools=False)
                return seconde_reponse.choices[0].message.content
                
            else:
                logger.info("Réponse vocale standard générée.")
                return message_ia.content
                
        except Exception as e:
            logger.error(f"Erreur lors de la génération de la réponse : {e}")
            return "Désolé Monsieur, mes circuits cognitifs rencontrent un problème technique."

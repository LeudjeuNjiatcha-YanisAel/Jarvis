# Just A Rather Very Intelligent System
from openai import OpenAI
import json
from core.config import Config
from core.memory import Memory
from utils.logger import setup_logger
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
from skills.network import(
    check_internet_connection,
    get_local_ip,
    ping_host,
    toggle_wifi
)

from skills.power import(
    shutdown_system,
    restart_system,
    suspend_system,
    lock_session
)

logger = setup_logger("Cerveau")

class LLMEngine:
    """Le moteur d'intelligence artificielle (le cerveau) de Jarvis."""
    
    def __init__(self):
        # Construction de la liste des fournisseurs actifs
        self.active_providers = []
        for p in Config.PROVIDERS:
            valid_keys = [k for k in p.get("keys", []) if k]
            if valid_keys:
                self.active_providers.append({
                    "name": p["name"],
                    "keys": valid_keys,
                    "base_url": p["base_url"],
                    "model": p["model"]
                })
                
        if not self.active_providers:
            logger.error("Aucun fournisseur d'IA avec une clé valide n'a été trouvé. Vérifiez votre .env.")
        else:
            noms_fournisseurs = ", ".join([p["name"] for p in self.active_providers])
            logger.info(f"{len(self.active_providers)} fournisseur(s) d'IA disponible(s) : {noms_fournisseurs}")
            
        # On garde des variables par défaut pour compatibilité externe éventuelle
        self.base_url = Config.BASE_URL
        self.model = Config.MODEL_NAME
        
        # La personnalité de Jarvis
        self.system_prompt = (
            "Ton nom est JARVIS., un assistant virtuel très intelligent, poli et un peu sarcastique. "
            "Tu réponds en français. Tes réponses doivent être concises (sauf indication contraire). Capable aussi de faire des suggestions."
        )
        
        # Gestion du contexte et de la mémoire
        from core.context_manager import ContextManager
        self.context_manager = ContextManager(self.system_prompt)
        self.memory = self.context_manager.memory
        
        self.available_functions = {
            "open_website": open_website,
            "get_datetime": get_datetime,
            "open_application": open_application,
            "set_volume": set_volume,
            "get_system_info": get_system_info,
            "save_note": save_note,
            "read_notes": read_notes,
            "search_web": search_web,
            "youtube_video": youtube_video,
            "toggle_wifi": toggle_wifi,
            "check_internet_connection": check_internet_connection,
            "get_local_ip": get_local_ip,
            "ping_host": ping_host,
            "shutdown_system": shutdown_system,
            "restart_system": restart_system,
            "suspend_system": suspend_system,
            "lock_session": lock_session
        }
        
        self.tools = [
            #  Skill 1 : Ouvrir un site web 
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
            #  Skill 2 : Date et heure 
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
            #  Skill 3 : Ouvrir une application 
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
            #  Skill 4 : Régler le volume 
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
            #  Skill 5 : Infos système 
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
            #  Skill 6 : Sauvegarder une note 
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
            #  Skill 7 : Lire les notes 
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
            #  Skill 8 : Recherche web 
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
            },
            #  Skill 9 : Ouvre une video youtube specifique 
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
            },
            # Skill 11 :
            {
                "type": "function",
                "function": {
                    "name": "toggle_wifi",
                    "description": "Active ou désactive le Wi-Fi",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "enable": {
                                "type": "boolean",
                                "description": "True pour activer le Wi-Fi, False pour désactiver"
                            }
                        },
                        "required": ["enable"]
                    }
                }
            },
            # Skill 12 :
            {
                "type": "function",
                "function": {
                    "name": "check_internet_connection",
                    "description": "Vérifie si l'ordinateur est connecté à Internet",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            # Skill 13 :
            {
                "type": "function",
                "function": {
                    "name": "get_local_ip",
                    "description": "Donne l'adresse IP locale de l'ordinateur",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            # Skill 14 :
            {
                "type": "function",
                "function": {
                    "name": "ping_host",
                    "description": "Effectue un ping vers un hôte distant pour vérifier la connectivité réseau",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "host": {
                                "type": "string",
                                "description": "L'adresse IP ou le nom d'hôte à pinger"
                            }
                        },
                        "required": ["host"]
                    }
                }
            },
            #Skill 15 :
            {
                "type":"function",
                "function":{
                    "name":"lock_session",
                    "description":"Verrouille la session utilisateur",
                    "parameters":{
                        "type":"object",
                        "properties":{
                            "host":{
                                "type":"string",
                                "description":"Lock la session utilisateur"
                            }
                        }
                    }  
                }
            }
        ]
        
    def _create_client(self, api_key, base_url):
        """Crée un client OpenAI avec une clé spécifique et une URL."""
        return OpenAI(api_key=api_key, base_url=base_url)
    
    def _call_with_fallback(self, messages, use_tools, specific_provider=None):
        """Essaie les fournisseurs d'IA configurés jusqu'à ce qu'un fonctionne, ou utilise un spécifique."""
        providers_to_try = self.active_providers
        if specific_provider:
            providers_to_try = [p for p in self.active_providers if p["name"].lower() == specific_provider.lower()]
            if not providers_to_try:
                logger.warning(f"Fournisseur demandé '{specific_provider}' non trouvé ou sans clé valide. Utilisation des fournisseurs par défaut.")
                providers_to_try = self.active_providers
                
        for provider in providers_to_try:
            for i, api_key in enumerate(provider["keys"]):
                try:
                    logger.debug(f"Tentative avec {provider['name']} (clé {i+1})...")
                    client = self._create_client(api_key, provider["base_url"])
                    
                    params = {
                        "model": provider["model"],
                        "messages": messages,
                        "temperature": 0.7
                    }
                    
                    if use_tools:
                        params["tools"] = self.tools
                    
                    response = client.chat.completions.create(**params)
                    logger.info(f"✅ Réponse obtenue avec {provider['name']} (clé n°{i + 1}).")
                    return response, client
                    
                except Exception as e:
                    logger.warning(f"❌ {provider['name']} (Clé n°{i + 1}) échouée : {e}")
                    continue
        
        raise Exception("Tous les fournisseurs et clés API ont échoué.")
        
    def generate_response(self, user_text: str, provider: str = None) -> str:
        """Envoie le texte à l'IA et gère l'exécution des compétences si nécessaire."""
        
        info_provider = f" avec le fournisseur {provider}" if provider else ""
        logger.info(f"Je réfléchis à la requête : '{user_text}'{info_provider}")
        
        # Mise à jour du contexte dynamique (heure, humeur)
        self.context_manager.update_system_prompt()
        
        # Ajout du message utilisateur dans la mémoire
        self.memory.add_user_message(user_text)
        
        try:
            # 1. On envoie la requête en essayant chaque clé/fournisseur avec l'historique complet
            response, client = self._call_with_fallback(self.memory.get_messages(), use_tools=True, specific_provider=provider)
            message_ia = response.choices[0].message
            
            # 2. On vérifie si l'IA a décidé d'utiliser un ou plusieurs outils
            if message_ia.tool_calls:
                logger.info("L'IA a décidé d'utiliser une compétence (Skill) !")
                self.memory.add_raw_message(message_ia)
                
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
                    
                    # On renvoie le résultat à l'IA dans la mémoire
                    self.memory.add_raw_message({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(resultat)
                    })
                        
                # 4. Deuxième requête pour la réponse finale
                logger.info("Analyse du résultat de l'action...")
                seconde_reponse, _ = self._call_with_fallback(self.memory.get_messages(), use_tools=False, specific_provider=provider)
                reponse_finale = seconde_reponse.choices[0].message.content
                
                # Ajout de la réponse finale à la mémoire
                self.memory.add_assistant_message(reponse_finale)
                return reponse_finale
                
            else:
                logger.info("Réponse vocale standard générée.")
                self.memory.add_assistant_message(message_ia.content)
                return message_ia.content
                
        except Exception as e:
            logger.error(f"Erreur lors de la génération de la réponse : {e}")
            return "Désolé Monsieur, mes circuits cognitifs rencontrent un problème technique."

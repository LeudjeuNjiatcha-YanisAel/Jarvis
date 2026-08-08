import webbrowser
from utils.logger import setup_logger

logger = setup_logger("Skills")

def open_website(url: str) -> str:
    """Ouvre un site web dans le navigateur par défaut de l'ordinateur."""
    # 1. On affiche dans la console ce qu'on fait
    logger.info(f"Exécution de l'action : Ouverture de {url}")
    
    try:
        # 2. On utilise la librairie Python 'webbrowser' pour ouvrir le navigateur
        webbrowser.open(url)
        
        # 3. On retourne un message texte qui sera lu par l'IA (le cerveau) pour lui dire que c'est fait
        return f"Action réussie : j'ai ouvert le site {url} sur l'écran."
    except Exception as e:
        # Si le navigateur plante, on avertit l'IA
        return f"L'action a échoué avec l'erreur : {e}"

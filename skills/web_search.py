import webbrowser
from utils.logger import setup_logger

logger = setup_logger("Skills-Web-Search")


def open_website(url: str) -> str:
    """Ouvre un site web dans le navigateur par défaut de l'ordinateur."""
    logger.info(f"Exécution : Ouverture de {url}")
    try:
        webbrowser.open(url)
        return f"Action réussie : j'ai ouvert le site {url} sur l'écran."
    except Exception as e:
        return f"L'action a échoué : {e}"
    
def search_web(query: str) -> str:
    """Effectue une recherche Google avec la requête donnée."""
    logger.info(f"Exécution : Recherche web pour '{query}'")
    
    # On encode la requête pour l'URL (les espaces deviennent des +)
    import urllib.parse
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    
    try:
        webbrowser.open(url)
        return f"J'ai lancé une recherche Google pour : '{query}'."
    except Exception as e:
        return f"Erreur lors de la recherche : {e}"

# Suggestions de fonctions a ajoutees
def youtube_video(video_name: str) -> str:
    """Ouvre une vidéo YouTube avec le nom donné."""
    logger.info(f"Exécution : Ouverture de la vidéo '{video_name}'")
    import urllib.parse
    encoded_video_name = urllib.parse.quote_plus(video_name)
    url = f"https://www.youtube.com/watch?v={encoded_video_name}"
    try:
        webbrowser.open(url)
        return f"Action réussie : j'ai ouvert la vidéo '{video_name}' sur l'écran."
    except Exception as e:
        return f"L'action a échoué : {e}"
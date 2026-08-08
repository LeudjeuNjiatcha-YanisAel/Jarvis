import logging # 1. Importe la bibliothèque standard de Python pour gérer un historique d'événements (logs).
import sys     # 2. Importe le module système, qui nous permettra d'afficher du texte dans le terminal.

def setup_logger(name: str = "Jarvis") -> logging.Logger:
    """Configure et retourne un logger.""" # 3. Une "docstring" expliquant ce que fait la fonction.
    
    # 4. Crée ou récupère un objet Logger avec le nom spécifié (par défaut, il s'appellera "Jarvis").
    logger = logging.getLogger(name) 
    
    # 5. Définit le niveau d'importance minimal des messages à afficher.
    # INFO signifie "montre-moi les infos normales, les avertissements et les erreurs, mais ignore les détails de debug".
    logger.setLevel(logging.INFO) 
    
    # 6. Vérifie si le logger a déjà des "handlers" (des gestionnaires d'affichage) pour éviter d'afficher le même message en double.
    if not logger.handlers:
        # 7. Crée un gestionnaire (handler) qui envoie les messages vers sys.stdout (qui est ton écran/terminal).
        console_handler = logging.StreamHandler(sys.stdout)
        
        # 8. Définit un format précis pour chaque message : 
        # [Date et Heure] - Nom du module - NIVEAU - Le message lui-même.
        formatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
        
        # 9. Applique le format qu'on vient de définir à notre gestionnaire d'écran.
        console_handler.setFormatter(formatter)
        
        # 10. Attache ce gestionnaire d'écran à notre logger "Jarvis".
        logger.addHandler(console_handler)
        
    # 11. Retourne notre outil de log prêt à l'emploi.
    return logger

# 1. On importe la fonction qu'on vient de créer dans notre dossier "utils".
from utils.logger import setup_logger 

# 2. On crée un "logger" spécifique pour ce fichier principal, qu'on appellera "Main".
logger = setup_logger("Main")

def main(): # 3. On définit la fonction principale de notre programme.
    
    # 4. On utilise notre logger pour afficher une information (INFO). 
    # Grâce à notre configuration, il affichera automatiquement l'heure et le nom "Main".
    logger.info("Initialisation du système J.A.R.V.I.S...")
    
    # (Plus tard, c'est ici qu'on allumera le microphone, la synthèse vocale et l'IA)
    
    # 5. On affiche un second message.
    logger.info("Système en ligne et prêt à recevoir des commandes.")

# 6. Cette ligne est très importante en Python. Elle vérifie si ce fichier (main.py) est 
# exécuté directement par l'utilisateur. Si oui, elle lance la suite.
if __name__ == "__main__":
    
    # 7. On appelle notre fonction main() définie plus haut pour démarrer le programme.
    main()

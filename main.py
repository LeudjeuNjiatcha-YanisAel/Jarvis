# 1. On importe la fonction qu'on vient de créer dans notre dossier "utils".
from utils.logger import setup_logger 

# 2. On importe notre nouveau cerveau (LLMEngine)
from core.llm_engine import LLMEngine

# 3. On crée un "logger" spécifique pour ce fichier principal
logger = setup_logger("Main")

def main(): # 4. On définit la fonction principale de notre programme.
    
    # 5. Message de démarrage
    logger.info("Initialisation du système J.A.R.V.I.S...")
    
    # 6. On "allume" le cerveau en créant une instance de LLMEngine
    # Note : Cela va vérifier si la clé API dans .env est correcte
    cerveau = LLMEngine()
    
    # 7. On affiche un message confirmant que tout est prêt
    logger.info("Système en ligne et prêt à recevoir des commandes.")
    
    # 8. On simule un message de l'utilisateur pour tester le cerveau
    message_test = "Bonjour Jarvis, qui es-tu et comment vas-tu ?"
    logger.info(f"Utilisateur dit : {message_test}")
    
    # 9. On demande au cerveau de générer une réponse
    reponse = cerveau.generate_response(message_test)
    
    # 10. On affiche la réponse de Jarvis
    print(f"\n[J.A.R.V.I.S.] : {reponse}\n")

# 11. Cette ligne vérifie si on exécute ce fichier directement.
if __name__ == "__main__":
    
    # 12. On appelle notre fonction main()
    main()

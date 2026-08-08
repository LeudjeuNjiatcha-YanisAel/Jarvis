# 1. On importe la fonction qu'on vient de créer dans notre dossier "utils".
from utils.logger import setup_logger 

# 2. On importe notre nouveau cerveau (LLMEngine) et nos oreilles (SpeechToText)
from core.llm_engine import LLMEngine
from interfaces.input.speech_to_text import SpeechToText

# 3. On crée un "logger" spécifique pour ce fichier principal
logger = setup_logger("Main")

def main(): # 4. On définit la fonction principale de notre programme.
    
    # 5. Message de démarrage
    logger.info("Initialisation du système J.A.R.V.I.S...")
    
    # 6. On "allume" le cerveau et les oreilles
    cerveau = LLMEngine()
    oreilles = SpeechToText()
    
    # 7. On affiche un message confirmant que tout est prêt
    logger.info("Système en ligne et prêt à recevoir des commandes.")
    
    # 8. On écoute ce que dit l'utilisateur (ça va bloquer jusqu'à ce qu'on parle)
    texte_entendu = oreilles.listen_and_transcribe()
    
    # 9. Si Jarvis a bien entendu et compris quelque chose :
    if texte_entendu:
        logger.info("Transmission du texte au cerveau pour analyse...")
        reponse = cerveau.generate_response(texte_entendu)
        print(f"\n[J.A.R.V.I.S.] : {reponse}\n")
    else:
        logger.info("Aucune commande valide reçue. Fin du programme.")

# 10. Cette ligne vérifie si on exécute ce fichier directement.
if __name__ == "__main__":
    main()

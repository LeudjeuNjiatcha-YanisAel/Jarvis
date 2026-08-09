from utils.logger import setup_logger 
from core.llm_engine import LLMEngine
from interfaces.input.speech_to_text import SpeechToText
from interfaces.output.text_to_speech import TextToSpeech

# 3. On crée un "logger" spécifique pour ce fichier principal
logger = setup_logger("Main")

def main(): 
    
    # 4. Message de démarrage
    logger.info("Initialisation du système J.A.R.V.I.S...")
    
    # 5. On "allume" tous les organes
    cerveau = LLMEngine()
    oreilles = SpeechToText()
    voix = TextToSpeech() # Nouveau !
    
    # 6. Message de bienvenue vocal
    voix.speak("Système en ligne. Bonjour monsieur.")
    logger.info("Système en ligne et prêt à recevoir des commandes.")
    
    # 7. On écoute (ça va bloquer jusqu'à ce qu'on parle)
    texte_entendu = oreilles.listen_and_transcribe()
    
    # 8. Si Jarvis a bien entendu :
    if texte_entendu:
        logger.info("Transmission du texte au cerveau...")
        
        # Le cerveau génère la réponse
        reponse = cerveau.generate_response(texte_entendu)
        print(f"\n[J.A.R.V.I.S.] : {reponse}\n")
        
        # 9. Jarvis parle !
        voix.speak(reponse)
        
    else:
        logger.info("Aucune commande valide reçue. Fin du programme.")

# 10. Lancement
if __name__ == "__main__":
    main()

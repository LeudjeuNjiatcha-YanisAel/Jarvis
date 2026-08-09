from utils.logger import setup_logger 
from core.llm_engine import LLMEngine
from interfaces.input.speech_to_text import SpeechToText
from interfaces.output.text_to_speech import TextToSpeech


logger = setup_logger("Main")

def main(): 
    
    # Message de démarrage
    logger.info("Initialisation du système J.A.R.V.I.S...")
    
    # On "allume" tous les organes
    cerveau = LLMEngine()
    oreilles = SpeechToText()
    voix = TextToSpeech()
    
    # Message de bienvenue vocal
    voix.speak("Système en ligne. Bonjour monsieur.")
    logger.info("Système en ligne et prêt à recevoir des commandes en continu.")
    
    # Boucle d'écoute infinie
    while True:
        try:
            # On écoute (ça va bloquer jusqu'à ce qu'on parle)
            texte_entendu = oreilles.listen_and_transcribe()
            
            # Si Jarvis a bien entendu :
            if texte_entendu:
                texte_lower = texte_entendu.lower()
                
                # Mots clés pour arrêter le programme
                mots_arret = ["arrête-toi", "désactive-toi", "au revoir", "éteins-toi", "stop", "quitter"]
                if any(mot in texte_lower for mot in mots_arret):
                    logger.info("Commande d'arrêt reçue.")
                    voix.speak("Au revoir monsieur, extinction des systèmes.")
                    break
                
                logger.info("Transmission du texte au cerveau...")
                
                # Le cerveau génère la réponse
                reponse = cerveau.generate_response(texte_entendu)
                print(f"\n[J.A.R.V.I.S.] : {reponse}\n")
                
                # Jarvis parle !
                voix.speak(reponse)
                
            else:
                logger.debug("Aucun son compris, on continue l'écoute...")
                
        except KeyboardInterrupt:
            logger.info("Interruption clavier (Ctrl+C) détectée.")
            voix.speak("Interruption manuelle. Au revoir monsieur.")
            break
        except Exception as e:
            logger.error(f"Erreur inattendue dans la boucle principale : {e}")

# Lancement
if __name__ == "__main__":
    main()

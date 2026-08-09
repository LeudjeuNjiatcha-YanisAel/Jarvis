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
            # On écoute (ça va bloquer jusqu'à ce qu'on parle, ou jusqu'au timeout)
            texte_entendu = oreilles.listen_and_transcribe()
            
            # Si Jarvis a entendu quelque chose :
            if texte_entendu:
                texte_lower = texte_entendu.lower()
                
                # 1. GESTION DE LA VEILLE
                if cerveau.context_manager.is_sleeping:
                    # On vérifie si l'utilisateur l'appelle (mot de réveil)
                    mots_reveil = ["jarvis", "réveille-toi", "debout"]
                    if any(mot in texte_lower for mot in mots_reveil):
                        cerveau.context_manager.reset_inactivity()
                        logger.info("Sortie de veille détectée.")
                        voix.speak("Je suis de nouveau à votre écoute, monsieur.")
                    else:
                        # On ignore le reste s'il est en veille et qu'on ne l'a pas appelé
                        logger.debug(f"Input ignoré car en veille : {texte_entendu}")
                    continue
                
                # Si Jarvis n'est pas en veille et entend quelque chose, on réinitialise l'inactivité
                cerveau.context_manager.reset_inactivity()
                
                # 2. COMMANDES D'ARRÊT
                mots_arret = ["arrête-toi", "désactive-toi", "au revoir", "éteins-toi", "stop", "quitter"]
                if any(mot in texte_lower for mot in mots_arret):
                    logger.info("Commande d'arrêt reçue.")
                    voix.speak("Au revoir monsieur, extinction des systèmes.")
                    break
                
                # 3. COMMANDE DE MISE EN VEILLE MANUELLE
                mots_veille = ["mets-toi en veille", "dors", "repose-toi"]
                if any(mot in texte_lower for mot in mots_veille):
                    cerveau.context_manager.set_sleep_mode(True)
                    logger.info("Mise en veille manuelle.")
                    voix.speak("Je me mets en veille. Appelez-moi 'Jarvis' pour me réveiller.")
                    continue
                
                # 4. TRAITEMENT NORMAL
                logger.info("Transmission du texte au cerveau...")
                reponse = cerveau.generate_response(texte_entendu)
                print(f"\n[J.A.R.V.I.S.] : {reponse}\n")
                voix.speak(reponse)
                
            else:
                # S'il n'entend rien (le SpeechRecognition renvoie "" au bout de 5 sec de silence)
                if not cerveau.context_manager.is_sleeping:
                    cerveau.context_manager.increment_inactivity()
                    
                    # S'il s'ennuie et qu'il est d'humeur causante
                    if cerveau.context_manager.should_be_chatty():
                        logger.info("Jarvis s'ennuie et devient proactif (humeur causante).")
                        reponse = cerveau.generate_response("Contexte interne : Je n'ai rien dit depuis un moment. Fais une remarque amusante, pose-moi une question ou propose tes services de manière proactive. Sois assez bref.")
                        print(f"\n[J.A.R.V.I.S.] : {reponse}\n")
                        voix.speak(reponse)
                        
                    # S'il n'y a toujours rien après un long moment, il s'endort
                    elif cerveau.context_manager.should_sleep():
                        cerveau.context_manager.set_sleep_mode(True)
                        logger.info("Mise en veille automatique suite à l'inactivité.")
                        voix.speak("Je ne détecte aucune instruction. Je passe en mode veille autonome. Appelez-moi si vous avez besoin de moi.")
                
        except KeyboardInterrupt:
            logger.info("Interruption clavier (Ctrl+C) détectée.")
            voix.speak("Interruption manuelle. Au revoir monsieur.")
            break
        except Exception as e:
            logger.error(f"Erreur inattendue dans la boucle principale : {e}")

# Lancement
if __name__ == "__main__":
    main()

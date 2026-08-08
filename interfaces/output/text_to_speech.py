from gtts import gTTS
import pygame
import os
import time
from utils.logger import setup_logger

logger = setup_logger("Voix")

class TextToSpeech:
    def __init__(self, lang: str = 'fr'):
        # 1. On définit la langue de Jarvis (Français par défaut)
        self.lang = lang
        
        # 2. On initialise le mixer audio de pygame (qui permet de jouer des sons)
        # On met le volume de pygame à "silencieux" dans la console pour cacher son message de bienvenue
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
        pygame.mixer.init()
        
    def speak(self, text: str):
        """Transforme le texte en voix et le joue dans les haut-parleurs."""
        if not text:
            return
            
        logger.info("Génération de la synthèse vocale...")
        temp_file = "temp_voice.mp3"
        
        try:
            # 3. On utilise Google Text-to-Speech (gTTS) pour générer l'audio
            tts = gTTS(text=text, lang=self.lang)
            
            # 4. On sauvegarde l'audio dans un fichier temporaire
            tts.save(temp_file)
            
            # 5. On charge la musique (la voix) dans notre lecteur audio
            pygame.mixer.music.load(temp_file)
            
            # 6. On lance la lecture
            logger.info("Jarvis parle...")
            pygame.mixer.music.play()
            
            # 7. On met le programme en pause tant que Jarvis n'a pas fini de parler
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
        except Exception as e:
            logger.error(f"Erreur lors de la synthèse vocale : {e}")
            
        finally:
            # 8. On décharge la musique de la mémoire
            pygame.mixer.music.unload()
            
            # 9. On supprime le fichier audio temporaire pour garder le dossier propre
            if os.path.exists(temp_file):
                os.remove(temp_file)

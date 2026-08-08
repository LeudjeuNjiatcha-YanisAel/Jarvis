from gtts import gTTS
import pygame
import os
import time
from utils.logger import setup_logger
from core.config import Config # 1. On importe la configuration pour lire la clé ElevenLabs

logger = setup_logger("Voix")

class TextToSpeech:
    def __init__(self, lang: str = 'fr'):
        self.lang = lang
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
        pygame.mixer.init()
        
        # 2. On vérifie si une clé ElevenLabs est configurée
        self.use_elevenlabs = bool(Config.ELEVENLABS_API_KEY and Config.ELEVENLABS_API_KEY != "votre_cle_elevenlabs_ici")
        
        if self.use_elevenlabs:
            from elevenlabs.client import ElevenLabs
            # 3. Initialise le client ElevenLabs
            self.eleven_client = ElevenLabs(api_key=Config.ELEVENLABS_API_KEY)
            
            # 4. ID d'une voix masculine profonde. (Tu pourras chercher d'autres voix sur le site d'ElevenLabs)
            self.voice_id = "pNInz6obbfIdGrmRpep" 
            logger.info("Système vocal : ElevenLabs activé (Qualité Premium).")
        else:
            logger.info("Système vocal : Google TTS activé (Standard).")
        
    def speak(self, text: str):
        """Transforme le texte en voix et le joue dans les haut-parleurs."""
        if not text:
            return
            
        logger.info("Génération de la synthèse vocale...")
        temp_file = "temp_voice.mp3"
        
        try:
            if self.use_elevenlabs:
                from elevenlabs import save
                # 5. Utilise l'IA d'ElevenLabs pour générer la voix
                audio_generator = self.eleven_client.generate(
                    text=text,
                    voice=self.voice_id,
                    model="eleven_multilingual_v2" # Supporte le français avec l'accent natif
                )
                save(audio_generator, temp_file)
            else:
                # 6. Fallback sur Google TTS si pas de clé ElevenLabs
                tts = gTTS(text=text, lang=self.lang)
                tts.save(temp_file)
            
            # 7. Lecture du fichier audio généré
            pygame.mixer.music.load(temp_file)
            logger.info("Jarvis parle...")
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
        except Exception as e:
            logger.error(f"Erreur lors de la synthèse vocale : {e}")
            
        finally:
            pygame.mixer.music.unload()
            if os.path.exists(temp_file):
                os.remove(temp_file)

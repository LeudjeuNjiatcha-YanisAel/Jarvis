from gtts import gTTS
import pygame
import os
import time
from utils.logger import setup_logger
# On importe la configuration pour lire la clé ElevenLabs
from core.config import Config

logger = setup_logger("Voix")

class TextToSpeech:
    def __init__(self, lang: str = 'fr'):
        # Langue de Jarvis (Français par défaut)
        self.lang = lang
        
        # On cache le message "Hello from pygame community" dans le terminal
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
        
        # On initialise le lecteur audio
        pygame.mixer.init()
        
        # On vérifie si une clé ElevenLabs est configurée
        self.use_elevenlabs = bool(
            Config.ELEVENLABS_API_KEY 
            and Config.ELEVENLABS_API_KEY != "votre_cle_elevenlabs_ici"
        )
        
        if self.use_elevenlabs:
            # On importe le client ElevenLabs seulement si on en a besoin
            from elevenlabs.client import ElevenLabs
            
            # On crée le client avec notre clé API
            self.eleven_client = ElevenLabs(api_key=Config.ELEVENLABS_API_KEY)
            
            # ID d'une voix masculine profonde (Adam)
            # Tu peux trouver d'autres voix sur https://elevenlabs.io/app/voice-library
            self.voice_id = "pNInz6obBkDQRn5Bq7LI"
            
            logger.info("Système vocal : ElevenLabs activé (Qualité Premium).")
        else:
            logger.info("Système vocal : Google TTS activé (Standard).")
        
    def speak(self, text: str):
        """Transforme le texte en voix et le joue dans les haut-parleurs."""
        # Si le texte est vide, on ne fait rien
        if not text:
            return
            
        logger.info("Génération de la synthèse vocale...")
        temp_file = "temp_voice.mp3"
        
        try:
            if self.use_elevenlabs:
                # --- Mode ElevenLabs (voix ultra-réaliste) ---
                
                # On appelle l'API de synthèse vocale d'ElevenLabs v2
                # La méthode "convert" renvoie un générateur d'octets audio (bytes)
                audio_iterator = self.eleven_client.text_to_speech.convert(
                    text=text,
                    voice_id=self.voice_id,
                    # Ce modèle supporte le français avec un accent natif
                    model_id="eleven_multilingual_v2",
                    output_format="mp3_44100_128"
                )
                
                # On écrit tous les morceaux d'audio dans un fichier mp3
                with open(temp_file, "wb") as f:
                    for chunk in audio_iterator:
                        f.write(chunk)
                        
            else:
                # --- Mode Google TTS (gratuit, standard) ---
                tts = gTTS(text=text, lang=self.lang)
                tts.save(temp_file)
            
            # On charge le fichier audio dans le lecteur pygame
            pygame.mixer.music.load(temp_file)
            logger.info("Jarvis parle...")
            
            # On lance la lecture du son
            pygame.mixer.music.play()
            
            # On attend que Jarvis ait fini de parler avant de continuer le programme
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
        except Exception as e:
            logger.error(f"Erreur lors de la synthèse vocale : {e}")
            
        finally:
            # On décharge la musique de la mémoire
            pygame.mixer.music.unload()
            
            # On supprime le fichier audio temporaire
            if os.path.exists(temp_file):
                os.remove(temp_file)

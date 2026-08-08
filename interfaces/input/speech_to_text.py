import speech_recognition as sr
from openai import OpenAI
from core.config import Config
from utils.logger import setup_logger
import os

logger = setup_logger("Oreilles")

class SpeechToText:
    def __init__(self):
        # 1. On prépare l'outil de reconnaissance vocale
        self.recognizer = sr.Recognizer()
        
        # 2. On connecte le client à l'API (pour utiliser Whisper)
        # On force l'URL de Groq car "whisper-large-v3-turbo" n'existe que chez eux !
        # On utilise GROQ_API_KEY, et si elle n'existe pas, on tente l'API_KEY normale.
        cle_groq = Config.GROQ_API_KEY if Config.GROQ_API_KEY else Config.API_KEY
        self.client = OpenAI(
            api_key=cle_groq, 
            base_url="https://api.groq.com/openai/v1" 
        )
        
    def listen_and_transcribe(self) -> str:
        """Écoute le micro et transforme la voix en texte."""
        try:
            # 3. Ouvre le microphone de l'ordinateur
            with sr.Microphone() as source:
                logger.info("Ajustement au bruit de fond...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                logger.info("J'écoute... (Parlez maintenant)")
                # Timeout = s'arrête s'il n'y a pas de son pendant 5s
                audio_data = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                logger.info("Traitement de l'audio en cours...")
                
                temp_file = "temp_audio.wav"
                try:
                    # 4. Sauvegarde l'audio dans un fichier temporaire
                    with open(temp_file, "wb") as f:
                        f.write(audio_data.get_wav_data())
                    
                    # 5. Envoie à l'IA pour transcrire
                    # Attention : Le modèle "whisper-large-v3-turbo" marche avec GROQ
                    # Si tu utilises Gemini ou Cerebras ici, il faudra adapter le nom du modèle audio
                    with open(temp_file, "rb") as audio_file:
                        transcription = self.client.audio.transcriptions.create(
                            file=audio_file,
                            model="whisper-large-v3-turbo",
                        )
                    
                    result = transcription.text
                    logger.info(f"Vous avez dit : {result}")
                    return result
                    
                except Exception as e:
                    logger.error(f"Erreur de transcription : {e}")
                    return ""
                finally:
                    # 6. Supprime le fichier audio temporaire
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                        
        except OSError:
            logger.error("Aucun microphone n'a été détecté sur votre système ou l'accès a été refusé.")
            return ""
        except sr.WaitTimeoutError:
            logger.warning("Vous n'avez rien dit.")
            return ""

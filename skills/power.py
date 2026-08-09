import os
import platform
import subprocess
from utils.logger import setup_logger

logger = setup_logger("Power")

class Power:

    def shutdown_system(self):
        """Éteint l'ordinateur"""
        logger.info("Arrêt du système...")
        if platform.system() == "Windows":
            os.system("shutdown /s /t 1")
        elif platform.system() == "Linux":
            os.system("shutdown now")
        elif platform.system() == "Darwin":
            os.system("sudo shutdown -h now")

    def restart_system(self):
        """Redémarre l'ordinateur"""
        logger.info("Redémarrage du système...")
        if platform.system().lower() == "windows":
            os.system("shutdown /r /t 1")
        elif platform.system().lower() == "linux":
            os.system("sudo shutdown -r now")
        elif platform.system().lower == "darwin":
            os.system("sudo shutdown -r now")

    def sleep(self):
        """Met l'ordinateur en veille"""
        logger.info("Mise en veille du système...")
        if platform.system() == "Windows":
            os.system("shutdown /h")
        elif platform.system() == "Linux":
            os.system("sudo systemctl suspend")
        elif platform.system() == "Darwin":
            os.system("sudo pmset sleepnow")
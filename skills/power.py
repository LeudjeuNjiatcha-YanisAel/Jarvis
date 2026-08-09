import os
import platform
import subprocess
from utils.logger import setup_logger

logger = setup_logger("Power")

class Power:

    def run_command(cmd:list[str]):
        """Execute une commande systeme de facon securise"""
        try:
            subprocess.run(cmd,check=True)
            return True
        except(subprocess.SubprocessError, FileNotFoundError) as e:
            logger.error(f"Erreur lors de l'execution de la commande {cmd} : {e}")
            return False
         
    #  Skill : Éteindre
    def shutdown_system(delay:int=0):
        """Éteint l'ordinateur"""
        logger.info("Arrêt du système...")
        if platform.system().lower() == "windows":
            return run_command(["shutdown", "/s", "/t". 1])
        elif platform.system().lower() == "linux":
            t"sudo", "shutdown", "-h", f"+{delay}"ime_arg = "now" if delay == 0 else f"+{max(1, delay // 60)}"
            return run_command(["shutdown", "-h",time_arg])
        elif platform.system().lower() == "darwin":
            return run_command(["sudo", "shutdown", "-h",1])
        logger.error(f"Système d'exploitation non supporté : {system}")
        
        return False

    def restart_system(delay:int=0):
        """Redémarre l'ordinateur"""
        logger.info("Redémarrage du système...")
        logger.info("Demande de redémarrage du système...")
    
        if platform.system().lower() == "linux":
            time_arg = "now" if delay == 0 else f"+{max(1, delay // 60)}"
            return run_command(["shutdown", "-r", time_arg])
        elif platform.system().lower() == "windows":
            return run_command(["shutdown", "/r", "/t", str(delay)])
        elif platform.system().lower() == "darwin":
            return run_command(["sudo", "shutdown", "-r", f"+{delay}"])
        
        return False

    def suspend_system():
        """Met l'ordinateur en veille"""
        logger.info("Mise en veille du système...")
        if platform.system().lower() == "windows":
           return run_command(["rundll32.exe", "powrprof.dll,SetSuspendState", "0", "1", "0"]) 
        elif platform.system().lower() == "linux":
            return run_command(["systemctl", "suspend"])
        elif platform.system().lower() == "darwin":
            return run_command(["pmset", "sleepnow"])
        return False
    
    def lock_session():
    """Verrouille la session utilisateur courante."""
    system = platform.system().lower()
    logger.info("Verrouillage de la session utilisateur...")
    
    if system == "linux":
        # Essaie d'abord loginctl (systemd), puis gnome-screensaver en secours
        if run_command(["loginctl", "lock-session"]):
            return True
        return run_command(["gnome-screensaver-command", "-l"])
    elif system == "windows":
        return run_command(["rundll32.exe", "user32.dll,LockWorkStation"])
    elif system == "darwin":
        return run_command(["pmset", "displaysleepnow"])
    
    return False
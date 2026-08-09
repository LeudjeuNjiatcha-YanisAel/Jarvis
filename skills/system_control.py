import webbrowser
import subprocess
import os
import datetime
from utils.logger import setup_logger

logger = setup_logger("Skills")

def get_datetime() -> str:
    """Retourne la date et l'heure actuelles du système."""
    # On récupère la date/heure formatée en français
    now = datetime.datetime.now()
    # On formate la date : "Vendredi 08 Août 2026, 23h15"
    date_str = now.strftime("%A %d %B %Y, %Hh%M")
    logger.info(f"Date/Heure demandée : {date_str}")
    return f"Nous sommes le {date_str}."

def open_application(app_name: str) -> str:
    """Ouvre une application installée sur le système Linux."""
    logger.info(f"Exécution : Lancement de l'application '{app_name}'")
    
    # Dictionnaire qui associe des noms courants aux vraies commandes Linux
    # Tu peux ajouter tes propres applications ici !
    apps = {
        "terminal": "gnome-terminal",
        "navigateur": "firefox",
        "firefox": "firefox",
        "google-chrome": "google-chrome",
        "fichiers": "nautilus",
        "explorateur": "nautilus",
        "éditeur": "gedit",
        "gedit": "gedit",
        "calculatrice": "gnome-calculator",
        "musique": "rhythmbox",
        "vidéo": "totem",
        "vlc": "vlc",
        "vscode": "code",
        "code": "code",
    }
    
    # On cherche l'application dans notre dictionnaire (en minuscules)
    commande = apps.get(app_name.lower(), app_name.lower())
    
    try:
        # subprocess.Popen lance la commande sans bloquer le programme
        # stdout et stderr DEVNULL empêchent l'application de polluer notre terminal
        subprocess.Popen(
            [commande], 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        return f"Action réussie : l'application '{app_name}' a été lancée."
    except FileNotFoundError:
        return f"Erreur : l'application '{app_name}' n'est pas installée sur ce système."
    except Exception as e:
        return f"Erreur lors du lancement de '{app_name}' : {e}"

def set_volume(level: int) -> str:
    """Règle le volume du système entre 0 et 100."""
    logger.info(f"Exécution : Réglage du volume à {level}%")
    
    # On s'assure que le volume reste entre 0 et 100
    level = max(0, min(100, level))
    
    try:
        
        subprocess.run(
            ["amixer", "set", "Master", f"{level}%"],
            capture_output=True
        )
        return f"Volume réglé à {level}%."
    except Exception as e:
        return f"Erreur lors du réglage du volume : {e}"

def get_system_info() -> str:
    """Retourne les informations sur l'état actuel du système."""
    logger.info("Exécution : Récupération des informations système")
    info = []
    
    try:
        # --- RAM (Mémoire vive) ---
        # On lit /proc/meminfo qui contient les infos mémoire sous Linux
        with open("/proc/meminfo", "r") as f:
            lines = f.readlines()
        # On extrait la mémoire totale et la mémoire disponible
        mem_total = int(lines[0].split()[1]) // 1024  # Convertir KB en MB
        mem_available = int(lines[2].split()[1]) // 1024
        mem_used = mem_total - mem_available
        info.append(f"RAM : {mem_used} Mo utilisés / {mem_total} Mo total")
        
        # --- CPU (Processeur) ---
        # On lit /proc/loadavg pour la charge moyenne du processeur
        with open("/proc/loadavg", "r") as f:
            load = f.read().split()
        info.append(f"Charge CPU : {load[0]} (1 min), {load[1]} (5 min)")
        
        # --- Batterie ---
        # Le chemin standard de la batterie sous Linux
        bat_path = "/sys/class/power_supply/BAT0/capacity"
        if os.path.exists(bat_path):
            with open(bat_path, "r") as f:
                battery = f.read().strip()
            info.append(f"Batterie : {battery}%")
        else:
            info.append("Batterie : non détectée (PC de bureau ?)")
            
    except Exception as e:
        info.append(f"Erreur : {e}")
    
    return " | ".join(info)

# Le fichier où Jarvis stocke ses notes
NOTES_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "notes.txt")

def save_note(content: str) -> str:
    """Sauvegarde une note dans un fichier texte."""
    logger.info(f"Exécution : Sauvegarde d'une note")
    
    # On crée le dossier 'data' s'il n'existe pas encore
    os.makedirs(os.path.dirname(NOTES_FILE), exist_ok=True)
    
    # On ajoute la note avec la date en en-tête
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # mode "a" = append = ajouter à la fin du fichier sans écraser
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {content}\n")
    
    return f"Note sauvegardée avec succès : '{content}'"


def read_notes() -> str:
    """Lit toutes les notes sauvegardées."""
    logger.info("Exécution : Lecture des notes")
    
    if not os.path.exists(NOTES_FILE):
        return "Aucune note enregistrée pour le moment."
    
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        notes = f.read().strip()
    
    if not notes:
        return "Aucune note enregistrée pour le moment."
    
    return f"Voici vos notes :\n{notes}"

import socket
import platform
import subprocess
from utils.logger import logger

def check_internet_connection(host= "8.8.8.8", port = 53, timeout = 3) :
    """Vérifie si la connexion Internet est active via un socket TCP rapide."""
    try:
        socket.setdefaulttimeout(timeout)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
        return True
    except OSError:
        return False

def get_local_ip() -> str:
    """Récupère l'adresse IP locale principale de la machine."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # On ne se connecte pas réellement, permet de trouver l'interface de sortie principale
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception as e:
        logger.error(f"Impossible de déterminer l'adresse IP locale : {e}")
        return "127.0.0.1"

def ping_host(host: str = "google.com", count: int = 2) -> dict:
    """Effectue un ping vers un hôte et retourne un diagnostic complet."""
    system = platform.system().lower()
    param = "-n" if system == "windows" else "-c"
    cmd = ["ping", param, str(count), host]
    
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
        is_reachable = result.returncode == 0
        return {
            "success": is_reachable,
            "host": host,
            "message": "Hôte joignable" if is_reachable else "Hôte injoignable",
            "output": result.stdout if is_reachable else result.stderr
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "host": host, "message": "Délai d'attente dépassé (Timeout)", "output": ""}
    except Exception as e:
        logger.error(f"Erreur lors du ping vers {host}: {e}")
        return {"success": False, "host": host, "message": str(e), "output": ""}

def toggle_wifi(enable: bool) -> bool:
    """Active ou désactive le Wi-Fi (Optimisé pour Linux NetworkManager)."""
    system = platform.system().lower()
    state = "on" if enable else "off"
    logger.info(f"Modification de l'état du Wi-Fi -> {state}")
    
    try:
        if system == "linux":
            subprocess.run(["nmcli", "radio", "wifi", state], check=True)
            return True
        elif system == "windows":
            cmd = ["netsh", "interface", "set", "interface", "Wi-Fi", "enabled" if enable else "disabled"]
            subprocess.run(cmd, check=True)
            return True
        else:
            logger.warning(f"Gestion du Wi-Fi non implémentée sur {system}")
            return False
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        logger.error(f"Échec de la modification du Wi-Fi : {e}")
        return False
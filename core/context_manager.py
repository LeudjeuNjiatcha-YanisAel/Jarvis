import datetime
from core.memory import Memory

class ContextManager:
    """Gère le contexte de la conversation, l'humeur et l'état de veille de Jarvis."""
    
    def __init__(self, base_prompt: str):
        self.base_prompt = base_prompt
        self.is_sleeping = False
        self.inactivity_counter = 0
        
        # Nombre de boucles (timeout) sans rien entendre avant que Jarvis relance la conversation
        self.max_inactivity_before_chatty = 3 
        # Nombre de boucles sans rien entendre avant de se mettre en veille
        self.max_inactivity_before_sleep = 6
        
        # Humeur actuelle de Jarvis
        self.mood = "causant" 
        
        # On initialise la mémoire avec le prompt dynamique calculé
        self.memory = Memory(self.get_dynamic_system_prompt())
        
    def get_dynamic_system_prompt(self) -> str:
        """Construit un prompt système dynamique injectant le contexte temporel et l'humeur."""
        time_now = datetime.datetime.now().strftime("%H:%M")
        prompt = self.base_prompt + f"\n[Contexte système : Il est actuellement {time_now}. "
        
        if self.mood == "causant":
            prompt += "Humeur de Jarvis : Très causante, proactive, amicale, curieuse, avec une pointe de sarcasme. N'hésite pas à faire la conversation, être engageant et prendre des initiatives.]"
        else:
            prompt += "Humeur de Jarvis : Normale, concise, réactive et professionnelle.]"
            
        return prompt
        
    def update_system_prompt(self):
        """Met à jour le prompt système dans la mémoire avant une requête IA."""
        self.memory.system_prompt = self.get_dynamic_system_prompt()
        
        # On s'assure que le premier message de la mémoire est bien le prompt système mis à jour
        if len(self.memory.messages) > 0 and self.memory.messages[0].get("role") == "system":
            self.memory.messages[0]["content"] = self.memory.system_prompt
            
    def reset_inactivity(self):
        """Réinitialise les compteurs d'inactivité lorsqu'on interagit avec Jarvis."""
        self.inactivity_counter = 0
        self.is_sleeping = False
        
    def increment_inactivity(self):
        """Incrémente le compteur d'inactivité à chaque écoute sans succès."""
        self.inactivity_counter += 1
        
    def should_be_chatty(self) -> bool:
        """Détermine si Jarvis doit prendre l'initiative de parler (s'il s'ennuie)."""
        return self.inactivity_counter == self.max_inactivity_before_chatty and not self.is_sleeping
        
    def should_sleep(self) -> bool:
        """Détermine s'il faut passer en veille en raison d'une trop longue inactivité."""
        return self.inactivity_counter >= self.max_inactivity_before_sleep and not self.is_sleeping
        
    def set_sleep_mode(self, sleep: bool):
        """Active ou désactive la mise en veille manuellement/automatiquement."""
        self.is_sleeping = sleep
        if sleep:
            self.inactivity_counter = self.max_inactivity_before_sleep
        else:
            self.inactivity_counter = 0

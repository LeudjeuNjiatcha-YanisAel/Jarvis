class Memory:
    """Gère l'historique de la conversation de Jarvis."""
    
    def __init__(self, system_prompt: str, max_messages: int = 30):
        self.system_prompt = system_prompt
        self.max_messages = max_messages
        self.messages = [{"role": "system", "content": system_prompt}]
        
    def add_user_message(self, content: str):
        self.messages.append({"role": "user", "content": content})
        self._enforce_limit()
        
    def add_assistant_message(self, content: str):
        self.messages.append({"role": "assistant", "content": content})
        self._enforce_limit()

    def add_raw_message(self, message):
        """Ajoute un message brut (dictionnaire ou objet API comme un tool_call)."""
        self.messages.append(message)
        self._enforce_limit()
        
    def get_messages(self):
        return self.messages
        
    def _enforce_limit(self):
        # Si on dépasse la taille max, on tronque pour ne pas saturer le contexte de l'IA.
        # On garde le prompt système (index 0) et on récupère les N derniers messages.
        if len(self.messages) > self.max_messages:
            safe_limit = 10
            self.messages = [self.messages[0]] + self.messages[-safe_limit:]
            
    def clear(self):
        self.messages = [{"role": "system", "content": self.system_prompt}]

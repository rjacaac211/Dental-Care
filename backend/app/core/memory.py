# memory.py
from typing import List, Dict, Any

class WindowMemoryManager:
    """
    An ephemeral in-memory conversation store with a fixed window size.
    Stores up to `window_size * 2` messages (i.e., user+assistant pairs).
    """

    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        # {session_id: [ {role: "...", content: "..."}, ... ]}
        self._storage: Dict[str, List[Dict[str, Any]]] = {}

    def load_conversation(self, session_id: str) -> List[Dict[str, Any]]:
        # Return a copy of the conversation
        return list(self._storage.get(session_id, []))

    def save_user_message(self, session_id: str, content: str) -> None:
        conversation = self._storage.setdefault(session_id, [])
        conversation.append({"role": "user", "content": content})
        self._prune(session_id)

    def save_assistant_message(self, session_id: str, content: str) -> None:
        conversation = self._storage.setdefault(session_id, [])
        conversation.append({"role": "assistant", "content": content})
        self._prune(session_id)

    def clear_conversation(self, session_id: str) -> None:
        if session_id in self._storage:
            del self._storage[session_id]

    def _prune(self, session_id: str) -> None:
        """Ensures we don't exceed window_size*2 messages."""
        conversation = self._storage[session_id]
        max_messages = self.window_size * 2
        if len(conversation) > max_messages:
            overflow = len(conversation) - max_messages
            self._storage[session_id] = conversation[overflow:]

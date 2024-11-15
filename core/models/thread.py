# .
from .session import Session


class Thread:
    def __init__(self, index: int = None, sessions: list[Session] = None):
        self.index = index
        self.sessions = sessions

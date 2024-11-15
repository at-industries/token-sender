class Sheet:
    def __init__(self, name: str, view: bool, protected: bool, headers: list[str]):
        self.name = name
        self.view = view
        self.headers = headers
        self.protected = protected

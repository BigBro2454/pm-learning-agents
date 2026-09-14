class Memory:
    """
    Logs the history of the negotiation for inspection and debugging.
    This acts as a global observation of the agents' interactions.
    """
    def __init__(self):
        self.history = []

    def add_entry(self, entry: dict):
        """Add an entry to the negotiation history log."""
        self.history.append(entry)

    def get_history(self) -> list:
        """Retrieve the full history of the negotiation."""
        return self.history

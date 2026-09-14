from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Message:
    """Represents a single message passed between agents."""
    sender: str
    receiver: str
    msg_type: str  # e.g., 'proposal', 'critique', 'approval'
    content: str
    round_num: int

class ConversationBuffer:
    """
    Manages the inter-agent message passing.
    Provides a shared memory space for the agents to communicate.
    """
    def __init__(self):
        self.messages: List[Message] = []

    def add_message(self, sender: str, receiver: str, msg_type: str, content: str, round_num: int):
        """Add a new message to the buffer."""
        msg = Message(sender, receiver, msg_type, content, round_num)
        self.messages.append(msg)

    def get_last_message(self) -> Optional[Message]:
        """Retrieve the most recent message from the buffer."""
        if not self.messages:
            return None
        return self.messages[-1]
    
    def get_formatted_history(self) -> str:
        """Get a formatted string of the entire conversation history."""
        history = ""
        for msg in self.messages:
            history += f"Round {msg.round_num} - {msg.sender} to {msg.receiver} ({msg.msg_type}):\n{msg.content}\n\n"
        return history

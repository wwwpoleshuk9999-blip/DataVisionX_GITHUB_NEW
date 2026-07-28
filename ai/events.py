from datetime import datetime


class AIEvent:

    def __init__(self, event, data=None):

        self.event = event
        self.data = data or {}
        self.created_at = datetime.utcnow().isoformat()


    def payload(self):

        return {
            "type": "ai",
            "event": self.event,
            "data": self.data,
            "created_at": self.created_at
        }

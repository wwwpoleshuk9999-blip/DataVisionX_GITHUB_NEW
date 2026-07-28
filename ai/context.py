from datetime import datetime


class AIContext:

    def __init__(self):

        self.session_id = (
            datetime.utcnow()
            .strftime("%Y%m%d%H%M%S")
        )

        self.data = {
            "session_id": self.session_id,
            "messages": 0,
            "last_message": None
        }


    def update(self, message):

        self.data["messages"] += 1
        self.data["last_message"] = message


    def info(self):

        return self.data

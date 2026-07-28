from ai.memory import AIMemory


class AIService:

    def __init__(self):

        self.name = "DataVisionX AI Assistant"
        self.version = "0.7.1"
        self.status = "READY"

        self.memory = AIMemory()


    def status_info(self):

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status
        }


    def chat(self, message):

        self.memory.save(
            "user",
            message
        )

        response = (
            "AI Core is online. "
            "Memory system active."
        )

        self.memory.save(
            "assistant",
            response
        )

        return {
            "assistant": self.name,
            "input": message,
            "response": response,
            "memory": self.memory.history(10)
        }


    def history(self, limit=20):

        return self.memory.history(limit)

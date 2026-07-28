from ai.memory import AIMemory
from ai.context import AIContext
from ai.events import AIEvent

from core.runtime import runtime


class AIService:

    def __init__(self):

        self.name = "DataVisionX AI Assistant"
        self.version = "0.7.3"
        self.status = "READY"

        self.memory = AIMemory()
        self.context = AIContext()


    def status_info(self):

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status
        }


    def emit_event(self, event):

        bus = runtime.get_service(
            "event_bus"
        )

        if bus:

            bus.emit(
                "system",
                event.event,
                event.payload()
            )


    def chat(self, message):

        self.context.update(
            message
        )

        self.memory.save(
            "user",
            message
        )


        response = (
            "AI Core is online. "
            "Memory, Context and Events active."
        )


        self.memory.save(
            "assistant",
            response
        )


        event = AIEvent(
            "ai_chat_completed",
            {
                "message": message,
                "response": response
            }
        )


        self.emit_event(
            event
        )


        return {
            "assistant": self.name,
            "input": message,
            "response": response,
            "context": self.context.info(),
            "memory": self.memory.history(10)
        }


    def history(self, limit=20):

        return self.memory.history(
            limit
        )


    def context_info(self):

        return self.context.info()

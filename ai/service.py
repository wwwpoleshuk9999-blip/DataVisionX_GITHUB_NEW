from ai.memory import AIMemory
from ai.context import AIContext
from ai.events import AIEvent
from ai.knowledge import AIKnowledge
from core.runtime import runtime

class AIService:
    def __init__(self):
        self.name = "DataVisionX AI Assistant"
        self.version = "0.8.0"
        self.status = "READY"
        self.memory = AIMemory()
        self.context = AIContext()
        self.knowledge = AIKnowledge()

    def status_info(self):
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status,
            "knowledge_topics": len(self.knowledge.list_topics())
        }

    def emit_event(self, event):
        bus = runtime.get_service("event_bus")
        if bus:
            bus.emit("system", event.event, event.payload())

    def chat(self, message):
        self.context.update(message)
        self.memory.save("user", message)

        kb_results = self.knowledge.search(message, limit=5)
        if kb_results:
            context_str = "\n".join([f"- {r['topic']} v{r['version']} (rel {r['relevance']}): {r['content'][:200]}" for r in kb_results])
            response = f"Found {len(kb_results)} in knowledge:\n{context_str}\n\nAI answer based on {kb_results[0]['topic']}."
        else:
            # команда обучения: "topic: content"
            if ":" in message and len(message.split(":",1)[1].strip()) > 5:
                t, c = message.split(":",1)
                if 2 <= len(t.strip()) <= 64:
                    res = self.knowledge.add(t.strip(), c.strip())
                    if res.get("duplicate"):
                        response = f"Already known: topic='{t.strip()}' v{res.get('version')}"
                    else:
                        response = f"Learned! topic='{t.strip()}' v{res.get('version')} id={res.get('id')}"
                else:
                    response = f"AI Core online. No KB hit for '{message}'. Use 'topic: content' to teach me."
            else:
                response = f"AI Core online. Memory+Context active. No KB hit for '{message}'. Topics: {len(self.knowledge.list_topics())}"

        self.memory.save("assistant", response)
        event = AIEvent("ai_chat_completed", {"message": message, "response": response, "kb_hits": len(kb_results)})
        self.emit_event(event)
        return {
            "assistant": self.name,
            "input": message,
            "response": response,
            "context": self.context.info(),
            "memory": self.memory.history(10),
            "knowledge": kb_results
        }

    def history(self, limit=20): return self.memory.history(limit)
    def context_info(self): return self.context.info()
    def knowledge_search(self, q, limit=10): return self.knowledge.search(q, limit=limit)
    def knowledge_add(self, topic, content, external=False, source="internal"):
        if external: return self.knowledge.add_external(topic, content, source)
        return self.knowledge.add(topic, content, source)

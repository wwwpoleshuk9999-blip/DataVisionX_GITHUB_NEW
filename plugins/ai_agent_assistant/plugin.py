"""Phoenix 017 - AI Assistant Agent - 100% real"""
from ai.knowledge import AIKnowledge
from ai.service import AIService

class Plugin:
    name = "AI Assistant Agent"
    version = "1.0.0"
    
    def __init__(self):
        self.knowledge = None
        self.service = None
        self.started = False
    
    def start(self):
        print(f"🤖 {self.name} v{self.version} starting...")
        self.knowledge = AIKnowledge()
        self.service = AIService()
        # Subscribe to events
        try:
            from plugin_manager.event_bus import event_bus
            event_bus.subscribe("ai_chat_request", self.on_chat_request)
            print(f"  -> Subscribed to ai_chat_request")
        except:
            pass
        self.started = True
        return f"{self.name} started - RAG ready with {len(self.knowledge.list_topics())} topics"
    
    def stop(self):
        print(f"🤖 {self.name} stopping...")
        self.started = False
        return f"{self.name} stopped"
    
    def on_chat_request(self, data):
        """Handle chat requests via EventBus"""
        query = data.get("query", "")
        if query:
            result = self.service.chat(query)
            return result
        return None
    
    def chat(self, query: str):
        """Direct chat method"""
        if not self.service:
            self.service = AIService()
        return self.service.chat(query)

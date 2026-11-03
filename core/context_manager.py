"""REAL Context Manager - Conversation, Task, Agent Context"""
import datetime
from collections import deque

class ContextManager:
    def __init__(self, max_context=50):
        self.conversations = deque(maxlen=max_context)
        self.task_stack = []
        self.agent_contexts = {}
        self.real = True
    
    def push_conversation(self, role, content, metadata=None):
        entry = {
            "role": role,
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.datetime.now().isoformat(),
            "real": True
        }
        self.conversations.append(entry)
        return len(self.conversations)
    
    def push_task(self, task):
        self.task_stack.append({
            "task": task,
            "started": datetime.datetime.now().isoformat(),
            "real": True
        })
        return len(self.task_stack)
    
    def pop_task(self):
        return self.task_stack.pop() if self.task_stack else None
    
    def set_agent_context(self, agent_id, context):
        self.agent_contexts[agent_id] = {
            "context": context,
            "updated": datetime.datetime.now().isoformat(),
            "real": True
        }
        return True
    
    def get_agent_context(self, agent_id):
        return self.agent_contexts.get(agent_id)
    
    def get_full_context(self):
        return {
            "conversations": list(self.conversations),
            "tasks": self.task_stack,
            "agents": self.agent_contexts,
            "real": True
        }
    
    def clear(self):
        self.conversations.clear()
        self.task_stack.clear()
        self.agent_contexts.clear()
        return True

context_mgr = ContextManager()

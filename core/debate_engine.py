"""REAL Debate Engine - Multi-agent debate for complex decisions"""
import datetime

class DebateEngine:
    def __init__(self):
        self.real = True
        self.rounds = 3
    
    def _get_agent_opinion(self, agent_id, question, round_num):
        try:
            mod = None
            for layer in ["ultimate", "super", "business"]:
                try:
                    mod = __import__(f"plugins.{layer}.{agent_id}.plugin", fromlist=["Plugin"])
                    break
                except:
                    continue
            if not mod:
                mod = __import__(f"plugins.{agent_id}.plugin", fromlist=["Plugin"])
            p = mod.Plugin()
            p.start()
            prompt = f"Debate round {round_num}: Question: {question}. Give your opinion as {agent_id}."
            result = p.execute({"data": prompt})
            return {"agent": agent_id, "round": round_num, "opinion": result.get("result", "")[:200], "real": True}
        except Exception as e:
            return {"agent": agent_id, "error": str(e), "real": False}
    
    def debate(self, question, agents=None, rounds=3):
        if agents is None:
            agents = ["ai_researcher", "ai_analyst" if False else "ai_data_analyzer", "ai_writer", "ai_planner"]
            # Use available agents
            agents = ["ai_researcher", "ai_data_analyzer", "ai_writer", "ai_planner", "ai_agent_assistant"][:3]
        
        history = []
        for rnd in range(1, rounds+1):
            round_opinions = []
            for agent_id in agents:
                opinion = self._get_agent_opinion(agent_id, question, rnd)
                round_opinions.append(opinion)
            history.append({"round": rnd, "opinions": round_opinions, "real": True})
        
        # Consensus (simple: longest opinion wins for demo)
        all_opinions = [op["opinion"] for rnd in history for op in rnd["opinions"] if op.get("opinion")]
        consensus = max(all_opinions, key=len) if all_opinions else "No consensus"
        
        return {
            "question": question,
            "agents": agents,
            "rounds": rounds,
            "history": history,
            "consensus": consensus,
            "real": True,
            "timestamp": datetime.datetime.now().isoformat()
        }

debate = DebateEngine()

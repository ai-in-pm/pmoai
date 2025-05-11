from crewai.agents.agent_adapters.langgraph.langgraph_adapter import LangGraphAgentAdapter as CrewAILangGraphAdapter

# Re-export CrewAI's LangGraphAdapter with our preferred name
LangGraphAdapter = CrewAILangGraphAdapter

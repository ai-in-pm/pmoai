from crewai.llm import LLM as CrewAILLM
from crewai.llms.base_llm import BaseLLM as CrewAIBaseLLM

# Re-export CrewAI's LLM and BaseLLM
LLM = CrewAILLM
BaseLLM = CrewAIBaseLLM

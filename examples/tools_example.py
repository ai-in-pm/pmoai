"""Example of using the tools module in PMOAI."""

from pmoai.agent import Agent
from pmoai.llm import LLM
from pmoai.tools import (
    AddImageTool,
    AgentTools,
    AskQuestionTool,
    BaseTool,
    CacheTools,
    DelegateWorkTool,
    Tool,
    ToolCalling,
    ToolResult,
    ToolUsage,
    tool,
)


@tool
def calculate_project_duration(start_date: str, end_date: str) -> str:
    """
    Calculate the duration of a project in days.
    
    Args:
        start_date: The start date in YYYY-MM-DD format
        end_date: The end date in YYYY-MM-DD format
        
    Returns:
        The duration of the project in days
    """
    from datetime import datetime
    
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    duration = (end - start).days
    
    return f"The project duration is {duration} days."


@tool("calculate_budget_variance")
def budget_variance(planned_budget: float, actual_cost: float) -> str:
    """
    Calculate the budget variance for a project.
    
    Args:
        planned_budget: The planned budget amount
        actual_cost: The actual cost amount
        
    Returns:
        The budget variance and percentage
    """
    variance = planned_budget - actual_cost
    percentage = (variance / planned_budget) * 100
    
    if variance >= 0:
        return f"Under budget by ${variance:.2f} ({percentage:.1f}% of planned budget)"
    else:
        return f"Over budget by ${abs(variance):.2f} ({abs(percentage):.1f}% of planned budget)"


def main():
    """Run the tools example."""
    # Initialize an LLM
    llm = LLM(provider="openai")
    
    # Create agents
    project_manager = Agent(
        role="Project Manager",
        goal="Ensure the project is completed on time and within budget",
        backstory="You are an experienced project manager with a track record of successful projects.",
        llm=llm,
    )
    
    business_analyst = Agent(
        role="Business Analyst",
        goal="Gather and analyze requirements from stakeholders",
        backstory="You are a skilled business analyst with expertise in requirements gathering and analysis.",
        llm=llm,
    )
    
    # Create agent tools
    agent_tools = AgentTools(
        agents=[project_manager, business_analyst],
    ).get_tools()
    
    # Create a cache for tools
    cache = CacheTools(ttl=3600)  # Cache for 1 hour
    
    # Create a custom tool using the Tool class
    risk_assessment_tool = Tool(
        name="Risk Assessment",
        description="Assess the risk level of a project component",
        func=lambda component, probability, impact: f"Risk assessment for {component}: {'Low' if probability * impact < 0.3 else 'Medium' if probability * impact < 0.6 else 'High'} risk",
    )
    
    # Combine all tools
    all_tools = [
        calculate_project_duration,
        budget_variance,
        risk_assessment_tool,
        *agent_tools,
    ]
    
    # Example of tool usage
    print("Tool Examples:")
    
    # Example 1: Using a decorated tool
    print("\nExample 1: Using a decorated tool")
    result = calculate_project_duration("2023-01-01", "2023-03-15")
    print(f"Result: {result}")
    
    # Example 2: Using a tool with a custom name
    print("\nExample 2: Using a tool with a custom name")
    result = budget_variance(100000, 95000)
    print(f"Result: {result}")
    
    # Example 3: Using a Tool class instance
    print("\nExample 3: Using a Tool class instance")
    result = risk_assessment_tool.run(component="Database migration", probability=0.4, impact=0.8)
    print(f"Result: {result}")
    
    # Example 4: Parsing tool calls from LLM response
    print("\nExample 4: Parsing tool calls from LLM response")
    llm_response = """
    I need to calculate the project duration and budget variance.
    
    ```json
    {
        "tool_name": "calculate_project_duration",
        "arguments": {
            "start_date": "2023-01-01",
            "end_date": "2023-06-30"
        }
    }
    ```
    
    And also check the budget:
    
    ```json
    {
        "tool_name": "calculate_budget_variance",
        "arguments": {
            "planned_budget": 250000,
            "actual_cost": 240000
        }
    }
    ```
    
    Let me also assess the risk:
    
    ```json
    {
        "tool_name": "Risk Assessment",
        "arguments": {
            "component": "Cloud migration",
            "probability": 0.7,
            "impact": 0.9
        }
    }
    ```
    """
    
    clean_response, tool_calls = ToolUsage.parse_tool_calls(llm_response)
    print(f"Clean response: {clean_response.strip()}")
    print(f"Found {len(tool_calls)} tool calls:")
    for i, call in enumerate(tool_calls):
        print(f"  {i+1}. {call['tool_name']} with arguments: {call['arguments']}")
    
    # Example 5: Executing tool calls
    print("\nExample 5: Executing tool calls")
    results = ToolUsage.execute_tool_calls(tool_calls, all_tools)
    formatted_results = ToolUsage.format_tool_results(results)
    print(formatted_results)


if __name__ == "__main__":
    main()

import pmoai

def main():
    print(f"PMOAI version: {pmoai.__version__}")
    print("PMOAI is installed successfully!")
    
    print("\n=== Available PMOAI Components ===")
    print("- Agent: Project management focused agent")
    print("- Task: Project management focused task")
    print("- Crew: Project management focused crew")
    print("- Process: Project management process flows")
    
    print("\n=== Available PM-Specific Tools ===")
    print("- ProjectCharterTool: Creates project charter documents")
    print("- RiskRegisterTool: Creates risk register documents")
    print("- ResourceAllocationTool: Creates resource allocation plans")
    print("- GanttChartTool: Creates Gantt chart visualizations")
    print("- StakeholderCommunicationTool: Creates stakeholder communication plans")
    
    print("\n=== Usage Instructions ===")
    print("1. Set your OpenAI API key as an environment variable:")
    print("   export OPENAI_API_KEY=your-api-key  # Linux/Mac")
    print("   set OPENAI_API_KEY=your-api-key     # Windows")
    print("2. Run one of the example scripts:")
    print("   python examples/project_initiation_example.py")
    
    print("\nFor more information, see the documentation at https://docs.pmoai.org")


if __name__ == "__main__":
    main()

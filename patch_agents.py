"""
Patch for the agents package to mock the missing FunctionTool and Tool classes.
"""

import sys
import types

# Check if agents is already imported
if 'agents' in sys.modules:
    import agents
    
    # Create mock classes if they don't exist
    if not hasattr(agents, 'FunctionTool'):
        class MockFunctionTool:
            """Mock FunctionTool class"""
            def __init__(self, *args, **kwargs):
                pass
        
        agents.FunctionTool = MockFunctionTool
        print("Successfully patched agents.FunctionTool")
    
    if not hasattr(agents, 'Tool'):
        class MockTool:
            """Mock Tool class"""
            def __init__(self, *args, **kwargs):
                pass
        
        agents.Tool = MockTool
        print("Successfully patched agents.Tool")
else:
    print("agents not imported yet, creating a mock module")
    
    # Create mock classes
    class MockFunctionTool:
        """Mock FunctionTool class"""
        def __init__(self, *args, **kwargs):
            pass
    
    class MockTool:
        """Mock Tool class"""
        def __init__(self, *args, **kwargs):
            pass
    
    # Create a mock agents module
    mock_agents = types.ModuleType('agents')
    mock_agents.FunctionTool = MockFunctionTool
    mock_agents.Tool = MockTool
    
    # Add the mock agents module to sys.modules
    sys.modules['agents'] = mock_agents
    
    print("Successfully created mock agents module with FunctionTool and Tool classes")

print("agents patch loaded")

#!/usr/bin/env python3
"""
# Meta Tooling Agent

This agent demonstrates Strands Agents' advanced meta-tooling capabilities - the ability of an agent
to create, load, and use custom tools dynamically at runtime.

It creates custom tools using the Agent's built-in tools for file operations and implicit tool calling.
"""

import os
from pathlib import Path
from strands import Agent, tool
from strands.models import BedrockModel
from strands_tools import shell, editor, load_tool
from config import Settings

# Define an enhanced system prompt for our tool builder agent
TOOL_BUILDER_SYSTEM_PROMPT = """You are an advanced agent that creates and uses custom Strands Agents tools.

Use all available tools implicitly as needed without being explicitly told. Always use tools instead of suggesting code 
that would perform the same operations. Proactively identify when tasks can be completed using available tools.

## CRITICAL RULE: ALWAYS CHECK EXISTING TOOLS FIRST
BEFORE doing ANYTHING related to tool creation, you MUST:
1. Run `ls tools/` to see all existing tools
2. Check if ANY similar tool already exists
3. If a similar tool exists, DO NOT CREATE A NEW ONE - instead inform the user about the existing tool

## TOOL NAMING CONVENTION:
   - The tool name (function name) MUST match the file name without the extension
   - Example: For file "tool_name.py", use tool name "tool_name"

## MANDATORY EXISTING TOOL CHECK:
   - NEVER create a tool without first running `ls tools/` command
   - If you see ANY tool that could serve a similar purpose, STOP and inform the user
   - Examples of similar tools:
     * If user wants "drug_analyzer" but "molecular_calculator.py" exists, suggest using existing tool
     * If user wants "compound_checker" but similar analysis tools exist, suggest existing tools
   - Only create new tools if NO existing tool can serve the purpose
   - When suggesting existing tools, explain what they do and how they can help

## TOOL CREATION vs. TOOL USAGE:
   - FIRST: Always check existing tools with `ls tools/`
   - SECOND: If similar tool exists, suggest using it instead of creating new one
   - THIRD: Only create new tool if user explicitly confirms they need something different
   - FOURTH: If creating, make sure it's truly different from existing tools

## AUTONOMOUS TOOL CREATION WORKFLOW - MANDATORY STEPS:

Step 1: ALWAYS run `ls tools/` first
Step 2: Analyze existing tools and check for similarities
Step 3: If similar tool found:
   - Inform user about existing tool
   - Explain what the existing tool does
   - Ask if they want to use existing tool instead
   - DO NOT proceed with creation unless user explicitly wants a different tool
Step 4: Only if no similar tool exists OR user explicitly wants different implementation:
   - Generate the complete Python code for the tool
   - Use the editor tool to write the code to "tools/tool_name.py"
   - Use the load_tool tool to dynamically load the newly created tool
   - Report the exact tool name and path created
   - Announce "TOOL_CREATED: <filename>"

## TOOL STRUCTURE
When creating a tool (only after checking existing tools), follow this structure:

```python
from strands import tool

@tool
def tool_name(input_data: str) -> str:
    \"\"\"
    Tool description
    \"\"\"
    try:
        # Tool logic here
        result = f"Result: {input_data}"
        return result
    except Exception as e:
        return f"Error: {str(e)}"
```

## IMPORTANT REMINDERS:
- NEVER skip the `ls tools/` check
- ALWAYS inform user about existing similar tools
- PREFER using existing tools over creating new ones
- Only create truly unique tools that serve different purposes

Always use the following tools when appropriate:
- shell: For checking existing tools with `ls tools/` (MANDATORY before any creation)
- editor: For writing code to files (only after confirming no similar tool exists)
- load_tool: For loading custom tools (only after creation is confirmed necessary)

Remember: Your primary job is to help users use existing tools efficiently, not to create redundant tools.
"""

# Create our agent with the necessary tools and implicit tool calling enabled
bedrock_model = BedrockModel(
    model_id=Settings.get_model_id("Claude Sonnet 4.0"),
    region_name=Settings.AWS_REGION
)
agent = Agent(
    model=bedrock_model,
    system_prompt=TOOL_BUILDER_SYSTEM_PROMPT,
    tools=[load_tool, shell, editor]
)

@tool
def create_tool(tool_name: str, description: str) -> str:
    """Create a new tool dynamically"""
    
    try:
        creation_request = f'Create a Python tool based on this description: "{description}". Name it "{tool_name}". Save it to tools/{tool_name}.py. Load the tool after it is created. Handle all steps autonomously including naming and file creation.'
        
        response = agent(creation_request)
        
        return f"Tool creation completed!\n\nTool name: {tool_name}\nDescription: {description}\n\nAgent response:\n{response}"
        
    except Exception as e:
        return f"Tool creation failed: {str(e)}"

# Example usage
if __name__ == "__main__":
    print("\nMeta-Tooling Agent Demonstration")
    print("==================================")
    print("Commands:")
    print("  • create <description> - Create a new tool")
    print("  • make a tool that <description>")
    print("  • list tools - Show created tools")
    print("  • exit - Exit the program")

    # Interactive loop
    while True:
        try:
            user_input = input("\n> ")

            # Handle exit command
            if user_input.lower() == "exit":
                print("\nGoodbye!")
                break

            # Regular interaction - let the agent's system prompt handle tool creation detection
            else:
                response = agent(
                    f'Create a Python tool based on this description: "{user_input}". Save it to tools/ folder. Load the tool after it is created. '
                    f"Handle all steps autonomously including naming and file creation."
                )
                print(response)
                
        except KeyboardInterrupt:
            print("\n\nExecution interrupted. Exiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try a different request.")

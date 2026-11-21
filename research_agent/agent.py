import re
import json
from unittest import result
from llm import call_llm
from research_agent.tools.calculator import calculator_tool
from research_agent.prompt import SYSTEM_PROMPT


# ==== TOOL REGISTERY ====

TOOLS = {
    "calculator": calculator_tool

}

def execute_tool(tool_name: str, tool_input: str) -> str:
    """
    Executes the specified tool with the given input.

    Args:
        tool_name (str): The name of the tool to execute.
        tool_input (str): The input for the tool.

    Returns:
        str: The result from the tool execution.
    """
    if tool_name in TOOLS:
        return TOOLS[tool_name](tool_input)
    else:
        return f"Tool '{tool_name}' not found."

def parse_llm_response(response: str) -> dict:
    """
    Parses the LLM response to extract the action and action_input.

    Args:
        response (str): The response from the LLM.

    Returns:
        dict: A dictionary containing the action and action_input.
    """
    response = re.sub(r"```json|```", "", response).strip()
    return json.loads(response)

if __name__ == "__main__":

    conversation_history = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    print("========================================")
    print("Welcome to the Research Agent!")
    print("========================================")

    while True:
        user_input = input("Enter your question for the Agent (or type 'exit' to quit): ")
        
        if user_input.lower() == 'exit':
            break

        conversation_history.append(
            {
                "role": "user",
                "content": user_input
            }
        )


        llm_response = call_llm(conversation_history)

        conversation_history.append(
            {
                "role": "assistant",
                "content": llm_response
            }
        )

        decision = parse_llm_response(llm_response)


        action = decision["action"]
        action_input = decision["action_input"]

        if action == "calculator":
            print(f"Agent Response: {decision}")
            tool_result = execute_tool(action, action_input)
            print(f"Tool Result: {tool_result}")

            conversation_history.append(
                {
                    "role": "user",
                    "content": f"Tool Result: {tool_result}"
                }
            )

            final_response = call_llm(conversation_history)

            print(f"Final Response: {final_response}.")

        elif action == "finish":
            print(f"Agent Response: {action_input}")
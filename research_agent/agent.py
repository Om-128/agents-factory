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

def test_call_llm(user_input: str = "What is the capital of France?") -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]
    provider = "gemini" 

    response = call_llm(messages, provider)

    return response

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

def get_final_response(user_question, tool_result=None):
    messages = [
        {
            'role': 'system',
            'content': SYSTEM_PROMPT
        },
        {
            'role': 'user',
            'content': f"""
                User Question: {user_question}
                Tool Result: {tool_result if tool_result else 'No tool result available.'}
                Please provide a final response to the user based on the above information."""
        }
    ]

    return messages

if __name__ == "__main__":
    while True:
        user_input = input("Enter your question for the Agent (or type 'exit' to quit): ")
        
        if user_input.lower() == 'exit':
            break

        llm_response = test_call_llm(user_input)
        decision = parse_llm_response(llm_response)

        action = decision["action"]
        action_input = decision["action_input"]

        if action == "calculator":
            print(f"Agent Response: {decision}")
            tool_result = execute_tool(action, action_input)
            print(f"Tool Result: {tool_result}")

            final_question = get_final_response(user_input, tool_result)
            final_response = call_llm(final_question, "groq")

            print(f"Final Response: {final_response}.")

        elif action == "finish":
            print(f"Agent Response: {action_input}")
import re
import json
from logger import logger
from llm import call_llm
from research_agent.tools.calculator import calculator_tool
from research_agent.tools.date_time import get_date_time
from research_agent.tools.web_search import web_search
from research_agent.prompt import SYSTEM_PROMPT


# ==== TOOL REGISTERY ====

TOOLS = {
    "calculator": calculator_tool,
    "date_time": get_date_time,
    "web_search": web_search
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

    MAX_ITERATIONS = 5

    conversation_history = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    print("========================================")
    print("Welcome to the Research Agent!")
    print("========================================")

    for i in range(MAX_ITERATIONS):
        user_input = input("Enter your question for the Agent (or type 'exit' to quit): ")
        
        if user_input.lower() == 'exit':
            break
        
        
        conversation_history.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        while True:

            try:
                llm_response = call_llm(conversation_history)
                decision = parse_llm_response(llm_response)

            except json.JSONDecodeError: # If LLM return invalid json
                logger.error("Error: LLM returned invalid json")
                break

            except Exception as e:
                logger.error(f"LLM Error: {e}")
                break

            conversation_history.append(
                {
                    "role": "assistant",
                    "content": llm_response
                }
            )

            action = decision["action"]
            action_input = decision["action_input"]

            if action == "finish":
                logger.info(f"Final Agent Response: {action_input}")
                break

            logger.info(f"Agent Decision: {decision}")

            tool_result = execute_tool(action, action_input)

            logger.info(f"Tool Result: {tool_result}")

            print("========================================\n")

            conversation_history.append(
                {
                    "role": "user",
                    "content": f"Tool Result: {tool_result}"
                }
            )
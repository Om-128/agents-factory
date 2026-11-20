def calculator_tool(expression: str) -> str:
    """
    A simple calculator tool that evaluates mathematical expressions.
    """
    try:
        # Evaluate the expression safely
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"
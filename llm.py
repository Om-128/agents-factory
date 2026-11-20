from litellm import Router
from litellm.setup_wizard import PROVIDERS
from config import MODEL_LIST, FALLBACKS

router = Router(
    model_list=MODEL_LIST, 
    fallbacks=FALLBACKS,
    num_retries=0
)

def call_llm(messages, provider):

    try:
        response = router.completion(
            model="groq-primary",
            messages=messages
        )
    except Exception as e:
        print(f"Error occurred while calling LLM: {e}")
        raise


    return response.choices[0].message["content"]
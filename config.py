from settings import settings

MODEL_LIST = [
    {
        "model_name": "groq-primary",
        "litellm_params": {
            "model": "groq/gpt-oss-120b",
            "api_key": settings.GROQ_API_KEY.get_secret_value(),
            "order": 1
        }
    },
    {
        "model_name": "gemini-fallback",
        "litellm_params": {
            "model": "gemini/gemini-3.5-flash-lite",
            "api_key": settings.GEMINI_API_KEY.get_secret_value()
        }
    }
]

FALLBACKS = [
    {"groq-primary": ["gemini-fallback"]}
]
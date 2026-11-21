from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # API KEYS
    GROQ_API_KEY: SecretStr
    GEMINI_API_KEY: SecretStr
    LANGSEARCH_API_KEY: SecretStr
    
    model_config = SettingsConfigDict(
                        env_file=".env", 
                        env_file_encoding="utf-8", 
                        extra="ignore"
                    )

settings = Settings()

if __name__ == "__main__":
    print("GROQ_API_KEY:", settings.GROQ_API_KEY.get_secret_value())
    print("GEMINI_API_KEY:", settings.GEMINI_API_KEY.get_secret_value())

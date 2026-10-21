import os

class Config:
    GEMMA_PROVIDER: str = os.getenv("GEMMA_PROVIDER", "openai_compat")  # "openai_compat" | "ollama"
    GEMMA_BASE_URL: str = os.getenv("GEMMA_BASE_URL", "https://integrate.api.nvidia.com/v1")
    GEMMA_API_KEY: str = os.getenv("GEMMA_API_KEY", "")
    GEMMA_MODEL: str = os.getenv("GEMMA_MODEL", "google/gemma-3-27b-it")
    GEMMA_TIMEOUT_SECONDS: float = float(os.getenv("GEMMA_TIMEOUT_SECONDS", "20.0"))
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    MAX_IMAGE_SIZE_MB: int = int(os.getenv("MAX_IMAGE_SIZE_MB", "10"))

config = Config()

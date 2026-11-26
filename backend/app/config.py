"""Application settings for SOFA INTEL DZ. Copyright (c) 2026 saifiwalid."""

from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_env: str = "development"
    app_name: str = "SOFA INTEL DZ"
    app_copyright: str = "saifiwalid"
    debug: bool = True
    database_url: str = "sqlite:///./sofa_intel_dz.db"
    allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    api_rate_limit_per_minute: int = 120
    llm_provider: str = "local_heuristic"
    daily_llm_token_budget: int = 250000
    google_cse_api_key: str = ""
    google_cse_cx: str = ""
    facebook_graph_access_token: str = ""
    instagram_graph_access_token: str = ""
    tiktok_research_api_key: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()

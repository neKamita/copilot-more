"""
Settings module for copilot-more using pydantic-settings for configuration management.
"""
from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings using pydantic-settings for validation and environment variable loading.

    This centralizes all configuration values and provides validation.
    """
    # GitHub Copilot API settings
    refresh_token: str = Field(
        default="",
        description="GitHub Copilot refresh token for authentication"
    )

    chat_completions_api_endpoint: str = Field(
        default="https://api.individual.githubcopilot.com/chat/completions",
        description="GitHub Copilot chat completions API endpoint"
    )
    models_api_endpoint: str = Field(
        default="https://api.individual.githubcopilot.com/models",
        description="GitHub Copilot models API endpoint"
    )
    editor_version: str = Field(
        default="vscode/1.95.3",
        description="Editor version to use in API requests"
    )

    # Request and response settings
    max_tokens: int = Field(
        default=10240,
        description="Maximum number of tokens in API responses"
    )
    timeout_seconds: int = Field(
        default=300,
        description="Timeout for API requests in seconds"
    )

    # Proxy and traffic recording settings
    record_traffic: bool = Field(
        default=False,
        description="Whether to record API traffic for debugging"
    )

    # Pydantic model configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @field_validator("refresh_token")
    def validate_refresh_token(cls, v: str) -> str:
        """Validate that the refresh token is provided and starts with 'gho_'."""
        if not v:
            raise ValueError("REFRESH_TOKEN environment variable is required")

        if not v.startswith("gho_"):
            raise ValueError("REFRESH_TOKEN should be a GitHub OAuth token starting with 'gho_'")
        return v


@lru_cache()
def get_settings() -> Settings:
    """
    Get the application settings.

    Using a function with lru_cache allows for lazy loading and efficient reuse.
    """
    return Settings()


# Create a global instance for direct import in most cases
settings = get_settings()
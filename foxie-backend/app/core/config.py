"""
Configuration management for Foxie Backend.
Centralizes all configuration and environment variables.
Backend no longer requires GOOGLE_API_KEY - users provide their own keys via requests.
"""
import os
from typing import Optional
from pydantic import BaseModel, Field


class AppConfig(BaseModel):
    """Main application configuration."""
    
    # API Configuration
    title: str = "Foxie AI Backend"
    description: str = "AI code generation for FastAPI projects"
    version: str = "2.0.0"
    
    # Server Configuration
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    
    # AI Configuration
    gemini_model: str = Field(default="gemini-2.5-flash", description="Gemini model to use")
    generation_temperature: float = Field(default=0.7, description="Temperature for code generation")
    rag_knowledge_base_path: str = Field(default="data/rag_knowledge_base", description="Path to RAG knowledge base")
    
    class Config:
        """Pydantic config."""
        env_prefix = ""
    
    @classmethod
    def from_env(cls) -> "AppConfig":
        """Create configuration from environment variables."""
        return cls(
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "8000")),
            gemini_model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            generation_temperature=float(os.getenv("GENERATION_TEMPERATURE", "0.7")),
            rag_knowledge_base_path=os.getenv("RAG_KNOWLEDGE_BASE_PATH", "data/rag_knowledge_base"),
        )


# Global configuration instance
config = AppConfig.from_env()

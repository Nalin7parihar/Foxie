"""
Configuration management for Foxie Backend.
Centralizes all configuration and environment variables.
"""
import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()


class AppConfig(BaseModel):
    """Main application configuration."""
    
    # API Configuration
    title: str = "Foxie AI Backend - Phase 2"
    description: str = "AI code generation for FastAPI projects"
    version: str = "2.0.0"
    
    # Server Configuration
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    
    # AI Configuration
    google_api_key: str = Field(description="Google Gemini API key")
    gemini_model: str = Field(default="gemini-2.5-flash", description="Gemini model to use")
    generation_temperature: float = Field(default=0.7, description="Temperature for code generation")
    correction_temperature: float = Field(default=0.1, description="Temperature for corrections")
    
    # Self-Correction Configuration
    max_correction_iterations: int = Field(default=3, ge=1, le=10, description="Max correction iterations")
    enable_self_correction_by_default: bool = Field(default=False, description="Enable self-correction by default (opt-in)")
    
    # RAG Configuration
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
            google_api_key=os.getenv("GOOGLE_API_KEY", ""),
            gemini_model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            generation_temperature=float(os.getenv("GENERATION_TEMPERATURE", "0.7")),
            correction_temperature=float(os.getenv("CORRECTION_TEMPERATURE", "0.1")),
            max_correction_iterations=int(os.getenv("MAX_CORRECTION_ITERATIONS", "3")),
            enable_self_correction_by_default=os.getenv("ENABLE_SELF_CORRECTION", "false").lower() == "true",
            rag_knowledge_base_path=os.getenv("RAG_KNOWLEDGE_BASE_PATH", "data/rag_knowledge_base"),
        )
    
    def validate_api_key(self) -> bool:
        """Validate that API key is set."""
        return bool(self.google_api_key and self.google_api_key.strip())


# Global configuration instance
config = AppConfig.from_env()

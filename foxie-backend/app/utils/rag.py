import os
import typer
from typing import List

def load_style_guide_snippets(base_dir: str = "data/rag_knowledge_base/fastapi") -> str:
    """
    Reads all .example files from the RAG knowledge base
    and concatenates them into a single string for the prompt.
    """
    snippets: List[str] = []
    
    try:
        # Loop through all files in the directory
        for filename in os.listdir(base_dir):
            if filename.endswith(".example"):
                file_path = os.path.join(base_dir, filename)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Add headers to help the AI distinguish between files
                    snippets.append(f"--- START: {filename} ---\n{content}\n--- END: {filename} ---")
                    
    except FileNotFoundError:
        # Don't fail the whole app, just warn the user
        typer.secho(f"Warning: RAG directory not found at {base_dir}. Skipping style guide.", fg=typer.colors.YELLOW)
        return ""
    
    return "\n\n".join(snippets)
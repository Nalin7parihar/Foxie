import typer
from google import genai
from dotenv import load_dotenv
import os
load_dotenv()

app=typer.Typer()

try:
  client=genai.Client()
except Exception as e:
  print("Error initializing GenAI client:", e)
  exit(1)
  
@app.command()
def generate(file_path : str):
  """
  Generates a docstring for a given Python file
  """
  if not client:
    typer.echo("Gemini CLient not initialized. Is your api key set in env?")
    raise typer.Exit(code=1)
  
  typer.echo(f"Generating docstring for {file_path}...")
  
  try:
    with open(file_path,'r') as f:
      code =f.read()
    prompt=f"""You are an expert Python programmer specializing in writing documentation.
    Generate a concise, Google-style docstring for the following Python code. 
    Only return the docstring itself, with no other explanation or text.
    ---CODE START---
    {code}
    ---CODE END---
    """
    response=client.models.generate_content(
      model="gemini-2.5-flash",
      contents=prompt                                      
    )
    generated_docstring=response.text
    typer.echo("\n--- Generated Docstring ---")
    typer.echo(generated_docstring)
  
  except FileNotFoundError:
    typer.echo(f"Error:file not found at {file_path}")
    raise typer.Exit(code=1)
  except Exception as e:
    typer.echo(f"An unexpected error occurred: {e}")
    raise typer.Exit(code=1)
  
if __name__ == "__main__":
  app()
      
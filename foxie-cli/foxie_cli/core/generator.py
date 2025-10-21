import instructor
from dotenv import load_dotenv
from google import genai
from google.genai import types
import typer
from foxie_cli.utils.rag import load_style_guide_snippets
from foxie_cli.core.prompts import MASTER_PROMPT_TEMPLATE
from foxie_cli.core.models import GeneratedCode
from foxie_cli.utils.parser import parse_fields,Field
from typing import List
load_dotenv()


try:
  client = genai.Client()

except Exception as e:
  typer.secho("Error initializing Gemini client. Please check your API key and internet connection.",fg=typer.colors.RED)
  raise typer.Exit(code=1)



def generate_crud_feature(resource : str, fields_str : str,project_name : str) -> GeneratedCode:
  parsed_fields : List[Field] =[]
  try:
    parsed_fields : List[Field] = parse_fields(fields_str)
  except Exception as e:
    typer.secho(f"Error parsing fields : {e}",fg=typer.colors.BRIGHT_RED)
    
  fields_list_str = "\n".join([f"- **{f.name}**: {f.type}" for f in parsed_fields])
  
  typer.secho("Loading style guide snippets from RAG knowledge base...",fg=typer.colors.CYAN)
  style_guide = load_style_guide_snippets()
  
  
  prompt = MASTER_PROMPT_TEMPLATE.format(
    resource=resource,fields_list=fields_list_str,project_name=project_name,style_guide=style_guide)
  typer.secho("Generating CRUD feature using Gemini model...",fg=typer.colors.CYAN)
  try:
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config={
      "response_mime_type" : "application/json",
      "response_schema" : GeneratedCode
    }
    )
    
    typer.secho("Received response from Gemini model",fg=typer.colors.BRIGHT_GREEN)
    
    return response.parsed
  except Exception as e:
    typer.secho(f"Error generating CRUD feature: {e}", fg=typer.colors.BRIGHT_RED)
    raise typer.Exit(code=1)  


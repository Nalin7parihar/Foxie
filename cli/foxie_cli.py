import typer
from dotenv import load_dotenv
import os
import requests
from pathlib import Path
import questionary
load_dotenv()

CONFIG_DIR= Path.home() / ".config" / "foxie"

TOKEN_FILE = CONFIG_DIR / "credentials"

def save_token(token : str):
  
  try:
    CONFIG_DIR.mkdir(parents=True,exist_ok=True)
    TOKEN_FILE.write_text(token)
    typer.echo(f"Token saved to {TOKEN_FILE}")
  except Exception as e:
    typer.echo(f"Error saving token: {e}")
    raise typer.Exit(code=1)

def load_token() ->str | None:
  if not TOKEN_FILE.exists():
    return None
  
  try:
    return TOKEN_FILE.read_text()
  except Exception as e:
    typer.echo(f"Error reading token : {e}")
    return None


app=typer.Typer()
@app.command()
def generate(file_path : str):
  """
  Generates a docstring for a given Python file
  """
  token = load_token()
  if not token:
    typer.echo("No token found. Please login.")
    raise typer.Exit(code=1)
  
  docstring_type = typer.prompt("Enter docstring type (e.g., Google, NumPy, reStructuredText)", default="Google")
  typer.echo(f"Generating docstring for {file_path}...")
  
  try:
    with open(file_path,'r') as f:
      code =f.read()
    
    url = "http://localhost:8000/generate"
    headers = {
      "Authorization" : f"Bearer {token}"
    }
    payload = {
      "code" : code,
      "type" : docstring_type
    }
    response = requests.post(url,json=payload,headers=headers)
    typer.echo("\n--- Generated Docstring ---")
    typer.echo(response.json().get("docstring"))
    typer.echo("\n---------------------------")
  
  except FileNotFoundError:
    typer.echo(f"Error:file not found at {file_path}")
    raise typer.Exit(code=1)
  except Exception as e:
    typer.echo(f"An unexpected error occurred: {e}")
    raise typer.Exit(code=1)
  
@app.command()
def register():
  """Register a new Foxie user
  """
  typer.echo("Register yourself to foxie")
  email=typer.prompt("Enter Email")
  name=typer.prompt("Enter Name")
  password=typer.prompt("Enter Password",hide_input=True)
  
  url = "http://localhost:8000/auth/register"
  try:
    response  = requests.post(url,json={"email":email,"name":name,"password":password})
    
    response.raise_for_status()
    
    data=response.json()
    typer.echo(f"Registration successful! for user : {data.get('name')} with email : {data.get('email')}")
  
  except requests.exceptions.HTTPError as err:
    typer.echo(f"Registeration failed: {err.response.status_code} - {err.response.text}")
  except requests.exceptions.RequestException as err:
    typer.echo(f"An error occurred: {err}")
    raise typer.Exit(code=1) 
  
@app.command()
def login():
  """Register a new Foxie user
  """
  typer.echo("Login to foxie")
  email=typer.prompt("Enter Email")
  password=typer.prompt("Enter Password",hide_input=True)
  
  url = "http://localhost:8000/auth/login"
  try:
    response  = requests.post(url,json={"email":email,"password":password})
    
    response.raise_for_status()
    
    data=response.json()
    access_token=data.get("access_token")
    
    if access_token:
      typer.echo("Login successful!")
      save_token(access_token)
    
    else:
      typer.echo("Registration failed: No access token received.")
      raise typer.Exit(code=1)
  
  except requests.exceptions.HTTPError as err:
    typer.echo(f"Login failed: {err.response.status_code} - {err.response.text}")
  except requests.exceptions.RequestException as err:
    typer.echo(f"An error occurred: {err}")
    raise typer.Exit(code=1) 
  
  
if __name__ == "__main__":
  app()
      
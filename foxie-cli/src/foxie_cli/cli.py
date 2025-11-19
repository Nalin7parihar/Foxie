import typer
import requests
from typing_extensions import Annotated
from typing import Optional
import os
import getpass
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from dotenv import load_dotenv, dotenv_values

# Assuming your file writer utility is here
from .utils.file_writer import write_files
from .utils.template_generator import generate_pyproject_toml, generate_env_file
# Assuming your Pydantic models for the response are here
from .core.models import GeneratedCode, CodeFile

# Helper function to get the config directory path (following XDG Base Directory spec)
def get_config_path() -> Path:
    """
    Get the configuration directory path following XDG Base Directory specification.
    Uses ~/.config/foxie/ on all platforms (works on Linux, macOS, and Windows 10+).
    """
    return Path.home() / ".config" / "foxie"

def get_config_file() -> Path:
    """Get the path to the config file."""
    return get_config_path() / "config.env"

# Load .env files to populate environment variables
# This ensures os.getenv() can find GOOGLE_API_KEY from .env files
load_dotenv()  # Loads .env in current directory
foxie_config = get_config_file()
if foxie_config.exists():
    load_dotenv(foxie_config)  # Also load ~/.config/foxie/config.env

# --- Configuration ---
# Define the URL of your backend service. Default is localhost.
BACKEND_URL = os.getenv("FOXIE_BACKEND_URL", "http://127.0.0.1:8000")

# Scaffold timeout in seconds
SCAFFOLD_TIMEOUT = int(os.getenv("FOXIE_SCAFFOLD_TIMEOUT", "300"))  # Default 5 minutes

console = Console()
app = typer.Typer(
    name="foxie",
    help="🦊 A smart AI-powered code scaffolding CLI for FastAPI"
)

scaffold_app = typer.Typer(
    name="scaffold",
    help="Scaffold new features and code structures using AI."
)
app.add_typer(scaffold_app)


def get_api_key() -> Optional[str]:
    """
    Get Google Gemini API key from environment or prompt user.
    Priority:
    1. GOOGLE_API_KEY environment variable (includes values loaded from .env files)
    2. .env file in current directory (fallback if not loaded)
    3. ~/.config/foxie/config.env file (fallback if not loaded)
    4. Prompt user to enter it
    
    Returns:
        API key string or None
    """
    # Check environment variable first (this will include values from .env files
    # that were loaded by load_dotenv() at module level)
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        # Determine source for user feedback
        env_file = Path(".env")
        foxie_config = get_config_file()
        if env_file.exists() and "GOOGLE_API_KEY" in dotenv_values(env_file):
            console.print("[dim]✓ Using API key from .env file[/dim]")
        elif foxie_config.exists() and "GOOGLE_API_KEY" in dotenv_values(foxie_config):
            console.print("[dim]✓ Using API key from config file[/dim]")
        else:
            console.print("[dim]✓ Using API key from environment[/dim]")
        return api_key
    
    # Fallback: Check .env file in current directory directly
    # (in case load_dotenv() didn't work for some reason)
    env_file = Path(".env")
    if env_file.exists():
        config = dotenv_values(env_file)
        api_key = config.get("GOOGLE_API_KEY")
        if api_key:
            console.print("[dim]✓ Using API key from .env file[/dim]")
            return api_key
    
    # Fallback: Check ~/.config/foxie/config.env directly
    foxie_config = get_config_file()
    if foxie_config.exists():
        config = dotenv_values(foxie_config)
        api_key = config.get("GOOGLE_API_KEY")
        if api_key:
            console.print("[dim]✓ Using API key from config file[/dim]")
            return api_key
    
    # Prompt user
    console.print("\n[yellow]⚠️  Google Gemini API Key Required[/yellow]")
    console.print("[dim]No API key found in environment or config files.[/dim]\n")
    
    console.print("[cyan]You can get your API key from:[/cyan]")
    console.print("[cyan]https://makersuite.google.com/app/apikey[/cyan]\n")
    
    api_key = getpass.getpass("🔑 Enter your Google Gemini API key (hidden): ")
    
    if api_key:
        # Offer to save it
        config_file = get_config_file()
        save_it = Confirm.ask(f"\n💾 Save this API key to {config_file} for future use?", default=True)
        if save_it:
            config_dir = get_config_path()
            config_dir.mkdir(parents=True, exist_ok=True)
            
            with open(config_file, "w") as f:
                f.write(f"GOOGLE_API_KEY={api_key}\n")
            
            console.print(f"[green]✓ API key saved to {config_file}[/green]")
    
    return api_key


def interactive_scaffold():
    """Interactive mode - prompts user for all inputs."""
    console.print(Panel.fit(
        "[bold cyan]🦊 Foxie AI Code Scaffolding[/bold cyan]\n"
        "Generate production-ready FastAPI CRUD features with AI",
        border_style="cyan"
    ))
    
    # Get API key first
    api_key = get_api_key()
    if not api_key:
        console.print("[red]❌ API key is required to use Foxie[/red]")
        raise typer.Exit(code=1)
    
    # Project name
    project_name = Prompt.ask(
        "\n[cyan]📦 Project name[/cyan]",
        default="my-fastapi-project"
    )
    
    # Resource name
    resource = Prompt.ask(
        "[cyan]🏷️  Resource name[/cyan] (e.g., product, user, order)",
        default="product"
    )
    
    # Fields
    console.print("\n[cyan]📝 Define your fields[/cyan]")
    console.print("[dim]Format: field_name:type (comma-separated)[/dim]")
    console.print("[dim]Example: name:str,price:float,description:str,stock:int[/dim]")
    
    fields = Prompt.ask(
        "\n[cyan]Fields[/cyan]",
        default="name:str,price:float,description:str"
    )
    
    # Database type
    console.print("\n[cyan]🗄️  Database Type[/cyan]")
    console.print("[dim]Choose your database system:[/dim]")
    console.print("[bold]1. SQL[/bold] (SQLAlchemy with PostgreSQL/MySQL/SQLite)")
    console.print("[bold]2. MongoDB[/bold] (NoSQL with Beanie ODM)")
    
    db_choice = Prompt.ask(
        "\n[yellow]Select database type[/yellow]",
        choices=["1", "2"],
        default="1"
    )
    database_type = "sql" if db_choice == "1" else "mongodb"
    
    # Authentication
    console.print("\n[cyan]🔐 Authentication[/cyan]")
    console.print("[dim]Enable authentication? This will generate:[/dim]")
    console.print("[dim]  - User model with password hashing[/dim]")
    console.print("[dim]  - Registration and login endpoints[/dim]")
    console.print("[dim]  - JWT token generation[/dim]")
    
    enable_auth = Confirm.ask(
        "[yellow]Enable authentication?[/yellow]",
        default=False
    )
    
    return {
        "project_name": project_name,
        "resource": resource,
        "fields": fields,
        "database_type": database_type,
        "enable_auth": enable_auth,
        "mode": "1",  # Always use Standard mode
        "api_key": api_key
    }


@scaffold_app.command(
    "fastapi-crud",
    help="Scaffolds a full CRUD feature via the backend AI service."
)
def scaffold_fastapi_crud(
    project_name: Annotated[Optional[str], typer.Option(
        "--project-name", "-p",
        help="The name for the new project folder."
    )] = None,
    resource: Annotated[Optional[str], typer.Option(
        "--resource", "-r",
        help="The name of the resource, e.g., 'product', 'user'."
    )] = None,
    fields: Annotated[Optional[str], typer.Option(
        "--fields", "-f",
        help='A comma-separated string of fields and types, e.g., "name:str,price:float".'
    )] = None,
    database_type: Annotated[Optional[str], typer.Option(
        "--database-type", "-d",
        help="Database type: 'sql' or 'mongodb' (default: sql)"
    )] = None,
    enable_auth: Annotated[bool, typer.Option(
        "--enable-auth",
        help="Enable authentication (generates User model, auth endpoints, JWT)"
    )] = False,
):
    """
    Sends a request to the Foxie backend to generate code.
    If no options provided, launches interactive mode.
    """
    # If no arguments provided, use interactive mode
    if not project_name and not resource and not fields:
        params = interactive_scaffold()
        project_name = params["project_name"]
        resource = params["resource"]
        fields = params["fields"]
        database_type = params["database_type"]
        enable_auth = params["enable_auth"]
        api_key = params["api_key"]
    else:
        # Validate required parameters
        if not project_name or not resource or not fields:
            console.print("[red]❌ Error: When using command-line options, --project-name, --resource, and --fields are all required.[/red]")
            console.print("\n[yellow]💡 Tip: Run without options for interactive mode[/yellow]")
            raise typer.Exit(code=1)
        
        # Get API key
        api_key = get_api_key()
        if not api_key:
            console.print("[red]❌ API key is required to use Foxie[/red]")
            raise typer.Exit(code=1)
        
        # Set defaults for optional parameters
        if database_type is None:
            database_type = "sql"
        if database_type not in ["sql", "mongodb"]:
            console.print("[red]❌ Error: --database-type must be 'sql' or 'mongodb'[/red]")
            raise typer.Exit(code=1)
    
    # Display summary
    console.print(f"\n[cyan]✨ Scaffolding Configuration:[/cyan]")
    console.print(f"  Project: [bold]{project_name}[/bold]")
    console.print(f"  Resource: [bold]{resource}[/bold]")
    console.print(f"  Fields: [bold]{fields}[/bold]")
    console.print(f"  Database: [bold]{database_type.upper()}[/bold]")
    console.print(f"  Authentication: [bold]{'✅ Enabled' if enable_auth else '❌ Disabled'}[/bold]")
    
    # --- Prepare API Request ---
    request_data = {
        "project_name": project_name,
        "resource": resource,
        "fields_str": fields,
        "database_type": database_type,
        "enable_auth": enable_auth,
        "api_key": api_key
    }
    scaffold_endpoint = f"{BACKEND_URL}/scaffold"
    typer.echo(f"\n⚡ Generating code...")
    typer.echo(f"   Contacting backend at {scaffold_endpoint}...")

    # --- Call Backend API ---
    generated_code: GeneratedCode = None
    try:
        # Use a spinner while waiting for the backend
        with console.status("[bold green]🤖 AI is generating your code...", spinner="dots") as status:
            response = requests.post(
                scaffold_endpoint, 
                json=request_data, 
                timeout=SCAFFOLD_TIMEOUT
            )
            response.raise_for_status() # Check for HTTP errors
            response_data = response.json()
            
            # Response is GeneratedCode
            generated_code = GeneratedCode(**response_data)
            
            status.stop()
            
        typer.secho("\n✅ Received generated code from backend!", fg=typer.colors.GREEN)

    except requests.exceptions.ConnectionError:
        console.print(f"\n[red]❌ Error: Could not connect to backend at {BACKEND_URL}.[/red]")
        console.print("[yellow]    Please ensure the backend server (`foxie-backend`) is running.[/yellow]")
        console.print("[dim]    Run: docker-compose up -d backend[/dim]")
        raise typer.Exit(code=1)
    except requests.exceptions.Timeout:
        console.print(f"\n[red]❌ Error: Request to backend timed out after {SCAFFOLD_TIMEOUT} seconds.[/red]")
        console.print("[yellow]    The AI generation is taking longer than expected.[/yellow]")
        console.print("[dim]    Tip: You can increase the timeout by setting FOXIE_SCAFFOLD_TIMEOUT environment variable[/dim]")
        console.print(f"[dim]    Current timeout: {SCAFFOLD_TIMEOUT}s. Try: export FOXIE_SCAFFOLD_TIMEOUT=300[/dim]")
        raise typer.Exit(code=1)
    except requests.exceptions.HTTPError as e:
        error_detail = e.response.text # Get error detail from backend if available
        console.print(f"\n[red]❌ Backend Error ({e.response.status_code}):[/red]")
        console.print(f"[red]{error_detail}[/red]")
        raise typer.Exit(code=1)
    except Exception as e: # Catch Pydantic validation errors or other issues
        console.print(f"\n[red]❌ Error processing backend response: {e}[/red]")
        raise typer.Exit(code=1)
    
    if generated_code is None:
        console.print("\n[red]❌ Error: No code was generated by the backend.[/red]")
        raise typer.Exit(code=1)

    # --- Write Files ---
    try:
        write_files(generated_code, base_dir=project_name)
        
        # Generate static template files (pyproject.toml and .env)
        console.print("\n[bold cyan]📝 Generating configuration files...[/bold cyan]")
        
        pyproject_path = os.path.join(project_name, "pyproject.toml")
        generate_pyproject_toml(
            project_name=project_name,
            database_type=database_type,
            enable_auth=enable_auth,
            output_path=pyproject_path
        )
        console.print(f"  ✅ Created: {pyproject_path}")
        
        env_path = os.path.join(project_name, ".env")
        generate_env_file(
            database_type=database_type,
            output_path=env_path
        )
        console.print(f"  ✅ Created: {env_path}")
        
        console.print(f"\n[bold bright_green]🎉 Successfully scaffolded project '{project_name}'![/bold bright_green]")
        
        # Show file count (including the 2 template files)
        total_files = len(generated_code.files) + 2
        console.print(f"[green]📄 Generated {total_files} files ({len(generated_code.files)} code files + 2 config files)[/green]")
        
        # --- Setup Instructions ---
        console.print("\n[bold cyan]📋 Next Steps:[/bold cyan]")
        
        console.print(f"\n[bold]1. Navigate to your project:[/bold]")
        console.print(f"   [cyan]cd {project_name}[/cyan]")
        
        console.print(f"\n[bold]2. Setup environment:[/bold]")
        console.print(f"   [cyan]uv venv[/cyan]")
        console.print(f"   [cyan].venv\\Scripts\\activate[/cyan]  [dim](Windows)[/dim]")
        console.print(f"   [cyan]source .venv/bin/activate[/cyan]  [dim](Linux/macOS)[/dim]")
        
        console.print(f"\n[bold]3. Install dependencies:[/bold]")
        console.print(f"   [cyan]uv pip install -e .[/cyan]")
        
        # Database-specific setup instructions
        if database_type == "sql":
            console.print(f"\n[bold]4. Configure database (optional):[/bold]")
            console.print(f"   [cyan]# SQLite is configured by default in .env[/cyan]")
            console.print(f"   [cyan]# For PostgreSQL: Update DATABASE_URL in .env file[/cyan]")
        else:  # mongodb
            console.print(f"\n[bold]4. Configure database:[/bold]")
            console.print(f"   [cyan]# Update DATABASE_URL in .env file if needed[/cyan]")
            console.print(f"   [cyan]# Default: mongodb://localhost:27017[/cyan]")
        
        if enable_auth:
            console.print(f"\n[bold]5. Configure authentication:[/bold]")
            console.print(f"   [cyan]# Update SECRET_KEY in .env file for production[/cyan]")
            console.print(f"   [cyan]# Default key is provided for development only[/cyan]")
        
        console.print(f"\n[bold]6. Run your FastAPI app:[/bold]")
        console.print(f"   [cyan]uvicorn app.main:app --reload[/cyan]")
        
        console.print(f"\n[dim]💡 Tip: Your API will be available at http://localhost:8000/docs[/dim]")
        
        if enable_auth:
            console.print(f"\n[dim]🔐 Authentication: Use /api/v1/auth/register and /api/v1/auth/login endpoints[/dim]")

    except Exception as e:
        console.print(f"\n[red]❌ An error occurred while writing files: {e}[/red]")
        raise typer.Exit(code=1)


@app.command("config")
def configure_api_key():
    """
    Configure Google Gemini API key for Foxie.
    Saves the key to ~/.config/foxie/config.env for future use.
    """
    console.print(Panel.fit(
        "[bold cyan]🔑 Configure Foxie API Key[/bold cyan]\n"
        "Set up your Google Gemini API key",
        border_style="cyan"
    ))
    
    console.print("\n[cyan]Get your API key from:[/cyan]")
    console.print("[cyan]https://makersuite.google.com/app/apikey[/cyan]\n")
    
    api_key = getpass.getpass("🔑 Enter your Google Gemini API key (hidden): ")
    
    if not api_key:
        console.print("[red]❌ No API key provided[/red]")
        raise typer.Exit(code=1)
    
    # Save to ~/.config/foxie/config.env
    config_dir = get_config_path()
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = get_config_file()
    
    with open(config_file, "w") as f:
        f.write(f"GOOGLE_API_KEY={api_key}\n")
    
    console.print(f"\n[green]✓ API key saved to {config_file}[/green]")
    console.print("\n[dim]You can now use Foxie without entering your API key each time.[/dim]")


if __name__ == "__main__":
    app()
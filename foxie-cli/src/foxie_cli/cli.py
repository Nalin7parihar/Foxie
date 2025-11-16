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

# Assuming your file writer utility is here
from .utils.file_writer import write_files
# Assuming your Pydantic models for the response are here
from .core.models import GeneratedCode, CodeFile

# --- Configuration ---
# Define the URL of your backend service. Default is localhost.
BACKEND_URL = os.getenv("FOXIE_BACKEND_URL", "http://127.0.0.1:8000")

console = Console()
app = typer.Typer(
    name="foxie",
    help="🦊 A smart AI-powered code scaffolding CLI with Agentic Self-Correction"
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
    1. GOOGLE_API_KEY environment variable
    2. .env file in current directory
    3. ~/.foxie/.env file
    4. Prompt user to enter it
    
    Returns:
        API key string or None
    """
    # Check environment variable
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        console.print("[dim]✓ Using API key from environment[/dim]")
        return api_key
    
    # Check .env file in current directory
    env_file = Path(".env")
    if env_file.exists():
        from dotenv import dotenv_values
        config = dotenv_values(env_file)
        api_key = config.get("GOOGLE_API_KEY")
        if api_key:
            console.print("[dim]✓ Using API key from .env file[/dim]")
            return api_key
    
    # Check ~/.foxie/.env
    foxie_env = Path.home() / ".foxie" / ".env"
    if foxie_env.exists():
        from dotenv import dotenv_values
        config = dotenv_values(foxie_env)
        api_key = config.get("GOOGLE_API_KEY")
        if api_key:
            console.print("[dim]✓ Using API key from ~/.foxie/.env[/dim]")
            return api_key
    
    # Prompt user
    console.print("\n[yellow]⚠️  Google Gemini API Key Required[/yellow]")
    console.print("[dim]No API key found in environment or config files.[/dim]\n")
    
    console.print("[cyan]You can get your API key from:[/cyan]")
    console.print("[cyan]https://makersuite.google.com/app/apikey[/cyan]\n")
    
    api_key = getpass.getpass("🔑 Enter your Google Gemini API key (hidden): ")
    
    if api_key:
        # Offer to save it
        save_it = Confirm.ask("\n💾 Save this API key to ~/.foxie/.env for future use?", default=True)
        if save_it:
            foxie_dir = Path.home() / ".foxie"
            foxie_dir.mkdir(exist_ok=True)
            foxie_env = foxie_dir / ".env"
            
            with open(foxie_env, "w") as f:
                f.write(f"GOOGLE_API_KEY={api_key}\n")
            
            console.print(f"[green]✓ API key saved to {foxie_env}[/green]")
    
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
    
    protect_routes = False
    if enable_auth:
        protect_routes = Confirm.ask(
            "[yellow]Protect resource routes with authentication?[/yellow]",
            default=False
        )
    
    return {
        "project_name": project_name,
        "resource": resource,
        "fields": fields,
        "database_type": database_type,
        "enable_auth": enable_auth,
        "protect_routes": protect_routes,
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
    protect_routes: Annotated[bool, typer.Option(
        "--protect-routes",
        help="Protect resource routes with authentication (requires --enable-auth)"
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
        protect_routes = params["protect_routes"]
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
        
        # Validate protect_routes requires enable_auth
        if protect_routes and not enable_auth:
            console.print("[yellow]⚠️  Warning: --protect-routes requires --enable-auth. Ignoring --protect-routes.[/yellow]")
            protect_routes = False
    
    # Display summary
    console.print(f"\n[cyan]✨ Scaffolding Configuration:[/cyan]")
    console.print(f"  Project: [bold]{project_name}[/bold]")
    console.print(f"  Resource: [bold]{resource}[/bold]")
    console.print(f"  Fields: [bold]{fields}[/bold]")
    console.print(f"  Database: [bold]{database_type.upper()}[/bold]")
    console.print(f"  Authentication: [bold]{'✅ Enabled' if enable_auth else '❌ Disabled'}[/bold]")
    if enable_auth:
        console.print(f"  Protected Routes: [bold]{'✅ Yes' if protect_routes else '⚠️  No'}[/bold]")
    
    # --- Prepare API Request ---
    request_data = {
        "project_name": project_name,
        "resource": resource,
        "fields_str": fields,
        "database_type": database_type,
        "enable_auth": enable_auth,
        "protect_routes": protect_routes,
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
            response = requests.post(scaffold_endpoint, json=request_data, timeout=60) # 1 minute timeout
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
        console.print(f"\n[red]❌ Error: Request to backend timed out.[/red]")
        console.print("[yellow]    The AI generation is taking too long.[/yellow]")
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
        
        console.print(f"\n[bold bright_green]🎉 Successfully scaffolded project '{project_name}'![/bold bright_green]")
        
        # Show file count
        console.print(f"[green]📄 Generated {len(generated_code.files)} files[/green]")
        
        # --- Setup Instructions ---
        console.print("\n[bold cyan]📋 Next Steps:[/bold cyan]")

        # Build dependencies based on database type and auth
        base_deps = [
            "fastapi",
            "uvicorn[standard]",
            "pydantic",
            "pydantic-settings",
        ]
        
        if database_type == "sql":
            db_deps = [
                "sqlalchemy",
            ]
        else:  # mongodb
            db_deps = [
                "motor",
                "beanie",
            ]
        
        auth_deps = []
        if enable_auth:
            auth_deps = [
                "python-jose[cryptography]",
                "passlib[bcrypt]",
                "python-multipart",
            ]
        
        all_deps = base_deps + db_deps + auth_deps
        deps_str = ",\n    ".join([f'"{dep}"' for dep in all_deps])
        
        # Define the pyproject.toml content separately
        pyproject_content = f'''[project]
name = "{project_name}"
version = "0.1.0"
requires-python = ">=3.9"
dependencies = [
    {deps_str},
]

[tool.setuptools]
packages = ["app"]'''

        console.print(f"\n[bold]1. Navigate to your project:[/bold]")
        console.print(f"   [cyan]cd {project_name}[/cyan]")
        
        console.print(f"\n[bold]2. Create pyproject.toml with this content:[/bold]")
        console.print(Panel(pyproject_content, border_style="dim"))
        
        console.print(f"\n[bold]3. Setup environment:[/bold]")
        console.print(f"   [cyan]uv venv[/cyan]")
        console.print(f"   [cyan].venv\\Scripts\\activate[/cyan]  [dim](Windows)[/dim]")
        console.print(f"   [cyan]source .venv/bin/activate[/cyan]  [dim](Linux/macOS)[/dim]")
        
        console.print(f"\n[bold]4. Install dependencies:[/bold]")
        console.print(f"   [cyan]uv pip install -e .[/cyan]")
        
        # Database-specific setup instructions
        if database_type == "sql":
            console.print(f"\n[bold]5. Setup database:[/bold]")
            console.print(f"   [cyan]# For SQLite (default): No setup needed[/cyan]")
            console.print(f"   [cyan]# For PostgreSQL: Install and configure PostgreSQL[/cyan]")
            console.print(f"   [cyan]# Update DATABASE_URL in .env file[/cyan]")
        else:  # mongodb
            console.print(f"\n[bold]5. Setup MongoDB:[/bold]")
            console.print(f"   [cyan]# Install MongoDB locally or use MongoDB Atlas[/cyan]")
            console.print(f"   [cyan]# Update DATABASE_URL in .env file (mongodb://localhost:27017)[/cyan]")
        
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
    Saves the key to ~/.foxie/.env for future use.
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
    
    # Save to ~/.foxie/.env
    foxie_dir = Path.home() / ".foxie"
    foxie_dir.mkdir(exist_ok=True)
    foxie_env = foxie_dir / ".env"
    
    with open(foxie_env, "w") as f:
        f.write(f"GOOGLE_API_KEY={api_key}\n")
    
    console.print(f"\n[green]✓ API key saved to {foxie_env}[/green]")
    console.print("\n[dim]You can now use Foxie without entering your API key each time.[/dim]")


if __name__ == "__main__":
    app()
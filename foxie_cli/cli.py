import typer
from typing import Annotated
from foxie_cli.utils.parser import parse_fields
from foxie_cli.utils.file_writer import write_files
from foxie_cli.core.generator import generate_crud_feature


app = typer.Typer(help="Foxie CLI helping scaffold Project CLI")
scaffold_app = typer.Typer(name="scaffold",help="Scaffold FastAPI project with basic setup")

app.add_typer(scaffold_app)

@app.command()
def greet(
    name: Annotated[str, typer.Argument(help="Name to greet")]
):
    """Greet someone with a personalized message."""
    typer.echo(f"Hello {name}! I am foxie and I am here to help you scaffold FastAPI projects with necessary basic setup with the help of GenAI")

@scaffold_app.command("fastapi_crud",help="Scaffolds a full CRUD FastAPI application")
def fastapi_crud(
  project_name : Annotated[str,typer.Option("--project-name","-p",help="The name of the FastAPI project to be created.")],
  resource : Annotated[str,typer.Option("--resource","-r",help="The name of the resource, e.g., 'product', 'user'.")],
  fields : Annotated[str,typer.Option("--fields","-f",help="Comma-separated list of fields for the resource.")]
  
):
  typer.echo(f"Scaffolding FastAPI project '{project_name}' with resource '{resource}' and fields '{fields}'")
  try:
    
    parse_fields_str = parse_fields(fields)
    typer.secho("Parsed the fields successfully",fg=typer.colors.BRIGHT_GREEN)
    typer.echo(f"   -Field:{field.name} Type:{field.type}" for field in parse_fields_str)

  except ValueError as e:
    typer.secho(f"Error parsing fields: {e}", fg=typer.colors.BRIGHT_RED)
    raise typer.Exit(code=1)
  
  with typer.progressbar(length=100,label="Generating Code..") as progress:
    generated_code = generate_crud_feature(resource,fields_str=fields,project_name=project_name)
    progress.update(100)
    
  if not generated_code:
    typer.secho("Error: failed to generate code.", fg=typer.colors.BRIGHT_RED)
    raise typer.Exit(code=1)
  
  try:
      write_files(generated_code=generated_code)
  
  except Exception as e:
    typer.secho(f"Error writing files: {e}", fg=typer.colors.BRIGHT_RED)
    raise typer.Exit(code=1)

  typer.secho("\n🎉 Feature scaffolded successfully! 🎉",fg=typer.colors.BRIGHT_GREEN,bold=True)


if __name__ == "__main__":
    app()
  
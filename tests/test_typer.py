# test_typer.py
import typer

app = typer.Typer()

@app.command()
def hello(name: str):
    """
    Says hello.
    """
    print(f"Hello {name}")

if __name__ == "__main__":
    app()
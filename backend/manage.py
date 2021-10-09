import typer
import uvicorn

app = typer.Typer()


@app.command()
def up():
    """Start development uvicorn server"""
    typer.echo(f"Starting backend")
    from api import app

    uvicorn.run(app)


if __name__ == "__main__":
    app()

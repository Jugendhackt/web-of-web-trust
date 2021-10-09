import typer
import uvicorn

app = typer.Typer()


@app.command()
def up():
    """Start development uvicorn server"""
    typer.echo(f"Starting backend")
    from api import api

    uvicorn.run("api:api", debug=True, reload=True)


if __name__ == "__main__":
    app()

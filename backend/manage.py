import typer
import uvicorn

app = typer.Typer()


@app.command()
def up():
    """Start development uvicorn server"""
    from api.db.config import API_DEBUG, API_HOST, API_RELOAD, API_DEBUG, API_PORT

    typer.echo(
        f"""
Starting backend with:
Debugging: {API_DEBUG}
Host: {API_HOST}:{API_PORT}
Reload: {API_RELOAD}
"""
    )

    uvicorn.run(
        "api:api", host=API_HOST, port=API_PORT, debug=API_DEBUG, reload=API_RELOAD
    )


if __name__ == "__main__":
    app()

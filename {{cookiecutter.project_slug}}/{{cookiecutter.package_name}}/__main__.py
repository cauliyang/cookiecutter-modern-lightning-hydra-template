import typer 

app = typer.Typer()

@app.command()
def main():
    print("Hello from __main__")


if __name__ == "__main__":
    app()

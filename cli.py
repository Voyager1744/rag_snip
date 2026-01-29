import typer
from pathlib import Path

from core.config import Settings
from pipeline.build_store import build_store
from pipeline.qa import ask

app = typer.Typer()


@app.command()
def build(config: Path, pdf: Path):
    cfg = Settings(config)
    build_store(cfg, pdf)


@app.command()
def query(config: Path, question: str):
    cfg = Settings(config)
    result = ask(cfg, question)
    print(result.content)


if __name__ == "__main__":
    app()

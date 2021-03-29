import logging
import sys

import click
from rich.console import Console

from .analyzer import ResourcesAnalyzer
from .app import Application
from .reporting import Reporter
from .resources import ResourcesFetcher, ResourcesModifier

LIB_PROJECT_HELP = (
    "The path to the android project whose resources you want to inspect."
)
CLIENT_PROJECT_HELP = (
    "The path to the client android project that consumes the reference"
    " project resources"
)

logging.basicConfig(level=logging.INFO)


@click.command()
@click.option("--app-path", metavar="PATH", required=True, help=LIB_PROJECT_HELP)
@click.option("--client-path", metavar="PATH", required=False, help=CLIENT_PROJECT_HELP)
def launch(app_path, client_path):
    try:
        app = Application(
            resources_fetcher=ResourcesFetcher(),
            resources_modifier=ResourcesModifier(),
            analyzer=ResourcesAnalyzer(),
            reporter=Reporter(console=Console()),
        )
        app.execute(app_path=app_path, client_app_path=client_path)
        sys.exit(0)
    except Exception:
        logging.exception("Could not complete analysis.")
        sys.exit(1)

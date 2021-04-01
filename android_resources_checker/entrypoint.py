import logging
import sys

import click
from rich.console import Console

from .analyzer import ResourcesAnalyzer
from .app import Application
from .files import FilesHandler
from .reporting import Reporter
from .resources import ResourcesFetcher, ResourcesModifier

LIB_PROJECT_HELP = (
    "The path to the android project whose resources you want to inspect."
)
CLIENT_PROJECT_HELP = (
    "The path to the client android project that consumes the reference"
    " project resources"
)


@click.command()
@click.option(
    "--app",
    type=click.Path(resolve_path=True, exists=True, file_okay=False),
    required=True,
    help=LIB_PROJECT_HELP,
)
@click.option(
    "--client",
    type=click.Path(resolve_path=True, exists=True, file_okay=True),
    multiple=True,
    required=False,
    help=CLIENT_PROJECT_HELP,
)
def launch(app, client):
    try:
        application = Application(
            resources_fetcher=ResourcesFetcher(FilesHandler()),
            resources_modifier=ResourcesModifier(),
            analyzer=ResourcesAnalyzer(),
            reporter=Reporter(console=Console()),
        )
        application.execute(app_path=app, clients=client)
        sys.exit(0)
    except Exception:
        logging.exception("Could not complete analysis.")
        sys.exit(1)

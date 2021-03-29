import logging
import sys

import click
from rich.console import Console

from analyzer import ResourcesAnalyzer
from app import Application
from reporting import MetricsReporter
from resources import ResourcesFetcher, ResourcesModifier

LIB_PROJECT_HELP = "The path to the library android project that provides the resources."
CLIENT_PROJECT_HELP = "The path to the client android project that consumes the resources"

logging.basicConfig(level=logging.INFO)


@click.command()
@click.option("--lib-app", metavar="PATH", required=True, help=LIB_PROJECT_HELP)
@click.option("--client-app", metavar="PATH", required=True, help=CLIENT_PROJECT_HELP)
def launch(lib_app, client_app):
    try:
        app = Application(
            resources_fetcher=ResourcesFetcher(),
            resources_modifier=ResourcesModifier(),
            analyzer=ResourcesAnalyzer(),
            reporter=MetricsReporter(console=Console())
        )
        app.execute(client_app, lib_app)
        sys.exit(0)
    except Exception as error:
        logging.exception("Could not complete analysis.")
        sys.exit(1)

import logging
import sys

import click

from app import Application
from resources import ResourcesFetcher

LIB_PROJECT_HELP = "The path to the library android project that provides the resources."
CLIENT_PROJECT_HELP = "The path to the client android project that consumes the resources"

logging.basicConfig(level=logging.INFO)


@click.command()
@click.option("--lib-app", metavar="PATH", required=True, help=LIB_PROJECT_HELP)
@click.option("--client-app", metavar="PATH", required=True, help=CLIENT_PROJECT_HELP)
def launch(lib_app, client_app):
    try:
        app = Application(
            client_resources_fetcher=ResourcesFetcher(client_app),
            lib_resources_fetcher=ResourcesFetcher(lib_app)
        )
        app.execute()
        sys.exit(0)
    except Exception as error:
        logging.exception("Could not complete analysis.")
        sys.exit(1)

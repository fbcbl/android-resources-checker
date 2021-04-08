import logging
import sys

import click
from rich.console import Console

from .analyzer import ResourcesAnalyzer
from .app import Application
from .files import FilesHandler
from .reporting import Reporter, CsvAnalysisReporter, StdoutReporter
from .resources import ResourcesFetcher, ResourcesModifier
from .validator import Validator

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
@click.option(
    "--reports-dir",
    type=click.Path(resolve_path=True, exists=True, file_okay=False),
    required=False,
    default=".",
    help="The directory where the csv reports will be written.",
)
@click.option(
    "--check",
    is_flag=True,
    default=False,
    help="Using this flag will fail the execution if any unused resources are found",
)
@click.option(
    "--report",
    type=click.Choice(["CSV", "STDOUT"], case_sensitive=False),
    required=False,
)
@click.option(
    "--delete",
    is_flag=True,
    default=False,
    help="Using this flag will automatically delete the unused resources",
)
def launch(app, client, report, reports_dir, check, delete):
    try:
        console = Console()
        error_console = Console(stderr=True, style="bold red")

        stdout_reporter = StdoutReporter(console)
        csv_reporter = CsvAnalysisReporter(console, reports_dir)
        choice_reporters = {
            None: [stdout_reporter, csv_reporter],
            "CSV": [csv_reporter],
            "STDOUT": [stdout_reporter],
        }

        application = Application(
            resources_fetcher=ResourcesFetcher(FilesHandler()),
            resources_modifier=ResourcesModifier(),
            analyzer=ResourcesAnalyzer(),
            reporter=Reporter(console, error_console, choice_reporters[report]),
            validator=Validator(),
        )
        application.execute(app, client, check, delete)
        sys.exit(0)
    except Exception:
        logging.exception("Could not complete analysis.")
        sys.exit(1)

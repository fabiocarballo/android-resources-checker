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

REPORTS_DIR_HELP = "The directory where the csv reports will be written."


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
    default=None,
    help=REPORTS_DIR_HELP,
)
@click.option("--stdout/--no-stdout", default=True)
@click.option("--check/--no-check", default=False)
def launch(app, client, reports_dir, stdout, check):
    try:
        console = Console()
        error_console = Console(stderr=True, style="bold red")

        reporters = []
        if stdout:
            reporters.append(StdoutReporter(console))

        if reports_dir is not None:
            reporters.append(CsvAnalysisReporter(console, reports_dir))

        application = Application(
            resources_fetcher=ResourcesFetcher(FilesHandler()),
            resources_modifier=ResourcesModifier(),
            analyzer=ResourcesAnalyzer(),
            reporter=Reporter(console, error_console, reporters),
            validator=Validator(),
        )
        application.execute(app, client, check)
        sys.exit(0)
    except Exception:
        logging.exception("Could not complete analysis.")
        sys.exit(1)

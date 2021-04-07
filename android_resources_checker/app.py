import sys

from rich.console import Console
from rich.prompt import Confirm

from android_resources_checker.validator import UnusedResourcesException


class Application(object):
    def __init__(
        self, resources_fetcher, resources_modifier, analyzer, reporter, validator
    ):
        self.resources_fetcher = resources_fetcher
        self.resources_modifier = resources_modifier
        self.analyzer = analyzer
        self.reporter = reporter
        self.validator = validator

    def execute(self, app_path, clients, check):
        self.reporter.apps(app_path, clients)

        app_name = app_path.split("/")[-1]

        # fetch resources data
        console = Console()

        self.reporter.resources_processing_started()
        with console.status("[bold green]Processing project resources..."):
            packaged_resources = self.resources_fetcher.fetch_packaged_resources(
                app_path
            )
            console.log(f"{app_name} - packaged resources processed!")

            usage_references = self.resources_fetcher.fetch_used_resources(app_path)
            console.log(f"{app_name} - used resources processed!")
            for client in clients:
                client_app_name = client.split("/")[-1]
                usage_references = usage_references.union(
                    self.resources_fetcher.fetch_used_resources(client)
                )
                console.log(f"{client_app_name} - used resources processed!")

        # analyze data
        analysis = self.analyzer.analyze(
            app_path.split("/")[-1], usage_references, packaged_resources
        )

        # report
        self.reporter.reporting_started(analysis)
        self.reporter.report(analysis)

        # check
        if check:
            try:
                self.validator.validate(analysis)
            except UnusedResourcesException as e:
                paths = "\n".join([r.filepath for r in e.unused_resources])
                self.reporter.error(f"\nUnused Resources have been found!\n{paths}")
                sys.exit(1)

        # optional resource deletion
        delete_unused_resources = Confirm.ask("Delete unused resources?")
        if delete_unused_resources:
            resources_to_delete = set.union(*analysis.unused_resources.values())
            self.resources_modifier.delete_resources(resources_to_delete)
            self.reporter.deletion_completed(len(resources_to_delete))

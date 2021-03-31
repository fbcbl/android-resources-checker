from rich.console import Console
from rich.prompt import Confirm


class Application(object):
    def __init__(self, resources_fetcher, resources_modifier, analyzer, reporter):
        self.resources_fetcher = resources_fetcher
        self.resources_modifier = resources_modifier
        self.analyzer = analyzer
        self.reporter = reporter

    def execute(self, app_path, client_app_path=None):
        self.reporter.apps(client_app_path, app_path)

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

            if client_app_path is not None:
                client_app_name = client_app_path.split("/")[-1]
                usage_references = usage_references.union(
                    self.resources_fetcher.fetch_used_resources(client_app_path)
                )
                console.log(f"{client_app_name} - used resources processed!")

        # analyze data
        analysis = self.analyzer.analyze(
            app_path.split("/")[-1], usage_references, packaged_resources
        )

        # report
        self.reporter.report(analysis)

        # optional resource list visualization
        if Confirm.ask("Do you want to see the list of unused resources?"):
            self.reporter.report_unused_resources_list(analysis)

        # optional resource deletion
        delete_unused_resources = Confirm.ask("Delete unused resources?")
        if delete_unused_resources:
            resources_to_delete = set.union(*analysis.unused_resources.values())
            self.resources_modifier.delete_resources(resources_to_delete)
            self.reporter.deletion_completed(len(resources_to_delete))

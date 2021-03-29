from rich.console import Console
from rich.prompt import Confirm


class Application(object):

    def __init__(self, resources_fetcher, resources_modifier, analyzer, reporter):
        self.resources_fetcher = resources_fetcher
        self.resources_modifier = resources_modifier
        self.analyzer = analyzer
        self.reporter = reporter

    def execute(self, client_app_path, lib_app_path):
        self.reporter.apps(client_app_path, lib_app_path)

        lib_app_name = lib_app_path.split("/")[-1]
        client_app_name = client_app_path.split("/")[-1]

        # fetch resources data
        console = Console()
        self.reporter.resources_processing_started()
        with console.status("[bold green]Processing project resources...") as status:
            lib_packaged_res = self.resources_fetcher.fetch_packaged_resources(lib_app_path)
            console.log(f"{lib_app_name} - packaged resources processed!")

            lib_used_refs = self.resources_fetcher.fetch_used_resources(lib_app_path)
            console.log(f"{lib_app_name} - used resources processed!")

            client_used_refs = self.resources_fetcher.fetch_used_resources(client_app_path)
            console.log(f"{client_app_name} - used resources processed!")

        # analyze data
        analysis = self.analyzer.analyze(
            name=lib_app_path.split("/")[-1],
            client_used_refs=client_used_refs,
            lib_used_refs=lib_used_refs,
            lib_packaged_res=lib_packaged_res)

        # report
        self.reporter.report(analysis)

        # optional resource deletion
        delete_unused_resources = Confirm.ask("Delete unused resources?")
        if delete_unused_resources:
            resources_to_delete = set.union(*analysis.unused_resources.values())
            self.resources_modifier.delete_resources(resources_to_delete)
            self.reporter.deletion_completed(len(resources_to_delete))

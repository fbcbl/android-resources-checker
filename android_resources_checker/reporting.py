from rich.table import Table

from .models import ResourceType, AnalysisBreakdown


def _format_bytes(size):
    # 2**10 = 1024
    power = 2 ** 10
    n = 0
    power_labels = {0: "", 1: "kilo", 2: "mega", 3: "giga", 4: "tera"}
    while size > power:
        size /= power
        n += 1
    return f"{size:.2f} {str(power_labels[n])}bytes"


def _format_to_kb(size):
    return f"{size / 2 ** 10:.2f} kb"


class Reporter:
    def __init__(self, console):
        self.console = console
        self.output_delegate = StdoutReporter(console)

    def apps(self, client_app_path, lib_app_path):
        self.output_delegate.apps(client_app_path, lib_app_path)

    def deletion_completed(self, num_resources):
        self.console.print(f"{num_resources} resources deleted! :rocket:")

    def resources_processing_started(self):
        self.console.print("\n[bold]Resources processing started![/bold]")

    def report(self, breakdown):
        self.output_delegate.report(breakdown)

    def report_unused_resources_list(self, breakdown):
        self.output_delegate.report_unused_resources_list(breakdown)


class ContextReporter:
    def __init__(self, console):
        self.console = console

    def apps(self, client_app_path, lib_app_path):
        self.__print("Reference app", lib_app_path, "cyan")
        if client_app_path is not None:
            self.__print("Client app", client_app_path, "cyan")

    def __print(self, prefix, content, color):
        printer = self.console
        printer.print(f"{prefix} → [bold {color}]{content}[/bold {color}]")


class StdoutReporter(ContextReporter):
    def report(self, breakdown: AnalysisBreakdown):
        printer = self.console
        printer.print("\nAnalysis done with success!")

        printer.print(f"\nProject: [bold green]{breakdown.project_name}[/bold green]")
        printer.print(
            f"\nPotential size savings → {_format_bytes(breakdown.unused_size_bytes)}"
        )
        table = Table(show_header=True, header_style="bold magenta")
        table.pad_edge = False
        table.add_column("Resource Type")
        table.add_column("Num of used resources")
        table.add_column("Num of unused resources")

        for resource_type in ResourceType:
            rows = [
                resource_type.name,
                str(len(breakdown.used_resources[resource_type])),
                str(len(breakdown.unused_resources[resource_type])),
            ]
            table.add_row(*rows)

        printer.print(table)

    def report_unused_resources_list(self, breakdown):
        printer = self.console

        printer.print("\n[bold green]Unused Resources List[/bold green]")
        table = Table(show_header=True, header_style="bold magenta")
        table.pad_edge = False
        table.add_column("Resource Path")
        table.add_column("Resource Type")
        table.add_column("Resource Size")

        for grouped_resources in breakdown.unused_resources.values():
            sorted_resources = sorted(grouped_resources, key=lambda r: r.filepath)
            for package_resource in sorted_resources:
                rows = [
                    package_resource.filepath,
                    package_resource.resource.resource_type.name,
                    _format_to_kb(package_resource.size),
                ]
                table.add_row(*rows)

        printer.print(table)

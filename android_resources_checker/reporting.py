import csv

from rich.table import Table

from .models import ResourceType, AnalysisBreakdown, PackagingType

HEADER_RESOURCE_TYPE = "Resource Type"
HEADER_NUM_USED_RESOURCES = "Num used resources"
HEADER_NUM_UNUSED_RESOURCES = "Num unused resources"
HEADER_RESOURCE_NAME = "Resource Entry"
HEADER_RESOURCE_LOCATION = "Resource Location"
HEADER_RESOURCE_SIZE = "Resource Size"


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
    def __init__(self, console, error_console, reporters):
        self.console = console
        self.error_console = error_console
        self.reporters = reporters

    def apps(self, lib_app_path, clients):
        self.__print("Reference app", lib_app_path, "cyan")
        for client in clients:
            self.__print("Client app", client, "cyan")

    def deletion_completed(self, num_resources):
        self.console.print(f"{num_resources} resources deleted! :rocket:")

    def resources_processing_started(self):
        self.console.print("\n[bold]Processing:[/bold]")

    def reporting_started(self, breakdown):
        self.console.print("\n[bold]Reporting:[/bold]")
        self.console.print(
            f"\nProject: [bold green]{breakdown.project_name}[/bold green]"
        )
        self.console.print(
            f"\nPotential size savings → {_format_bytes(breakdown.unused_size_bytes)}"
        )

    def report(self, breakdown):
        for reporter in self.reporters:
            reporter.report(breakdown)
            reporter.report_unused_resources_list(breakdown)

    def error(self, error):
        self.error_console.print(error)

    def __print(self, prefix, content, color):
        printer = self.console
        printer.print(f"{prefix} → [bold {color}]{content}[/bold {color}]")


class AnalysisReporter:
    def __init__(self, console):
        self.console = console

    def report(self, breakdown: AnalysisBreakdown):
        pass

    def report_unused_resources_list(self, breakdown: AnalysisBreakdown):
        pass

    def _resources_usage_report_content(self, breakdown):
        content = [
            [
                HEADER_RESOURCE_TYPE,
                HEADER_NUM_USED_RESOURCES,
                HEADER_NUM_UNUSED_RESOURCES,
            ]
        ]
        for resource_type in sorted(ResourceType, key=lambda r: r.name):
            row = [
                resource_type.name,
                str(len(breakdown.used_resources.get(resource_type, []))),
                str(len(breakdown.unused_resources.get(resource_type, []))),
            ]
            content.append(row)

        return content

    def _resources_unused_resources_report_content(self, breakdown):
        content = [
            [HEADER_RESOURCE_NAME, HEADER_RESOURCE_LOCATION, HEADER_RESOURCE_SIZE]
        ]

        for grouped_resources in breakdown.unused_resources.values():
            sorted_resources = sorted(grouped_resources, key=lambda r: r.filepath)
            for r in sorted_resources:
                resource_entry = r.filepath
                if r.packaging_type is PackagingType.entry:
                    resource_entry += f" ({r.resource.name})"

                content.append(
                    [
                        f"R.{r.resource.resource_type.name}.{r.resource.name}",
                        r.filepath,
                        _format_to_kb(r.size),
                    ]
                )

        return content


class CsvAnalysisReporter(AnalysisReporter):
    def __init__(self, console, reports_dir):
        super().__init__(console)
        self.reports_dir = reports_dir

    def report(self, breakdown: AnalysisBreakdown):
        file = "resources_usage.csv"
        report_filepath = f"{self.reports_dir}/{file}"

        content = self._resources_usage_report_content(breakdown)

        with open(report_filepath, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=";")
            for row in content:
                csv_writer.writerow(row)

        self.console.log(f"Resources usage breakdown written in {report_filepath}")

    def report_unused_resources_list(self, breakdown: AnalysisBreakdown):
        file = "unused_resources.csv"
        report_filepath = f"{self.reports_dir}/{file}"

        content = self._resources_unused_resources_report_content(breakdown)

        csv_writer = csv.writer(open(report_filepath, "w", newline=""), delimiter=";")
        for row in content:
            csv_writer.writerow(row)

        self.console.log(f"Unused resources list written in {report_filepath}")


class StdoutReporter(AnalysisReporter):
    def report(self, breakdown: AnalysisBreakdown):
        printer = self.console
        printer.print("\n[bold green]Resources Usage[/bold green]")

        table = Table(show_header=True, header_style="bold magenta")
        table.pad_edge = False

        content = self._resources_usage_report_content(breakdown)

        for header in content[0]:
            table.add_column(header)

        for row in content[1:]:
            table.add_row(*row)

        printer.print(table)

    def report_unused_resources_list(self, breakdown):
        printer = self.console

        printer.print("\n[bold green]Unused Resources List[/bold green]")
        table = Table(show_header=True, header_style="bold magenta")
        table.pad_edge = False

        content = self._resources_unused_resources_report_content(breakdown)

        for header in content[0]:
            table.add_column(header)

        for row in content[1:]:
            table.add_row(*row)

        printer.print(table)

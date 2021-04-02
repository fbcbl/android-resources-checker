import csv
from typing import Any, Union

import pytest
from rich.console import Console, JustifyMethod, OverflowMethod
from rich.style import Style
from rich.table import Table

from android_resources_checker.models import (
    AnalysisBreakdown,
    ResourceType,
    PackagedResource,
    ResourceReference,
    PackagingType,
)
from android_resources_checker.reporting import (
    CsvAnalysisReporter,
    HEADER_RESOURCE_TYPE,
    HEADER_NUM_UNUSED_RESOURCES,
    HEADER_NUM_USED_RESOURCES,
    StdoutReporter,
    HEADER_RESOURCE_SIZE,
    HEADER_RESOURCE_LOCATION,
    HEADER_RESOURCE_NAME,
)


def _create_test_packaged_resource(
    name, type, packaging_type=PackagingType.file, size=10
):
    return PackagedResource(
        ResourceReference(name, type), packaging_type, f"path/to/{name}.xml", size
    )


def test_csv_report_usage_breakdown(tmpdir, breakdown_for_usage):
    # Arrange
    reports_dir = tmpdir.mkdir("reports")
    reporter = CsvAnalysisReporter(Console(), reports_dir)

    # Act
    reporter.report(breakdown_for_usage)

    # Assert
    expected_csv_files = [
        [HEADER_RESOURCE_TYPE, HEADER_NUM_USED_RESOURCES, HEADER_NUM_UNUSED_RESOURCES],
        ["anim", "0", "1"],
        ["color", "1", "0"],
        ["dimen", "0", "0"],
        ["drawable", "3", "2"],
        ["raw", "0", "0"],
        ["string", "0", "0"],
    ]
    file_lines = []
    with (open(f"{tmpdir}/reports/resources_usage.csv")) as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            file_lines.append(row)

    assert file_lines == expected_csv_files


def test_csv_report_unused_resources(tmpdir, breakdown_for_unused_resources_list):
    # Arrange
    reports_dir = tmpdir.mkdir("reports")
    reporter = CsvAnalysisReporter(Console(), reports_dir)

    # Act
    reporter.report_unused_resources_list(breakdown_for_unused_resources_list)

    # Assert
    expected_csv_files = [
        [HEADER_RESOURCE_NAME, HEADER_RESOURCE_LOCATION, HEADER_RESOURCE_SIZE],
        ["R.drawable.name1", "path/to/name1.xml", "1.95 kb"],
        ["R.drawable.name3", "path/to/name3.xml", "0.01 kb"],
        ["R.color.color1", "path/to/color1.xml", "0.00 kb"],
        ["R.color.color_selector", "path/to/color_selector.xml", "0.01 kb"],
        ["R.anim.anim1", "path/to/anim1.xml", "0.02 kb"],
    ]
    file_lines = []
    with (open(f"{tmpdir}/reports/unused_resources.csv")) as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            file_lines.append(row)

    assert file_lines == expected_csv_files


class FakeConsole(Console):
    def __init__(self):
        super().__init__()
        self.calls = []

    def print(
        self,
        *objects: Any,
        sep=" ",
        end="\n",
        style: Union[str, Style] = None,
        justify: JustifyMethod = None,
        overflow: OverflowMethod = None,
        no_wrap: bool = None,
        emoji: bool = None,
        markup: bool = None,
        highlight: bool = None,
        width: int = None,
        height: int = None,
        crop: bool = True,
        soft_wrap: bool = None,
    ) -> None:
        self.calls.append(*objects)


def test_stdout_unused_resources_list(breakdown_for_unused_resources_list):
    # Arrange
    console = FakeConsole()
    reporter = StdoutReporter(console)

    # Act
    reporter.report_unused_resources_list(breakdown_for_unused_resources_list)

    # Assert
    expected_table = Table(show_header=True, header_style="bold magenta")
    expected_table.pad_edge = True
    expected_table.add_column(HEADER_RESOURCE_NAME)
    expected_table.add_column(HEADER_RESOURCE_LOCATION)
    expected_table.add_column(HEADER_RESOURCE_SIZE)
    expected_table.add_row(*["R.drawable.name1", "path/to/name1.xml", "1.95 kb"])
    expected_table.add_row(*["R.drawable.name3", "path/to/name3.xml", "0.01 kb"])
    expected_table.add_row(*["R.color.color1", "path/to/color1.xml", "0.00 kb"])
    expected_table.add_row(
        *["R.color.color_selector", "path/to/color_selector.xml", "0.01 kb"]
    )
    expected_table.add_row(*["R.anim.anim1", "path/to/anim1.xml", "0.02 kb"])

    expected_stdout = [
        "\n[bold green]Unused Resources List[/bold green]",
        expected_table,
    ]

    assert console.calls[0] == expected_stdout[0]
    assert console.calls[1].columns == expected_stdout[1].columns
    assert console.calls[1].rows == expected_stdout[1].rows


def test_stdout_report_usage_breakdown(breakdown_for_usage):
    # Arrange
    console = FakeConsole()
    reporter = StdoutReporter(console)

    # Act
    reporter.report(breakdown_for_usage)

    # Assert
    expected_table = Table(show_header=True, header_style="bold magenta")
    expected_table.pad_edge = True
    expected_table.add_column(HEADER_RESOURCE_TYPE)
    expected_table.add_column(HEADER_NUM_USED_RESOURCES)
    expected_table.add_column(HEADER_NUM_UNUSED_RESOURCES)
    expected_table.add_row(*["anim", "0", "1"])
    expected_table.add_row(*["color", "1", "0"])
    expected_table.add_row(*["dimen", "0", "0"])
    expected_table.add_row(*["drawable", "3", "2"])
    expected_table.add_row(*["raw", "0", "0"])
    expected_table.add_row(*["string", "0", "0"])

    expected_stdout = ["\n[bold green]Resources Usage[/bold green]", expected_table]

    assert console.calls[0] == expected_stdout[0]
    assert console.calls[1].columns == expected_stdout[1].columns
    assert console.calls[1].rows == expected_stdout[1].rows


@pytest.fixture
def breakdown_for_usage():
    return AnalysisBreakdown(
        project_name="test-project",
        used_resources={
            ResourceType.drawable: {
                _create_test_packaged_resource("name1", ResourceType.drawable),
                _create_test_packaged_resource("name2", ResourceType.drawable),
                _create_test_packaged_resource("name3", ResourceType.drawable),
            },
            ResourceType.color: {
                _create_test_packaged_resource("color1", ResourceType.color)
            },
        },
        unused_resources={
            ResourceType.drawable: {
                _create_test_packaged_resource("name1", ResourceType.drawable),
                _create_test_packaged_resource("name3", ResourceType.drawable),
            },
            ResourceType.color: {},
            ResourceType.anim: {
                _create_test_packaged_resource("anim1", ResourceType.anim)
            },
        },
        unused_size_bytes=55,
    )


@pytest.fixture
def breakdown_for_unused_resources_list():
    return AnalysisBreakdown(
        project_name="test-project",
        used_resources={
            ResourceType.drawable: {
                _create_test_packaged_resource("name3", ResourceType.drawable),
            },
            ResourceType.color: {
                _create_test_packaged_resource("color1", ResourceType.color)
            },
        },
        unused_resources={
            ResourceType.drawable: {
                _create_test_packaged_resource(
                    "name1", ResourceType.drawable, size=2000
                ),
                _create_test_packaged_resource("name3", ResourceType.drawable, size=10),
            },
            ResourceType.color: {
                _create_test_packaged_resource(
                    "color1", ResourceType.color, PackagingType.entry, 1
                ),
                _create_test_packaged_resource(
                    "color_selector", ResourceType.color, PackagingType.file, 10
                ),
            },
            ResourceType.anim: {
                _create_test_packaged_resource(
                    "anim1", ResourceType.anim, PackagingType.file, 20
                )
            },
        },
        unused_size_bytes=55,
    )

import csv

from rich.console import Console

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
)


def _create_test_packaged_resource(
    name, type, packaging_type=PackagingType.file, size=10
):
    return PackagedResource(
        ResourceReference(name, type), packaging_type, f"path/to/{name}.xml", size
    )


def test_csv_report_usage_breakdown(tmpdir):
    # Arrange
    reports_dir = tmpdir.mkdir("reports")
    reporter = CsvAnalysisReporter(Console(), reports_dir)
    breakdown = AnalysisBreakdown(
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

    # Act
    reporter.report(breakdown)

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


def test_csv_report_unused_resources(tmpdir):
    # Arrange
    reports_dir = tmpdir.mkdir("reports")
    reporter = CsvAnalysisReporter(Console(), reports_dir)
    breakdown = AnalysisBreakdown(
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

    # Act
    reporter.report_unused_resources_list(breakdown)

    # Assert
    expected_csv_files = [
        ["Resource Entry", "Resource Location", "Resource Size"],
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

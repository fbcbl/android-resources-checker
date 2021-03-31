from android_resources_checker.analyzer import ResourcesAnalyzer
from android_resources_checker.models import (
    AnalysisBreakdown,
    ResourceReference,
    ResourceType,
    PackagedResource,
    PackagingType,
)


def _test_packaged_resource(
    index, resource_type, size=10, packaging_type=PackagingType.file
):
    name = f"{resource_type.name}_{index}"

    return PackagedResource(
        ResourceReference(name, resource_type), packaging_type, f"/path/{name}", size
    )


def test_analyze_resources_usage():
    # Given
    name = "test"
    color_0 = _test_packaged_resource(0, ResourceType.color)
    color_1 = _test_packaged_resource(1, ResourceType.color, size=25)
    color_2 = _test_packaged_resource(
        2,
        ResourceType.color,
    )
    drawable_0 = _test_packaged_resource(0, ResourceType.drawable, size=50)
    drawable_1 = _test_packaged_resource(1, ResourceType.drawable, size=55)
    drawable_2 = _test_packaged_resource(2, ResourceType.drawable, size=40)
    analyzer = ResourcesAnalyzer()

    # Act
    breakdown = analyzer.analyze(
        name=name,
        usage_references=[
            drawable_0.resource,
            color_0.resource,
            color_2.resource,
            drawable_2.resource,
        ],
        packaged_resources=[
            color_0,
            color_1,
            color_2,
            drawable_0,
            drawable_1,
            drawable_2,
        ],
    )

    # Assert
    expected_breakdown = AnalysisBreakdown(
        name,
        used_resources={
            ResourceType.anim: set(),
            ResourceType.color: {color_0, color_2},
            ResourceType.dimen: set(),
            ResourceType.drawable: {drawable_0, drawable_2},
            ResourceType.raw: set(),
            ResourceType.string: set(),
        },
        unused_resources={
            ResourceType.anim: set(),
            ResourceType.color: {color_1},
            ResourceType.dimen: set(),
            ResourceType.drawable: {drawable_1},
            ResourceType.raw: set(),
            ResourceType.string: set(),
        },
        unused_size_bytes=80,
    )

    assert breakdown == expected_breakdown

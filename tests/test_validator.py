import pytest

from android_resources_checker.models import (
    AnalysisBreakdown,
    ResourceType,
    PackagedResource,
    ResourceReference,
    PackagingType,
)
from android_resources_checker.validator import Validator, UnusedResourcesException


def test_validator_throws_exception_when_there_are_unused_resources():
    validator = Validator()

    analysis = AnalysisBreakdown(
        "proj-test",
        {},
        {
            ResourceType.drawable: {
                PackagedResource(
                    ResourceReference("resource", ResourceType.drawable),
                    PackagingType.entry,
                    "filepath/to/file",
                    10,
                )
            }
        },
        0,
    )

    with pytest.raises(UnusedResourcesException):
        validator.validate(analysis)


def test_validator_does_not_throw_exception_where_there_are_no_unused_resources():
    validator = Validator()

    analysis = AnalysisBreakdown("proj-test", {}, {ResourceType.drawable: set()}, 0)

    validator.validate(analysis)

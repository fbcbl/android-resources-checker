import os

from android_resources_checker.files import FilesHandler
from android_resources_checker.models import (
    PackagedResource,
    ResourceReference,
    ResourceType,
    PackagingType,
)
from android_resources_checker.resources import ResourcesFetcher
import xml.etree.ElementTree as ET

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class FakeFilesHandler(FilesHandler):
    def __init__(self, root_path, fake_config):
        self.root_path = root_path
        self.fake_config = fake_config

    def xml_files(self, root):
        if self.root_path == root:
            return self.fake_config.keys()
        else:
            return []

    def file_size(self, filepath):
        return self.fake_config[filepath]["size"]

    def file_content(self, filepath):
        return self.fake_config[filepath]["content"]

    def xml_tree(self, filepath):
        return self.fake_config[filepath]["xml_content"]


def test_fetch_packaged_resources():
    # Given
    fake_files_handler = FakeFilesHandler(
        "root",
        {
            "path/to/drawable/file1.xml": {
                "size": 10,
                "xml_content": ET.parse(f"{TEST_DIR}/fixtures/dummy-drawable.xml"),
            },
            "path/to/anim/file2.xml": {
                "size": 20,
                "xml_content": ET.parse(f"{TEST_DIR}/fixtures/dummy-anim.xml"),
            },
            "path/to/color/file3.xml": {
                "size": 30,
                "xml_content": ET.parse(f"{TEST_DIR}/fixtures/dummy-color.xml"),
            },
            "path/to/values/file4.xml": {
                "size": 40,
                "xml_content": ET.parse(f"{TEST_DIR}/fixtures/dummy-values-color.xml"),
            },
        },
    )
    resources_fetcher = ResourcesFetcher(fake_files_handler)

    # Act
    resources = resources_fetcher.fetch_packaged_resources("root")

    # Assert
    assert resources == {
        PackagedResource(
            ResourceReference("file1", ResourceType.drawable),
            PackagingType.file,
            "path/to/drawable/file1.xml",
            10,
        ),
        PackagedResource(
            ResourceReference("file2", ResourceType.anim),
            PackagingType.file,
            "path/to/anim/file2.xml",
            20,
        ),
        PackagedResource(
            ResourceReference("file3", ResourceType.color),
            PackagingType.file,
            "path/to/color/file3.xml",
            30,
        ),
        PackagedResource(
            ResourceReference("color_entry_0", ResourceType.color),
            PackagingType.entry,
            "path/to/values/file4.xml",
            0,
        ),
        PackagedResource(
            ResourceReference("color_entry_1", ResourceType.color),
            PackagingType.entry,
            "path/to/values/file4.xml",
            0,
        ),
    }


def test_fetch_used_resources():
    # Arrange
    fake_files_handler = FakeFilesHandler(
        "root",
        {
            "path/to/values/dummy-layout.xml": {
                "content": open(f"{TEST_DIR}/fixtures/dummy-layout.xml").readlines()
            }
        },
    )

    resources_fetcher = ResourcesFetcher(fake_files_handler)

    # Act
    references = resources_fetcher.fetch_used_resources("root")

    # Assert
    assert references == {
        ResourceReference("background_white", ResourceType.drawable),
        ResourceReference("spacing_small", ResourceType.dimen),
        ResourceReference("dummy_string", ResourceType.string),
        ResourceReference("red", ResourceType.color),
        ResourceReference("spacing_normal", ResourceType.dimen),
        ResourceReference("background_red", ResourceType.drawable),
        ResourceReference("file3", ResourceType.color),
        ResourceReference("spacing_large", ResourceType.dimen),
    }

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

    def java_kt_files(self, root):
        return [
            f
            for f in self.fake_config.keys()
            if f.endswith(".kt") or f.endswith(".java")
        ]

    def resource_files(self, root, extension="*"):
        if self.root_path == root:
            return [
                f
                for f in self.fake_config.keys()
                if extension == "*" or f.endswith(extension)
            ]
        else:
            return []

    def files_by_type(self, root, extension="*"):
        if self.root_path == root:
            return [
                f
                for f in self.fake_config.keys()
                if extension == "*" or f.endswith(extension)
            ]
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
            "path/to/raw/lottie.json": {"size": 500},
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
        PackagedResource(
            ResourceReference("lottie", ResourceType.raw),
            PackagingType.file,
            "path/to/raw/lottie.json",
            500,
        ),
    }


def test_fetch_used_resources():
    # Arrange
    fake_files_handler = FakeFilesHandler(
        "root",
        {
            "path/to/values/dummy-layout.xml": {
                "content": open(f"{TEST_DIR}/fixtures/dummy-layout.xml").readlines()
            },
            "path/to/dummy.kt": {
                "content": open(f"{TEST_DIR}/fixtures/dummy-class.kt").readlines()
            },
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
        ResourceReference("drawable_used_programatically", ResourceType.drawable),
        ResourceReference("programatic_1", ResourceType.color),
        ResourceReference("programatic_2", ResourceType.color),
    }


def test_styles_xml_usage_detection():
    # Arrange
    fake_files_handler = FakeFilesHandler(
        "root",
        {
            "path/to/values/dummy-styles.xml": {
                "content": open(f"{TEST_DIR}/fixtures/dummy-styles.xml").readlines()
            },
        },
    )

    resources_fetcher = ResourcesFetcher(fake_files_handler)

    # Act
    references = resources_fetcher.fetch_used_resources("root")

    # Assert
    expected_used_styles = {
        ResourceReference("BaseThemeA", ResourceType.style),
        ResourceReference("BaseThemeA.ThemeA", ResourceType.style),
        ResourceReference("BaseThemeB", ResourceType.style),
        ResourceReference("BaseThemeB.ThemeB", ResourceType.style),
        ResourceReference("BaseThemeC.BaseThemeD", ResourceType.style),
        ResourceReference("BaseThemeG", ResourceType.style),
        ResourceReference("BaseThemeG.ThemeG", ResourceType.style),
    }

    assert references == expected_used_styles


def test_styles_programatic_usage_detection():
    # Arrange
    fake_files_handler = FakeFilesHandler(
        "root",
        {
            "path/to/MyClass.kt": {
                "content": open(f"{TEST_DIR}/fixtures/dummy-styles.kt").readlines()
            },
        },
    )

    resources_fetcher = ResourcesFetcher(fake_files_handler)

    # Act
    references = resources_fetcher.fetch_used_resources("root")

    # Assert
    expected_used_styles = {
        ResourceReference("MyTheme.ThemeA.ThemeB", ResourceType.style),
        ResourceReference("OtherTheme", ResourceType.style),
    }

    assert references == expected_used_styles

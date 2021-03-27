import glob
import logging
import os
import re
from dataclasses import dataclass
from enum import Enum


class ResourceType(Enum):
    drawable = "drawable"


@dataclass(frozen=True)
class ResourceReference:
    name: str
    type: ResourceType


@dataclass(frozen=True)
class PackagedResource:
    resource: ResourceReference
    size: int


class ResourcesFetcher:

    def __init__(self, project_path):
        self.project_path = project_path

    def fetch_packaged_resources(self) -> set[PackagedResource]:
        logging.info("fetching resources for " + self.project_path)
        resources = set()

        for filepath in glob.glob(self.project_path + "/**/res/**", recursive=True):
            if re.match(".*/res/drawable/.*", filepath):
                logging.debug("-- found drawable: " + filepath)

                filename = filepath.split("/")[-1]  # extracting the 'filename.xml' or 'filename.png'
                drawable_name = "R.drawable." + filename.split(".")[0]
                drawable_size = os.stat(filepath).st_size

                resources.add(PackagedResource(ResourceReference(drawable_name, ResourceType.drawable), drawable_size))

        logging.info("Packaged resources count [" + self.project_path + "] => " + str(len(resources)))

        return resources

    def fetch_used_resources(self) -> set[ResourceReference]:
        resources = set()

        for filepath in glob.glob(self.project_path + "/**/*.xml", recursive=True):
            with open(filepath) as f:
                for line in f.readlines():
                    for result in re.finditer("@drawable/" + DRAWABLE_NAME_REGEX, line):
                        resource_reference = ResourceReference("R.drawable." + result.group().split("/")[-1], ResourceType.drawable)
                        resources.add(resource_reference)

        java_files = glob.glob(self.project_path + "/**/*.java", recursive=True)
        kotlin_files = glob.glob(self.project_path + "/**/*.kt", recursive=True)

        for filepath in (java_files + kotlin_files):
            with open(filepath) as f:
                for line in f.readlines():
                    for result in re.finditer("R.drawable." + DRAWABLE_NAME_REGEX, line):
                        resource_reference = ResourceReference(result.group(), ResourceType.drawable)
                        resources.add(resource_reference)

        logging.info("Used resources count [" + self.project_path + "] => " + str(len(resources)))

        return resources


DRAWABLE_NAME_REGEX = "[A-Za-z1-9_]+"

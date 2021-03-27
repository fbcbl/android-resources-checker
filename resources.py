import glob
import logging
import os
import re
from dataclasses import dataclass
from enum import Enum


class ResourceType(Enum):
    drawable = "drawable",
    color = "color",
    anim = "anim",
    raw = "raw"


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
            match = re.match(".*/res/(" + RESOURCES_OPTIONS + ").*/", filepath)
            if match is not None:
                logging.debug("-- found resource: " + filepath)

                filename = filepath.split("/")[-1]  # extracting the 'filename.xml' or 'filename.png'
                resource_name = filename.split(".")[0]
                print(resource_name)
                resource_type = match.groups()[0]
                resource_size = os.stat(filepath).st_size
                resource_ref = ResourceReference(resource_name, ResourceType[resource_type])

                resources.add(PackagedResource(resource_ref, resource_size))

        logging.info("Packaged resources count [" + self.project_path + "] => " + str(len(resources)))

        return resources

    def fetch_used_resources(self) -> set[ResourceReference]:
        resources = set()

        for filepath in glob.glob(self.project_path + "/**/*.xml", recursive=True):
            with open(filepath) as f:
                for line in f.readlines():
                    for result in re.finditer("@(" + RESOURCES_OPTIONS + ")/" + RESOURCE_NAME_REGEX, line):
                        resource_reference = ResourceReference(result.group().split("/")[-1],
                                                               ResourceType[result.groups()[0]])
                        resources.add(resource_reference)

        java_files = glob.glob(self.project_path + "/**/*.java", recursive=True)
        kotlin_files = glob.glob(self.project_path + "/**/*.kt", recursive=True)

        for filepath in (java_files + kotlin_files):
            with open(filepath) as f:
                for line in f.readlines():
                    for result in re.finditer("R.drawable." + RESOURCE_NAME_REGEX, line):
                        resource_reference = ResourceReference(result.group(), ResourceType.drawable)
                        resources.add(resource_reference)

        logging.info("Used resources count [" + self.project_path + "] => " + str(len(resources)))

        return resources


RESOURCE_NAME_REGEX = "[A-Za-z1-9_]+"
RESOURCES_OPTIONS = "drawable|color|anim|raw"

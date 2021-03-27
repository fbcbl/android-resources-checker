import glob
import logging
import os
import re

from models import ResourceReference, ResourceType, PackagedResource


class ResourcesFetcher:

    def fetch_packaged_resources(self, project_path) -> set[PackagedResource]:
        logging.info("fetching resources for " + project_path)
        resources = set()

        for filepath in glob.glob(project_path + "/**/res/**", recursive=True):
            match = re.match(".*/res/(" + RESOURCES_OPTIONS + ").*/", filepath)
            if match is not None:
                logging.debug("-- found resource: " + filepath)

                filename = filepath.split("/")[-1]  # extracting the 'filename.xml' or 'filename.png'
                resource_name = filename.split(".")[0]
                resource_type = match.groups()[0]
                resource_size = os.stat(filepath).st_size
                resource_ref = ResourceReference(resource_name, ResourceType[resource_type])

                resources.add(PackagedResource(resource_ref, resource_size))

        logging.info("Packaged resources count [" + project_path + "] => " + str(len(resources)))

        return resources

    def fetch_used_resources(self, project_path) -> set[ResourceReference]:
        resources = set()

        for filepath in glob.glob(project_path + "/**/*.xml", recursive=True):
            with open(filepath) as f:
                for line in f.readlines():
                    for result in re.finditer("@(" + RESOURCES_OPTIONS + ")/" + RESOURCE_NAME_REGEX, line):
                        resource_reference = ResourceReference(result.group().split("/")[-1],
                                                               ResourceType[result.groups()[0]])
                        resources.add(resource_reference)

        java_files = glob.glob(project_path + "/**/*.java", recursive=True)
        kotlin_files = glob.glob(project_path + "/**/*.kt", recursive=True)

        for filepath in (java_files + kotlin_files):
            with open(filepath) as f:
                for line in f.readlines():
                    for result in re.finditer("R.drawable." + RESOURCE_NAME_REGEX, line):
                        resource_reference = ResourceReference(result.group(), ResourceType.drawable)
                        resources.add(resource_reference)

        logging.info("Used resources count [" + project_path + "] => " + str(len(resources)))

        return resources


RESOURCE_NAME_REGEX = "[A-Za-z1-9_]+"
RESOURCES_OPTIONS = "drawable|color|anim|raw"

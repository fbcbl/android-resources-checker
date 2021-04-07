import os
import re

from typing import Set

from .models import ResourceReference, ResourceType, PackagedResource, PackagingType


class ResourcesFetcher:
    def __init__(self, files_handler):
        self.files_handler = files_handler

    def fetch_packaged_resources(self, project_path) -> Set[PackagedResource]:
        resource_files = self.files_handler.resource_files(project_path)
        xml_files = [f for f in resource_files if f.endswith(".xml")]

        file_resources = self._extract_file_resources(resource_files)
        entry_resources = self._extract_entry_resources(xml_files)

        return file_resources.union(file_resources.union(entry_resources))

    def _extract_entry_resources(self, xml_files):
        resources = set()
        for filepath in xml_files:
            tree = self.files_handler.xml_tree(filepath)
            entry_resource_types = ["dimen", "string", "color", "style"]
            for resource_type in entry_resource_types:
                for entry in tree.findall(resource_type):
                    resources.add(
                        PackagedResource(
                            resource=ResourceReference(
                                entry.get("name"), ResourceType[resource_type]
                            ),
                            filepath=filepath,
                            size=0,
                            packaging_type=PackagingType.entry,
                        )
                    )

        return resources

    def _extract_file_resources(self, resource_files):
        resources = set()
        for filepath in resource_files:
            match = re.match(".*/(" + RESOURCES_OPTIONS + ").*/", filepath)
            if match is not None:
                filename = filepath.split("/")[-1]
                resource_name = filename.split(".")[0]
                resource_type = match.groups()[0]
                resource_size = self.files_handler.file_size(filepath)
                resource_ref = ResourceReference(
                    resource_name, ResourceType[resource_type]
                )

                resources.add(
                    PackagedResource(
                        resource=resource_ref,
                        filepath=filepath,
                        size=resource_size,
                        packaging_type=PackagingType.file,
                    )
                )

        return resources

    def fetch_used_resources(self, project_path) -> Set[ResourceReference]:
        resources = set()

        xml_regex = "@(" + RESOURCES_OPTIONS + ")/" + RESOURCE_NAME_REGEX
        for filepath in self.files_handler.files_by_type(project_path, extension="xml"):
            # look-up for styles
            styles_references = self._style_usages_in_xml(filepath)
            resources = resources.union(styles_references)

            for line in self.files_handler.file_content(filepath):
                for result in re.finditer(xml_regex, line):
                    resource_reference = ResourceReference(
                        result.group().split("/")[-1],
                        ResourceType[result.groups()[0]],
                    )
                    resources.add(resource_reference)

        code_regex = r"R\.(" + RESOURCES_OPTIONS + r")\." + RESOURCE_NAME_REGEX
        for filepath in self.files_handler.java_kt_files(project_path):
            for line in self.files_handler.file_content(filepath):
                for result in re.finditer(code_regex, line):
                    resource_split = result.group().split(".")
                    resource_type = ResourceType[resource_split[1]]
                    resource_name = (
                        resource_split[-1]
                        if resource_type is not ResourceType.style
                        else resource_split[-1].replace("_", ".")
                    )

                    resource_reference = ResourceReference(resource_name, resource_type)
                    resources.add(resource_reference)

        return resources

    def _style_usages_in_xml(self, filepath):
        usages = set()

        style_usage_regexes = [
            # <item name="theme">@style/MyStyle</item>
            r"@style/([A-Za-z\.]+)",
            # <style name="OtherThemeB" parent="BaseThemeB.OtherTheme"/>
            r'parent="([A-Za-z\.]+)"',
            # <style name="OtherThemeB.OtherThemeC.OtherThemeD" />
            r'style name="([A-Za-z\.]+)\..*"',
        ]

        for line in self.files_handler.file_content(filepath):
            for regex in style_usage_regexes:
                match = re.search(regex, line)
                if match is not None:
                    usages.add(ResourceReference(match.groups()[0], ResourceType.style))

        return usages


class ResourcesModifier:
    def delete_resources(self, resources_list):
        for packaged_resource in resources_list:
            if packaged_resource.packaging_type is PackagingType.file:
                os.remove(packaged_resource.resource.filepath)
            else:
                self._delete_resource_entry(packaged_resource)

    def _delete_resource_entry(self, packaged_resource):
        entry_regex = f'.*name="{packaged_resource.resource.name}".*'

        with open(packaged_resource.filepath, "r") as infile:
            lines = infile.readlines()

            with open(packaged_resource.filepath, "w") as outfile:
                for line in lines:
                    if re.match(entry_regex, line) is None:
                        outfile.write(line)


RESOURCE_NAME_REGEX = "[A-Za-z0-9_]+"
RESOURCES_OPTIONS = "|".join([r.name for r in ResourceType])

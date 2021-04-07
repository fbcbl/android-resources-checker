class Validator:
    def validate(self, analysis):
        all_unused_resources = []
        for unused_resources in analysis.unused_resources.values():
            for resource in unused_resources:
                all_unused_resources.append(resource)

        if len(all_unused_resources) > 0:
            raise UnusedResourcesException(all_unused_resources)


class UnusedResourcesException(Exception):
    def __init__(self, unused_resources):
        self.unused_resources = unused_resources

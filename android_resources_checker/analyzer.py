# analyzer.py
from typing import Dict, Set

from .models import AnalysisBreakdown, ResourceType, PackagedResource


class ResourcesAnalyzer:
    def _create_breakdown(
        self, resources_list
    ) -> Dict[ResourceType, Set[PackagedResource]]:
        breakdown = {}
        for resource_type in ResourceType:
            resources_of_type = set(
                [
                    pr
                    for pr in resources_list
                    if pr.resource.resource_type == resource_type
                ]
            )
            breakdown[resource_type] = resources_of_type

        return dict(sorted(breakdown.items(), key=lambda item: item[0].name))

    def analyze(self, name, usage_references, packaged_resources) -> AnalysisBreakdown:
        used_packaged_resources = []
        unused_packaged_resources = []

        for pr in packaged_resources:
            if pr.resource in usage_references:
                used_packaged_resources.append(pr)
            else:
                unused_packaged_resources.append(pr)

        return AnalysisBreakdown(
            project_name=name,
            used_resources=self._create_breakdown(used_packaged_resources),
            unused_resources=self._create_breakdown(unused_packaged_resources),
            unused_size_bytes=sum([pr.size for pr in unused_packaged_resources]),
        )

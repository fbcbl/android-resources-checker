from models import AnalysisBreakdown, ResourceType, PackagedResource


class ResourcesAnalyzer:

    def _create_breakdown(self, resources_list) -> dict[ResourceType, set[PackagedResource]]:
        breakdown = {}
        for resource_type in ResourceType:
            resources_of_type = set([pr for pr in resources_list
                                     if pr.resource.type == resource_type])
            breakdown[resource_type] = resources_of_type

        return breakdown

    def analyze(self, name, client_used_refs, app_used_refs, app_packaged_res) -> AnalysisBreakdown:
        app_packaged_refs = [r.resource for r in app_packaged_res]
        app_public_refs = [r for r in app_packaged_refs if r not in app_used_refs]
        app_unused_refs = [r for r in app_public_refs if r not in client_used_refs]

        app_used_packaged_res = [pr for pr in app_packaged_res if pr.resource in app_used_refs]
        app_unused_packaged_res = [pr for pr in app_packaged_res if pr.resource in app_unused_refs]

        return AnalysisBreakdown(
            project_name=name,
            used_resources=self._create_breakdown(app_used_packaged_res),
            unused_resources=self._create_breakdown(app_unused_packaged_res),
            unused_size_bytes=sum([pr.size for pr in app_unused_packaged_res])
        )

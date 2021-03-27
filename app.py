from resources import PackagedResource


def _format_bytes(size):
    # 2**10 = 1024
    power = 2 ** 10
    n = 0
    power_labels = {0: '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
    while size > power:
        size /= power
        n += 1
    return str(size) + " " + str(power_labels[n]) + "bytes"


class Application(object):

    def __init__(self, client_resources_fetcher, lib_resources_fetcher):
        self.client_resources_fetcher = client_resources_fetcher
        self.lib_resources_fetcher = lib_resources_fetcher

    def execute(self):
        lib_packaged_resources: list[PackagedResource] = self.lib_resources_fetcher.fetch_packaged_resources()

        client_used_res_refs = self.client_resources_fetcher.fetch_used_resources()
        lib_used_res_refs = self.lib_resources_fetcher.fetch_used_resources()
        lib_packaged_resource_refs = [r.resource for r in lib_packaged_resources]

        lib_public_resources = [r for r in lib_packaged_resource_refs if r not in lib_used_res_refs]

        lib_unused_res = [r for r in lib_public_resources if r not in client_used_res_refs]
        print(len(lib_unused_res))
        lib_unused_packaged_res = [pr for pr in lib_packaged_resources if pr.resource in lib_unused_res]
        for pr in lib_unused_packaged_res:
            print(pr)
        print(len(lib_unused_packaged_res))
        total_size = sum([pr.size for pr in lib_unused_packaged_res])
        print(_format_bytes(total_size))

from resources import Resources


class Application(object):

    def __init__(self, client_resources_fetcher, lib_resources_fetcher):
        self.client_resources_fetcher = client_resources_fetcher
        self.lib_resources_fetcher = lib_resources_fetcher

    def execute(self):
        client_used_resources = self.client_resources_fetcher.fetch_used_resources()

        lib_packaged_resources = self.lib_resources_fetcher.fetch_packaged_resources()
        lib_used_resources = self.lib_resources_fetcher.fetch_used_resources()

        lib_public_resources = lib_packaged_resources.difference(lib_used_resources)
        print(len(lib_public_resources.drawables))

        lib_unused_resources = lib_public_resources.difference(client_used_resources)
        print(len(lib_unused_resources.drawables))

        for drawable in lib_unused_resources.drawables:
            print(drawable)
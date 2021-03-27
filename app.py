class Application(object):

    def __init__(self, resources_fetcher, analyzer, reporter):
        self.resources_fetcher = resources_fetcher
        self.analyzer = analyzer
        self.reporter = reporter

    def execute(self, client_app_path, lib_app_path):
        self.reporter.apps(client_app_path, lib_app_path)

        # fetch resources data
        lib_packaged_res = self.resources_fetcher.fetch_packaged_resources(lib_app_path)
        client_used_refs = self.resources_fetcher.fetch_used_resources(client_app_path)
        lib_used_refs = self.resources_fetcher.fetch_used_resources(lib_app_path)

        # analyze data
        analysis = self.analyzer.analyze(
            name=lib_app_path.split("/")[-1],
            client_used_refs=client_used_refs,
            lib_used_refs=lib_used_refs,
            lib_packaged_res=lib_packaged_res)

        # report
        self.reporter.report(analysis)

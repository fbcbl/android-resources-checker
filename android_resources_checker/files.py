import glob
import os
import xml.etree.ElementTree


class FilesHandler:
    def resource_files(self, root, extension="*"):
        return glob.glob(f"{root}/**/res/**/*.{extension}", recursive=True)

    def files_by_type(self, root, extension="*"):
        return glob.glob(f"{root}/**/*.{extension}", recursive=True)

    def java_kt_files(self, root):
        java_files = glob.glob(root + "/**/*.java", recursive=True)
        kotlin_files = glob.glob(root + "/**/*.kt", recursive=True)

        return java_files + kotlin_files

    def file_size(self, filepath):
        return os.stat(filepath).st_size

    def file_content(self, filepath):
        return open(filepath).readlines()

    def xml_tree(self, xml_filepath):
        return xml.etree.ElementTree.parse(xml_filepath)

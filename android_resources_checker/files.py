import glob
import os
import xml.etree.ElementTree


class FilesHandler:
    def xml_files(self, root):
        return glob.glob(root + "/**/res/**/*.xml", recursive=True)

    def file_size(self, filepath):
        return os.stat(filepath).st_size

    def xml_tree(self, xml_filepath):
        return xml.etree.ElementTree.parse(xml_filepath)

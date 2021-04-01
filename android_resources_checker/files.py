import glob
import os
import xml.etree.ElementTree


class FilesHandler:
    def xml_files(self, root):
        return glob.glob(root + "/**/res/**/*.xml", recursive=True)

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
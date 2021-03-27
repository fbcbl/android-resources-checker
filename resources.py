import glob
import logging
import re
from dataclasses import dataclass


@dataclass
class Resources:
    drawables: set[str]

    def difference(self, other):
        if isinstance(other, Resources):
            return Resources(
                drawables=self.drawables.difference(other.drawables)
            )
        else:
            return self


class ResourcesFetcher:

    def __init__(self, project_path):
        self.project_path = project_path

    def fetch_packaged_resources(self) -> Resources:
        logging.info("fetching resources for " + self.project_path)
        drawables = set()
        for filepath in glob.glob(self.project_path + "/**/res/**", recursive=True):
            if re.match(".*/res/drawable/.*", filepath):
                filename = filepath.split("/")[-1]  # extracting the 'filename.xml' or 'filename.png'
                drawable_name = "R.drawable." + filename.split(".")[0]
                logging.debug("-- found drawable: " + drawable_name)
                drawables.add(drawable_name)

        logging.info("Packaged drawables count [" + self.project_path + "] => " + str(len(drawables)))

        return Resources(
            drawables=drawables
        )

    def fetch_used_resources(self) -> Resources:
        drawables = set()

        for filepath in glob.glob(self.project_path + "/**/*.xml", recursive=True):
            with open(filepath) as f:
                for line in f.readlines():
                    for result in re.finditer("@drawable/" + DRAWABLE_NAME_REGEX, line):
                        drawables.add("R.drawable." + result.group().split("/")[-1])

        java_files = glob.glob(self.project_path + "/**/*.java", recursive=True)
        kotlin_files = glob.glob(self.project_path + "/**/*.kt", recursive=True)

        for filepath in (java_files + kotlin_files):
            with open(filepath) as f:
                for line in f.readlines():
                    for result in re.finditer("R.drawable." + DRAWABLE_NAME_REGEX, line):
                        drawables.add(result.group())

        logging.info("Used drawables count [" + self.project_path + "] => " + str(len(drawables)))

        return Resources(
            drawables=drawables
        )


DRAWABLE_NAME_REGEX = "[A-Za-z1-9_]+"

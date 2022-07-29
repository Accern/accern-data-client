import os
import re
import xml.etree.ElementTree as ET


def merge_results(base_folder: str) -> None:
    xml_file_pattern = re.compile(r".*.xml")
    xml_files = sorted(os.listdir(os.path.join(base_folder, "parts")))

    testsuites = ET.Element("testsuites")
    combined = ET.SubElement(testsuites, "testsuite")
    failures = 0
    skipped = 0
    tests = 0
    errors = 0
    time = 0.0
    for file_name in xml_files:
        if xml_file_pattern.match(file_name):
            tree = ET.parse(os.path.join(base_folder, "parts", file_name))
            test_suite = list(tree.getroot())[0]

            combined.attrib["name"] = test_suite.attrib["name"]
            combined.attrib["timestamp"] = test_suite.attrib["timestamp"]
            combined.attrib["hostname"] = test_suite.attrib["hostname"]
            failures += int(test_suite.attrib["failures"])
            skipped += int(test_suite.attrib["skipped"])
            tests += int(test_suite.attrib["tests"])
            errors += int(test_suite.attrib["errors"])
            for testcase in list(test_suite):
                time += float(testcase.attrib["time"])
                ET.SubElement(combined, testcase.tag, testcase.attrib)

    combined.attrib["failures"] = f"{failures}"
    combined.attrib["skipped"] = f"{skipped}"
    combined.attrib["tests"] = f"{tests}"
    combined.attrib["errors"] = f"{errors}"
    combined.attrib["time"] = f"{time}"

    new_tree = ET.ElementTree(testsuites)
    new_tree.write(
        os.path.join(base_folder, "results.xml"),
        xml_declaration=True,
        encoding="utf-8")




import os
import re
import xml.etree.ElementTree as ET
from collections import defaultdict
from typing import Dict, List, Tuple

XML_FILE_PATTERN = re.compile(r".*\.xml")
TEST_FILE_PATTERN = re.compile(r"^test_.*\.py$")
DEFAULT_TEST_DURATION = 10.0


def find_tests(directory: str) -> List[str]:
    items = os.listdir(directory)
    test_files = []
    for item in items:
        if not os.path.isdir(item) and TEST_FILE_PATTERN.match(item):
            test_files.append(os.path.join(directory, item))
    return test_files


def merge_results(base_folder: str, out_filename: str = "result.xml") -> None:
    xml_files = sorted(os.listdir(os.path.join(base_folder, "parts")))

    testsuites = ET.Element("testsuites")
    combined = ET.SubElement(testsuites, "testsuite")
    failures = 0
    skipped = 0
    tests = 0
    errors = 0
    time = 0.0
    for file_name in xml_files:
        if XML_FILE_PATTERN.match(file_name):
            tree = ET.parse(os.path.join(base_folder, "parts", file_name))
            test_suite = tree.getroot()[0]

            combined.attrib["name"] = test_suite.attrib["name"]
            combined.attrib["timestamp"] = test_suite.attrib["timestamp"]
            combined.attrib["hostname"] = test_suite.attrib["hostname"]
            failures += int(test_suite.attrib["failures"])
            skipped += int(test_suite.attrib["skipped"])
            tests += int(test_suite.attrib["tests"])
            errors += int(test_suite.attrib["errors"])
            for testcase in test_suite:
                time += float(testcase.attrib["time"])
                ET.SubElement(combined, testcase.tag, testcase.attrib)

    combined.attrib["failures"] = f"{failures}"
    combined.attrib["skipped"] = f"{skipped}"
    combined.attrib["tests"] = f"{tests}"
    combined.attrib["errors"] = f"{errors}"
    combined.attrib["time"] = f"{time}"

    new_tree = ET.ElementTree(testsuites)
    new_tree.write(
        os.path.join(base_folder, out_filename),
        xml_declaration=True,
        encoding="utf-8")


def split_tests(filepath: str, total_nodes: int, cur_node: int) -> None:
    _, fname = os.path.split(filepath)
    if XML_FILE_PATTERN.match(fname):
        test_files = find_tests("tests")
        try:
            tree = ET.parse(filepath)
            test_time_map: Dict[str, float] = defaultdict(int)
            for testcases in tree.getroot()[0]:
                classname = testcases.attrib["classname"].replace(
                    ".", os.path.sep)
                test_time_map[classname] += float(testcases.attrib["time"])

            for file in test_files:
                if file not in test_time_map.keys():
                    test_time_map[file] = DEFAULT_TEST_DURATION

            time_keys: List[Tuple[str, float]] = sorted(
                test_time_map.items(), key=lambda el: el[1], reverse=True)
        except FileNotFoundError:
            time_keys = [(file, DEFAULT_TEST_DURATION) for file in test_files]

        def find_lowest_total_time(
                    test_sets: List[Tuple[List[str], float]]) -> int:
            minimum = None
            idx = -1
            for ix, val in enumerate(test_sets):
                if minimum is None or val[1] < minimum:
                    minimum = val[1]
                    idx = ix
            return idx

        test_sets: List[Tuple[List[str], float]] = [
            ([], 0.0) for _ in range(total_nodes)]
        for key, timing in time_keys:
            ix = find_lowest_total_time(test_sets)
            lowest_list, lowest_time = test_sets[ix]
            test_sets[ix] = (lowest_list + [key], lowest_time + timing)
        print(','.join(test_sets[cur_node][0]))
    else:
        raise TypeError(f"File {fname} is not a valid xml file.")

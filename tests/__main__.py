import argparse

from tests.utils import split_tests


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Accern Data Client Utilities")
    parser.add_argument(
        "--filepath",
        default="test-results/results.xml",
        type=str,
        help=(
            "The location for timings of all test cases. "
            "Must be an xml file."))

    parser.add_argument(
        "--total-nodes",
        type=int,
        help=("The total number of nodes/machines to allocate tests to."))
    parser.add_argument(
        "--node-id",
        type=int,
        help=(
            "Current node/machine id for which you want to get the set of "
            "testcases to run. "))
    return parser.parse_args()


def run() -> None:
    args = parse_args()
    split_tests(
        filepath=args.filepath,
        total_nodes=args.total_nodes,
        cur_node=args.node_id)


if __name__ == "__main__":
    run()

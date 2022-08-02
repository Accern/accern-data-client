import argparse

from tests.utils import merge_results, split_tests


def parse_args_split_tests(parser: argparse.ArgumentParser) -> None:
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


def parse_args_merge_results(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--dir",
        default="test-results",
        type=str,
        help=(
            "Directory inside which there is a folder named 'parts' "
            "containing all the xml files to join."))
    parser.add_argument(
        "--out-fname",
        type=str,
        help=("Name of combined xml file to be outputted."))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Accern Data Client Utilities")
    subparser = parser.add_subparsers(title="Commands")

    subparses_split_tests = subparser.add_parser("split_tests")
    subparses_split_tests.set_defaults(
        func=lambda args: split_tests(
            filepath=args.filepath,
            total_nodes=args.total_nodes,
            cur_node=args.node_id))
    parse_args_split_tests(subparses_split_tests)

    subparses_merge_results = subparser.add_parser("merge_results")
    subparses_merge_results.set_defaults(
        func=lambda args: merge_results(
            base_folder=args.dir,
            out_filename=args.out_fname))
    parse_args_merge_results(subparses_merge_results)
    return parser.parse_args()


def run() -> None:
    args = parse_args()
    args.func(args)


if __name__ == "__main__":
    run()

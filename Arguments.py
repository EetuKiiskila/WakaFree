import argparse


def initialize_parser() -> argparse.ArgumentParser:
    """Initialize argparse parser.

    :return: Argument parser.
    """
    parser = argparse.ArgumentParser(description="You can use this program to show your statistics from WakaTime.",
                                     usage=("python WakaFree.py {-h | -G | [-g GRAPHS] [-t TOTALS]"
                                            " [{-i IGNORE | -s SEARCH}] [-m MINIMUM_LABELING_PERCENTAGE]"
                                            " [--start-date START_DATE] [--end-date END_DATE] FILE}"))

    parser.add_argument("file", metavar="FILE", nargs="?", default="", help="path to file with statistics")
    parser.add_argument("-G", "--gui", action="store_true", help="use graphical user interface")
    parser.add_argument("-g", "--graphs",
                        help="show daily statistics: string with l, e, o for languages, editors, operating systems")
    parser.add_argument("-t", "--totals",
                        help="show total times: string with l, e, o for languages, editors, operating systems")
    parser.add_argument("-i", "--ignore", help="ignored stats: string with labels separated by commas (without spaces)")
    parser.add_argument("-s", "--search",
                        help="stats to search for: string with labels separated by commas (without spaces)")
    parser.add_argument("-m", "--minimum-labeling-percentage",
                        help="add together (under label Other) stats with lesser percentage than the given value")
    parser.add_argument("--start-date", help="start date in format YYYY-MM-DD (inclusive)")
    parser.add_argument("--end-date", help="end date in format YYYY-MM-DD (inclusive)")

    return parser

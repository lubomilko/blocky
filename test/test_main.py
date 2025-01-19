from test_common import compare_files
from test_basics import run_test_basics
from test_report import run_test_report


def main() -> None:
    run_test_basics("templates/basics.txt", "generated/basics.txt")
    run_test_report("templates/report.rst", "generated/report.rst", "data/report.json")

    compare_files("generated/basics.txt", "expected/basics.txt")
    compare_files("generated/report.rst", "expected/report.rst")


if __name__ == "__main__":
    main()

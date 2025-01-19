import sys
from pathlib import Path


sys.path.insert(0, str(Path(Path(__file__).parent.parent, "src").resolve()))

# pylint: disable = import-error, unused-import
from blocky import Block, BlockData     # noqa: F401, E402


def compare_files(generated_file: Path, expected_file: Path) -> None:
    gen_str = ""
    exp_str = ""
    with open(generated_file, "r", encoding="utf-8") as file:
        gen_str = file.read()
    with open(expected_file, "r", encoding="utf-8") as file:
        exp_str = file.read()

    if gen_str == exp_str:
        print(f"OK: Generated output file '{generated_file}' matches "
              f"the expected output file '{expected_file}'.")
    else:
        print(f"ERROR: Generated output file '{generated_file}' does not match the "
              f"expected output file '{expected_file}'.")

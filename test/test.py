# pylint: disable=missing-module-docstring, missing-function-docstring
import json
from pathlib import Path
from typing import Callable
from context import blocky


class ReportData(blocky.BlockData):
    def __init__(self, data_dict: dict = None, fill_hndl: Callable[[blocky.Block, object, int], None] = None) -> None:
        super().__init__(data_dict, fill_hndl)

    def import_json(self, json_file_path: str | Path) -> None:
        with open(json_file_path, "r", encoding="utf-8") as json_file:
            data_dict = json.load(json_file)
        self.import_dict(data_dict)


class ReportDoc():
    def __init__(self) -> None:
        self.data: ReportData = ReportData()
        self.block: blocky.Block = blocky.Block()
        self.default_template: str | Path = None

    def adjust_data(self) -> None:
        pass

    def generate(self, report_json_file: str | Path, generated_file: str | Path, template: str | Path = None) -> None:
        if template or self.default_template:
            self.data.import_json(report_json_file)
            self.adjust_data()
            if template:
                self.block.load_template(template)
            else:
                self.block.load_template(self.default_template)
            self.block.fill(self.data)
            self.block.save_content(generated_file)


class GTestReportDoc(ReportDoc):
    def __init__(self) -> None:
        super().__init__()
        self.default_template = Path(Path(__file__).parent.resolve(), "report_template.rst")

    def adjust_data(self) -> None:
        # pylint: disable=no-member
        # rationale: The ``testsuites`` member of data object is added dynamically by the ``import_dict`` method.
        for testsuite in self.data.testsuites:
            if int(testsuite.failures) > 0:
                testsuite.failures_wrap = ReportData()
                testsuite.failures_wrap.failure = []
            else:
                testsuite.failures_wrap = None
            for test in testsuite.testsuite:
                if hasattr(test, "failures"):
                    for failure in test.failures:
                        testsuite.failures_wrap.failure.append(
                            ReportData(dict(name=test.name, message=failure.message.replace("\n", " "))))
                test.fill_hndl = self.__fill_hndl_test
            testsuite.fill_hndl = self.__fill_hndl_testsuites_testsuite
        self.data.fill_hndl = self.__fill_hndl_testsuites_testsuite

    def __fill_hndl_testsuites_testsuite(self, block: blocky.Block, block_data: object, __subidx: int) -> None:
        block.get_subblock("RESULT").set(0 if int(block_data.failures) == 0 and int(block_data.errors) == 0 else 1)
        block.get_subblock("FAILURES_COLOR").set(0 if int(block_data.failures) == 0 else 1)
        block.get_subblock("ERRORS_COLOR").set(0 if int(block_data.errors) == 0 else 1)

    def __fill_hndl_test(self, block: blocky.Block, block_data: object, __subidx: int) -> None:
        blk_test_status = block.get_subblock("TEST_STATUS")
        if hasattr(block_data, "failures"):
            blk_test_status.set(2)
        elif block_data.status == "RUN":
            blk_test_status.set(0)
        else:
            blk_test_status.set(1)


def test_report(report_data_file: Path, generated_file: Path, template_file: Path) -> None:
    report_doc = GTestReportDoc()
    report_doc.generate(report_data_file, generated_file, template_file)


def test_basics(template_file: Path, generated_file: Path) -> None:
    blk_file = blocky.Block()

    blk_file.load_template(template_file)

    blk_simple = blk_file.get_subblock("SIMPLE1")
    blk_simple.clone(force=True)
    blk_simple.clone(force=True)
    blk_simple.clone(force=True)
    blk_simple.set()

    (blk_simple, blk_test1, blk_test2) = blk_file.get_subblock("SIMPLE2", "TEST1", "TEST2")

    blk_simple.template = "<VAL><.>,<^.>.</.>\n<VAL><.>,<^.>.</.>\n\n"
    blk_simple.set_variables(VAL=1)
    blk_simple.clone()
    blk_simple.set_variables(VAL=2)
    blk_simple.clone()
    blk_simple.set_variables(VAL="3")

    blk_val = blk_test1.get_subblock("VAL")
    for i in range(12):
        blk_val.set_variables(ID=i, LABEL="cyclic")
        blk_val.clone()
    blk_val.set()
    blk_test1.clone()

    blk_val.set_variables(ID="333", LABEL="manual1")
    blk_val.clone()
    blk_val.set_variables(ID="4798", LABEL="manual2")
    blk_val.set()

    blk_file.set_subblock(blk_simple, blk_test1)

    blk_val = blk_test2.get_subblock("VAL")
    blk_val.set_variables(ID=(11, 22, 33), LABEL="man")
    blk_test2.set(all_subblocks=True)

    blk_line = blk_file.get_subblock("LINE1")
    blk_val = blk_line.get_subblock("VAL")
    for i in range(31):
        blk_val.set_variables(ID=i)
        blk_val.clone()
        if (i + 1) % 10 == 0:
            blk_val.set()
            blk_line.clone()
    blk_val.set()
    blk_line.set()

    blk_line = blk_file.get_subblock("LINE2")
    blk_val = blk_line.get_subblock("VAL")
    for i in range(32):
        blk_val.clone()
        if (i + 1) % 10 == 0:
            blk_line.set_variables(SEP=20*"_")
            blk_line.clone(set_subblocks=True)
    blk_line.set(all_subblocks=True)

    blk_line = blk_file.get_subblock("LINE3")
    blk_val = blk_line.get_subblock("VAL")
    for i in range(20):
        blk_val.set_variables(ID=f"{i:03d}")
        if i < 10:
            blk_val.get_subblock("DEF").set()
        else:
            blk_val.get_subblock("DEF").set(1)
        blk_val.clone()
        if (i + 1) % 10 == 0:
            blk_line.clone(set_subblocks=True)
    # blk_val.set()   # Not necessary, because there is no remaining blk_val content to be set.
    blk_line.set(all_subblocks=True)

    blk_container = blk_file.get_subblock("CONTAINER")
    blk_line = blk_container.get_subblock("LINE4")
    blk_val = blk_line.get_subblock("VAL")
    blk_val.clone(num_copies=10)
    blk_line.clone(set_subblocks=True)
    blk_val.clone(num_copies=10)
    blk_line.set(all_subblocks=True)

    blk_container.clone()
    blk_val.clone(num_copies=3)
    blk_val.set()
    blk_line.clone()
    blk_val.clone(num_copies=2)
    blk_container.set(all_subblocks=True)

    blk_prm = blk_file.get_subblock("BLK_PRM")
    blk_prm.set_variables(ARR="", PRM_NAME="PARAM1")
    blk_prm.clear_subblock("NO_ARR")
    blk_arr_def = blk_prm.get_subblock("ARR_DEF")
    blk_arr_def.set_variables(SIZE="10")
    blk_arr_def.set()
    blk_prm.clone()
    blk_prm.set_variables(ARR="", PRM_NAME="PARAM2")
    blk_prm.clear_subblock("NO_ARR")
    blk_arr_def = blk_prm.get_subblock("ARR_DEF")
    blk_arr_def.set_variables(SIZE="11")
    blk_arr_def.set()
    blk_prm.set()

    blk_loop_test = blk_file.get_subblock("LOOP_TEST")
    blk_test = blk_loop_test.get_subblock("TEST")
    blk_test.set_variables(A="a", B="b")
    blk_test.set(0)
    blk_loop_test.clone()
    blk_test.set_variables(A="b")
    blk_test.clear_variables("B")
    blk_test.set(1)
    blk_loop_test.clone()
    blk_test.clear_variables("A", "B")
    blk_test.set(2)
    blk_loop_test.set()

    blk_container = blk_file.get_subblock("MULTI1")
    blk_blk = blk_container.get_subblock("BLK")
    blk_blk.set(0)
    blk_container.clone(force=True)
    blk_blk.set(1)
    blk_container.clone(force=True)
    blk_blk.set(2)
    blk_container.set()

    blk_container = blk_file.get_subblock("MULTI2")
    blk_blk = blk_container.get_subblock("BLK")
    blk_blk.set_variables(A=123)
    blk_blk.set(0, raw_content=True)
    blk_container.clone()
    blk_blk.set_variables(A=123456)
    blk_blk.set(1, raw_content=True)
    blk_container.clone()
    blk_blk.set_variables(A=123456789)
    blk_blk.set(2, raw_content=True)
    blk_container.set()

    blk_table = blk_file.get_subblock("TABLE")
    blk_row = blk_table.get_subblock("ROW")
    blk_row.set_variables(autoclone=True, A=1, B=23, C=456)
    blk_row.set_variables(autoclone=True, A="def", B="bc", C="a")
    blk_table.set(all_subblocks=True)

    tab_values = (
        ("name", "surname", "age"),
        ("Johnny", "Mnemonic", 35),
        ("Mr.", "Bean", 33),
        ("T-1000", "Terminator", 30))

    blk_html_table = blk_file.get_subblock("HTML_TABLE")
    blk_row = blk_html_table.get_subblock("ROW")
    blk_col = blk_row.get_subblock("COL")
    blk_col.raw_content = True
    for row_vals in tab_values:
        blk_col.set_variables(VALUE=row_vals)
        blk_row.clone(set_subblocks=True)
    blk_html_table.set(all_subblocks=True)

    blk_file.save_content(str(generated_file))


def compare_output(generated_file: Path, expected_file: Path) -> None:
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


def main() -> None:
    test_basics("basics_template.txt", "basics_generated.txt")
    compare_output("basics_generated.txt", "basics_expected.txt", )
    test_report("report_data.json", "report_generated.rst", "report_template.rst")
    compare_output("report_generated.rst", "report_expected.rst", )


if __name__ == "__main__":
    main()

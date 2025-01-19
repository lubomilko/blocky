import json
from typing import Callable
from test_common import Block, BlockData, Path


class ReportData(BlockData):
    def __init__(self, data_dict: dict = None, fill_hndl: Callable[[Block, object, int], None] = None) -> None:
        super().__init__(data_dict, fill_hndl)

    def import_json(self, json_file_path: str | Path) -> None:
        with open(json_file_path, "r", encoding="utf-8") as json_file:
            data_dict = json.load(json_file)
        self.import_dict(data_dict)


class ReportDoc():
    def __init__(self) -> None:
        self.data: ReportData = ReportData()
        self.block: Block = Block()
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

    def __fill_hndl_testsuites_testsuite(self, block: Block, block_data: object, __subidx: int) -> None:
        block.get_subblock("RESULT").set(0 if int(block_data.failures) == 0 and int(block_data.errors) == 0 else 1)
        block.get_subblock("FAILURES_COLOR").set(0 if int(block_data.failures) == 0 else 1)
        block.get_subblock("ERRORS_COLOR").set(0 if int(block_data.errors) == 0 else 1)

    def __fill_hndl_test(self, block: Block, block_data: object, __subidx: int) -> None:
        blk_test_status = block.get_subblock("TEST_STATUS")
        if hasattr(block_data, "failures"):
            blk_test_status.set(2)
        elif block_data.status == "RUN":
            blk_test_status.set(0)
        else:
            blk_test_status.set(1)


def run_test_report(template_file: Path, generated_file: Path, report_data_file: Path) -> None:
    report_doc = GTestReportDoc()
    report_doc.generate(report_data_file, generated_file, template_file)

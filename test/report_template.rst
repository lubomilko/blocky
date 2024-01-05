.. role:: orange
.. role:: red
.. role:: green

####################################################################################################
Test Report
####################################################################################################

.. list-table:: <NAME> test suites summary
    :header-rows: 1
    :width: 100 %
    :widths: 34 30 24 12

    *   -   **Execution time**
        -   **Timestamp**
        -   **Tests / Failures / Errors**
        -   **Result**
    *   -   <TIME>
        -   <TIMESTAMP>
        -   <TESTS> / <FAILURES_COLOR>:green:`<^FAILURES_COLOR>:red:`</FAILURES_COLOR><FAILURES>` / <ERRORS_COLOR>:green:`<^ERRORS_COLOR>:red:`</ERRORS_COLOR><ERRORS>`
        -   <RESULT>:green:`PASSED`<^RESULT>:red:`FAILED`</RESULT>

<TESTSUITES>
****************************************************************************************************
Test Suite: <NAME>
****************************************************************************************************

.. list-table:: <NAME> test suite summary
    :header-rows: 1
    :width: 100 %
    :widths: 64 24 12

    *   -   **Execution time**
        -   **Tests / Failures / Errors**
        -   **Result**
    *   -   <TIME>
        -   <TESTS> / <FAILURES_COLOR>:green:`<^FAILURES_COLOR>:red:`</FAILURES_COLOR><FAILURES>` / <ERRORS_COLOR>:green:`<^ERRORS_COLOR>:red:`</ERRORS_COLOR><ERRORS>`
        -   <RESULT>:green:`PASSED`<^RESULT>:red:`FAILED`</RESULT>

.. list-table:: <NAME> tests
    :header-rows: 1
    :width: 100 %
    :widths: 34 30 10 14 12

    *   -   **Test name**
        -   **File**
        -   **Line**
        -   **Exec. time**
        -   **Status**
    <TESTSUITE>
    *   -   <NAME>
        -   <FILE>
        -   <LINE>
        -   <TIME>
        -   <TEST_STATUS>:green:`PASSED`<^TEST_STATUS>:orange:`<STATUS>`<^TEST_STATUS>:red:`FAILURES`</TEST_STATUS>
    </TESTSUITE>

<FAILURES_WRAP>
.. list-table:: <NAME> test suite failures
    :header-rows: 1
    :width: 100 %
    :widths: 34 66

    *   -   **Test name**
        -   **Error message**
    <FAILURE>
    *   -   <NAME>
        -   :red:`<MESSAGE>`
    </FAILURE>
</FAILURES_WRAP>

</TESTSUITES>

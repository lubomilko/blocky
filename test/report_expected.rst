.. role:: orange
.. role:: red
.. role:: green

####################################################################################################
Test Report
####################################################################################################

.. list-table:: AllTests test suites summary
    :header-rows: 1
    :width: 100 %
    :widths: 34 30 24 12

    *   -   **Execution time**
        -   **Timestamp**
        -   **Tests / Failures / Errors**
        -   **Result**
    *   -   0.035s
        -   2011-10-31T18:52:42Z
        -   3 / :red:`1` / :green:`0`
        -   :red:`FAILED`

****************************************************************************************************
Test Suite: MathTest
****************************************************************************************************

.. list-table:: MathTest test suite summary
    :header-rows: 1
    :width: 100 %
    :widths: 64 24 12

    *   -   **Execution time**
        -   **Tests / Failures / Errors**
        -   **Result**
    *   -   0.015s
        -   2 / :red:`1` / :green:`0`
        -   :red:`FAILED`

.. list-table:: MathTest tests
    :header-rows: 1
    :width: 100 %
    :widths: 34 30 10 14 12

    *   -   **Test name**
        -   **File**
        -   **Line**
        -   **Exec. time**
        -   **Status**
    *   -   Addition
        -   test.cpp
        -   1
        -   0.007s
        -   :red:`FAILURES`
    *   -   Subtraction
        -   test.cpp
        -   2
        -   0.005s
        -   :green:`PASSED`

.. list-table:: MathTest test suite failures
    :header-rows: 1
    :width: 100 %
    :widths: 34 66

    *   -   **Test name**
        -   **Error message**
    *   -   Addition
        -   :red:`Value of: add(1, 1)   Actual: 3 Expected: 2`
    *   -   Addition
        -   :red:`Value of: add(1, -1)   Actual: 1 Expected: 0`

****************************************************************************************************
Test Suite: LogicTest
****************************************************************************************************

.. list-table:: LogicTest test suite summary
    :header-rows: 1
    :width: 100 %
    :widths: 64 24 12

    *   -   **Execution time**
        -   **Tests / Failures / Errors**
        -   **Result**
    *   -   0.005s
        -   1 / :green:`0` / :green:`0`
        -   :green:`PASSED`

.. list-table:: LogicTest tests
    :header-rows: 1
    :width: 100 %
    :widths: 34 30 10 14 12

    *   -   **Test name**
        -   **File**
        -   **Line**
        -   **Exec. time**
        -   **Status**
    *   -   NonContradiction
        -   test.cpp
        -   3
        -   0.005s
        -   :green:`PASSED`



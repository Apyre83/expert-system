#!/bin/bash

PYTHON_SCRIPT="main.py"

TEST_ERROR_FOLDER="./unit_tests/test_error_cases"
TEST_MANDATORY_FOLDER="./unit_tests/test_mandatory_cases"
TEST_EXPECTED_FOLDER="./unit_tests/test_expected_output"
TEST_OPTIONNAL_FOLDER="./unit_tests/test_optionnal_cases"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NO_COLOR='\033[0m'

echo -e "${BLUE}You can run this program with the options 'errors', 'optional', 'mandatory', or 'all'.${NO_COLOR}"
echo ""

compare_output() {
    expected_output_file="$1"
    actual_output_file="$2"

    sort "$expected_output_file" > temp_expected_output.txt
    sort "$actual_output_file" > temp_actual_output.txt

    diff -B -w --color -y "temp_expected_output.txt" "temp_actual_output.txt" > /dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Output Matched${NO_COLOR}"
    else
        echo -e "Expected      | Actual"
        diff -B -w --color -y -W 30 "temp_expected_output.txt" "temp_actual_output.txt"
        echo -e "${RED}Output Mismatch${NO_COLOR}"
    fi
}


error_tests() {
    for test_file in $TEST_ERROR_FOLDER/*.txt; do
        echo "Testing $test_case..."
        python3 $PYTHON_SCRIPT "$test_file"
        if [ $? -eq 1 ]; then
            echo -e "${GREEN}Test Passed${NO_COLOR}"
        else
            echo -e "${RED}Test Failed${NO_COLOR}"
        fi
        echo ""
    done
}

mandatory_tests() {
    for test_file in $TEST_MANDATORY_FOLDER/*.txt; do
        echo "----------------------------------------"
        test_case=$(basename "$test_file")
        echo "Testing $test_case..."
        python3 $PYTHON_SCRIPT "$test_file" > temp_output.txt

        if [ $? -eq 0 ]; then
            compare_output "${TEST_EXPECTED_FOLDER}/${test_case}" "temp_output.txt"
        else
            echo -e "${RED}Test Failed${NO_COLOR}"
        fi
    done
    rm temp_output.txt temp_expected_output.txt temp_actual_output.txt
}

case "$1" in
    errors)
        error_tests
        ;;
    optional)
        optional_tests
        ;;
    mandatory)
        mandatory_tests
        ;;
    all)
        error_tests
        mandatory_tests
        optional_tests
        ;;
    *)
        echo -e "You did not specify a valid option. So only mandatory tests will be run."
        echo ""
        mandatory_tests
        ;;
esac

#!/bin/bash

# Chemin vers le script Python
PYTHON_SCRIPT="main.py"

# Dossier contenant les cas de test
TEST_ERROR_FOLDER="./test_error_cases"

TEST_GOOD_FOLDER="./test_good_cases"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
NO_COLOR='\033[0m'


for test_file in $TEST_ERROR_FOLDER/*.txt; do
    test_case=$(basename "$test_file")
    echo "Testing $test_case..."
    python3 $PYTHON_SCRIPT "$test_file"
    if [ $? -eq 1 ]; then
        echo -e "${GREEN}Test Passed${NO_COLOR}"
    else
        echo -e "${RED}Test Failed${NO_COLOR}"
    fi
    echo ""
done

for test_file in $TEST_GOOD_FOLDER/*.txt; do
    test_case=$(basename "$test_file")
    echo "Testing $test_case..."
    python3 $PYTHON_SCRIPT "$test_file"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Test Passed${NO_COLOR}"
    else
        echo -e "${RED}Test Failed${NO_COLOR}"
    fi
    echo ""
done

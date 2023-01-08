#!/bin/bash
# Run all control tests
# Usage: run-all-control-tests.sh

# Check if kubernetes is running
if ! kubectl cluster-info &> /dev/null
then
    echo "Kubernetes is not running"
    exit 1
fi

# Print Kubernetes version
kubectl version

# Check if python or python3 is available
PYTHON_EXECUTABLE=na
if command -v python3 &> /dev/null
then
    PYTHON_EXECUTABLE=python3
elif command -v python &> /dev/null
then
    PYTHON_EXECUTABLE=python
else
    echo "python could not be found"
    exit 1
fi

# Result variable
result=0
# Run all control tests
for control in $(ls controls); do
    echo "Running test $control"
    pushd controls/$control
    $PYTHON_EXECUTABLE ../../scripts/run-control-test.py
    # Check if test failed
    if [ $? -ne 0 ]; then
        echo "Test $control failed"
        result=1
    else
        echo "Test $control passed"
    fi
done

exit $result
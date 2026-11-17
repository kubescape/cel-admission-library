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

# Refuse installed production CRDs, create owned fixtures, and clean up on exit.
source "$(dirname "${BASH_SOURCE[0]}")/agent-test-crds.sh"
setup_agent_test_crds test-resources/agent-sandbox-test-crds.yaml || exit 1

# Run all control and runtime policy tests
for control in controls/* runtime-policies/*; do
    if [[ -f $control/tests.json ]]; then
        echo "=================================================="
        echo "Running test $control"
        echo "--------------------------------------------------"
        pushd $control
        $PYTHON_EXECUTABLE ../../scripts/run-control-tests.py
        TEST_RESULT=$?
        # Check if test failed
        echo "--------------------------------------------------"
        if [ $TEST_RESULT -ne 0 ]; then
            echo "Test $control failed"
            result=1
        else
            echo "Test $control passed"
        fi
        popd
        echo "=================================================="
    fi
done

exit $result

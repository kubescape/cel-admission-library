#!/bin/bash
# This script creates the release artifacts for the project at the specified directory
# Usage: ./scripts/create-release-objects.sh <release-directory>

# Check if release directory is specified exists
if [ -z "$1" ]; then
    echo "Please specify the release directory"
    exit 1
fi

RELEASE_DIR=$1

# Create YAML file which contains all policies
RELEASE_POLICY_YAML_FILE_NAME=$RELEASE_DIR/kubescape-validating-admission-policies.yaml

echo "Creating release policy YAML file $RELEASE_POLICY_YAML_FILE_NAME"
echo "" > $RELEASE_POLICY_YAML_FILE_NAME

# Loop through all policies and add them to the release YAML file
for control in $(ls controls); do
    # Verify if policy file is in the control directory exists
    if [ ! -f "controls/$control/policy.yaml" ]; then
        echo "Warning: Policy file for control $control does not exist"
    fi
    # Copy policy file contents to release YAML file
    cat controls/$control/policy.yaml >> $RELEASE_POLICY_YAML_FILE_NAME
    echo "---" >> $RELEASE_POLICY_YAML_FILE_NAME
done

# Delete the last line of the policy file
cp $RELEASE_POLICY_YAML_FILE_NAME $RELEASE_POLICY_YAML_FILE_NAME.bak
tail -n +2 $RELEASE_POLICY_YAML_FILE_NAME.bak > $RELEASE_POLICY_YAML_FILE_NAME
rm $RELEASE_POLICY_YAML_FILE_NAME.bak

exit 0
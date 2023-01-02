import json, yaml
import subprocess
import os
import tempfile

SCRIPTS_DIR = os.path.join('..', '..', 'scripts')
TEST_RESOURCES_DIR = os.path.join('..', '..', 'test-resources')

# Get the name of the python executable
python_executable = 'python3'
try:
    subprocess.check_call([python_executable, '--version'])
except:
    python_executable = 'python'


# check access to scripts folder
if not os.path.exists(SCRIPTS_DIR):
    raise Exception('Scripts folder not found')
# check access to test-resources folder
if not os.path.exists(TEST_RESOURCES_DIR):
    raise Exception('Test resources folder not found')

# Open tests.json file and read it into a variable
with open('tests.json', 'r') as f:
    tests = json.load(f)

# Open policy yaml
with open(os.path.join('policy.yaml'), 'r') as f:
    policy = yaml.load(f, Loader=yaml.FullLoader)

# Loop through the tests
for test in tests:
    template = test['template']
    field_change_list = test['field_change_list']
    expected = test['expected']

    # Generate temporary file name for the output file with tempfile
    with tempfile.NamedTemporaryFile() as temp_file:
        test_object_yaml = temp_file.name

    # Run the change yaml field script
    subprocess.check_call([python_executable, os.path.join(SCRIPTS_DIR, 'change-yaml-field.py'), '-i', os.path.join(TEST_RESOURCES_DIR, template), '-o', test_object_yaml] + field_change_list)
    print('Generated test object: ' + test_object_yaml)

    # Generate temporary file name for the binding file with tempfile
    with tempfile.NamedTemporaryFile() as temp_file:
        policy_bind_temp_file_name = temp_file.name
    # Create the policy binding file
    policy_name = policy['metadata']['name']
    policy_bind_change_list = ['spec.policyName=' + policy_name, 'metadata.name=' + policy_name + '-binding']
    subprocess.check_call([python_executable, os.path.join(SCRIPTS_DIR, 'change-yaml-field.py'), '-i', os.path.join(TEST_RESOURCES_DIR, 'policy-binding.yaml'), '-o', policy_bind_temp_file_name] + policy_bind_change_list)
    print('Generated policy binding: ' + policy_bind_temp_file_name)

    # Run kubectl apply on the policy and policy binding
    subprocess.check_call(['kubectl', 'apply', '-f', policy_bind_temp_file_name])
    subprocess.check_call(['kubectl', 'apply', '-f', 'policy.yaml'])

    # Run kubectl apply on the test object
    result = None
    try:
        subprocess.check_call(['kubectl', 'apply', '-f', test_object_yaml])
        result = 0
    except subprocess.CalledProcessError as e:
        result = e.returncode

    input('Press enter to continue...')

    # Check if the result is as expected
    if expected == 'pass' and result != 0:
        print('Test failed: ' + test['name'] + ' expected to pass but failed')
    elif expected == 'fail' and result == 0:
        print('Test failed: ' + test['name'] + ' expected to fail but passed')
    else:
        print('Test passed: ' + test['name'])
    

    # Run kubectl delete on the policy and policy binding
    try:
        subprocess.check_call(['kubectl', 'delete', '-f', 'policy.yaml'])
        subprocess.check_call(['kubectl', 'delete', '-f', policy_bind_temp_file_name])
        subprocess.check_call(['kubectl', 'delete', '-f', test_object_yaml])
    except:
        pass
    
    


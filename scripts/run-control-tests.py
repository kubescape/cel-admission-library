import json, yaml
import subprocess
import os
import sys
import tempfile
from termcolor import colored


SCRIPTS_DIR = os.path.join('..', '..', 'scripts')
TEST_RESOURCES_DIR = os.path.join('..', '..', 'test-resources')
CONFIGURATION_DIR = os.path.join('..', '..', 'configuration')

# Get the name of the python executable
python_executable = 'python3'
try:
    subprocess.check_call([python_executable, '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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

# Apply the configuraton CRD
subprocess.check_call(['kubectl', 'apply', '-f', os.path.join(CONFIGURATION_DIR, 'policy-configuration-definition.yaml')])

# Open policy yaml
with open(os.path.join('policy.yaml'), 'r') as f:
    policy = yaml.load(f, Loader=yaml.FullLoader)

# Test result variable
all_tests_passed = True

# Loop through the tests
for test in tests:
    name = test['name']
    template = test['template']
    field_change_list = test['field_change_list'] if 'field_change_list' in test else []
    expected = test['expected']

    print('-'*120)
    print('Running test: ' + name)

    # Generate temporary file name for the output file with tempfile
    with tempfile.NamedTemporaryFile() as temp_file:
        test_object_yaml = temp_file.name

    # Run the change yaml field script
    if len(field_change_list) > 0:
        print('Changing fields: ' + str(field_change_list))
        subprocess.check_call([python_executable, os.path.join(SCRIPTS_DIR, 'change-yaml-field.py'), '-i', os.path.join(TEST_RESOURCES_DIR, template), '-o', test_object_yaml] + field_change_list)
    else:
        subprocess.check_call(['cp', os.path.join(TEST_RESOURCES_DIR, template), test_object_yaml])
    print('Generated test object: ' + test_object_yaml)

    # Generate temporary file name for the binding file with tempfile
    with tempfile.NamedTemporaryFile() as temp_file:
        policy_bind_temp_file_name = temp_file.name
    # Create the policy binding file
    policy_name = policy['metadata']['name']
    policy_bind_change_list = ['spec.policyName=' + policy_name, 'metadata.name=' + policy_name + '-binding', 'spec.paramRef.name=' + policy_name + '-params']
    subprocess.check_call([python_executable, os.path.join(SCRIPTS_DIR, 'change-yaml-field.py'), '-i', os.path.join(TEST_RESOURCES_DIR, 'policy-binding.yaml'), '-o', policy_bind_temp_file_name] + policy_bind_change_list)
    print('Generated policy binding: ' + policy_bind_temp_file_name)

    # Create parameter file
    with tempfile.NamedTemporaryFile() as temp_file:
        param_file_name = temp_file.name
    param_file_change_list = ['metadata.name=' + policy_name + '-params']
    subprocess.check_call([python_executable, os.path.join(SCRIPTS_DIR, 'change-yaml-field.py'), '-i', os.path.join(TEST_RESOURCES_DIR, 'default-control-configuration.yaml'), '-o', param_file_name] + param_file_change_list)
    print('Generated parameter file: ' + param_file_name)


    # Run kubectl apply on the policy and policy binding
    subprocess.check_call(['kubectl', 'apply', '-f', param_file_name])
    subprocess.check_call(['kubectl', 'apply', '-f', policy_bind_temp_file_name])
    subprocess.check_call(['kubectl', 'apply', '-f', 'policy.yaml'])

    # Run kubectl apply on the test object
    result = None
    try:
        subprocess.check_call(['kubectl', 'apply', '-f', test_object_yaml])
        result = 0
    except subprocess.CalledProcessError as e:
        result = e.returncode

    test_passed = False
    # Check if the result is as expected
    if expected == 'pass' and result != 0:
        print(colored('Test failed: expected to pass but failed','red'))
    elif expected == 'fail' and result == 0:
        print(colored('Test failed: expected to fail but passed','red'))
    else:
        test_passed = True
        print(colored('Test passed!','green'))
   
    print(colored('Cleaning up...', 'yellow'))
    # Run kubectl delete on the policy and policy binding
    try:
        subprocess.check_call(['kubectl', 'delete', '-f', 'policy.yaml'],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call(['kubectl', 'delete', '-f', policy_bind_temp_file_name],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call(['kubectl', 'delete', '-f', test_object_yaml],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call(['kubectl', 'delete', '-f', param_file_name],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass
    
    # Call kubectl wait --for=delete pod -l app=test-pod  --timeout=360s
    subprocess.check_call(['kubectl', 'wait', '--for=delete', 'pod', '-l', 'app=test-pod', '--timeout=360s'])

    if not test_passed:
        os.remove(policy_bind_temp_file_name)
        os.remove(test_object_yaml)
        os.remove(param_file_name)
        print(colored('Done (left generated object in place)', 'yellow'))
    else:
        print(colored('Done', 'yellow'))

    all_tests_passed = all_tests_passed and test_passed

    print('-'*120)
    print('')
    
    
if all_tests_passed:
    print(colored('Control tests passed!','green'))
    sys.exit(0)
else:
    print(colored('Some control tests failed','red'))
    sys.exit(1)


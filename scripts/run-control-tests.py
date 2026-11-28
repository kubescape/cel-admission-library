import json, yaml
import subprocess
import os
import sys
import time
import tempfile
from termcolor import colored


SCRIPTS_DIR = os.path.join('..', '..', 'scripts')
TEST_RESOURCES_DIR = os.path.join('..', '..', 'test-resources')
CONFIGURATION_DIR = os.path.join('..', '..', 'configuration')

# Query parameters for tests that send a CONNECT request to a Pod subresource
# ("connect": "exec" in tests.json) instead of applying the test object.
CONNECT_QUERIES = {
    'attach': 'stdout=true',
    'exec': 'command=true&stdout=true',
    'portforward': 'ports=8086',
}

DONT_CLEANUP = False
if len(sys.argv) > 1:
    if '--dont-cleanup' in sys.argv or '-d' in sys.argv:
        DONT_CLEANUP = True

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

# Create a test namespace
subprocess.check_call(['kubectl', 'create', 'namespace','test-namespace'])

try:
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
        binding_template = test['binding_template'] if 'binding_template' in test else 'policy-binding.yaml'
        param_template = test['param_template'] if 'param_template' in test else 'default-control-configuration.yaml'
        connect = test.get('connect')
        resize = test.get('resize')
        if resize is not None and not isinstance(resize, dict):
            raise Exception('resize must be an object with field_change_list and optionally template')
        if connect and resize:
            raise Exception('a test cannot use both connect and resize')
        namespace_args = ['-n', 'test-namespace'] if connect or resize else []

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
        policy_bind_change_list = ['spec.policyName=' + policy_name, 'metadata.name=' + policy_name + '-binding']
        if not test.get('omit_param_ref', False):
            policy_bind_change_list.append('spec.paramRef.name=' + policy_name + '-params')
        subprocess.check_call([python_executable, os.path.join(SCRIPTS_DIR, 'change-yaml-field.py'), '-i', os.path.join(TEST_RESOURCES_DIR, binding_template), '-o', policy_bind_temp_file_name] + policy_bind_change_list)
        print('Generated policy binding: ' + policy_bind_temp_file_name)

        # Create parameter file
        with tempfile.NamedTemporaryFile() as temp_file:
            param_file_name = temp_file.name
        param_file_change_list = ['metadata.name=' + policy_name + '-params']
        subprocess.check_call([python_executable, os.path.join(SCRIPTS_DIR, 'change-yaml-field.py'), '-i', os.path.join(TEST_RESOURCES_DIR, param_template), '-o', param_file_name] + param_file_change_list)
        print('Generated parameter file: ' + param_file_name)


        # Run kubectl apply on the policy and policy binding
        subprocess.check_call(['kubectl', 'apply', '-f', param_file_name])
        subprocess.check_call(['kubectl', 'apply', '-f', policy_bind_temp_file_name])
        subprocess.check_call(['kubectl', 'apply', '-f', 'policy.yaml'])

        time.sleep(1)

        # A test object can name an object the cluster already has, such as the
        # kubernetes Service in the default namespace. The apply below is a dry run, so
        # the cleanup must not delete such an object: only delete what didn't exist.
        object_existed = subprocess.call(['kubectl', 'get'] + namespace_args + ['-f', test_object_yaml],
                                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

        if connect:
            # CONNECT requests (pods/exec, pods/attach, pods/portforward) can't
            # be dry-run: create the Pod in the test namespace and send the
            # request to its subresource. Without a running container the
            # request still fails after admission, so only the policy decision
            # counts: the request is denied when the error names the policy.
            if connect not in CONNECT_QUERIES:
                raise Exception('unsupported connect subresource "' + str(connect) + '"')
            with open(test_object_yaml, 'r') as f:
                pod_name = yaml.load(f, Loader=yaml.FullLoader)['metadata']['name']
            # A new namespace gets its default ServiceAccount a moment after
            # creation, and Pod admission rejects the Pod until it exists.
            for attempt in range(30):
                if subprocess.call(['kubectl', 'apply'] + namespace_args + ['-f', test_object_yaml]) == 0:
                    break
                time.sleep(1)
            else:
                raise Exception('could not create ' + pod_name + ' in test-namespace')
            path = '/api/v1/namespaces/test-namespace/pods/' + pod_name + '/' + connect + '?' + CONNECT_QUERIES[connect]
            proc = subprocess.run(
                ['kubectl', 'create', '--raw', path, '-f', os.devnull, '--request-timeout=30s'],
                capture_output=True, text=True
            )
            result = 1 if policy_name in proc.stderr else 0
        elif resize:
            # In-place resize goes through the pods/resize subresource: the Pod
            # has to exist first, and only its container resources may change.
            # Create the Pod from the test object, then PATCH the resources of
            # the object built from the resize template onto that subresource.
            with open(test_object_yaml, 'r') as f:
                pod_name = yaml.load(f, Loader=yaml.FullLoader)['metadata']['name']
            for attempt in range(30):
                if subprocess.call(['kubectl', 'apply'] + namespace_args + ['-f', test_object_yaml]) == 0:
                    break
                time.sleep(1)
            else:
                raise Exception('could not create ' + pod_name + ' in test-namespace')

            resize_template = resize.get('template', template)
            with tempfile.NamedTemporaryFile() as temp_file:
                resize_object_yaml = temp_file.name
            resize_change_list = resize.get('field_change_list', [])
            if len(resize_change_list) > 0:
                subprocess.check_call([python_executable, os.path.join(SCRIPTS_DIR, 'change-yaml-field.py'), '-i', os.path.join(TEST_RESOURCES_DIR, resize_template), '-o', resize_object_yaml] + resize_change_list)
            else:
                subprocess.check_call(['cp', os.path.join(TEST_RESOURCES_DIR, resize_template), resize_object_yaml])
            with open(resize_object_yaml, 'r') as f:
                resize_object = yaml.load(f, Loader=yaml.FullLoader)
            # A strategic merge patch keeps the untouched fields of every
            # container, so only the resources built above reach the server.
            patch = {'spec': {}}
            for container_field in ('containers', 'initContainers'):
                containers = [c for c in resize_object['spec'].get(container_field, []) if 'resources' in c]
                if len(containers) > 0:
                    patch['spec'][container_field] = [{'name': c['name'], 'resources': c['resources']} for c in containers]
            patch_file = resize_object_yaml + '.json'
            with open(patch_file, 'w') as f:
                json.dump(patch, f)
            proc = subprocess.run(
                ['kubectl', 'patch', 'pod', pod_name] + namespace_args + ['--subresource', 'resize', '--type', 'strategic', '--patch-file', patch_file, '--request-timeout=30s'],
                capture_output=True, text=True
            )
            os.remove(patch_file)
            result = proc.returncode
        else:
            # Run kubectl apply on the test object and capture output
            proc = subprocess.run(
                ['kubectl', '--dry-run=server', 'apply', '-f', test_object_yaml],
                capture_output=True, text=True
            )
            result = proc.returncode

        test_passed = False
        valid_expected = {'pass', 'fail', 'warn'}
        if expected not in valid_expected:
            print(colored('Test failed: unsupported expected value "' + str(expected) + '"','red'))
        elif expected == 'pass' and result != 0:
            print(colored('Test failed: expected to pass but failed','red'))
            print(proc.stderr)
        elif expected == 'fail' and result == 0:
            print(colored('Test failed: expected to fail but passed','red'))
        elif expected == 'fail' and result != 0 and policy_name not in proc.stderr:
            print(colored('Test failed: expected VAP denial from "' + policy_name + '" but got different error','red'))
            print(proc.stderr)
        elif expected == 'warn' and result != 0:
            print(colored('Test failed: expected to pass with a warning but failed','red'))
            print(proc.stderr)
        elif expected == 'warn' and result == 0 and policy_name not in proc.stderr:
            print(colored('Test failed: expected VAP warning from "' + policy_name + '" but none was emitted','red'))
            print(proc.stderr)
        else:
            test_passed = True
            print(colored('Test passed!','green'))

        print(colored('Cleaning up...', 'yellow'))
        # Run kubectl delete on the policy and policy binding.
        try:
            subprocess.check_call(['kubectl', 'delete', '-f', 'policy.yaml'],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.check_call(['kubectl', 'delete', '-f', policy_bind_temp_file_name],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if not object_existed:
                subprocess.check_call(['kubectl', 'delete'] + namespace_args + ['-f', test_object_yaml],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.check_call(['kubectl', 'delete', '-f', param_file_name],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass

        # Call kubectl wait --for=delete pod -l app=test-pod  --timeout=360s
        subprocess.check_call(['kubectl', 'wait', '--for=delete', 'pod', '-l', 'app=test-pod', '--timeout=360s'])

        if not test_passed:
            if not DONT_CLEANUP:
                os.remove(policy_bind_temp_file_name)
                os.remove(test_object_yaml)
                os.remove(param_file_name)
                print(colored('Done ', 'yellow'))
            else:
                print(colored('Done (left generated object in place)', 'yellow'))
        else:
            print(colored('Done', 'yellow'))

        all_tests_passed = all_tests_passed and test_passed

        print('-'*120)
        print('')
except Exception as e:
    print(colored('Exception: ' + str(e),'red'))
    all_tests_passed = False




# Delete the test namespace
subprocess.check_call(['kubectl', 'delete', 'namespaces', 'test-namespace'],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if all_tests_passed:
    print(colored('Control tests passed!','green'))
    sys.exit(0)
else:
    print(colored('Some control tests failed','red'))
    sys.exit(1)


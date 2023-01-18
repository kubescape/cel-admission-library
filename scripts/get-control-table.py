import requests
import re
import yaml
import os

# Get the control table from GitHub https://github.com/kubescape/regolibrary/releases/download/latest/controls and parse it as JSON
response = requests.get("https://github.com/kubescape/regolibrary/releases/latest/download/controls")
# Check if the response was successful
if response.status_code != 200:
    print("Error: Failed to get control table from GitHub")
    exit(1)
control_table = response.json()

lines = []
# Loop over all controls in the control directory
for control_id in os.listdir('controls'):
    # Get the control file path
    control_path = os.path.join('controls', control_id,'policy.yaml')
    # Check if the control path is a file
    if os.path.isfile(control_path):
        # Open the control file
        with open(control_path, 'r') as control_file:
            # Load the control file as YAML
            control = yaml.load(control_file, Loader=yaml.FullLoader)

            # Check if the control is configurable and what is the parameter name
            configuration_parameter = 'not configurable'
            if 'paramKind' in control['spec']:
                cel = control['spec']['validations'][0]['expression']
                # Check if the control is configurable by a parameter with re 
                m = re.search(r"params\.settings\.([a-zA-Z0-9]+)", cel)
                # Check that there is a match
                if m:
                    configuration_parameter = m.group(1)
                    #print(f'Control {control_id} is configurable by parameter {configuration_parameter}')


            # Loop over all controls in the control table
            found = False
            for control_table_control in control_table:
                # Check if the control ID matches
                if control_table_control['controlID'] == control_id:
                    lines.append([control_id, control_table_control["name"], control['metadata']['name'] , control_table_control["description"], configuration_parameter])
                    found = True
            if not found:
                print(f'Error: Control {control_id} not found in control table')
    else:
        print(f'Error: Control {control_path} is not a file')

# Print markdown table
print('| Control ID | Name | Policy name | Configuration parameter |')
print('| --- | --- | --- | --- |')
# Sort the lines by control ID
lines.sort(key=lambda line: line[0])
# Loop over all lines
for line in lines:
    doc_url = f'https://hub.armosec.io/docs/{line[0].lower()}'
    if line[4] == 'not configurable':
        print(f'| [{line[0]}]({doc_url}) | {line[1]} | {line[2]} | {line[4]} |')
    else:
        configparam_url = f'https://hub.armosec.io/docs/configuration_parameter_{line[4].lower()}'
        print(f'| [{line[0]}]({doc_url}) | {line[1]} | {line[2]} | [{line[4]}]({configparam_url}) |')

#print(json.dumps(control_table[0], indent=4))


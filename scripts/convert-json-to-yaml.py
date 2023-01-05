import sys
import yaml
import json

# Open first argument as JSON file
with open(sys.argv[1]) as f:
    # Load JSON file
    data = json.load(f)
    # Read second argument as string
    path = sys.argv[2]
    # Split string into list
    path = path.split('.')
    # Iterate over list
    for p in path:
        # Read key from list
        data = data[p]

    # Print data in YAML format
    print(yaml.dump(data))
    
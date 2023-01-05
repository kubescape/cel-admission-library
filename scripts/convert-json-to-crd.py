import json
import sys
import yaml

def convert_node_to_openapiv3_schema(n):
    if type(n) == dict:
        return {
            'type': 'object',
            'properties': {
                k: convert_node_to_openapiv3_schema(v)
                for k, v in n.items()
            }
        }
    elif type(n) == list:
        return {
            'type': 'array',
            'items': convert_node_to_openapiv3_schema(n[0])
        }
    elif type(n) == str:
        return {
            'type': 'string'
        }
    elif type(n) == int:
        return {
            'type': 'integer'
        }
    elif type(n) == bool:
        return {
            'type': 'boolean'
        }
    else:
        raise Exception('Unknown type: {}'.format(n.type))

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

    # Convert data to OpenAPIv3 schema
    schema = convert_node_to_openapiv3_schema(data)
    # Print schema in YAML format
    print(yaml.dump(schema))
    
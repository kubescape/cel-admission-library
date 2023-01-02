import yaml
import json
import sys
import re
import argparse
import os

__DEBUG__ = False

def apply_field(data, field, value):
    # Check if value looks like JSON
    try:
        value = json.loads(value)
    except ValueError:
        pass
    
    # Parse the field name into a list
    fields = field.split('.')
    root = data
    for f in fields[:-1]:
        # Check if the field is a json key and contains only letters
        if not re.match(r'[a-zA-Z]\w+', f) and not re.match(r'\[\d+\]', f):
            raise ValueError('Invalid field name: ' + f)

        # Check with regex if the field is a list index in the format of [x]
        if re.match(r'\[\d+\]', f):
            f = int(f[1:-1])
            if type(root) is not list:
                root = []
            if len(root) < f:
                root += [None] * (f - len(root) + 1)


        if (type(root) is list and root[f] == None) or (type(root) is dict and f not in root):
            # Check the next field to see if it's a number
            try:
                int(fields[fields.index(f) + 1])
                root[f] = []
            except ValueError:
                root[f] = {}
                            
        root = root[f]

    # Set the value
    root[fields[-1]] = value


def main():
    # Parse the command line arguments with argparse (-i is the input file, -o is the output file and the rest are field=value)
    parser = argparse.ArgumentParser(description='Change a field in a YAML file')
    parser.add_argument('-i', '--input', help='Input file', default='-')
    parser.add_argument('-o', '--output', help='Output file', default='-')
    parser.add_argument('fields', nargs='*', help='Fields to change')
    args = parser.parse_args()

    # Check if input file exists
    if args.input != '-' and not os.path.exists(args.input):
        raise ValueError('Input file does not exist: ' + args.input)
    input_file = open(args.input, 'r') if args.input != '-' else sys.stdin
    if input_file == sys.stdin:
        print('Reading YAML from stdin...', file=sys.stderr)

    # Check if the parent directory of the output file exists
    if args.output != '-' and not os.path.exists(os.path.dirname(args.output)):
        raise ValueError('Output file directory does not exist: ' + os.path.dirname(args.output))
    output_file = open(args.output, 'w') if args.output != '-' else sys.stdout

    
    # Read the YAML file from stdin
    data = yaml.load(input_file, Loader=yaml.FullLoader)

    # Get the field name and value from the command line
    for arg in args.fields:    
        if arg.count('=') != 1:
            raise ValueError('Invalid argument: missing \'=\' in ' + arg)
        field, value = arg.split('=')
        apply_field(data, field, value)
   
    # Write the YAML file to stdout
    yaml.dump(data, output_file, default_flow_style=False)

if __name__ == '__main__':
    main()     


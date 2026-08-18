import yaml
import json
import sys
import re
import argparse
import os

__DEBUG__ = False

def is_index(field):
    """True if the field selects a list element, e.g. [0]."""
    return re.fullmatch(r'\[\d+\]', field) is not None


def key_of(field):
    """The value to index a container with: an int for [0], the name otherwise."""
    return int(field[1:-1]) if is_index(field) else field


def grow_to(lst, index):
    """Pad a list with None so index is addressable."""
    if len(lst) <= index:
        lst += [None] * (index - len(lst) + 1)


def apply_field(data, field, value):
    # Check if value looks like JSON
    try:
        value = json.loads(value)
    except ValueError:
        pass

    # Parse the field name into a list
    fields = field.split('.')
    for f in fields:
        # Check if the field is a json key starting with a letter, or a list
        # index in the format of [x]. Deliberately a prefix match, not a full
        # one: keys like `top-secret-allowed` and `app.kubernetes.io/name` are
        # ordinary in Kubernetes objects and were always accepted here.
        if not re.match(r'[a-zA-Z]\w*', f) and not is_index(f):
            raise ValueError('Invalid field name: ' + f)

    root = data
    for i, f in enumerate(fields[:-1]):
        key = key_of(f)
        if not isinstance(root, (dict, list)):
            raise ValueError('Cannot descend past ' + '.'.join(fields[:i]) +
                             ' in ' + field + ': it holds a scalar, not a mapping or a list')
        # What this level has to hold depends on how the NEXT field indexes into
        # it: [0] needs a list, a name needs a dict. Deciding it from the next
        # field is what lets a path create containers that are not there yet.
        missing = [] if is_index(fields[i + 1]) else {}

        if isinstance(root, list):
            if not is_index(f):
                raise ValueError('Expected a list index like [0] for ' + f + ' in ' + field)
            grow_to(root, key)
        elif is_index(f):
            raise ValueError('Cannot index ' + f + ' into a mapping in ' + field)

        # Create the container in place. Assigning to a fresh local would build a
        # structure detached from the document, so always write through the
        # parent.
        if isinstance(root, list):
            if root[key] is None:
                root[key] = missing
        elif root.get(f) is None:
            root[f] = missing

        root = root[key]

    # Set the value
    key = key_of(fields[-1])
    if not isinstance(root, (dict, list)):
        raise ValueError('Cannot set ' + field + ': ' + '.'.join(fields[:-1]) +
                         ' holds a scalar, not a mapping or a list')
    if isinstance(root, list):
        if not is_index(fields[-1]):
            raise ValueError('Expected a list index like [0] for ' + fields[-1] + ' in ' + field)
        grow_to(root, key)
    root[key] = value


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


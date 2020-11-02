""" The run script of the aws_mfa_config package """
import sys

import parse_arguments

def main():
    """ Main runtime function """
    context = parse_arguments.parse(sys.argv[1:])

    context.func(context)

if __name__ == "__main__":
    main()

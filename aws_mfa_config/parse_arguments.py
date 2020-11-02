
import sys
import argparse
import os
import auth
import profile

def add_common_arguments(parser):
    """Add common arguments to a parsers"""
    parser.add_argument('-p', '--profile-name', dest='profile_name', type=str,
                        help='AWS Configuration profile to use', default='default')

    parser.add_argument('--config-path', dest='config_path', type=str,
                        help='Path to aws configuration', default=os.path.expanduser('~/.aws'))

    return parser

def add_profile_subparser(subparsers):
    profile_parser = subparsers.add_parser('profile', help='Add AWS Profile action')

    profile_subparsers = profile_parser.add_subparsers(help='Profile command')
    profile_subparsers.required = True

    add_parser = profile_subparsers.add_parser('add', help='Add an AWS Profile')
    add_parser.set_defaults(func=profile.add)

    delete_parser = profile_subparsers.add_parser('delete', help='Delete an AWS Profile')
    delete_parser.set_defaults(func=profile.delete)

    add_common_arguments(add_parser)
    add_common_arguments(delete_parser)

    return profile_parser

def add_auth_subparser(subparsers):
    auth_parser = subparsers.add_parser('auth', help='Authenticate to AWS')

    auth_parser.set_defaults(func=auth.mfa)
    add_common_arguments(auth_parser)

    auth_parser.add_argument('-t', '--ttl', dest='ttl', type=int,
                        help='The TTL for the AWS Session Token', default=900)

    return auth_parser

def parse(args):
    """Parse the command line arguments and return the action"""

    parser = argparse.ArgumentParser(
        description='Create aws profiles that support mfa \
                     authentication and temporary sessions',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        # exit_on_error=False
    )

    subparsers = parser.add_subparsers(help='Valid actions')
    subparsers.required = True

    profile_parser = add_profile_subparser(subparsers)
    auth_parser = add_auth_subparser(subparsers)

    context = parser.parse_args(args)
    return context
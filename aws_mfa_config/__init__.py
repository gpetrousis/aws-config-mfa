import argparse
import configparser
import os
import sys
import boto3

# TODO: Do not request new token if it's not expired. Or force update
def parse_arguments():
	# TODO: Print default values
	# TODO: Make --mfa mandatory for auth-mfa command
	parser = argparse.ArgumentParser(description='Create aws profiles that also support mfa '
												 'and fetch temporary credentials')
	parser.add_argument('command', metavar='command', type=str, nargs=1, choices=['add', 'auth-mfa'], help='Which operation to run')
	parser.add_argument('-p', '--profile-name', dest='profile_name', type=str, help='AWS Configuration profile to use', default='default')
	parser.add_argument('--mfa', dest='mfa', help='MFA pin code')
	parser.add_argument('--config-path', dest='config_path', help='Path to aws configuration', default=os.path.expanduser('~/.aws'))

	context = parser.parse_args()
	context.command = context.command[0]
	return context

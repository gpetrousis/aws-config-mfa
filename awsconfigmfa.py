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
	parser.add_argument('-p, --profile', dest='profile', help='AWS Configuration profile to use', default='default')
	parser.add_argument('--mfa', dest='mfa', help='MFA pin code')
	parser.add_argument('--config-path', dest='config_path', help='Path to aws configuration', default=os.path.expanduser('~/.aws'))

	context = parser.parse_args()
	context.command = context.command[0]
	return context

def add_profile(context):
	credentials_path = os.path.join(context.config_path, 'credentials')
	config_path = os.path.join(context.config_path, 'config')

	if ((not os.path.exists(credentials_path)) or (not os.path.exists(config_path))):
		print('Could not locate a credentials or a config file in {config_path}. Would you like to create them for (y/n): '.format(config_path=context.config_path))
		choice = input().lower()
		if(choice != 'y'):
			print('Please provide a path that contains a valid aws credentials and config file.')
			sys.exit()

	config = configparser.ConfigParser()
	credentials = configparser.ConfigParser()
	config.read('/'.join([context.config_path, 'config']))
	credentials.read('/'.join([context.config_path, 'credentials']))

	profile_name = context.profile
	# TODO: Update profile
	# if(profile_name in config or profile_name in context):
	# 	print('The selected profile exist. Would you like to update it? (y/n): ')
	# 	choice = input().lower()
	# 	if(choice != 'y'):
	# 		sys.exit()

	# TODO: Use getpass
	# TODO: Input in one line
	print('AWS Access Key ID: ')
	aws_access_key_id = input()
	
	print('AWS Secret Access Key: ')
	aws_secret_access_key = input()

	print('AWS MFA Device ARN')
	aws_mfa_device_arn = input()

	print('Default region name: ')
	aws_region = input()

	print('Default output format: ')
	aws_output_format = input()

	# TODO: Update profle as one object
	if (aws_mfa_device_arn != ''):
		profile_name = '-'.join([profile_name, 'mfa'])

	config[profile_name] = {}
	config[profile_name]['region'] = aws_region
	config[profile_name]['output'] = aws_output_format

	credentials[profile_name] = {}
	credentials[profile_name]['aws_access_key_id'] = aws_access_key_id
	credentials[profile_name]['aws_secret_access_key'] = aws_secret_access_key

	if (aws_mfa_device_arn != ''):
		credentials[profile_name]['aws_mfa_device_arn'] = aws_mfa_device_arn

	# TODO: Add non-mfa config profile
	with open(config_path, 'w') as configfile:
		config.write(configfile)

	with open(credentials_path, 'w') as credentialsfile:
		credentials.write(credentialsfile)

def auth_mfa(context):
	credentials_path = os.path.join(context.config_path, 'credentials')

	if (not os.path.exists(credentials_path)):
		print('Could not locate a credentials file in {config_path}.'.format(config_path=context.config_path))
		print('Please provide a path that contains a valid aws credentials and config file.')
		sys.exit()

	credentials = configparser.ConfigParser()
	credentials.read('/'.join([context.config_path, 'credentials']))

	profile_name_mfa = '-'.join([context.profile, 'mfa'])
	if(profile_name_mfa not in credentials):
		print('The selected profile does not exist. Please create one.')
		sys.exit()

	session = boto3.Session(profile_name=profile_name_mfa)

	sts_client = session.client('sts')
	profile_name='dev'
	response = sts_client.get_session_token(
		# TODO: Add token ttl
		# DurationSeconds=context.token_ttl,
		SerialNumber=credentials[profile_name_mfa]['aws_mfa_device_arn'],
		TokenCode=context.mfa
	)

	# TODO: Handle exceptions
	credentials[context.profile] = {
		'aws_access_key_id': response['Credentials']['AccessKeyId'],
		'aws_secret_access_key': response['Credentials']['SecretAccessKey'],
		'aws_session_token': response['Credentials']['SessionToken'],
		'aws_access_token_expiration': response['Credentials']['Expiration']
	}

	with open(credentials_path, 'w') as credentialsfile:
		credentials.write(credentialsfile)

def run():
	context = parse_arguments()

	print(context)
	if(context.command == 'add'):
		add_profile(context)
		print('Profile added')

	elif(context.command == 'auth-mfa'):
		auth_mfa(context)
		print('Done')
""" Collection of functions regarding AWS config profiles """

import os
import configparser
import sys
import re

def mask_value(value):
    if value is None:
        return value

    return re.sub(r".(?=.{4})", '*', value)

def get_input(prompt, default_value, mask=False):
    existing_value = default_value
    if mask:
        existing_value = mask_value(default_value)

    return input('{} [{}]: '.format(prompt, existing_value)).strip() or default_value

def add(context):
    """ Parse the command line arguments and return a context object """
    credentials_path = os.path.join(context.config_path, 'credentials')
    config_path = os.path.join(context.config_path, 'config')

    if ((not os.path.exists(credentials_path)) or (not os.path.exists(config_path))):
        print('Could not locate a credentials or a config file in \
		{config_path}. Would you like to create them for (y/n): '
			.format(config_path=context.config_path))

        choice = input().lower()
        if choice != 'y':
            print(
                'Please provide a path that contains a valid aws credentials and config file.')
            sys.exit()

    config = configparser.ConfigParser()
    credentials = configparser.ConfigParser()
    config.read('/'.join([context.config_path, 'config']))
    credentials.read('/'.join([context.config_path, 'credentials']))

    profile_name = context.profile_name
    mfa_profile_name = '{}-mfa'.format(profile_name)

    if config.has_section(mfa_profile_name):
        profile_name = mfa_profile_name


    profile_config = config[profile_name] if config.has_section(profile_name) else dict()
    profile_credentials = credentials[profile_name] if credentials.has_section(profile_name) else dict()

    aws_access_key_id = profile_credentials.get('aws_access_key_id', None)
    aws_secret_access_key = profile_credentials.get('aws_access_key_secret', None)
    aws_mfa_device_arn = profile_credentials.get('aws_mfa_device_arn', None)
    aws_region = profile_config.get('region', None)
    aws_output_format = profile_config.get('output', None)

    aws_access_key_id = get_input('AWS Access Key ID', aws_access_key_id, True)
    aws_secret_access_key = get_input('AWS Secret Access Key', aws_secret_access_key, True)
    aws_mfa_device_arn = get_input('AWS MFA Device ARN', aws_mfa_device_arn, True)
    aws_region = get_input('Default region name', aws_region)
    aws_output_format = get_input('Default output format', aws_output_format)

    if aws_mfa_device_arn != '':
        profile_name = '-'.join([profile_name, 'mfa'])

    config[profile_name] = {
        'region': aws_region,
        'output': aws_output_format
    }

    credentials[profile_name] = {
        'aws_access_key_id': aws_access_key_id,
        'aws_secret_access_key': aws_secret_access_key
    }

    if aws_mfa_device_arn != '':
        credentials[profile_name]['aws_mfa_device_arn'] = aws_mfa_device_arn

    with open(config_path, 'w') as configfile:
        config.write(configfile)

    with open(credentials_path, 'w') as credentialsfile:
        credentials.write(credentialsfile)

def delete(context):
    """ Delete an AWS Profile from the config files"""

    credentials_path = os.path.join(context.config_path, 'credentials')
    config_path = os.path.join(context.config_path, 'config')

    if ((not os.path.exists(credentials_path)) or (not os.path.exists(config_path))):
        print('Could not locate a credentials or a config file in \
		{}.'.format(context.config_path))

        sys.exit()

    profile_name = context.profile_name

    choice = input('Are you sure you want to delete the profile with name {}? [y/N] '.format(
        profile_name)).lower()

    if choice != 'y':
        sys.exit()

    config = configparser.ConfigParser()
    credentials = configparser.ConfigParser()
    config.read('/'.join([context.config_path, 'config']))
    credentials.read('/'.join([context.config_path, 'credentials']))

    config.remove_section(profile_name)
    credentials.remove_section(profile_name)

    mfa_profile_name = '{}-mfa'.format(profile_name)
    if config.has_section(mfa_profile_name) or credentials.has_section(mfa_profile_name):
        choice = input('An MFA profile was found ({}). Do you want to delete it as well? [Y/n] '.format(
            mfa_profile_name)).lower()
        if choice == 'n':
            sys.exit()

        config.remove_section(mfa_profile_name)
        credentials.remove_section(mfa_profile_name)

    with open(config_path, 'w') as configfile:
        config.write(configfile)

    with open(credentials_path, 'w') as credentialsfile:
        credentials.write(credentialsfile)

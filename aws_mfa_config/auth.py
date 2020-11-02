""" Collection of auth functions """

import configparser
import os
import sys
import re
import boto3

def read_mfa():
    """ Read an MFA code from the stdin and validate it """
    while True:
        mfa_token = input('MFA: ')
        if re.match(r"^\d{6}$", mfa_token):
            return mfa_token

        print("This doesn't look like an MFA code. Try again.")


def mfa(context):
    """ Authenticate using an MFA code """
    credentials_path = os.path.join(context.config_path, 'credentials')

    if not os.path.exists(credentials_path):
        print('Could not locate a credentials file in {config_path}.'.format(
            config_path=context.config_path))
        print(
            'Please provide a path that contains a valid aws credentials and config file.')
        sys.exit()

    credentials = configparser.ConfigParser()
    credentials.read('/'.join([context.config_path, 'credentials']))

    profile_name_mfa = '-'.join([context.profile_name, 'mfa'])
    if profile_name_mfa not in credentials:
        print('The selected profile ({profile}) does not exist. Please create one.'.format(
            profile=profile_name_mfa))
        sys.exit()

    session = boto3.Session(profile_name=profile_name_mfa)

    sts_client = session.client('sts')

    mfa_token = read_mfa()
    response = sts_client.get_session_token(
        # DurationSeconds=context.ttl,
        SerialNumber=credentials[profile_name_mfa]['aws_mfa_device_arn'],
        TokenCode=mfa_token
    )

    # TODO: Handle exceptions
    credentials[context.profile_name] = {
        'aws_access_key_id': response['Credentials']['AccessKeyId'],
        'aws_secret_access_key': response['Credentials']['SecretAccessKey'],
        'aws_session_token': response['Credentials']['SessionToken'],
        'aws_access_token_expiration': response['Credentials']['Expiration']
    }

    with open(credentials_path, 'w') as credentialsfile:
        credentials.write(credentialsfile)

# AWS MFA Config
An aws configure wrapper tha adds support for MFA protected profiles.

When adding a profile, the wrapper will add a new entry in the credentials and config files
that are generated by `aws configure`. If an MFA device is specified, the profile will have
`-mfa` suffix. When requesting a session through the wrapper, a new profile will be created
using the credentials from `aws get-session-token` without the `-mfa` suffix, including 
a session token and an expiration date.
NOTE: This might lead to overwritting existing profiles.

![GitHub](https://img.shields.io/github/license/gpetrousis/aws-mfa-config)

## Installation
`python3 setup.py install`

### Requirements
boto3

## Usage
`aws-mfa-config add --profile <profile_name>`

`aws-mfa-config auth-mfa --profile <profile_name> --mfa <mfa_pin>`

`aws-mfa-config --help`

## Future improvements
- Improve Readme
- Add meaningfull exit codes
- Add tests
- Do not request new token if the current one is not expired. Support force token update.
- Add support to add non-mfa config profiles
- Handle exceptions
- Add changelog
- Add auto completion
- Capture ctrl+c
- Update setuptools config
- Publish to pypi
- Print nice errors if the arguments are invalid
- Print nice error when the MFA is wrong

## Licence
[MIT](LICENCE)

## Project status
This is the first iteration. It has the bare minimum functionality but it works.

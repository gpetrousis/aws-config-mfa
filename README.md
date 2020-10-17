# AWS MFA Config

An aws configure wrapper tha adds support for MFA protected profiles.

When adding a profile, the wrapper will add a new entry in the credentials and config files
that are generated by `aws configure`. If an MFA device is specified, the profile will have
`-mfa` suffix. When requesting a session through the wrapper, a new profile will be created
using the credentials from `aws get-session-token` without the `-mfa` suffix, including 
a session token and an expiration date.
NOTE: This might lead to overwritting existing profiles.

![GitHub](https://img.shields.io/github/license/gpetrousis/aws-mfa-config.svg)

## Installation
`python3 setup.py install`

### Requirements
boto3

## Usage
`aws-mfa-config add --profile <profile_name>`

`aws-mfa-config auth-mfa --profile <profile_name> --mfa <mfa_pin>`

`aws-mfa-config --help`

## Future improvements
- Do not request new token if the current one is not expired. Support force token update.
- Add default values to the --help command.
- Make --mfa mandatory or add it as a prompt.
- Add update profile support
- Use getpass for credentials
- Move prompts to the same line as the text.
- Update profile as an object and not as separate values.
- Add support to add non-mfa config profiles
- Add token ttl argument
- Handle exceptions
- Add tests
- Add changelog
- Add auto completion

<!-- Authors/Aknowldement -->

<!-- Licence -->
## Licence
[MIT](LICENCE)

<!-- Project status -->
## Project status
This is the first iteration. It has the bare minimum functionality but it works.

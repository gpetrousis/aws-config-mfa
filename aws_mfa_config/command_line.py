import auth
import profile
import aws_mfa_config


def main():
    context = aws_mfa_config.parse_arguments()

    print(context)
    if context.command == 'add':
        profile.add(context)
        print('Profile added')

    elif context.command == 'auth-mfa':
        auth.mfa(context)
        print('Done')

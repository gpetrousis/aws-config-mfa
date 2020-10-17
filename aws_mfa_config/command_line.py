import aws_mfa_config

def main():
	context = aws_mfa_config.parse_arguments()

	print(context)
	if(context.command == 'add'):
		aws_mfa_config.add_profile(context)
		print('Profile added')

	elif(context.command == 'auth-mfa'):
		aws_mfa_config.auth_mfa(context)
		print('Done')
""" Tests for the parse_arguments util function """

from unittest import TestCase

from aws_mfa_config.utils import parse_arguments

class TestParseArguments(TestCase):
    def test_action_add(self):
        # Action add
        context = parse_arguments(['add'])
        self.assertEqual(context.command, 'add')

        # Action auth-mfa
        context = parse_arguments(['auth-mfa'])
        self.assertEqual(context.command, 'auth-mfa')

        # Action invalid

        with self.assertRaises(SystemExit):
            parse_arguments(['invalid'])


    def test_profile(self):
        # Short argument
        context = parse_arguments(['add', '-p', 'foo'])
        self.assertEqual(context.profile, 'foo')

        # Long argument
        context = parse_arguments(['auth-mfa', '--profile', 'bar'])
        self.assertEqual(context.profile, 'bar')

        # Default profile
        context = parse_arguments(['add'])
        self.assertEqual(context.profile, 'default')

    def test_mfa(self):
        # Valid mfa
        context = parse_arguments(['add', '--mfa', '123456'])
        self.assertEqual(context.mfa, 123456)

        # Invalid mfa
        # with self.assertRaises(argparse.ArgumentTypeError):
        #     aws_mfa_config.parse_arguments(['add', '--mfa', 'somemfa'])

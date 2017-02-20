import sys
import subprocess
import os
import socket
import getpass
from slacker import Slacker


SLACK_API_TOKEN = os.environ.get('SLACK_API_TOKEN')
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL', '#experiments-status')


def notify(message, slack_api_token=None, slack_channel=None):
    if slack_api_token is None:
        slack_api_token = SLACK_API_TOKEN

    if slack_channel is None:
        slack_channel = SLACK_CHANNEL

    slack = Slacker(slack_api_token)
    slack.chat.post_message(slack_channel, message, username='Experiment Bot')


def shell(shell_command):
    process = subprocess.run(shell_command, shell=True, stdout=subprocess.PIPE)
    return process.stdout.decode('utf8')


def cli():
    hostname = socket.gethostname()
    user = getpass.getuser()
    command = ' '.join(sys.argv[1:])
    result = shell(command)
    notify('{user}@{hostname} $ {command}\n{result}'.format(
        user=user,
        hostname=hostname,
        command=command,
        result=result
    ))

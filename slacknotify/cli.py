import sys
import subprocess
import os
import socket
import getpass
import time
import datetime
from slacker import Slacker

SLACK_API_TOKEN = os.environ.get('SLACK_API_TOKEN')
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL', '#experiments-status')

COLORS = {
    'green': '#36a64f',
    'light-blue': '#5bc0de',
    'red': '#c9302c',
    'yellow': '#f0ad4e'
}


def notify(message, attachments, slack_api_token=None, slack_channel=None):
    if slack_api_token is None:
        slack_api_token = SLACK_API_TOKEN

    if slack_channel is None:
        slack_channel = SLACK_CHANNEL

    slack = Slacker(slack_api_token)
    slack.chat.post_message(
        slack_channel, message,
        attachments=attachments, username='Experiment Bot'
    )


def create_attachment(title, message, color):
    return {
        'fallback': message,
        'color': COLORS[color],
        'text': message,
        'title': title,
        'mrkdwn_in': ['text']
    }


def shell(shell_command):
    process = subprocess.Popen(shell_command, shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout = ''
    stderr = ''
    while True:
        stdout_nextline = process.stdout.readline()
        stderr_nextline = process.stderr.readline()
        if stdout_nextline == b'' and stderr_nextline == b'' and process.poll() is not None:
            break
        stdout_line = stdout_nextline.decode('utf8')
        stderr_line = stderr_nextline.decode('utf8')
        stdout += stdout_line
        stderr += stderr_line
        sys.stdout.write(stdout_line)
        sys.stdout.flush()
        sys.stderr.write(stderr_line)
    return stdout, stderr, process.returncode


def cli():
    hostname = socket.gethostname()
    user = getpass.getuser()
    command = ' '.join(sys.argv[1:])
    start_time = time.time()
    stdout, stderr, returncode = shell(command)
    total_time = time.time() - start_time
    delta = str(datetime.timedelta(seconds=total_time))
    attachments = []
    input_command = 'User: `{user}`\tHostname: `{hostname}`\t Running Time: `{time}`\nDirectory: ' \
                    '`{pwd}`\n Command: `{command}`'.format(
                                                    user=user,
                                                    hostname=hostname,
                                                    pwd=os.getcwd(),
                                                    command=command,
                                                    time=delta
                                                )
    attachments.append(create_attachment('Command', input_command, 'light-blue'))
    if stdout != '':
        attachments.append(create_attachment('Standard Out', '```\n' + stdout + '```', 'green'))
    else:
        attachments.append(create_attachment('Standard Out', 'No Output', 'green'))
    if returncode != 0:
        if stderr != '':
            attachments.append(create_attachment('Standard Error', '```\n' + stderr + '```', 'red'))
        else:
            attachments.append(create_attachment('Standard Error', 'No Output', 'red'))
    else:
        if stderr != '':
            attachments.append(create_attachment(
                'Standard Error (0 Status Code)', '```\n' + stderr + '```', 'yellow'))
    notify('Command Completed', attachments)

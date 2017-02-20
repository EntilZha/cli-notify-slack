# cli-notify-slack
Simple command line utility that takes any CLI command. When it finishes a notification will be sent to slack that it is done which can be optionally augmented with a message

## Usage

1. Install by cloning the repository and running `python setup.py install`
2. Set the environment variable `SLACK_API_TOKEN` to your API token
3. Set the environment variable `SLACK_CHANNEL` to where you want messages to go
4. Run any command prepended with `notify`. When the command completes a message will be sent to slack using the API token and channel provided via environment variables that includes the user, hostname, command, and output.

For example, running `notify ls` in this repository's directory like

```bash
$ notify ls
```

Will result in the following message to slack

```
pedro@terminus.local $ ls
LICENSE
README.md
setup.py
slacknotify
```

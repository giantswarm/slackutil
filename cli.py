import argparse
import os
import sys
import requests
import re

TOKEN = None
BASE_URL = "https://slack.com/api/"

def get_channels():
    url = BASE_URL + "channels.list"
    params = {"token": TOKEN, "exclude_archived": 1}
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()["channels"]

def join_channel(channel_name):
    url = BASE_URL + "channels.join"
    params = {"token": TOKEN, "name": channel_name}
    r = requests.get(url, params=params)
    r.raise_for_status()

def leave_channel(channel_id):
    url = BASE_URL + "channels.leave"
    params = {"token": TOKEN, "channel": channel_id}
    r = requests.get(url, params=params)
    r.raise_for_status()


if __name__ == "__main__":
    TOKEN = os.getenv("SLACK_TOKEN")

    parser = argparse.ArgumentParser(description='Do things with Slack')
    parser.add_argument('command', metavar='command', help='Can be "join", "leave", or "list".')
    parser.add_argument("--include", dest="include_pattern", nargs="*",
                    help='Regex pattern to use for matching channels to work on')
    parser.add_argument("--exclude", dest="exclude_pattern", nargs="*",
                    help='Regex pattern to use for matching channels to exclude')
    args = parser.parse_args()

    if TOKEN is None:
        sys.stderr.write("Please set the SLACK_TOKEN environment variable.\n")
        sys.stderr.write("Go to https://api.slack.com/docs/oauth-test-tokens to create a new token.\n\n")
        sys.exit(1)

    result_channels = []

    for channel in get_channels():
        # make sure the item matches all include patterns

        if args.include_pattern is not None:
            include_patterns_ok = 0
            for pattern in args.include_pattern:
                if re.match(pattern, channel["name"]) is not None:
                    include_patterns_ok += 1
            if include_patterns_ok != len(args.include_pattern):
                continue

        if args.exclude_pattern is not None:
            exclude_patterns_ok = 0
            for pattern in args.exclude_pattern:
                if re.match(pattern, channel["name"]) is None:
                    exclude_patterns_ok += 1
            if exclude_patterns_ok != len(args.exclude_pattern):
                continue

        result_channels.append(channel)

    # processing result set
    for channel in result_channels:
        if args.command == "leave":
            print("Leaving %s" % channel["name"])
            leave_channel(channel["id"])
        elif args.command == "join":
            print("Joining %s" % channel["name"])
            join_channel(channel["name"])
        elif args.command == "list":
            print(channel["name"])

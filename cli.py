import argparse
import os
import sys
import requests
import re
import json

TOKEN = None
BASE_URL = "https://slack.com/api/"


def get_channels():
    url = BASE_URL + "conversations.list"
    params = {"token": TOKEN, "exclude_archived": 1, "limit":1000}
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()["channels"]


def join_channel(channel_name):
    url = BASE_URL + "conversations.join"
    params = {"token": TOKEN, "name": channel_name}
    r = requests.get(url, params=params)
    r.raise_for_status()


def leave_channel(channel_id):
    url = BASE_URL + "conversations.leave"
    params = {"token": TOKEN, "channel": channel_id}
    r = requests.get(url, params=params)
    r.raise_for_status()


def star_channel(channel_id):
    url = BASE_URL + "stars.add"
    params = {"token": TOKEN, "channel": channel_id}
    r = requests.get(url, params=params)
    r.raise_for_status()


def unstar_channel(channel_id):
    url = BASE_URL + "stars.remove"
    params = {"token": TOKEN, "channel": channel_id}
    r = requests.get(url, params=params)
    r.raise_for_status()


def get_muted_channels():
    url = BASE_URL + "users.prefs.get"
    params = {"token": TOKEN}
    r = requests.get(url, params=params)
    r.raise_for_status()
    data = json.loads(r.text)
    return data["prefs"]["muted_channels"]


def remute_channel(channel_id):
    url = BASE_URL + "chat.command"
    params = {"token": TOKEN, "channel": channel_id, "command": "/mute"}
    r = requests.get(url, params=params)
    r.raise_for_status()


def get_last_message(channel_id):
    url = BASE_URL + "chat.command"
    params = {"token": TOKEN, "channel": channel_id, "command": "/mute"}
    r = requests.get(url, params=params)
    r.raise_for_status()


def auth_test():
    url = BASE_URL + "auth.test"
    params = {"token": TOKEN}
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()["ok"]


if __name__ == "__main__":
    TOKEN = os.getenv("SLACK_TOKEN")
    TOKEN = "xoxp-2171500629-208815728849-1091177369459-4667365003b3bab1b499c9a8a12da7e3"

    parser = argparse.ArgumentParser(description='Do things with Slack')
    parser.add_argument('command', metavar='command',
                        help='Can be "join", "leave", "star", "unstar", "mute", "unmute" or "list".')
    parser.add_argument("--include", dest="include_pattern", nargs="*",
                        help='Regex pattern to use for matching channels to work on')
    parser.add_argument("--exclude", dest="exclude_pattern", nargs="*",
                        help='Regex pattern to use for matching channels to exclude')
    args = parser.parse_args()

    if TOKEN is None or TOKEN == "":
        sys.stderr.write("Please set the SLACK_TOKEN environment variable.\n")
        sys.stderr.write(
            "Go to https://api.slack.com/docs/oauth-test-tokens to create a new token.\n\n")
        sys.exit(1)

    if auth_test() is False:
        sys.stderr.write("Authentication Failed.\n")
        sys.stderr.write("Please set the SLACK_TOKEN environment variable.\n")
        sys.stderr.write(
            "Go to https://api.slack.com/docs/oauth-test-tokens to create a new token.\n\n")
        sys.exit(1)

    result_channels = []
    muted_channels = []

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
            print("{} - {}".format(channel["name"], channel["id"]))
        elif args.command == "star":
            print("Starring %s" % channel["name"])
            star_channel(channel["id"])
        elif args.command == "unstar":
            print("Unstarring %s" % channel["name"])
            unstar_channel(channel["id"])
        elif args.command == "mute":
            if not muted_channels:
                muted_channels = get_muted_channels()
            if channel["id"] not in muted_channels:
                print("Muting %s" % channel["name"])
                remute_channel(channel["id"])
            else:
                print("Channel %s already muted" % channel["name"])

        elif args.command == "unmute":
            if not muted_channels:
                muted_channels = get_muted_channels()
            if channel["id"] in muted_channels:
                print("Unmuting %s" % channel["name"])
                remute_channel(channel["id"])
            else:
                print("Channel %s already unmuted" % channel["name"])

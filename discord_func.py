# TODO   Save message content from all historical messages
# TODO   Remember last message timestamp
# TODO   Only download new messages


import requests
import json

from decouple import config
from pprint import pprint


def retrieve_messages(channel_id):
    headers = {"authorization": config("discord_auth")}
    r = requests.get(
        f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=5",
        headers=headers,
    )
    jsonn = json.loads(r.text)
    for value in jsonn:
        content = value["content"]
        # print(content)
        print(value["timestamp"])


retrieve_messages(config("discord_channel_id"))

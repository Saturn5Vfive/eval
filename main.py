import base64
import ctypes
import sys
import threading
import discord
from pyfiglet import Figlet
import hashlib
import discord
from discord import Message
import random
import traceback
import string
import requests
import json
from discord.ext import commands

TOKEN = None # PUT YOUR ACCOUNT TOKEN HERE
out = ""
msg = None

super_properties = {
    "os":"Windows",
    "browser":"Chrome",
    "device":"",
    "system_locale":"en-US",
    "browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    "browser_version":"97.0.4692.99",
    "os_version":"10",
    "referrer":"https://discord.com/",
    "referring_domain":"discord.com",
    "referrer_current":"",
    "referring_domain_current":"",
    "release_channel":"stable",
    "client_build_number": 113584,
    "client_event_source": None
}

client = commands.Bot(command_prefix="~", self_bot=True, fetch_offline_members = False)

def historyBackend(channel, token, guild_id, limit=50):
    #https://discord.com/api/v9/channels/889246102635806760/messages?limit=50
    headers = {
        "accept":"*/*", 
        "accept-encoding": "gzip, deflate, br", 
        "accept-language": "en-US,en;q=0.9", 
        "authorization": f"{token}", 
        "origin":"https://discord.com", 
        "referer": f"https://discord.com/channels/{guild_id}/{channel}", 
        "sec-ch-ua":"\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"97\", \"Chromium\";v=\"97\"", 
        "sec-ch-ua-mobile":"?0", 
        "sec-ch-ua-platform":"\"Windows\"", 
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
        "x-debug-options": "bugReporterEnabled",
        "x-discord-locale":"en-US",
        "x-super-properties": base64.b64encode(json.dumps(super_properties).encode('ascii')).decode('ascii')
    }
    re = requests.get(f"https://discord.com/api/v9/channels/{channel}/messages?limit={limit}", headers=headers)
    return json.loads(re.text)

def sendChatMessage(message, guild_id, channel_id, token, tts):
    global tokens
    nonce = random.randint(0, 1000000000000000000)
    payload = {"nonce": nonce, "tts": tts, "content": message}
    headers = {
        "accept":"*/*", 
        "accept-encoding": "gzip, deflate, br", 
        "accept-language": "en-US,en;q=0.9", 
        "authorization": f"{token}", 
        "content-length": str(len(json.dumps(payload))), 
        "content-type": "application/json", 
        "origin":"https://discord.com", 
        "referer": f"https://discord.com/channels/{guild_id}/{channel_id}", 
        "sec-ch-ua":"\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"97\", \"Chromium\";v=\"97\"", 
        "sec-ch-ua-mobile":"?0", 
        "sec-ch-ua-platform":"\"Windows\"", 
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
        "x-debug-options": "bugReporterEnabled",
        "x-discord-locale":"en-US",
        "x-super-properties": base64.b64encode(json.dumps(super_properties).encode('ascii')).decode('ascii')
    }
    re = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers, json=payload)

def push(message, tts=False):
    sendChatMessage(message, msg.channel.guild.id, msg.channel.id, TOKEN, tts)

def history(channel=msg.channel.id, limit=50):
    return historyBackend(channel, TOKEN, msg.channel.guild.id, limit=limit)

def printf(text):
    sys.stdout.write(str(text) + "\n")

def print(text):
    global out
    out += str(text) + "\n"

def encode(text: str):
    return base64.b64encode(text.encode()).decode()

def decode(text: str):
    return base64.b64decode(text.encode()).decode()

@client.event
async def on_message(message: Message):
    global out, msg
    if message.author.id == client.user.id:
        msg = message
        try:
            if message.content.startswith("!eval"):
                out = ""
                out = eval(message.content[5::].strip().strip("\r").strip("\n"))
                if len(str(out)) != 0:
                    await message.edit(content=str(out))
                return
            if message.content.startswith("!->>"):
                out = ""
                exec("global msg\n" + message.content[4::].strip().strip("\r").strip("\n"))
                if len(str(out)) != 0:
                    await message.edit(content=str(out))
                return
            if message.content.startswith("!->"):
                out = ""
                out = eval(message.content[3::].strip().strip("\r").strip("\n"))
                if len(str(out)) != 0:
                    await message.edit(content=str(out))
                return
            if message.content.startswith("!exec"):
                out = ""
                exec("global msg\n" + message.content[5::].strip().strip("\r").strip("\n"))
                if len(str(out)) != 0:
                    await message.edit(content=str(out))
                return
        except Exception as e:
            t = f"{traceback.format_exc()}\n{str(e)}"
            await message.channel.send(t)

client.run(TOKEN, bot=False)

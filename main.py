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
from functions import *

TOKEN = ""
out = ""
msg = None

client = commands.Bot(command_prefix="~", self_bot=True, fetch_offline_members = False)

def push(message, tts=False):
    sendChatMessage(message, msg.channel.guild.id, msg.channel.id, TOKEN, tts)

def history(channel=None, limit=50):
    if channel == None:
        channel = msg.channel.id
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



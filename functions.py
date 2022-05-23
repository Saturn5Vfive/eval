import base64
import sys
import random
import requests
import json

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
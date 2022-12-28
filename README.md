# python-twitter-notification-system

## About

This is a Python script that can be used in a cog. This script will send you in your Discord a Twitch notification from people you can define in a config, you can also choose a channel where you want to send the notification and a role you want to tag.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install asyncio, py-cord, tweepy
```

## Usage

### 1. ClientID and the ClientSecret
[![Watch the video](https://i.imgur.com/vKb2F1B.png)](https://www.youtube.com/watch?v=gonG7_ffwsk)

### 2. The Code

### 2.1
The script is a cog and therefore must be placed in a `cog directory`

```python
import discord
import asyncio
import tweepy
import json

from discord.ext import commands
from discord.ext import tasks

def get_config(name):
    with open("./config.json", "r") as f:
        json_file = json.load(f)
        return json_file[name]

auth = tweepy.OAuthHandler(str(get_config("twitter")["api-key"]), str(get_config("twitter")["api-key-secret"]), str(get_config("twitter")["access-token"]), str(get_config("twitter")["access-token-secret"]))
api = tweepy.API(auth)

ping_role = xxx #Paste here You Ping role
feed_channel = xxx #Paste here You Channel-ID

global tweet_var
tweet_var = "None"

class Linstener(tweepy.Stream):
    tweets = []
    def on_status(self, status):
        global tweet_var
        self.tweets.append(status)
        if status.user.screen_name in users:
            id = status.id_str
            tweet_var = f"https://twitter.com/{status.user.screen_name}/status/{id}"
        else:
            return

stream_tweet = Linstener(str(get_config("twitter")["api-key"]), str(get_config("twitter")["api-key-secret"]),
                         str(get_config("twitter")["access-token"]), str(get_config("twitter")["access-token-secret"]))

users = ["EpicGames", "XboxDach", "Minecraft", "Partymann2000"]
user_ids = []

for user in users:
    user_ids.append(api.get_user(screen_name=user).id)

stream_tweet.filter(follow=user_ids, threaded=True)


class twitter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_twitter.start()

    @tasks.loop(seconds=2)
    async def check_twitter(self):
        global tweet_var
        result = tweet_var
        if result != "None":
            channel = self.bot.get_channel(feed_channel)
            #Nutz die 2 Unteren umd die Nachircht in einem Annoucment channel zu senden
            #msg = await channel.send(f"<@&{ping_role}> \n" + result )
            #await msg.publish()
            await channel.send(f"<@&{ping_role}> \n" + result )
            tweet_var = "None"
            return

def setup(bot):
    bot.add_cog(twitter(bot))
```

### 2.2
The next one is a part of a `config` and has to be added to your `config.json` or you just take the file from here (just put it into the directory where the `main.py` is)

```json
{
	"twitter": {
        "api-key": "xxx",
        "api-key-secret": "xxx",
        "bearer-token": "xxx",
        "access-token": "xxx",
        "access-token-secret": "xxx"
    }
}
```

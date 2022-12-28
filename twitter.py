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

game_feed_role = 789237798082707516
game_feed_channel = 813325126232834098

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

#test = api.home_timeline()
#print(test)

stream_tweet = Linstener(str(get_config("twitter")["api-key"]), str(get_config("twitter")["api-key-secret"]),
                         str(get_config("twitter")["access-token"]), str(get_config("twitter")["access-token-secret"]))

users = ["EpicGames", "XboxDach", "Minecraft", "Xenority"]
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
            channel = self.bot.get_channel(game_feed_channel)
            #Nutz die 2 Unteren umd die Nachircht in einem Annoucment channel zu senden
            #msg = await channel.send(f"<@&{game_feed_role}> \n" + result )
            #await msg.publish()
            await channel.send(f"<@&{game_feed_role}> \n" + result )
            tweet_var = "None"
            return

def setup(bot):
    bot.add_cog(twitter(bot))
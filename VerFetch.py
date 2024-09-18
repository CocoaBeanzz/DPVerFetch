# VerFetch Version Control Fetch
# v1.0.1
# K Preston

# Web Requests
import requests
import feedparser
import urllib.request

# Webhook
import discord

# Parsing Tools
import time
import re

# Environment variables
import os
from dotenv import load_dotenv
load_dotenv()

# Interpret repository type.
repoType = str(os.environ.get("TYPE").lower())
if repoType == 'git':
    repoType = '-git'
elif repoType == 'svn':
    repoType = ''
else:
    print("Unrecognized repository type: " + repoType)

# Stash RSS info.
auth = urllib.request.HTTPBasicAuthHandler()
RSS = "https://trac" + repoType + ".digipen.edu/projects/" + str(os.environ.get("REPO")) + "/log/?verbose=on&format=rss"
domain = RSS.split("/")[2].split(".")[-2]
auth.add_password(domain, RSS.split("/")[2].split("."), str(os.environ.get("USR")), str(os.environ.get("PASS")))

# Version Update Discord Message Object
class Post:

    # webhook (String): Discord webhook URL string
    # entry (Entry): RSS Entry object
    def __init__(self, webhook, entry):
        self.webhook = webhook
        self.entry = entry

    # Prepare stashed data and send message.
    def prepare_and_notify(self):
        self.__notify_to_discord_channel(self.entry)

    # Send message with the given data.
    # data (Entry): RSS Entry object for which to compose message
    def __notify_to_discord_channel(self, data):
        headers = { "Content-Type": "application/json" }

        # Populate Embed object.
        embed = discord.Embed()
        embed.set_author(name=data["author"])
        embed.title = data["title"].split(":")[0]
        embed.description = re.sub("<.*>", "", data["description"]).replace("\n\n","\n")
        # Collapse doubled newlines.
        while "\n\n" in embed.description:
            embed.description = embed.description.replace("\n\n", "\n")
        embed.url = data["link"]
        embed.set_footer(text=str(data["published"]))

        # Prepare message payload.
        embeds = [discord.Embed.to_dict(embed)]
        payload = {
            "embeds": embeds
        }

        # Print to console.
        print(embed.author)
        print(embed.title)
        print(embed.description)
        print(embed.url)
        print(embed.footer)
        #print(data["id"])
        #print(discord.Embed.to_dict(embed))

        # Send Discord message.
        return requests.post(url=self.webhook, headers=headers, json=payload)

# Get the ID of the last reported version update.
file = open("lastID", "r")
lastID = file.read()
file.close()

# Loops every 30 seconds.
while 1:
    
    # From https://pythonhosted.org/feedparser/http-authentication.html#example-auth-inline-digest
    # "The easy but horribly insecure way"
    try:
        # Get RSS feed.
        feed = feedparser.parse("https://" + str(os.environ.get("USR")) + ":" + str(os.environ.get("PASS")) + "@" + str(str(os.environ.get("RSS")).split("//")[1]))

        # New lastID is latest entry. Don't change old var yet, that's the endpoint.
        newLastID = feed.entries[0]["id"]
        file = open("lastID", "w")
        file.write(lastID)
        file.close()

        # Send messages for each update until a previously sent update is found.
        for entry in feed.entries:
            
            # If this entry is the same as last time we checked...
            # OR if this is the first time we're checking this feed...
            if(entry["id"] == lastID or len(lastID) == 0):
                # Save new last entry ID and break.
                lastID = newLastID
                break
            # If this entry has not been seen before...
            else:
                # Prepare and send a Discord message for this update.
                post = Post(os.environ.get("HOOK"), entry)
                post.prepare_and_notify()

    # Print exceptions to console.            
    except Exception as e:
        print("Failed: ", e, ". Retrying...")
        
    time.sleep(30)

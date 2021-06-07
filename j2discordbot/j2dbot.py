import discord
import json

# Load the configuration
with open('config.json') as config_file:
    config = json.load(config_file)

# Derive the client from discord.Client.
class J2DClient(discord.Client):
    
    # Print that we're connected. Yes, this is from the example at: https://discordpy.readthedocs.io/en/stable/intro.html
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    # Save all received lines to the logfile.
    async def on_message(self, message):
        with open(config['message-log-file'], "a") as appendfile:
            appendfile.write('#{0.channel} | {0.author} : {0.content}\n'.format(message))

# Load the client.
client = J2DClient()
client.run(config['discord-token'])

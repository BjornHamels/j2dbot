import discord
import json

# Load the configuration
with open('config.json') as config_file:
    config = json.load(config_file)

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))


print("Lets go!")

client = MyClient()
client.run(config['discord-token'])

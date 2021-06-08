import discord
import json
import logging

# Load the configuration
with open("config.json") as config_file:
    config = json.load(config_file)

# Set up the logger.
logging.basicConfig(level=config["python-loging-level"])
logging.info("Logger started")
logging.debug(f"Config: {config}")

# Derive the client from discord.Client.
class J2DClient(discord.Client):
    
    # Print that we"re connected. Yes, this is from the example at: https://discordpy.readthedocs.io/en/stable/intro.html
    async def on_ready(self):
        logging.info("Logged on as `{0}`!".format(self.user))

    # Save all received lines to the logfile.
    async def on_message(self, message):
        with open(config["message-log-file"], "a") as appendfile:
            logging.debug(f"Received: {message}")
            appendfile.write("#{0.channel} | {0.author} : {0.content}\n".format(message))

# Load the client.
logging.debug("Starting the client.")
client = J2DClient()
client.run(config["discord-token"])

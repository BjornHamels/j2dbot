import discord
import json
import logging
from sleekxmpp import ClientXMPP


# Load the configuration
with open("config.json") as config_file:
    config = json.load(config_file)

# Set up the logger.
logging.basicConfig(level=config["python-loging-level"])
logging.info("Logger started")
logging.debug(f"Config: {config}")


# Derive the client from discord.Client.
class DiscordClient(discord.Client):
    
    # Print that we"re connected. Yes, this is from the example at: https://discordpy.readthedocs.io/en/stable/intro.html
    async def on_ready(self):
        logging.info("Discord: logged on as `{0}`!".format(self.user))

    # Save all received lines to the logfile.
    async def on_message(self, message):
        with open(config["message-log-file"], "a") as appendfile:
            logging.info(f"Discord: received: {message}")
            appendfile.write("#{0.channel} | {0.author} : {0.content}\n".format(message))


# Derive the client from ClientXMPP.
class ListenBot(ClientXMPP):

    # Constructor to set both handlers. You need the presence and roster to "go online". Adapted from: https://pypi.org/project/sleekxmpp/
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

    def session_start(self, event):
        logging.info("Jabber: session started.")
        self.send_presence()
        self.get_roster()

    # Log all received lines.
    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            logging.info(f"Jabber: received: {msg}")


# Entrypoint.
if __name__ == '__main__':
    logging.debug("Starting both clienst.")

    # Load the jabber client.
    xmpp = ListenBot(config["jabber-jid"], config["jabber-password"])
    xmpp.connect()
    xmpp.process(block=False)

    # Load the discord client.
    client = DiscordClient()
    client.run(config["discord-token"])

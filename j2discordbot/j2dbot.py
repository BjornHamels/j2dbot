from discord import Webhook, RequestsWebhookAdapter
from sleekxmpp import ClientXMPP
import json
import logging


# Load the configuration
with open("config.json") as config_file:
    config = json.load(config_file)
discordgreet = config["discord-greet-connect"]
discordwebhook = config["discord-webhook"]
discordpostmsg = config['discord-post-msg']
discordpremsg = config['discord-pre-msg']
jabberforwardfromjid = config["jabber-forward-from-jid"]
pythonloginglevel = config["python-loging-level"]

# Set up the logger.
logging.basicConfig(level=pythonloginglevel)
logging.info("Logger started")
logging.debug(f"Config: {config}")

# Discord webhooks are ideal if you want to push content to a channel.
webhook = Webhook.from_url(url=discordwebhook, adapter=RequestsWebhookAdapter())

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
        if len(discordgreet) > 0:
            webhook.send(discordgreet)

    # Forward all received lines.
    def message(self, msg):
        if (msg['type'] == 'chat') and (msg['from'].bare == jabberforwardfromjid):
            logging.info(f"Jabber: received: {msg}")
            msg = f"{discordpremsg}```{msg['body']}```{discordpostmsg}"
            webhook.send(msg)


# Entrypoint.
if __name__ == '__main__':

    # Connect the jabber client, blocking.
    xmpp = ListenBot(config["jabber-jid"], config["jabber-password"])
    xmpp.connect()
    xmpp.process(block=True)

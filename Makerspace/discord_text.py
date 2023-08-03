########################################################################
# discord_text
#
# DIRECTIONS to set up discord webhook
# [1] create a discord server
# [2] create a channel in your discord server to send the bot messages
# [2] go to Server Settings -> Integrations
# [3] click on Webhooks -> New Webhook
# [4] click on the webhook that was automatically created for you
# [5] edit the name and channel
# [6] click on Copy Webhook URL
# [7] you can now use that webhook url in the pagingDiscordServer function to send a bot message
# [8] you'll probably want to include your url in app.py
#
# REFERENCES
# [1] https://amunategui.github.io/discord-pager/index.html
########################################################################
import json
import requests


# send text to discord server webhook [R1]
def PagingDiscordServer(webhook_url, text_message):
    return requests.post(webhook_url, data=json.dumps({"content": text_message}),
                         headers={'Content-Type': 'application/json', })


if __name__ == '__main__':
    # EXAMPLE to send text to your discord webhook
    your_webhook_url = 'https://discord.com/api/webhooks/1102005034067173487/upAZ8En1k0z2KVQOYt_fD1IX05gz2H9vCACnxXNIwuRxLY-NccI2l9_EQ1tXSrmRzJfX'
    PagingDiscordServer(your_webhook_url, 'this is the message that will be sent')

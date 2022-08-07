# Telegram Message Forwarder Bot
# Requirements : telethon <pip install telethon>
# Catz - Sun, Aug  7, 2022  2:55:03 PM

####### CONFIG ##############
api_id = 10000000
api_hash = "xxxxxxxxxxxxxxxxxxxxxxxxxx"
bot_token = "00000:xxxxxxxxxxxxxxxxxxxxx"
#############################

from telethon import events
from telethon.sync import TelegramClient

@events.register(events.NewMessage)
async def forwarder(event):
    if event.is_private:
        person = await event.get_chat()
        if not event.message.text.startswith("/"):
            try:
                await bot.send_message(person.id, event.message)
            except Exception as x:
                print(x)
    elif event.mentioned == True:
        await event.delete()
        message = await event.get_reply_message()
        try:
            await bot.send_message(event.to_id, message)
        except Exception as x:
            print(x)

bot = TelegramClient('ForwardBot', int(api_id), api_hash).start(bot_token=bot_token)
with bot:
    bot.add_event_handler(forwarder)

bot.start()
print("ForwardBot Started...")
bot.run_until_disconnected()

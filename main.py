import discord
from discord.ext import commands
import asyncio
import random
import os
import aiohttp
from keep_alive import keep_alive
keep_alive()

intents = discord.Intents.all()
prefixes = ["&"]
bot = commands.Bot(command_prefix=prefixes, intents=intents)

async def fetch_user_messages(session, channel, author, mentions, history_limit):
    user_messages = []
    async for msg in channel.history(limit=history_limit):
        if msg.author == author and 1127148828403957861 not in [mention.id for mention in msg.mentions]:
            msg_content = msg.content.strip()
            if msg_content:
                user_messages.append(msg_content)
    return user_messages

async def process_message(message, bot_emojis, cleaned_content):
    channel = message.channel

    async with channel.typing():
        history_limit = random.randint(1, 10000)

        async with aiohttp.ClientSession() as session:
            user_messages = await fetch_user_messages(session, channel, message.author, message.mentions, history_limit)

        if user_messages:
            random_message_content = random.choice(user_messages)

            excluded_emojis = [
                "baslamaBar", "baslangicBar", "bosBitisBar", "bosBar",
                "doluBar", "doluBitisBar", "loading_bg", "loading",
                "exclamation_mark", "error", "death_note53", "animeyay",
                "1037831738707165214", "850656705322156052",
                "Wheel_No", "Wheel_No1", "Wheel_No2", "Wheel_No3", "Wheel_No4", "Wheel_No5",
                "Wheel_No6", "Wheel_Yes", "Wheel_Yes1", "Wheel_Yes2", "Wheel_Yes3", "Wheel_Yes4",
                "Wheel_Yes5", "Wheel_Yes6", "Wheel_Yes7", "Wherl_No7", "gatito_loading", "no",
                "sucess", "yes", "check", "outputonlinegiftools", "christimas_floppa_enter", "christimas_floppa_exit", "floppa_enter", "floppa_enter", "alert2", "3_", "1_", "2_"
            ]

            # Get a random emoji from any server the bot has joined (excluding the specified ones)
            emoji = random.choice([e for e in bot_emojis if e.name not in excluded_emojis])

            # Send the random emoji at the end of the same message with a blank space
            await message.reply(f"{random_message_content} {str(emoji)}")
        else:
            await message.reply('a')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Check if the message is from a DM channel
    if isinstance(message.channel, discord.DMChannel):
        return

    # Check if the bot is mentioned but not directly by its mention or @everyone/@here
    mentioned_users = [user.id for user in message.mentions]
    if bot.user.id in mentioned_users and not any(mention in ('@everyone', '@here') for mention in message.content.split()):
        bot_emojis = bot.emojis
        # Remove the bot's mention before processing the message
        cleaned_content = message.content.replace(f"<@{bot.user.id}>", "").replace(f"<@!{bot.user.id}>", "")
        await process_message(message, bot_emojis, cleaned_content)

    await bot.process_commands(message)

@bot.event
async def on_disconnect():
    print("Bot disconnected. Reconnecting...")

@bot.event
async def on_error(event, *args, **kwargs):
    print(f"Error in {event}: {args[0]}")
    if isinstance(args[0], discord.ConnectionClosed):
        print("Reconnecting...")
        await asyncio.sleep(5)
        await bot.login(token=token, bot=True)
        await bot.connect()

token = os.getenv("token")

if token is None:
    print("Error: Token not found in environment variables.")
else:
    bot.run(token)

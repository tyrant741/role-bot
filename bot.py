import discord
from discord.ext import commands, tasks
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ROLE_NAME = "did not use spy ops"        # Change this to the role name you want
CHANNEL_ID = 1426153091786608651  # Replace with the channel ID

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    assign_role_daily.start()

@tasks.loop(hours=24)
async def assign_role_daily():
    for guild in bot.guilds:
        role = discord.utils.get(guild.roles, name=ROLE_NAME)
        if role:
            for member in guild.members:
                if role not in member.roles:
                    await member.add_roles(role)

@bot.event
async def on_message(message):
    if message.channel.id == CHANNEL_ID and not message.author.bot:
        role = discord.utils.get(message.guild.roles, name=ROLE_NAME)
        if role in message.author.roles:
            await message.author.remove_roles(role)
    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))

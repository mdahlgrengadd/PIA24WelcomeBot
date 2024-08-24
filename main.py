import discord
from dotenv import load_dotenv
from discord.ext import commands
from responses import get_response
import json
import os

# Get configuration.json
with open("configuration.json", "r") as config: 
	data = json.load(config)
	load_dotenv()
	token = os.getenv('DISCORD_TOKEN') #data["token"]
	prefix = data["prefix"]
	owner_id = data["owner_id"]


class Greetings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None

# Intents
intents = discord.Intents.default()
intents.message_content = True
# The bot
bot = commands.Bot(prefix, intents = intents, owner_id = owner_id)

# Load cogs
if __name__ == '__main__':
	for filename in os.listdir("Cogs"):
		if filename.endswith(".py"):
			bot.load_extension(f"Cogs.{filename[:-3]}")

@bot.event
async def on_ready():
	print(f"We have logged in as {bot.user}")
	print(discord.__version__)
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"{bot.command_prefix}help"))

async def send_message(message: discord.Message, user_message:str) -> None:
	if not user_message:
		print('(Message empty. Is intents enabled?)')
		return
	if is_private := user_message[0] == '?':
		user_message = user_message[1:]

	try:
		response = get_response(user_message)
		await message.author.send(response) if is_private else await message.channel.send(response)
	except Exception(e):
		print(e)

@bot.event
async def on_message(message: discord.Message) -> None:
	if message.author == bot.user:
		return
	
	username = str(message.author)
	user_message = message.content
	channel = str(message.channel)

	print(f'[{channel}] {username}: "{user_message}')
	await send_message(message, user_message)

@bot.event
async def on_member_join(member):
	#channel = bot.get_channel(790274325533378682)
	#embed=discord.Embed(title="Welcome!",description=f"{member.mention} Just Joined")
	await member.send(f'Välkommen {member.mention}! Hoppas du ska trivas!')

bot.run(token)
import discord
from dotenv import load_dotenv
from discord.ext import commands
from image_response import generate_image
import json
import os

# Okänslig konfig från configuration.json
with open("configuration.json", "r") as config: 
	data = json.load(config)

	prefix = data["prefix"] # Vilket prefix som används för kommandon
	owner_id = data["owner_id"]

	# Ladda känslig konfig som exvis 'token' från en .env fil
	load_dotenv()
	token = os.getenv('DISCORD_TOKEN')

class Greetings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None

# Intents - Vad vill kunna göra
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=prefix, intents = intents, owner_id = owner_id)

if __name__ == '__main__':
	for filename in os.listdir("Cogs"):
		if filename.endswith(".py"):
			bot.load_extension(f"Cogs.{filename[:-3]}")

@bot.event
async def on_ready():
	print(f"Inloggad som {bot.user}")
	print(discord.__version__)
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"{bot.command_prefix}help"))

# Hälsa användare välkomna med ett privat meddelande
@bot.event
async def on_member_join(member):
	await member.send(f'Välkommen {member.mention}! Hoppas du ska trivas!')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hej, {ctx.author.name}!')

# Generera en bild med hjälp av stable diffusion
@bot.command()
async def generate(ctx):
	# Tar för mkt datorkraft
	#await generate_image(ctx)
	return

bot.run(token)
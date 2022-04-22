import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

import database
import queries

bot = commands.Bot(command_prefix='!beej ')

# print("updating database")
# database.update_db()
# print("database updated")

@bot.command()
async def test(ctx):
    response = database.get_list()
    await ctx.author.send(response)

@bot.command()
async def hi(ctx):
    message = "Whats up fucker"
    await ctx.author.send(message)

@bot.command()
async def secret(ctx):
    message = "This message will self destruct in 5 seconds"
    await ctx.send(message, delete_after=5.0)

@bot.command()
async def query(ctx):
    x = ctx.message.content[12:]
    query = queries.create_query(x)
    ret = database.get_list(query)
    await ctx.author.send(ret, delete_after=60.0)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
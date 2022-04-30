import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

import database
import queries

bot = commands.Bot(command_prefix='!beej ')

@bot.command()
async def list(ctx):
    ret = database.get_beej_list()
    await ctx.author.send(ret, delete_after=60.0)

@bot.command()
async def query(ctx):
    x = ctx.message.content[12:]
    query = queries.create_query(x)
    ret = database.get_list(query)
    await ctx.author.send(ret, delete_after=60.0)

@bot.command()
async def update(ctx):
    if ctx.author.id == 80714818876608512:
        print("updating database")
        database.update_db()
        print("database updated")

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
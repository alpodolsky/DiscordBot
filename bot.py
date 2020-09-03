import os
import discord as d

from dotenv import load_dotenv as ld
from discord.ext import commands, tasks
from discord import Embed
from itertools import cycle

status = cycle([' in my birdbath', ' for a cracker', ' a melody', 
                ' migration to a better life'])
emojis = ["1️⃣", "2⃣", "3⃣", "4⃣", "5⃣",
		   "6⃣", "7⃣", "8⃣", "9⃣", "🔟"]
ld()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

@bot.event
async def on_ready():
    change_status.start()
    print('Polly is ready to fly.')

@tasks.loop(hours = 1)
async def change_status():
    await bot.change_presence(activity = d.Game(next(status)))
    

@bot.command()
async def poll(ctx, *, messages):
    if ctx.author == bot.user:
        return 

    response = ''
    stringList = messages.split(", ")
    count = 0
    for i in stringList:
        response+= emojis[count] + ' for:   ' + i + '\n'
        count+=1
    
    msg = await ctx.send(response)
    for i in emojis[:count]:
        await msg.add_reaction(i)


#do error handling somehow
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Unknown or invalid command.\nType !help for list of commands')

@poll.error
async def poll_error(ctx, error):
    await ctx.send("Missing options, please try again")

@bot.command()
#create a help command, lists all other command options
async def help(ctx):
    if ctx.author == bot.user:
        return
    response = ''
    commandList=['!poll (options separated by ",") to start a poll\n'
                ,'poll supports max of 10 options\n'
                ]
    for i in commandList:
        response+=i
    await ctx.send(response)

bot.run(TOKEN)
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import requests
import sys
from pathlib import Path
from anime import anime

key = open('key.txt').readline().rstrip('\n')
bot = commands.Bot(command_prefix='$$')

@bot.event
async def on_ready():
    await bot.change_presence(game = discord.Game(name='with catnip'))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-------')

@bot.command(pass_context = True)
async def BOOST(ctx):
    await bot.say("https://i.imgur.com/Yvf3htW.gif")

@bot.command(pass_context = True)
async def trap(cxt):
    await bot.say("<:jack:403983194996736031>")

@bot.event
async def on_message(message):
    if message.author.id != bot.user.id:
        if 'osu.ppy.sh' in message.content:
                await bot.send_message(message.channel, 'Work in progress')
    await bot.process_commands(message)

@bot.command(pass_context = True)
async def boost(ctx):
    await bot.say("https://b.catgirlsare.sexy/QwAa.jpg")


@bot.command(pass_context = True)
async def a(ctx):
    split_message = ctx.message.content.split('\n').pop(0).split(' ')
    #split_message = ctx.message.content.split(' ')
    del split_message[0]
    split_message = ' '.join(split_message)

    embed = anime(split_message)
    await bot.say(embed=embed)
bot.run(key)

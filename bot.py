import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix='#')

@client.event
async def on_ready():

    print("==============READY===================")
    game = discord.Game("자가진단 매크로 테스트")
    await client.change_presence(status = discord.Status.online, activity = game)

@client.command(name="경로")
async def account(ctx):
    try:
        embed = discord.Embed(title = os.getcwd(),
        color = discord.Color.green()
        )
        await ctx.channel.send(embed=embed)

    except Exception as ex:
            
            embed = discord.Embed(title = "Failed",
            description = "#BeatifulSoup", color = discord.Color.red()
            )
            await ctx.channel.send(embed=embed)
            await ctx.channel.send(ex)
            
client.run(os.environ['token'])

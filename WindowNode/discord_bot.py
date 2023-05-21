import discord
import serial
from discord.ext import commands

ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)


@bot.command()
async def turnOffWindowGuard(ctx):
    ser.write(b'0')
    await ctx.send("You have turned off window guard")


@bot.command()
async def turnOnWindowGuard(ctx):
    ser.write(b'1')
    await ctx.send("You have turned on window guard")


bot.run("MTA5MjY1MzIyNDQ0MTQxMzY0Mg.GNYzVr.aty_mv8zMx0AoYUWfSMpMBj_xoaxiB_wSV6qUs")

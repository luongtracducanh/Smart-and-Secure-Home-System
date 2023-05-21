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


bot.run("ENTER_YOUR_API_KEY")

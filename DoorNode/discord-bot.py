import time

import discord
import serial
from discord.ext import commands

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    print("Bot is ready.")


@bot.command()
async def howto(ctx):
    await ctx.send(
        "Use the following commands:\n\nTo view the latest data: /data\nTo view the temperature: /temperature\nTo view the humidity: /humidity\nTo view the gas level: /gas\nTo open the door: /openDoor [password]\nTo set the temperature threshold: /setTemperature [temperature]\nTo set the humidity threshold: /setHumidity [humidity]\nTo set the gas threshold: /setGas [gas]\nTo turn on all weather alerts: /turnOn\nTo turn off all weather alerts: /turnOff\nTo turn off window guard: /turnOffWindowGuard\nTo turn on window guard: /turnOnWindowGuard")


@bot.command()
async def openDoor(ctx, password):
    if str(password) == "235689#":
        ser.write(b"1")
        await ctx.send("You have opened the door. It will be automatically locked within 18 seconds.")
        time.sleep(19)
        await ctx.send("The door is now locked.")
    else:
        ser.write(b"0")
        await ctx.send("Wrong password. Please try again.")


bot.run("ENTER_YOUR_API_KEY")

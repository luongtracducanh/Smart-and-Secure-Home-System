import MySQLdb
import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

dbConn = MySQLdb.connect("localhost", "root", "ducanh2003", "IOT") or die("Could not connect to the database")
print(dbConn)
cursor = dbConn.cursor()


@bot.event
async def on_ready():
    print("Bot is ready.")


@bot.command()
async def data(ctx):
    cursor.execute("SELECT * FROM newtable ORDER BY ID DESC limit 1")
    result = cursor.fetchall()
    for row in result:
        temperature = row[1]
        humidity = row[2]
        gas = row[3]
    await ctx.send(
        f"The temperature is: {temperature} degree Celsius, the humidity is {humidity} %, the gas level is: {gas} ppm.")


@bot.command()
async def temperature(ctx):
    cursor.execute("SELECT Temperature FROM newtable ORDER BY ID DESC limit 1")
    result = cursor.fetchall()
    for row in result:
        temperature = row[0]
    await ctx.send(f"The temperature is: {temperature} degree Celsius.")


@bot.command()
async def humidity(ctx):
    cursor.execute("SELECT Humidity FROM newtable ORDER BY ID DESC limit 1")
    result = cursor.fetchall()
    for row in result:
        humidity = row[0]
    await ctx.send(f"The humidity is: {humidity} %.")


@bot.command()
async def gas(ctx):
    cursor.execute("SELECT Gas FROM newtable ORDER BY ID DESC limit 1")
    result = cursor.fetchall()
    for row in result:
        gas = row[0]
    await ctx.send(f"The gas level is: {gas} ppm.")


@bot.command()
async def setTemperature(ctx, temperature):
    cursor.execute("SELECT alertHumid, alertGas FROM default_alert ORDER BY ID DESC limit 1")
    result = cursor.fetchall()
    for row in result:
        humidity = row[0]
        gas = row[1]
    data = (temperature, humidity, gas)
    cursor.execute("INSERT INTO default_alert (alertTemp, alertHumid, alertGas) VALUES (%s, %s, %s)" % (data))
    dbConn.commit()
    await ctx.send(f"You have set the alert temperature threshold to {temperature} degree Celsius.")


@bot.command()
async def setHumidity(ctx, humidity):
    cursor.execute("SELECT alertTemp, alertGas FROM default_alert ORDER BY ID DESC limit 1")
    result = cursor.fetchall()
    for row in result:
        temperature = row[0]
        gas = row[1]
    data = (temperature, humidity, gas)
    cursor.execute("INSERT INTO default_alert (alertTemp, alertHumid, alertGas) VALUES (%s, %s, %s)" % (data))
    dbConn.commit()
    await ctx.send(f"You have set the alert humidity threshold to {humidity} %.")


@bot.command()
async def setGas(ctx, gas):
    cursor.execute("SELECT alertTemp, alertHumid FROM default_alert ORDER BY ID DESC limit 1")
    result = cursor.fetchall()
    for row in result:
        temperature = row[0]
        humidity = row[1]
    data = (temperature, humidity, gas)
    cursor.execute("INSERT INTO default_alert (alertTemp, alertHumid, alertGas) VALUES (%s, %s, %s)" % (data))
    dbConn.commit()
    await ctx.send(f"You have set the alert gas threshold to {gas} ppm.")


@bot.command()
async def turnOff(ctx):
    data = (0.0, 0.0, 0.0)
    cursor.execute("INSERT INTO default_alert (alertTemp, alertHumid, alertGas) VALUES (%s, %s, %s)" % (data))
    dbConn.commit()
    await ctx.send("You have turned all alerts off.")


@bot.command()
async def turnOn(ctx):
    cursor.execute("SELECT * FROM default_alert ORDER BY ID DESC limit 1,1")
    result = cursor.fetchall()
    for row in result:
        temperature = row[1]
        humidity = row[2]
        gas = row[3]
    data = (temperature, humidity, gas)
    cursor.execute("INSERT INTO default_alert (alertTemp, alertHumid, alertGas) VALUES (%s, %s, %s)" % (data))
    dbConn.commit()
    await ctx.send("You have turned all alerts on.")


bot.run("ENTER_YOUR_API_KEY")

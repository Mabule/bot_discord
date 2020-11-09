print("Lancement du bot...")
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get
import requests
import json
from pprint import pprint
import time
import datetime

from math import *

bot = discord.Client()
token = "token of your bot"
bot = commands.Bot(command_prefix="!")


def register():
    global level_display_weather, activity, febuary
    # global data_A, data_W
    # big_data = data_A+data_W
    data = dict()
    data["Activity"] = activity
    data["Level of display"] = level_display_weather
    data["Febuary"] = febuary
    with open("save.json", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        print("données enregistrées : " + str(data))


@bot.event
async def on_ready():
    global level_display_weather, activity, febuary
    level_display_weather = 1
    activity = ""
    febuary = 0
    with open('save.json') as data_file:
        data_loaded = json.load(data_file)
    print("Data loaded = " + str(data_loaded))
    activity = data_loaded['Activity']
    level_display_weather = data_loaded['Level of display']
    febuary = data_loaded['Febuary']
    print("Activity onload = " + str(activity))
    print("Level of display onload = " + str(level_display_weather))
    print("Febuary = " + str(febuary))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(str(activity)))
    print("Boti lancé !")


@bot.event
async def on_member_join(member):
    print("New member ! Welcome to " + str(member.mention))
    await member.send("Bienvenue " + str(member.mention) + " dans " + str(member.guild) + " !!!")


@bot.command()
async def website(ctx):
    embed = discord.Embed(title="Site web", description="", color=0x3366CC)
    embed.add_field(name="🌐 💻 🖥️Site officiel :", value="https://lion-emmanuel.000webhostapp.com/", inline=False)
    embed.add_field(name="🌐 💻 🖥️Site multi-usage :", value="https://mabule.github.io/", inline=False)
    embed.add_field(name="🌐 💻 🖥️Site de l'IUT :", value="https://emmanuel-lion-etu.pedaweb.univ-amu.fr/", inline=False)
    await ctx.author.send(embed=embed)


@bot.command()
async def changeA(ctx, arg1):
    global activity
    activity = arg1
    await ctx.send("Activité changée pour : " + activity)
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(str(activity)))
    # data_A = dict()
    # data_A["Activity"] = activity
    # data["Level of display"] = level_display_weather
    register()
    # with open("save.json", "w") as f:
    #    json.dump(data, f, ensure_ascii=False, indent=4)
    #    print("données enregistrées : " + str(data["activity"]))


@bot.command()
async def display(ctx, arg3):
    global level_display_weather
    level_display_weather = int(arg3)
    # data_W = dict()
    # data_W["Level of display"] = level_display_weather
    # data["activity"] = activity
    register()
    if level_display_weather == 1:
        await ctx.send("Vous avez changé l'affichage de la météo en mode **précis**")
    elif level_display_weather == 2:
        await ctx.send("Vous avez changé l'affichage de la météo en mode **basique**")


@bot.command()
async def weather(ctx, city):
    global level_display_weather, febuary
    city = city
    r = requests.get(
        "http://api.openweathermap.org/data/2.5/weather?q=" + str(city) + "&appid=67304d7d1f587faeb69efa2619a1e0c7")
    data = r.json()
    # with open('weather.json', "r") as data_file:
    #    data_loaded = json.load(data_file)
    # old_year = floor(1970 + data_loaded['sys']['sunset']/60/60/24/365)
    with open("weather.json", "w") as f:
        json.dump(data, f)
    mydate = datetime.datetime.now()
    actual_seconde = mydate.strftime("%S")
    actual_minute = mydate.strftime("%M")
    actual_hour = mydate.strftime("%H")
    actual_day = mydate.strftime("%d")
    actual_month = mydate.strftime("%m")
    actual_year = mydate.strftime("%Y")
    print("Year : " + str(actual_year))
    print("Month : " + str(actual_month))
    print("Day : " + str(actual_day))
    print("Hour : " + str(actual_hour))
    print("Minute : " + str(actual_minute))
    print("Seconde : " + str(actual_seconde))

    year = 1970 + data['sys']['sunset'] / 60 / 60 / 24 / 365
    print("\n\n\n")
    pprint(data)
    place = str(data['name'])
    sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
    sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
    remainders = year - floor(year)
    remainders = floor(remainders * 100)
    remainders = remainders / 100
    print(str(remainders))
    day = floor(remainders * 365)
    print("day : " + str(day))
    month = day / 30.4167
    print("month : " + str(month))
    remainders = month - floor(month)
    print("remainde : " + str(remainders))
    day = remainders * 30.4167 / 0.1
    print("day : " + str(day))
    remainders = day - floor(day)
    print("remainde : " + str(remainders))
    description = str(data['weather'][0]['description'])
    feeling = str(round(data['main']['feels_like'] - 273.15))
    temp = str(round(data['main']['temp'] - 273.15))
    temp_max = str(round(data['main']['temp_max'] - 273.15))
    temp_min = str(round(data['main']['temp_min'] - 273.15))
    pressure = str(data['main']['pressure'])
    humidity = str(data['main']['humidity'])
    wind_loc = data['wind']['deg']
    wind_speed = str(data['wind']['speed'])
    print("Send the weather with level of precision equals to : " + str(level_display_weather))
    if level_display_weather == 1:
        embed = discord.Embed(title="Météo", description="**Météo actuelle || **☀☁⛅⛈🌤🌥🌦🌧🌨*️🌩*️", color=0x3366CC)
        embed.add_field(name="🧭Provenance de la météo :", value=place, inline=False)
        embed.add_field(name="🕛🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚 || 🕧🕜🕝🕞🕟🕠🕡🕢🕣🕤🕥🕦\nHeure actuelle :",
                        value=str(actual_hour + ":" + str(actual_minute)) + ":" + str(actual_seconde) + "\n" + str(
                            actual_day) + "/" + str(actual_month) + "/" + str(actual_year), inline=False)
        embed.add_field(name="🌄Heure levé de soleil :", value=str(sunrise), inline=False)
        embed.add_field(name="🌅Heure couché de soleil :", value=str(sunset), inline=False)
        embed.add_field(name="☀☁Description du temps :", value=description, inline=False)
        embed.add_field(name="🌡️Température actuelle :", value=temp + " °C", inline=False)
        embed.add_field(name="🌡️Température ressentie :", value=feeling + " °C", inline=False)
        embed.add_field(name="🌡️Température max :", value=temp_max + " °C", inline=False)
        embed.add_field(name="🌡️Température minimale :", value=temp_min + " °C", inline=False)
        embed.add_field(name="🌋Pression :", value=pressure + " hPa", inline=False)
        embed.add_field(name="💧Taux d'humidité :", value=humidity + " %", inline=False)
        if 330 <= wind_loc or wind_loc <= 30:
            embed.add_field(name="🧭🌪️️Provenance du vent :", value="Nord", inline=False)
        elif 15 <= wind_loc <= 75:
            embed.add_field(name="🧭🌪️️Provenance du vent :", value="Nord-Est", inline=False)
        elif 60 <= wind_loc <= 120:
            embed.add_field(name="🧭🌪️️Provenance du vent :", value="Est", inline=False)
        elif 105 <= wind_loc <= 165:
            embed.add_field(name="🧭🌪️️Provenance du vent :", value="Sud-Est", inline=False)
        elif 150 <= wind_loc <= 210:
            embed.add_field(name="🧭🌪️️Provenance du vent :", value="Sud", inline=False)
        elif 195 <= wind_loc <= 255:
            embed.add_field(name="🧭🌪️️Provenance du vent :", value="Sud-Ouest", inline=False)
        elif 240 <= wind_loc <= 300:
            embed.add_field(name="🧭🌪️️Provenance du vent :", value="Ouest", inline=False)
        elif 285 <= wind_loc <= 345:
            embed.add_field(name="🧭🌪️️Provenance du vent :", value="Nord-Ouest", inline=False)
        embed.add_field(name="🌪️Vitesse du vent :", value=wind_speed + " km/h", inline=False)
        await ctx.author.send(embed=embed)
    elif level_display_weather == 2:  # message.channel.send
        await ctx.author.send(">>> **---------------------------------------------------------------------**\n" +
                              "**-Provenance de la météo : **" + str(place) + "\n" +
                              "**-Heure couché de soleil : **" + str(sunset) + "\n" +
                              "**-Heure levé de soleil : **" + str(sunrise) + "\n" +
                              "**-Description du temps : **" + str(description) + "\n" +
                              "**-Température : **" + temp + "°C" + "\n" +
                              "**-Taux d'humidité : **" + str(humidity) + "%\n" +
                              "**---------------------------------------------------------------------**")


@bot.command()
async def ping(ctx):
    now = datetime.datetime.now().timestamp() * 1000
    message = await ctx.send("Pong!")
    ping = datetime.datetime.now().timestamp() * 1000 - now
    await message.edit(content=f"Ping!  `{int(ping)}ms`")
    print("ping = " + str(ping))


@bot.command(pass_context=True)
async def id(ctx, membre: discord.Member):
    pseudo = membre.mention
    id = membre.id
    print(str(pseudo))
    print(str(id))
    await ctx.author.send(str(pseudo) + " : " + str(id) + " is your id")


@bot.command()
async def love_on(ctx, member: discord.Member):
    await ctx.send("Des pétales d'amour sont envoyés à " + str(member.mention))


#----------Expérimentale------------
#@bot.command()
#async def create_chan(ctx):
"    guild = discord.Message.guild
"    channel = await guild.create_text_channel('cool-channel')


bot.run(token)

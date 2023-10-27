import discord
from discord.ext import commands, tasks
import requests
from googletrans import Translator
import pandas as pd
from datetime import *
import fastf1

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix="!", intents=intents)
session = fastf1.get_session(2019, 'Monza', 'Q')
session.load(telemetry=False, laps=False, weather=False)
vettel = session.get_driver('VET')
today = date.today()
print(f"Pronto {vettel['FirstName']}?")

def getMeteo():
    # Créez une instance du traducteur.
    translator = Translator()
    city = "Montpellier"
    api_key = '725142885bf7b5b1614f186c54933a33'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    data = response.json()
    # Extrayez les informations météorologiques de la réponse JSON.
    weather_description = translator.translate(data['weather'][0]['description'], src='en', dest='fr')
    temperature = data['main']['temp']
    return f"Aujourd'hui à {city}, le temps est {weather_description.text} et la température est de {round(temperature - 273.15 , 1)}°C."

def getCalendar():
        message_content = "```\n" + "Pays            | Date\n"
        message_content += "--------------- | ----------------\n"
        calendar_data = fastf1.get_event_schedule(2023)

        # Convertir l'objet EventSchedule en un DataFrame pandas
        calendar_df = pd.DataFrame(calendar_data)

        # Vérifier si le DataFrame est vide ou non
        if not calendar_df.empty:
            test = False
            pays = ""
            first = False
            for index, row in calendar_df.iterrows():
                date_obj = datetime.strptime(row.get('EventDate','').strftime("%Y-%m-%d"), "%Y-%m-%d").date()
                country = row.get('Country', '')
                event_date = row.get('Session5DateUtc', '')   
                if first ==False:
                    first = True
                    continue             
                if today > date_obj:
                    message_content += f"{country.ljust(15)} | {event_date} 🛑\n"
                else:
                    message_content += f"{country.ljust(15)} | {event_date}\n"
                if today.isocalendar()[1] == date_obj.isocalendar()[1]:
                    test = True
                    pays = country
            if test :
                message_content+=f"```\n@everyone IT'S RACE WEEK IN {pays}"                    
            else :
                message_content += "```"                
        else:
            message_content = "Erreur lors de la récupération des données du calendrier."
        return message_content

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name}')
    # Démarrer la tâche de mise à jour météo toutes les 1 heure.
    update_weather.start()
    Calendar.start()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('!meteo'):
        message_content = getMeteo()
        await message.channel.send(message_content)

    if message.content.startswith('!hello'):
        message_content = "Bonjour"
        await message.channel.send(message_content)

    if message.content.startswith("!Calendrier"):
        message_content = getCalendar()
        await message.channel.send(message_content)


    
@bot.command()
async def meteo(ctx):
    message_content = getMeteo()
    await ctx.send(message_content)

@bot.command()
async def clear(ctx, amount: int):
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"{amount} messages supprimés.", delete_after=0)  # Envoyez un message de confirmation
    else:
        await ctx.send("Vous n'avez pas la permission de supprimer des messages.")


@tasks.loop(hours=1)  # Exécutez cette tâche toutes les 1 heure.
async def update_weather():
    guild_id = 1152361774373404802
    guild = bot.get_guild(guild_id)
    channel_id = 1156733093848301598
    channel = guild.get_channel(channel_id)
    async for msg in channel.history(limit=2):
        if msg.author == bot.user:
            await msg.delete()
    message_content = getMeteo()
    await channel.send(message_content)

@tasks.loop(hours=24)
async def Calendar():
    if today.weekday() == 0:
        guild_id = 1152361774373404802
        channel_id = 1156722424277114890
        guild = bot.get_guild(guild_id)
        channel = guild.get_channel(channel_id)
        async for msg in channel.history(limit=2):
                if msg.author == bot.user:
                    await msg.delete()
        await channel.send(getCalendar())

bot.run('MTE1MjM1OTM1MDc3ODc0NDkxMw.GEqk-P.6XCPhiedOyPWTUPvqwkaCqxQKdGebojCLrAs5s')


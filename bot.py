import discord
import responses
import utils
import asyncio
import json
import os

def read_json(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data

class MyClient(discord.Client):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.config = read_json('config.json')
        
        self.news_channel_id = self.config['news_channel_id']
        self.bot_operations_channel_id =  self.config['operations_channel_id']
        
        self.test_news_channel_id = self.config['test_news_channel_id']
        self.test_bot_operations_channel_id = self.config['test_operations_channel_id']
        
        self.authorizedUsers = ['martinbamonte']  # 👈 Agrega aquí tu usuario o más en una lista
        self.testing = self.config["testing"]
        self.news_update_interval = 600

        if self.testing:
            self.botOperationsChannel = self.test_bot_operations_channel_id
            self.botChannel = self.test_news_channel_id
        else:
            self.botOperationsChannel = self.bot_operations_channel_id
            self.botChannel = self.news_channel_id

    async def setup_hook(self) -> None:
        self.bg_task = self.loop.create_task(self.update_news_bg_task())

    async def on_ready(self):
        print('Online')

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        message_author = message.author.name
        msg = message.content

        # Solo responde si es en el canal de operaciones y de un usuario autorizado
        if message.channel.id == self.botOperationsChannel and message_author in self.authorizedUsers:
            
            if message.content.lower() == '!ping':
                await message.channel.send('Pong!')

            if message.content.lower() == "!state":
                await responses.state(message)

            if message.content.lower() == "!quote":
                await responses.send_qoute(message)

            if msg.strip().lower()=="!timezone":
                await responses.handle_timezone_message(self,message)

            if msg.strip()==('!datetime'):
                await responses.handle_datetime_command(message)

            if msg.strip().startswith("!currencies:"):
                await responses.set_allowed_currencies(message)

            if msg.strip().startswith("!impacts:"):
                await responses.set_allowed_impacts(message) 

            # 👇 Modificado: !news se publica en el canal de noticias
            if msg.strip()=="!news":
                df = await utils.convert_timezone_and_create_csv()
                # Publica en el canal de noticias
                await utils.news_today(self, df, message=None, channel_id=self.botChannel)
                # Confirma en el canal de operaciones
                await message.channel.send("✅ Noticias publicadas en el canal de noticias.")

            if msg.strip().startswith("!daily:"):
                await responses.set_daily_update_time(message)

    async def update_news_bg_task(self):
        #### AT THE START OF THE MONTH, PUT df['10min_update_sent'] = False
        await self.wait_until_ready()
        
        df = await utils.convert_timezone_and_create_csv()
        while not self.is_closed():
            df = await utils.convert_timezone_and_create_csv()
            await utils.news_updates(self,df,self.botChannel)
            await asyncio.sleep(10)

from scraper_investing import scrape_investing

# Ejecuta scraper al iniciar
scrape_investing()

# Token desde variable de entorno en Railway
# 🚩 Desactiva el bot temporalmente
# client = MyClient(intents = discord.Intents.all())
# TOKEN = os.getenv("DISCORD_TOKEN")
# client.run(TOKEN)

# 🚩 Activa el debug del scraper
from scraper_investing_debug import debug_investing
debug_investing()





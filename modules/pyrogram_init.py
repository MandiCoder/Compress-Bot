from pyrogram.methods.utilities.idle import idle
from pyrogram import Client
from aiohttp import web
from dotenv import load_dotenv
from os import getenv
from .ansi import green
from .server import index

load_dotenv()

class PyrogramInit():
    def __init__(self, 
                 PORT=getenv("PORT"), 
                 HOST=getenv("HOST"),
                 API_HASH=getenv("API_HASH"),
                 API_ID=getenv("API_ID"),
                 BOT_TOKEN=getenv("BOT_TOKEN"),):
        
        self.PORT = PORT
        self.HOST = HOST
        self.API_HASH = API_HASH
        self.API_ID = API_ID
        self.BOT_TOKEN = BOT_TOKEN
        self.app = Client(name='TelegramBot', api_hash=self.API_HASH, api_id=self.API_ID, bot_token=self.BOT_TOKEN)
        
        
    def iniciar_bot(self):
        self.app.loop.run_until_complete(self.run_server())
        idle()
        
        
    async def run_server(self):
        server = web.Application()
        server.router.add_get("/", index)
        runner = web.AppRunner(server)
        
        await self.app.start()
        print(green('BOT INICIADO'))
        
        await runner.setup()
        await web.TCPSite(runner, host='0.0.0.0', port=self.PORT).start()
        print(green('SERVER INICIADO'))


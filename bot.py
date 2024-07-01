# bot.py

import discord
from discord.ext import commands
from config import Config
from commands import setup_commands
from utils.llm_utils import generate_response, load_grounding_data

def setup_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    
    bot = commands.Bot(
        command_prefix=Config.BOT_PREFIX,
        intents=intents,
        activity=discord.Game(name=Config.DISCORD_STATUS),
        help_command=commands.DefaultHelpCommand()
    )
    
    bot.config = Config
    bot.conversation_history = {}
    bot.request_timestamps = []
    bot.tts_enabled = Config.TTS_ENABLED

    async def bot_generate_response(messages):
        return await generate_response(bot, messages)

    bot.generate_response = bot_generate_response
    
    async def is_allowed(ctx):
        return (not Config.ALLOWED_CHANNEL_IDS or ctx.channel.id in Config.ALLOWED_CHANNEL_IDS) and \
               (not Config.ALLOWED_ROLE_IDS or any(role.id in Config.ALLOWED_ROLE_IDS for role in ctx.author.roles))
    
    bot.is_allowed = is_allowed
    
    setup_commands(bot)
    
    @bot.event
    async def on_ready():
        print(f"{bot.user} has connected to Discord!")
        if bot.config.USE_GROUNDING:
            load_grounding_data()
            print("Grounding data loaded")
        else:
            print("Grounding is disabled")
    
    @bot.event
    async def on_message(message):
        if message.author.bot or not await bot.is_allowed(message):
            return
        
        await bot.process_commands(message)
        
        if bot.user in message.mentions or isinstance(message.channel, discord.DMChannel):
            from utils.llm_utils import handle_chat_message
            await handle_chat_message(bot, message)
    
    return bot
import discord
from discord.ext import commands
from config import Config
from commands import setup_commands
from utils.llm_utils import load_grounding_data

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
    bot.conversation_history = {}  # Initialize conversation_history
    bot.request_timestamps = []  # Initialize request_timestamps for rate limiting
    bot.tts_enabled = Config.TTS_ENABLED  # Use the value from config
    
    
    # Add the is_allowed method to the bot object
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
            # Handle chat messages (implementation in utils/llm_utils.py)
            from utils.llm_utils import handle_chat_message
            await handle_chat_message(bot, message)
    
    return bot

async def is_allowed(ctx):
    return (not Config.ALLOWED_CHANNEL_IDS or ctx.channel.id in Config.ALLOWED_CHANNEL_IDS) and \
           (not Config.ALLOWED_ROLE_IDS or any(role.id in Config.ALLOWED_ROLE_IDS for role in ctx.author.roles))
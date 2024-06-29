from bot import setup_bot

if __name__ == "__main__":
    bot = setup_bot()
    bot.run(bot.config.DISCORD_BOT_TOKEN)

from discord.ext import commands
from utils.trivia_game import TriviaGame, active_games
from utils.llm_utils import generate_response

def setup_user_commands(bot):
    @bot.command(name="chathelp")
    async def chathelp(ctx):
        """Display help information for the chat commands."""
        help_text = (
            "**Chat Commands:**\n"
            f"`{bot.config.BOT_PREFIX}join` - Join your current voice channel\n"
            f"`{bot.config.BOT_PREFIX}leave` - Leave the current voice channel\n"
            f"`{bot.config.BOT_PREFIX}toggle_tts` - Toggle Text-to-Speech on/off (Admin only)\n"
            f"`{bot.config.BOT_PREFIX}setstatus` - Set a new status for the bot (Admin only)\n"
            f"`{bot.config.BOT_PREFIX}llm_info` - Display current LLM information (Admin only)\n"
            f"`{bot.config.BOT_PREFIX}clear_history` - Clear conversation history (Admin only)\n"
            f"`{bot.config.BOT_PREFIX}translate <text>` - Translate text to English\n"
            f"`{bot.config.BOT_PREFIX}reload_grounding` - Reload grounding data (Admin only)\n"
            f"`{bot.config.BOT_PREFIX}trivia <topic>` - Start a trivia game on the specified topic\n"
            "Mention the bot or DM it to start a conversation"
        )
        await ctx.send(help_text)

    @bot.command()
    async def translate(ctx, *, text: str):
        """Translate text to English."""
        try:
            translation = await generate_response(bot, [
                {"role": "user", "content": f"Translate the following text to English: {text}"}
            ])
            await ctx.send(f"Translation: {translation}")
        except Exception as e:
            print(f"Translation error: {e}")
            await ctx.send("An error occurred during translation. Please try again later.")



    @bot.command(name="trivia")
    async def trivia(ctx, *, topic: str):
        """Start a trivia game on a specific topic."""
        if ctx.channel.id in active_games:
            await ctx.send("A game is already in progress in this channel!")
            return

        try:
            game = TriviaGame(bot, ctx.channel, topic)
            active_games[ctx.channel.id] = game
            await game.start_game()
        except ValueError as e:
            await ctx.send(f"Error starting the game: {str(e)}")
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {str(e)}")
        finally:
            if ctx.channel.id in active_games:
                del active_games[ctx.channel.id]

    @bot.command(name="stop_trivia")
    @commands.has_permissions(administrator=True)
    async def stop_trivia(ctx):
        """Stop the current trivia game (Admin only)."""
        if ctx.channel.id in active_games:
            active_games[ctx.channel.id].is_active = False
            await ctx.send("Trivia game has been stopped.")
        else:
            await ctx.send("There is no active trivia game in this channel.")
from discord.ext import commands
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
            "Mention the bot or DM it to start a conversation"
        )
        await ctx.send(help_text)

    @bot.command()
    async def translate(ctx, *, text: str):
        """Translate text to English."""
        try:
            translation = await generate_response([
                {"role": "user", "content": f"Translate the following text to English: {text}"}
            ])
            await ctx.send(f"Translation: {translation}")
        except Exception as e:
            print(f"Translation error: {e}")
            await ctx.send("An error occurred during translation. Please try again later.")
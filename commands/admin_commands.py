from discord.ext import commands
from utils.llm_utils import load_grounding_data

def setup_admin_commands(bot):
    @bot.command()
    @commands.has_permissions(administrator=True)
    async def setstatus(ctx, *, new_status: str):
        """Set a new status for the bot (Admin only)."""
        await bot.change_presence(activity=discord.Game(name=new_status))
        await ctx.send(f"Status updated to: {new_status}")

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def toggle_tts(ctx):
        """Toggle Text-to-Speech on/off (Admin only)."""
        bot.tts_enabled = not bot.tts_enabled
        # Update the environment variable
        os.environ["TTS_ENABLED"] = str(bot.tts_enabled).lower()
        await ctx.send(f"Text-to-Speech is now {'enabled' if bot.tts_enabled else 'disabled'}.")

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def llm_info(ctx):
        """Display current LLM information (Admin only)."""
        info = f"LLM Type: {bot.config.LLM_TYPE}\n"
        info += f"LLM Model: {bot.config.LLM_MODEL}\n"
        if bot.config.LLM_TYPE == "local":
            info += f"Local LLM URL: {bot.config.LOCAL_LLM_URL}\n"
        settings_str = "\n".join(f"{k}: {v}" for k, v in bot.config.LLM_SETTINGS.items())
        info += f"LLM Settings:\n{settings_str}"
        await ctx.send(f"Current LLM configuration:\n```\n{info}\n```")

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def clear_history(ctx):
        """Clear conversation history for the current channel (Admin only)."""
        if ctx.channel.id in bot.conversation_history:
            del bot.conversation_history[ctx.channel.id]
            await ctx.send("Conversation history cleared for this channel.")
        else:
            await ctx.send("No conversation history found for this channel.")

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def reload_grounding(ctx):
        """Reload grounding data (Admin only)."""
        if not bot.config.USE_GROUNDING:
            await ctx.send("Grounding is currently disabled. Enable it in the configuration to use this feature.")
            return

        try:
            grounding_data = load_grounding_data()
            await ctx.send(f"Grounding data reloaded. {len(grounding_data)} files loaded.")
        except Exception as e:
            print(f"Error reloading grounding data: {e}")
            await ctx.send("An error occurred while reloading grounding data. Please check the logs.")
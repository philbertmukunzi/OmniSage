from discord.ext import commands

def setup_voice_commands(bot):
    @bot.command()
    @commands.check(bot.is_allowed)
    @commands.cooldown(bot.config.COOLDOWN_RATE, bot.config.COOLDOWN_PER, commands.BucketType.user)
    async def join(ctx):
        """Join the user's voice channel."""
        if not ctx.author.voice:
            await ctx.send("You need to be in a voice channel to use this command.")
            return
        
        channel = ctx.author.voice.channel
        try:
            await channel.connect()
            await ctx.send(f"Joined {channel.name}")
        except Exception as e:
            print(f"Error joining voice channel: {e}")
            await ctx.send("I couldn't join the voice channel. Please check my permissions.")

    @bot.command()
    async def leave(ctx):
        """Leave the current voice channel."""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Left the voice channel.")
        else:
            await ctx.send("I'm not in a voice channel.")
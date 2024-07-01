# utils/llm_utils.py

import time
import asyncio
from typing import List, Dict, Any
import discord
from litellm import acompletion
from .grounding_utils import load_grounding_data
from config import Config

async def generate_response(bot, messages: List[Dict[str, Any]]) -> str:
    """Generate a response using the configured LLM."""
    try:
        grounding_data = load_grounding_data() if bot.config.USE_GROUNDING else []
        grounding_context = "\n".join([f"Content of {data['filename']}:\n{data['content']}" for data in grounding_data])
        
        system_message = f"{bot.config.SYSTEM_PROMPT}\n\nGrounding Information:\n{grounding_context}" if grounding_data else bot.config.SYSTEM_PROMPT
        
        kwargs = {
            "model": bot.config.LLM_MODEL,
            "messages": [{"role": "system", "content": system_message}] + messages,
            **bot.config.LLM_SETTINGS
        }

        if bot.config.LLM_TYPE == "openai":
            kwargs["api_key"] = bot.config.OPENAI_API_KEY
        elif bot.config.LLM_TYPE == "anthropic":
            kwargs["api_key"] = bot.config.ANTHROPIC_API_KEY
        elif bot.config.LLM_TYPE == "local":
            kwargs["api_base"] = bot.config.LOCAL_LLM_URL

        response = await rate_limited_completion(bot, **kwargs)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in generate_response: {e}")
        return "An unexpected error occurred. Please try again later."

async def rate_limited_completion(bot, *args, **kwargs):
    """Perform rate-limited completion requests to the LLM."""
    current_time = time.time()
    bot.request_timestamps.append(current_time)
    
    bot.request_timestamps = [ts for ts in bot.request_timestamps if current_time - ts < Config.REQUEST_WINDOW]
    
    if len(bot.request_timestamps) > Config.MAX_REQUESTS_PER_MINUTE:
        wait_time = Config.REQUEST_WINDOW - (current_time - bot.request_timestamps[0])
        await asyncio.sleep(wait_time)
    
    return await acompletion(*args, **kwargs)

async def handle_chat_message(bot, message):
    """Handle incoming chat messages."""
    async with message.channel.typing():
        if message.channel.id not in bot.conversation_history:
            bot.conversation_history[message.channel.id] = []
        
        bot.conversation_history[message.channel.id].append({
            "role": "user",
            "content": message.content,
            "timestamp": time.time()
        })
        
        if len(bot.conversation_history[message.channel.id]) > Config.MAX_MESSAGES:
            bot.conversation_history[message.channel.id] = bot.conversation_history[message.channel.id][-Config.MAX_MESSAGES:]

        response = await generate_response(bot, bot.conversation_history[message.channel.id])

        bot.conversation_history[message.channel.id].append({
            "role": "assistant",
            "content": response,
            "timestamp": time.time()
        })

        await message.reply(response)

        if message.guild and message.guild.voice_client and bot.tts_enabled:
            from .tts_utils import generate_tts, cleanup_tts_file
            tts_file = await generate_tts(response)
            if tts_file:
                try:
                    message.guild.voice_client.play(discord.FFmpegPCMAudio(tts_file))
                    await cleanup_tts_file(message.guild.voice_client, tts_file)
                except Exception as e:
                    print(f"Error playing TTS: {e}")
                    await message.channel.send("I encountered an error while trying to play the audio response.")
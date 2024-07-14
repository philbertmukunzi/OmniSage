import time
import asyncio
import logging
from typing import List, Dict, Any
import discord
from litellm import acompletion
from .rag_utils import rag_query
from config import Config

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def generate_response(bot, messages: List[Dict[str, Any]]) -> str:
    """Generate a response using the configured LLM and RAG if available."""
    try:
        last_message = messages[-1]['content']
        logger.info(f"Generating response for message: {last_message[:50]}...")  # Log first 50 chars of the message
        
        logger.info("Querying RAG system")
        rag_response = await rag_query(last_message)
        logger.info(f"RAG query completed. Response length: {len(rag_response)} characters")
        
        system_message = f"{bot.config.SYSTEM_PROMPT}\n\nRelevant Information: {rag_response}"
        
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

        logger.info(f"Sending request to LLM: {bot.config.LLM_TYPE}")
        logger.debug(f"LLM request details: model={bot.config.LLM_MODEL}, message_count={len(messages)}")
        
        response = await rate_limited_completion(bot, **kwargs)
        
        logger.info("LLM response received")
        logger.debug(f"LLM response details: length={len(response.choices[0].message.content)} characters")
        
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error in generate_response: {e}", exc_info=True)
        return "An unexpected error occurred. Please try again later."

async def rate_limited_completion(bot, *args, **kwargs):
    """Perform rate-limited completion requests to the LLM."""
    current_time = time.time()
    bot.request_timestamps.append(current_time)
    
    bot.request_timestamps = [ts for ts in bot.request_timestamps if current_time - ts < bot.config.REQUEST_WINDOW]
    
    if len(bot.request_timestamps) > bot.config.MAX_REQUESTS_PER_MINUTE:
        wait_time = bot.config.REQUEST_WINDOW - (current_time - bot.request_timestamps[0])
        logger.warning(f"Rate limit reached. Waiting for {wait_time:.2f} seconds before next request.")
        await asyncio.sleep(wait_time)
    
    logger.info("Sending rate-limited completion request to LLM")
    start_time = time.time()
    try:
        response = await acompletion(*args, **kwargs)
        end_time = time.time()
        logger.info(f"LLM request completed in {end_time - start_time:.2f} seconds")
        return response
    except Exception as e:
        logger.error(f"Error in LLM completion request: {e}", exc_info=True)
        raise

async def handle_chat_message(bot, message):
    """Handle incoming chat messages."""
    logger.info(f"Handling chat message from user {message.author.name} in channel {message.channel.name}")
    
    async with message.channel.typing():
        if message.channel.id not in bot.conversation_history:
            bot.conversation_history[message.channel.id] = []
        
        bot.conversation_history[message.channel.id].append({
            "role": "user",
            "content": message.content,
            "timestamp": time.time()
        })
        
        if len(bot.conversation_history[message.channel.id]) > bot.config.MAX_MESSAGES:
            logger.info(f"Trimming conversation history for channel {message.channel.name}")
            bot.conversation_history[message.channel.id] = bot.conversation_history[message.channel.id][-bot.config.MAX_MESSAGES:]

        logger.info("Generating response")
        response = await generate_response(bot, bot.conversation_history[message.channel.id])
        logger.info(f"Response generated. Length: {len(response)} characters")

        # Truncate the response if it exceeds MAX_TEXT
        if len(response) > bot.config.MAX_TEXT:
            logger.warning(f"Response exceeds MAX_TEXT ({bot.config.MAX_TEXT}). Truncating.")
            truncation_msg = "... (response truncated due to length)"
            response = response[:bot.config.MAX_TEXT - len(truncation_msg)] + truncation_msg

        bot.conversation_history[message.channel.id].append({
            "role": "assistant",
            "content": response,
            "timestamp": time.time()
        })

        # Split the response into chunks of MAX_TEXT length
        chunks = [response[i:i+bot.config.MAX_TEXT] for i in range(0, len(response), bot.config.MAX_TEXT)]
        
        logger.info(f"Sending response in {len(chunks)} chunk(s)")
        for chunk in chunks:
            await message.reply(chunk)

        if message.guild and message.guild.voice_client and bot.tts_enabled:
            logger.info("Generating TTS for response")
            from .tts_utils import generate_tts, cleanup_tts_file
            tts_file = await generate_tts(response)
            if tts_file:
                try:
                    logger.info("Playing TTS audio")
                    message.guild.voice_client.play(discord.FFmpegPCMAudio(tts_file))
                    await cleanup_tts_file(message.guild.voice_client, tts_file)
                except Exception as e:
                    logger.error(f"Error playing TTS: {e}", exc_info=True)
                    await message.channel.send("I encountered an error while trying to play the audio response.")
            else:
                logger.warning("Failed to generate TTS file")

    logger.info(f"Finished handling chat message from user {message.author.name}")
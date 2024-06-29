import asyncio
import os
import openai
from config import Config

async def generate_tts(text: str) -> str:
    try:
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, lambda: openai.audio.speech.create(
            model=Config.TTS_MODEL,
            voice=Config.TTS_VOICE,
            input=text
        ))
        
        with open(Config.TTS_FILENAME, 'wb') as f:
            for chunk in response.iter_bytes():
                f.write(chunk)
        
        return Config.TTS_FILENAME
    except Exception as e:
        print(f"Error generating TTS: {e}")
        return None

async def cleanup_tts_file(voice_client, tts_file):
    while voice_client.is_playing():
        await asyncio.sleep(1)
    if os.path.exists(tts_file):
        os.remove(tts_file)
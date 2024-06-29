from .voice_commands import setup_voice_commands
from .admin_commands import setup_admin_commands
from .user_commands import setup_user_commands

def setup_commands(bot):
    setup_voice_commands(bot)
    setup_admin_commands(bot)
    setup_user_commands(bot)
import os
from dotenv import load_dotenv

load_dotenv()

# Discord Configuration
TOKEN = os.getenv('DISCORD_TOKEN')
COMMAND_PREFIX = '!'

# Database Configuration
DATABASE_URL = 'sqlite:///videos.db'

# Video Storage Configuration
VIDEO_DIRECTORY = 'videos'

# Create videos directory if it doesn't exist
if not os.path.exists(VIDEO_DIRECTORY):
    os.makedirs(VIDEO_DIRECTORY)
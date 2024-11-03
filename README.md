# Discord Video Streaming Bot

A Discord bot that can stream videos in voice channels with database management capabilities.

## Setup

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Install FFmpeg on your system:
- **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
- **Windows**: Download from [FFmpeg website](https://ffmpeg.org/download.html)
- **macOS**: `brew install ffmpeg`

3. Create a `.env` file and add your Discord bot token:
```
DISCORD_TOKEN=your_discord_token_here
```

4. Run the bot:
```bash
python bot.py
```

## Commands

- `!play <video_name>`: Play a video in your current voice channel
- `!add_video <name>`: Add a new video (attach the video file with the command)
- `!remove_video <name>`: Remove a video from the database
- `!list_videos`: List all available videos
- `!disconnect`: Disconnect the bot from the voice channel

## Permissions

- Regular users can use `!play` and `!list_videos`
- Only administrators can use `!add_video` and `!remove_video`

## Video Support

Supported formats:
- MP4
- AVI
- MKV

Videos are stored in the `videos` directory and their information is saved in an SQLite database.

## Troubleshooting

If you encounter voice-related errors:
1. Make sure you've installed all requirements: `pip install -r requirements.txt`
2. For Linux users, you might need to install additional system packages:
   ```bash
   sudo apt-get install python3-dev libffi-dev
   ```
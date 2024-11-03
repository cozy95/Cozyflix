import os
import discord
from discord.ext import commands
import asyncio
import ffmpeg
from database import Session, Video, init_db
from config import TOKEN, COMMAND_PREFIX, VIDEO_DIRECTORY

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    init_db()

@bot.command(name='play')
async def play(ctx, video_name: str):
    if not ctx.author.voice:
        await ctx.send("You must be in a voice channel to use this command!")
        return

    session = Session()
    video = session.query(Video).filter_by(name=video_name).first()
    session.close()

    if not video:
        await ctx.send(f"Video '{video_name}' not found!")
        return

    try:
        voice_channel = ctx.author.voice.channel
        voice_client = await voice_channel.connect()

        # Configure FFmpeg options for video streaming
        ffmpeg_options = {
            'options': '-f mp4 -ar 48000 -ac 2 -vn'  # Audio settings for Discord
        }
        
        # Start video stream
        voice_client.play(
            discord.FFmpegPCMAudio(
                video.file_path,
                **ffmpeg_options
            ),
            after=lambda e: print(f'Player error: {e}') if e else None
        )

        # Start Go Live session
        await voice_client.channel.guild.change_voice_state(
            channel=voice_channel,
            self_video=True
        )
        
        # Wait for the video to finish
        while voice_client.is_playing():
            await asyncio.sleep(1)
            
        # Stop streaming and disconnect
        await voice_client.channel.guild.change_voice_state(
            channel=None,
            self_video=False
        )
        await voice_client.disconnect()
        
    except Exception as e:
        await ctx.send(f"Error playing video: {str(e)}")
        if ctx.voice_client:
            await ctx.voice_client.disconnect()

@bot.command(name='add_video')
@commands.has_permissions(administrator=True)
async def add_video(ctx, *, name: str = None):
    if name is None:
        await ctx.send("Usage: !add_video <name>\nPlease provide a name for the video and attach the video file!")
        return

    if not ctx.message.attachments:
        await ctx.send("Please attach a video file!")
        return

    attachment = ctx.message.attachments[0]
    if not any(attachment.filename.lower().endswith(ext) for ext in ['.mp4', '.avi', '.mkv']):
        await ctx.send("Please upload a valid video file (MP4, AVI, or MKV)!")
        return

    try:
        # Create videos directory if it doesn't exist
        if not os.path.exists(VIDEO_DIRECTORY):
            os.makedirs(VIDEO_DIRECTORY)

        # Save with original filename but use provided name in database
        file_path = os.path.join(VIDEO_DIRECTORY, attachment.filename)
        await attachment.save(file_path)

        session = Session()
        try:
            # Check if name already exists
            existing_video = session.query(Video).filter_by(name=name).first()
            if existing_video:
                os.remove(file_path)  # Remove the saved file
                await ctx.send(f"A video with the name '{name}' already exists!")
                return

            video = Video(
                name=name,
                file_path=file_path,
                added_by=str(ctx.author)
            )
            session.add(video)
            session.commit()
            await ctx.send(f"Video '{name}' added successfully!")
        except Exception as e:
            session.rollback()
            if os.path.exists(file_path):
                os.remove(file_path)
            await ctx.send(f"Error adding video: {str(e)}")
        finally:
            session.close()
    except Exception as e:
        await ctx.send(f"Error saving video: {str(e)}")

@bot.command(name='remove_video')
@commands.has_permissions(administrator=True)
async def remove_video(ctx, name: str):
    session = Session()
    try:
        video = session.query(Video).filter_by(name=name).first()
        if video:
            if os.path.exists(video.file_path):
                os.remove(video.file_path)
            session.delete(video)
            session.commit()
            await ctx.send(f"Video '{name}' removed successfully!")
        else:
            await ctx.send(f"Video '{name}' not found!")
    except Exception as e:
        session.rollback()
        await ctx.send(f"Error removing video: {str(e)}")
    finally:
        session.close()

@bot.command(name='list_videos')
async def list_videos(ctx):
    session = Session()
    videos = session.query(Video).all()
    session.close()

    if not videos:
        await ctx.send("No videos available!")
        return

    video_list = "\n".join([f"- {video.name}" for video in videos])
    await ctx.send(f"Available videos:\n{video_list}")

@bot.command(name='disconnect')
async def disconnect(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from voice channel!")
    else:
        await ctx.send("I'm not connected to any voice channel!")

if __name__ == '__main__':
    bot.run(TOKEN)
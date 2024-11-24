import yt_dlp as youtube_dl  # Replace youtube-dl with yt-dlp
from pyrogram.types import Message

def get_song_info(song_name):
    # Search for the song on YouTube
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,  # Ensure only single songs are processed
        'cookiefile': 'cookies.txt',  # Use cookies to bypass CAPTCHA
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',  # Mimic a browser
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        # Search YouTube for the song
        result = ydl.extract_info(f"ytsearch1:{song_name}", download=False)
        if 'entries' in result:
            return {
                'song_id': result['entries'][0]['id'],
                'song_name': result['entries'][0]['title'],
                'artist': result['entries'][0]['uploader'],
            }
        return None

async def download_song(song_id, message: Message):
    # Download the song using yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'%(title)s.%(ext)s',  # Save with the title as the filename
        'cookiefile': 'cookies.txt',  # Use cookies to bypass CAPTCHA
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',  # Mimic a browser
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        # Download the song
        result = ydl.extract_info(song_id, download=True)
        file_path = f"{result['title']}.mp3"  # Path to the downloaded file
        # Send the downloaded file to the user
        await message.reply_audio(audio=file_path, title=result['title'], performer=result['uploader'])

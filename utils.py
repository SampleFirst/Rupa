import yt_dlp as youtube_dl
from pyrogram.types import Message

def get_song_info(song_name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
        'cookiefile': 'cookies.txt',  # Use cookies to bypass CAPTCHA
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f"ytsearch1:{song_name}", download=False)
        if 'entries' in result:
            return {
                'song_id': result['entries'][0]['id'],
                'song_name': result['entries'][0]['title'],
                'artist': result['entries'][0]['uploader'],
            }
        else:
            return None

async def download_song(song_id, message: Message):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'%(title)s.%(ext)s',
        'cookiefile': 'cookies.txt',  # Use cookies to bypass CAPTCHA
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(song_id, download=True)
        file_path = f"{result['title']}.mp3"
        await message.reply_audio(audio=file_path, title=result['title'], performer=result['uploader'])

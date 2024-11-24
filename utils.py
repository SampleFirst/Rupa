import youtube_dl
from pyrogram.types import Message

def get_song_info(song_name):
    # Use the youtube_dl library to search for the song on YouTube
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f"ytsearch:{song_name}", download=False)
        if 'entries' in result:
            # Return the first search result
            return {
                'song_id': result['entries'][0]['id'],
                'song_name': result['entries'][0]['title'],
                'artist': result['entries'][0]['uploader'],
            }
        else:
            return None

async def download_song(song_id, message: Message):
    # Use the youtube_dl library to download the song
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'%(title)s.%(ext)s'  # Save the file with the title name
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(song_id, download=True)
        file_path = f"{result['title']}.mp3"
        # Reply with the downloaded song
        await message.reply_audio(audio=file_path, title=result['title'], performer=result['uploader'])

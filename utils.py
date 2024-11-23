import youtube_dl


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

def download_song(song_id, message):
    # Use the youtube_dl library to download the song
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(song_id, download=True)
        # Send the downloaded song as a reply to the user
        await message.reply_audio(result['url'], title=result['title'], performer=result['uploader'])

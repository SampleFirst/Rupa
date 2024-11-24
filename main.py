from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN
from utils import get_song_info, download_song

app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Hello! I'm an MP3 music download bot. Send me the name of a song, and I'll help you download it!")

@app.on_message(filters.text)
async def handle_song_request(client, message):
    song_name = message.text
    song_info = get_song_info(song_name)
    if song_info:
        buttons = [
            [InlineKeyboardButton("Download", callback_data=f"download:{song_info['song_id']}")],
            [InlineKeyboardButton("Cancel", callback_data="cancel")]
        ]
        await message.reply(f"Song Name: {song_info['song_name']}\nArtist: {song_info['artist']}\n\nWhat would you like to do?", reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await message.reply("Sorry, I couldn't find that song.")

@app.on_callback_query()
async def callback_query(client, callback_query):
    data = callback_query.data.split(":")
    if data[0] == "download":
        song_id = data[1]
        await download_song(song_id, callback_query.message)
        await callback_query.answer()
    elif data[0] == "cancel":
        await callback_query.message.edit("Cancelled!")
        await callback_query.answer()

app.run()

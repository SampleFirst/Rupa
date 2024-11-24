
from pyrogram import Client, filters
from pymongo import MongoClient

# Bot configuration
API_ID = "10956858"
API_HASH = "cceefd3382b44d4d85be2d83201102b7"
BOT_TOKEN = "7248794433:AAG9Eqcf7bjPeriE3d0utaINsVpaTqoHd1k"
ADMINS = "5433924139"

# MongoDB configuration
MONGO_URI = "mongodb+srv://Rename:Rename@cluster0.m3eacgp.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "lofi_songs_db"


# Initialize bot and MongoDB client
app = Client("LofiSongBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
songs_collection = db["songs"]

# Command to start the bot
@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("🎶 Welcome to the Lofi Songs Bot! Use /search <keyword> to find songs.")

# Command to search for songs
@app.on_message(filters.command("search"))
async def search_song(_, message):
    query = " ".join(message.command[1:])  # Extract the query
    if not query:
        await message.reply_text("Please provide a keyword to search for songs. Example: /search calm")
        return

    # Search in the MongoDB collection
    results = songs_collection.find({"title": {"$regex": query, "$options": "i"}})
    songs = [f"🎵 {song['title']} by {song['artist']} - [Listen Here]({song['url']})" for song in results]

    if songs:
        await message.reply_text("

".join(songs), disable_web_page_preview=True)
    else:
        await message.reply_text("No matching songs found. Try a different keyword.")

# Admin command to add a song (optional feature)
@app.on_message(filters.command("add") & filters.user(ADMINS))
async def add_song(_, message):
    try:
        _, title, artist, url = message.text.split(",", 3)
        songs_collection.insert_one({"title": title.strip(), "artist": artist.strip(), "url": url.strip()})
        await message.reply_text(f"✅ Song '{title.strip()}' by {artist.strip()} added successfully!")
    except ValueError:
        await message.reply_text("Invalid format. Use: /add <title>, <artist>, <url>")

# Run the bot
if __name__ == "__main__":
    app.run()

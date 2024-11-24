
import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pymongo import MongoClient

# Bot and MongoDB configuration
API_ID = "10956858"
API_HASH = "cceefd3382b44d4d85be2d83201102b7"
BOT_TOKEN = "7248794433:AAG9Eqcf7bjPeriE3d0utaINsVpaTqoHd1k"

# MongoDB configuration
MONGO_URI = "mongodb+srv://Rename:Rename@cluster0.m3eacgp.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "lofi_songs_db"


# Initialize bot and MongoDB client
app = Client("LofiSongBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
songs_collection = db["songs"]

# Function to scrape the lofi music site and find song details
def scrape_song(query):
    base_url = "https://lofimusic.app"  # Base URL of the website
    search_url = f"{base_url}/?s={query}"  # Search query URL
    response = requests.get(search_url)
    
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Finding all song elements on the page (adjust the class name as per actual site)
    song_elements = soup.find_all('a', class_="entry-title")  # Modify class as needed
    songs = []

    for song in song_elements:
        title = song.get_text()
        url = song['href']
        
        # Extracting artist if available (you may need to adjust the extraction logic)
        artist = "Unknown Artist"
        
        songs.append({
            "title": title,
            "artist": artist,
            "url": url
        })
    
    return songs

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

    # Scrape songs based on the query
    songs = scrape_song(query)
    
    if songs:
        song_texts = [f"🎵 {song['title']} by {song['artist']} - [Listen Here]({song['url']})" for song in songs]
        await message.reply_text("".join(song_texts), disable_web_page_preview=True)
    else:
        await message.reply_text("No matching songs found. Try a different keyword.")

# Run the bot
if __name__ == "__main__":
    app.run()

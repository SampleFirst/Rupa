
import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pymongo import MongoClient

# Bot configuration
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

# Function to scrape songs from Lofi Music App
def scrape_lofi_music_app(query):
    base_url = "https://lofimusic.app"  # Base URL of the website
    search_url = f"{base_url}/?s={query}"  # Search query URL
    response = requests.get(search_url)
    
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    
    song_elements = soup.find_all('a', class_="entry-title")  # Modify class as needed
    songs = []

    for song in song_elements:
        title = song.get_text()
        url = song['href']
        artist = "Unknown Artist"
        
        songs.append({
            "title": title,
            "artist": artist,
            "url": url
        })
    
    return songs

# Function to scrape songs from ChilledCow (Lofi Hip Hop Radio)
def scrape_chilled_cow(query):
    base_url = "https://chilledcow.com"  # Base URL of ChilledCow
    search_url = f"{base_url}/?s={query}"  # Search query URL
    response = requests.get(search_url)
    
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    
    song_elements = soup.find_all('a', class_="post-title")  # Modify class as needed
    songs = []

    for song in song_elements:
        title = song.get_text()
        url = song['href']
        artist = "Unknown Artist"
        
        songs.append({
            "title": title,
            "artist": artist,
            "url": url
        })
    
    return songs

# Function to scrape songs from Lofi Girl
def scrape_lofi_girl(query):
    base_url = "https://lofigirl.com"  # Base URL of Lofi Girl
    search_url = f"{base_url}/?s={query}"  # Search query URL
    response = requests.get(search_url)
    
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    
    song_elements = soup.find_all('a', class_="post-title")  # Modify class as needed
    songs = []

    for song in song_elements:
        title = song.get_text()
        url = song['href']
        artist = "Unknown Artist"
        
        songs.append({
            "title": title,
            "artist": artist,
            "url": url
        })
    
    return songs

# Function to search songs on multiple websites
def search_songs(query):
    songs = []
    
    # Scrape Lofi Music App
    songs.extend(scrape_lofi_music_app(query))
    
    # Scrape ChilledCow
    songs.extend(scrape_chilled_cow(query))
    
    # Scrape Lofi Girl
    songs.extend(scrape_lofi_girl(query))
    
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

    # Search for songs on multiple websites
    songs = search_songs(query)
    
    if songs:
        song_texts = [f"🎵 {song['title']} by {song['artist']} - [Listen Here]({song['url']})" for song in songs]
        await message.reply_text("\n\n".join(song_texts), disable_web_page_preview=True)
    else:
        await message.reply_text("No matching songs found. Try a different keyword.")

# Run the bot
if __name__ == "__main__":
    app.run()

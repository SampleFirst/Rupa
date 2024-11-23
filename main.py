from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN
from utils import get_file_name, get_file_extension

app = Client("rename_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Hello! I'm a rename bot. Send me a file or document, and I'll help you rename it!")

@app.on_message(filters.document | filters.audio | filters.video | filters.photo)
async def rename_file(client, message):
    file = message.document or message.audio or message.video or message.photo
    file_name = get_file_name(file)
    file_extension = get_file_extension(file)

    buttons = [
        [InlineKeyboardButton("Rename", callback_data=f"rename:{file_name}:{file_extension}")],
        [InlineKeyboardButton("Cancel", callback_data="cancel")]
    ]

    await message.reply(f"File Name: {file_name}\nFile Extension: {file_extension}\n\nWhat would you like to do?", reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query()
async def callback_query(client, callback_query):
    data = callback_query.data.split(":")
    if data[0] == "rename":
        file_name = data[1]
        file_extension = data[2]
        await callback_query.message.edit(f"Enter new file name (without extension):\n\nCurrent File Name: {file_name}")
        await callback_query.answer()
        await client.listen((link_unavailable), timeout=300, on_result=on_rename_result(file_name, file_extension))
    elif data[0] == "cancel":
        await callback_query.message.edit("Cancelled!")
        await callback_query.answer()

async def on_rename_result(file_name, file_extension):
    async def func(_, message):
        new_file_name = message.text
        await message.reply_document(message.document.file_id, file_name=f"{new_file_name}.{file_extension}")
        await message.delete()
    return func

app.run()
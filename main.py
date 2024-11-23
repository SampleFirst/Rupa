from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN
from utils import get_file_name, get_file_extension

# Initialize the bot
app = Client("rename_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# State storage for renaming tasks
rename_tasks = {}

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Hello! I'm a rename bot. Send me a file or document, and I'll help you rename it!")

@app.on_message(filters.document | filters.audio | filters.video)
async def rename_file(client, message):
    file = message.document or message.audio or message.video
    file_name = get_file_name(file)
    file_extension = get_file_extension(file)

    buttons = [
        [InlineKeyboardButton("Rename", callback_data=f"rename:{file_name}:{file_extension}")],
        [InlineKeyboardButton("Cancel", callback_data="cancel")]
    ]

    await message.reply(
        f"File Name: {file_name}\nFile Extension: {file_extension}\n\nWhat would you like to do?",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query()
async def callback_query(client, callback_query):
    data = callback_query.data.split(":")
    
    if data[0] == "rename":
        file_name = data[1]
        file_extension = data[2]

        # Save task to track the user's action
        rename_tasks[callback_query.from_user.id] = {
            "file_name": file_name,
            "file_extension": file_extension,
            "message_id": callback_query.message.id
        }

        await callback_query.message.edit(
            f"Enter the new file name (without extension):\n\nCurrent File Name: {file_name}"
        )
        await callback_query.answer()

    elif data[0] == "cancel":
        await callback_query.message.edit("Cancelled!")
        await callback_query.answer()

@app.on_message(filters.text & filters.command)
async def handle_rename(client, message):
    user_id = message.from_user.id
    
    # Check if the user has an active rename task
    if user_id in rename_tasks:
        task = rename_tasks.pop(user_id)
        new_file_name = message.text.strip()
        original_message_id = task["message_id"]

        # Reply to the original message with the renamed file
        original_message = await client.get_messages(message.chat.id, original_message_id)
        if original_message.document:
            await message.reply_document(
                document=original_message.document.file_id,
                file_name=f"{new_file_name}.{task['file_extension']}"
            )
        elif original_message.audio:
            await message.reply_audio(
                audio=original_message.audio.file_id,
                title=f"{new_file_name}",
                performer=original_message.audio.performer
            )
        elif original_message.video:
            await message.reply_video(
                video=original_message.video.file_id,
                file_name=f"{new_file_name}.{task['file_extension']}"
            )

        await message.reply("File renamed successfully!")
    else:
        await message.reply("No file is being renamed right now. Please start the process by sending a file!")

# Run the bot
app.run()

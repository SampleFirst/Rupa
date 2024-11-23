from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def rename_button(file_name, file_extension):
    buttons = [
        [InlineKeyboardButton("Rename", callback_data=f"rename:{file_name}:{file_extension}")],
        [InlineKeyboardButton("Cancel", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(buttons)
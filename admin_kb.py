from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove

# Admin Keyboard Buttons
b1 = KeyboardButton('Share your PhoneNumber', request_contact=True)
button_tokens_used = KeyboardButton('/tokens_used')
button_chats = KeyboardButton('/chats')
button_voice = KeyboardButton('/voice_records')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).row(button_tokens_used, button_chats).add(button_voice).add(b1)
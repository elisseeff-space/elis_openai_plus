from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove

# Admin Keyboard Buttons
b1 = KeyboardButton('Share your PhoneNumber', request_contact=True)
button_tokens_used = KeyboardButton('/tokens_used')
button_chats = KeyboardButton('/chats')
button_voice = KeyboardButton('/voice_records')
button_elis_stat = KeyboardButton('/elis_stat')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).row(button_tokens_used, button_chats).row(button_voice, button_elis_stat).add(b1)
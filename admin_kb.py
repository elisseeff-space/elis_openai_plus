from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove

# Admin Keyboard Buttons
b1 = KeyboardButton('Share your PhoneNumber', request_contact=True)
button_descstat = KeyboardButton('/descstat')
button_itemsstat = KeyboardButton('/itemstat')
#button_delete = KeyboardButton('/Delete')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_descstat).add(button_itemsstat).add(b1)
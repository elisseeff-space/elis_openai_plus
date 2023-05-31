from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove

b1 = KeyboardButton('Share your PhoneNumber', request_contact=True)
b2 = KeyboardButton('/correction')
b3 = KeyboardButton('/affect')
b4 = KeyboardButton('/medical')
b5 = KeyboardButton('/dialog')


"""
Google speech models/
Which model to select for the given request. 
Select the model best suited to your domain to get best results. 
If a model is not explicitly specified, 
then we auto-select a model based on the parameters in the RecognitionConfig.
"""
# command_and_search "Command and search. Best for short queries such as voice commands or voice search."
# default "Default. Best for audio that is not one of the specific audio models. For example, long-form audio. Ideally the audio is high-fidelity, recorded at a 16khz or greater sampling rate."
# phone_call "Enhanced phone call. Best for audio that originated from a phone call (typically recorded at an 8khz sampling rate)."
# latest_long "Latest Long. Best for long form content like media or conversation."
# latest_short "Latest Short. Best for short form content like commands or single shot directed speech."
# medical_conversation "Best for audio that originated from a conversation between a medical provider and patient."
# medical_dictation "Best for audio that originated from dictation notes by a medical provider."

#b5 = KeyboardButton('Send Where I Am', request_location=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

#kb_client.add(b1).add(b2).add(b3).row(b4, b5)
kb_client.add(b5).row(b2, b3, b4).add(b1)
#kb_client.add(b1).add(b2).insert(b3)
#kb_client.row(b1, b2, b3)

import imbeddedgamedata
import re
from telebot import types

mainMenuPlayGame = 'Let\'s play a game.'
mainMenuEdit = 'Edit game data.'
mainMenuHelp = 'I need help.'
mainMenuRecord = 'Show me best scores'

buttonPlay = types.KeyboardButton(text=mainMenuPlayGame)
# buttonEdit = types.KeyboardButton(text=mainMenuEdit)
buttonHelp = types.KeyboardButton(text=mainMenuHelp)
buttonRecord = types.KeyboardButton(text=mainMenuRecord)
mainMenu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
mainMenu.add(buttonPlay,
             # buttonEdit,
             buttonHelp,
             buttonRecord)


def make_regex_pattern():
    buttons = {types.KeyboardButton(text=key) for key in imbeddedgamedata.gamedata.keys()}
    pattern_list = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    pattern_list.add(buttons)
    return pattern_list

import telebot
import json

import game
import leaderBoards
import menus

with open('config.json', 'r') as config_file:
    config = json.load(config_file)
TOKEN = config['token']
bot = telebot.TeleBot(TOKEN)
board = leaderBoards.Leaderboard()


@bot.message_handler(commands=['start'])
def greeting(message):
    bot.send_message(message.chat.id, 'Hi! I am Regex Resolver bot! I wanna play a game. \n'
                                      'I think of a regular expression pattern in Python synthaxis, '
                                      'you are trying to guess what it is based on the results of using '
                                      'regex.findall function with said pattern')
    show_main_menu(message.chat.id)


def show_main_menu(chat_id):
    bot.send_message(chat_id, "What would you like to do?", reply_markup=menus.mainMenu)


def show_help():
    pass


@bot.message_handler(content_types=['text'])
def main_menu_handler(message):
    print('Handled main menu')
    if message.text == menus.mainMenuPlayGame:
        bot_message = bot.send_message(message.chat.id, 'You wanna play? Let\'s play!')
        state = game.game_set_up(message.chat.id)
        bot.register_next_step_handler(bot_message, lambda l: game.player_input_handler(l, state))
    elif message.text == menus.mainMenuEdit:
        bot.send_message(message.chat.id, 'You want to change something? Fine, but don\'t break anything!')
    elif message.text == menus.mainMenuHelp:
        show_help()
    elif message.text == menus.mainMenuRecord:
        bot.send_message(message.chat.id, board.show_board())


def game_ended(message, game_state):
    bot.send_message(message.chat.id, u'\U0001f389\U0001f389\U0001f389' + 'CONGRATULATIONS!' +
                     u'\U0001f389\U0001f389\U0001f389' + '\n' + 'You have found the correct regex! Your score is '
                     + str(game_state.get_score()))
    board.register_new_leader(message.from_user.username, game_state.get_score())

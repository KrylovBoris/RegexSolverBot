import random
import re

import telebot
import gameState
import imbeddedgamedata as data
import botController
import menus


def get_regex():
    regex = random.choice(list(data.gamedata.keys()))
    return regex


def check_result(result_dictionary, correct_dictionary):
    return {k: result_dictionary[k] == correct_dictionary[k] for k in result_dictionary.keys()}


def show_check_result(flag):
    if flag:
        return u'\U00002714'
    else:
        return u'\U0000274C'


def print_first_message(chat_id, current_game_state):
    botController.bot.send_message(chat_id, 'I chose an expression. Here\'s the results of findall.\n')
    batch = current_game_state.get_new_string_batch()
    regex_result = {s: current_game_state.get_regex().findall(s) for s in batch}
    correctness = {s: True for s in batch}
    print_batch(chat_id, regex_result, correctness, lambda l: '')


def print_next_batch_message(chat_id, current_game_state):
    botController.bot.send_message(chat_id, 'You guessed correctly. Why don\'t we expand our sample?')
    batch = current_game_state.get_new_string_batch()
    regex_result = {s: current_game_state.get_regex().findall(s) for s in batch}
    correctness = {s: True for s in batch}
    print_batch(chat_id, regex_result, correctness, lambda l: '')


def print_batch(chat_id, batch_check_result, batch_correctness_result, mark_errors_callback):
    message = ''
    for s in batch_check_result.keys():
        regex_result = batch_check_result[s]
        if not regex_result:
            message += mark_errors_callback(batch_correctness_result[s]) + 'In' + '\"' + s + '\" we found nothing.\n'
        else:
            message += mark_errors_callback(batch_correctness_result[s]) + 'In' + '\"' + s + '\" we found:\n'
            for result_instance in regex_result:
                message += '-\"' + result_instance + '\";\n'

    return botController.bot.send_message(chat_id, message)


def game_set_up(chat_id):
    current_game_state = gameState.State(get_regex())
    print_first_message(chat_id, current_game_state)
    return current_game_state


def player_input_handler(message, game_state):
    if message.text == 'Exit':
        botController.show_main_menu(message.chat.id)
    else:
        regex_pattern = message.text
        regex = re.compile(regex_pattern)

        printed_strings = game_state.get_all_printed_strings()
        process_player_regex(game_state, message, printed_strings, regex, True)


def process_player_regex(game_state, message, printed_strings, regex, recordScore):
    botController.bot.send_message(message.chat.id, "Your regex:" + message.text)
    player_guess_result = {s: regex.findall(s) for s in printed_strings}
    right_answers = {s: game_state.get_regex().findall(s) for s in printed_strings}
    correctness = check_result(player_guess_result, right_answers)

    player_correct = compose_boolean(correctness, True, lambda a, b: a & b)
    player_correct_count = compose_boolean(correctness, 0, counter)

    if recordScore:
        game_state.record_score(player_correct_count, len(correctness))

    print_batch(message.chat.id, player_guess_result, correctness, lambda l: show_check_result(l))

    if player_correct:
        if game_state.has_unprinted_strings():
            print_next_batch_message(message.chat.id, game_state)
            process_player_regex(game_state, message, printed_strings, regex, False)
        else:
            botController.game_ended(message, game_state)
            botController.show_main_menu(message.chat.id)
    else:
        msg = botController.bot.send_message(message.chat.id, 'Error! Try again.')
        botController.bot.register_next_step_handler(msg, lambda l: player_input_handler(l, game_state))


def compose_boolean(correctness, initial_val, composition):
    player_correct = initial_val
    for val in correctness.values():
        player_correct = composition(player_correct, val)
    return player_correct


def counter(count, flag):
    if flag:
        count += 1
    return count

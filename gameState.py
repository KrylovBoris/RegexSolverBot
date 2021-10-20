import re
import imbeddedgamedata as data


class State(object):
    def __init__(self, regex):
        self.chosenRegex = re.compile(regex)
        self.listOfStrings = data.gamedata.get(regex)
        self.score = 0
        self.attempts = 0
        self.printedStrings = 0

    def get_new_string_batch(self):
        result = self.listOfStrings[self.printedStrings:self.printedStrings + 5]
        self.printedStrings += 5
        return result

    def get_all_printed_strings(self):
        return self.listOfStrings[:self.printedStrings]

    def get_regex(self):
        return self.chosenRegex

    def get_score(self):
        return self.score / self.attempts * 100

    def record_score(self, correct, entries):
        self.score += correct / entries
        self.attempts += 1

    def has_unprinted_strings(self):
        return self.printedStrings < len(self.listOfStrings)

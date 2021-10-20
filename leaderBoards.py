import json
import os.path


class Leaderboard(object):

    def __init__(self):
        self.leaders = []
        if os.path.exists('leaders.json'):
            with open('leaders.json', 'r') as leaders_file:
                board = json.load(leaders_file)
                self.leaders = board

    def register_new_leader(self, name, score):
        self.leaders.append({'name': name, 'score': score})
        self.leaders = sorted(self.leaders, key=lambda l: -l['score'])
        if len(self.leaders) > 10:
            self.leaders = self.leaders[:10]
        with open('leaders.json', 'w+') as leaders_file:
            leaders_file.write(json.dumps(self.leaders))

    def show_board(self):
        message = ''
        place = 0
        for leader in self.leaders:
            place += 1
            message += str(place) + '. ' + leader['name'] + ' : ' + str(leader['score']) + '\n'
        return message

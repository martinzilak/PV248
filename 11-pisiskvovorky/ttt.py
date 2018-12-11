#!/usr/bin/env python

from sys import argv
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse


def dump(dictionary):
    return json.dumps(dictionary, indent=2)


def has(parameters, params):
    for p in params:
        if p not in parameters:
            return False

    return True


def gp(parameters, param):
    return parameters[param][0]


class Ttt():
    def __init__(self, id, name):
        self.board = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]
        self.id = id
        self.name = name
        self.winner = None
        self.next = 1

    def status(self):
        if self.winner:
            return {"winner": self.winner}
        return {
            "board": self.board,
            "next": self.next
        }

    def play(self, player, x, y):
        if self.winner:
            if self.winner == 0:
                return "draw"
            else:
                return "player {} won".format(self.winner)
        if self.board[x][y] != 0:
            return "cell already taken"
        if player != self.next:
            return "it's players {} turn".format(self.next)

        self.board[x][y] = player
        self.next = 2 if player == 1 else 1

        if self.win_condition(player, x, y):
            self.winner = player
        if (not self.winner) and self.draw_condition():
            self.winner = 0

        return "ok"

    def win_condition(self, player, x, y):
        if player == self.board[0][y] == self.board[1][y] == self.board[2][y]:
            return True
        if player == self.board[x][0] == self.board[x][1] == self.board[x][2]:
            return True
        if player == self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return True
        if player == self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return True

        return False

    def draw_condition(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return False

        return True


class CustomHttpRequestHandler(BaseHTTPRequestHandler):
    running_games = []

    def do_GET(self):
        parsed = parse.urlparse(self.path)
        parameters = parse.parse_qs(parsed.query)
        param = parsed.path.replace("/", "")

        if param == "start":
            return self.start(gp(parameters, "name") if has(parameters, ["name"]) else "")
        elif param == "status":
            if not has(parameters, ["game"]):
                return self.send_error_reply("missing 'game'")
            try:
                id = int(gp(parameters, "game"))
            except:
                return self.send_error_reply("incorrect 'game'")
            return self.status(id)
        elif param == "play":
            if not has(parameters, ["game", "player", "x", "y"]):
                return self.send_error_reply("missing parameter")
            try:
                id = int(gp(parameters, "game"))
                player = int(gp(parameters, "player"))
                x = int(gp(parameters, "x"))
                y = int(gp(parameters, "y"))
            except:
                return self.send_error_reply("incorrect parameter")
            return self.play(id, player, x, y)
        else:
            return self.send_error_reply("couldn't process request")

    def start(self, name):
        game = Ttt(len(self.running_games), name)
        self.running_games.append(game)
        return self.send_json_reply(200, dump({"id": game.id}))

    def status(self, id):
        if id < 0 or id >= len(self.running_games):
            return self.send_error_reply("game with id {} doesn't exist".format(id))

        return self.send_json_reply(200, dump(self.running_games[id].status()))

    def play(self, id, player, x, y):
        if id < 0 or id >= len(self.running_games):
            return self.send_error_reply("game with id {} doesn't exist".format(id))
        if player != 1 and player != 2:
            return self.send_error_reply("unknown player {}".format(player))
        if x < 0 or y < 0 or x > 2 or y > 2:
            return self.send_server_reply(200, "bad", "coordinates out of bounds")

        status = self.running_games[id].play(player, x, y)
        if status == "ok":
            return self.send_server_reply(200, "ok")
        else:
            return self.send_error_reply(status)

    def send_json_reply(self, code, response_data):
        self.send_response(code=code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_data)))
        self.end_headers()
        self.wfile.write(response_data.encode("UTF-8"))

    def send_server_reply(self, code, status, message=None):
        response_json = {
            "status": status,
            "message": message
        } if message else {
            "status": status
        }

        self.send_json_reply(code, dump(response_json))

    def send_error_reply(self, message):
        self.send_server_reply(400, "bad", message)


def main():
    if len(argv) != 2:
        raise ValueError('Wrong number of arguments passed')
    port = int(argv[1])

    server_address = ('', port)
    server = HTTPServer(server_address, CustomHttpRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()

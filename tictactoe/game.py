import time
import model
import curses
from subprocess import call

class Game:

    def __init__(self, player1, player2, boardsize):
        self.player1 = player1
        self.player2 = player2
        self.boardsize = boardsize
        self.board = model.Boardstate(self.boardsize, self.player1, self.player2)

    def play(self, player):
        if self.board.haswinner() == True:
            rc = call("./tictactoe/displaygame.sh")
            self.board.printgame()
            print(f"victory for {player.opponent.piece}!")
            return None
        elif len(self.board.nodes) == self.boardsize**2:
            rc = call("./tictactoe/displaygame.sh")
            self.board.printgame()
            print("tie game!")
            return None

        else:
            ### testing
            #for node in self.nodes:
            #    print("node on board: " + node.ID)
            ###
            rc = call("./tictactoe/displaygame.sh")
            self.board.printgame()
            player.makemove(self.board)
            if player.mode == "computer":
                time.sleep(0.5)
            self.play(player.opponent)

    def main(self):
        self.board.generatepaths(self.boardsize)
        self.play(self.player1)

class Display:

    def __init__(self):
        self.screen = curses.initscr()
        self.num_rows, self.num_columns = self.screen.getmaxyx()

    def render(self):
        pass

    def renderwin(self):
        pass

    def rendertie(self):
        pass

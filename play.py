import game
import model
import argparse

parser = argparse.ArgumentParser(description="setup tictactoe game")
parser.add_argument('b', nargs='?', default=3, type=int, help="board size")
parser.add_argument('p1', nargs='?', default="human", type=str, help="player2 human or computer")
parser.add_argument('pi1', nargs='?', default="X", type=str, help="player1 piece shape")
parser.add_argument('p2', nargs='?', default="computer", type=str, help="player2 human or computer")
parser.add_argument('pi2', nargs='?', default="O", type=str, help="player2 piece shape")

args = parser.parse_args()

player1 = model.Player(args.p1, args.pi1)
player2 = model.Player(args.p2, args.pi2)
player1.opponent = player2
player2.opponent = player1
game1 = game.Game(player1, player2, args.b)

if __name__ == '__main__':
    game1.main()

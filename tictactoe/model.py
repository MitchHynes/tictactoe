import random

class Node:
    """
    A square on the board is occupied when a node is defined for it.
    Attributes:
    ----------
    state: str
            The player who creates the nodes Piece
    ID: str
            The position of the node on the board
    """


    def __init__(self, state, ID):
        self.state = state
        self.ID = ID

class Player:
    """
    Players are the objects that play the game.
    Attributes:
    ----------
    mode: str
            human or computer
    piece: str
            symbol that appears on board for that player
    opponent: Player
            Who the players opponent is
    """

    def __init__(self, mode, piece):

        self.mode = mode
        self.piece = piece
        self.opponent = None

    def makemove(self, board):

        #HUMAN PLAYER

        if self.mode == "human":
           print(f"enter your move, {self.piece}!")
           invalid = True
           while invalid:
                move = input()
                if board.validmove(move):
                    invalid = False
                    break
                print(f"invalid move! try again, {self.piece}!")

           temp = Node(self.piece, move)
           board.nodes.append(temp)

           for path in board.winningpaths:
               if temp.ID in path.nodeIDs:
                   path.addnode(temp)

        #COMPUTER PLAYER

        elif self.mode == "computer":
           # print("COMPUTER TIME")
            winning = []
            empty = []
            losing = []
            ties = []
            numuntilloss = 9999
            numuntilwin = 9999
            losingarrayposition = None
            winningarrayposition = None

            for path in board.winningpaths: 
                #path.displayinfo()
                if path.state == 0: #winning paths that can still be won

                    if len(path.nodes) == 0: #empty winning path
                        empty.append(path)
                        #print("append empty")
                        continue
                    elif path.nodes[0].state != self.piece:
                        losing.append(path)
                        #print("append losing")

                        if len(losing[len(losing)-1].nodesneeded()) < numuntilloss:
                            numuntilloss = len(losing[len(losing)-1].nodesneeded())
                            losingarrayposition = len(losing) - 1
                            continue
                    else:
                        winning.append(path)
                        #print("append winning")
                        if len(winning[len(winning) - 1].nodesneeded()) < numuntilwin:
                            numuntilwin = len(winning[len(winning) - 1].nodesneeded())
                            winningarrayposition = len(winning) - 1
                            continue
                elif path.state == -1 and len(path.nodesneeded()) > 0:
                    #print("append ties")
                    ties.append(path)

            #check if computer has imminent wins
            if numuntilwin == 1:
                nextmove = winning[winningarrayposition].nodesneeded()[0]
                temp = Node(self.piece, nextmove)
                board.nodes.append(temp)
                for path in board.winningpaths:
                    if temp.ID in path.nodeIDs:
                        path.addnode(temp)
                return None

            elif numuntilloss == 1:

                nextmove = losing[losingarrayposition].nodesneeded()[0]
                temp = Node(self.piece, nextmove)
                board.nodes.append(temp)
                for path in board.winningpaths:
                    if temp.ID in path.nodeIDs:
                        path.addnode(temp)
                return None

            else:
                if len(winning) > 0:
                    nextmove = random.choice(random.choice(winning).nodesneeded())
                    temp = Node(self.piece, nextmove)
                    board.nodes.append(temp)
                    for path in board.winningpaths:
                        if temp.ID in path.nodeIDs:
                            path.addnode(temp)
                    return None
                elif len(losing) > 0:
                    nextmove = random.choice(random.choice(losing).nodesneeded())
                    temp = Node(self.piece, nextmove)
                    board.nodes.append(temp)
                    for path in board.winningpaths:
                        if temp.ID in path.nodeIDs:
                            path.addnode(temp)
                    return None
                elif len(empty) > 0:
                    nextmove = random.choice(random.choice(empty).nodesneeded())
                    temp = Node(self.piece, nextmove)
                    board.nodes.append(temp)
                    for path in board.winningpaths:
                        if temp.ID in path.nodeIDs:
                            path.addnode(temp)
                    return None
                else:
                    nextmove = random.choice(random.choice(ties).nodesneeded())
                    temp = Node(self.piece, nextmove)
                    board.nodes.append(temp)
                    for path in board.winningpaths:
                        if temp.ID in path.nodeIDs:
                            path.addnode(temp)
                    return None

        return None

class Winningpath:
    """
    Data Structure that contains a way to win the game.
    Attributes:
    ----------
    ID: str
            the node IDs of the WinningPath concatenated together
    nodeIDs: str[]
            list of node IDs as strings
    nodes: Node[]
            list of the Node objects currently present
    state: int
        state of the winningpath, 0 = can still win, 1 = won, -1 = can't win in this path

    """

    def __init__(self, nodeIDs):

      #  self.ID = ID
        self.nodeIDs = nodeIDs
        self.nodes = []  
        self.state = 0
        self.winner = None

    def addnode(self, node):
        """
        A node needed to win in this winning path has been obtained, track it
        """
        self.nodes.append(node)
        for i in range(0, len(self.nodes)- 1):
            if self.nodes[i].state != self.nodes[i+1].state:
                self.state = -1 #cant win in this winningpath now
                return None

        if len(self.nodes) == len(self.nodeIDs):
            self.state = 1 #won the game
            self.winner = self.nodes[0].ID
            return None

        return None

    def nodesneeded(self):
        """
        returns nodes needed to win game with this winningpath
        """
        needed = []
        for i in self.nodeIDs:
            needID = True
            for node in self.nodes:
                if node.ID == i:
                    needID = False
            if needID:
                needed.append(i)

        return needed


#    def displayinfo(self):
#       print("\n")
#       print("path ID: " + self.ID)
#       print("nodes currently on path:") 
#       for node in self.nodes:
#           print("\tID: " + node.ID)
#           print("\tstate: " + str(node.state))
#       print("path state:" + str(self.state))
#       print("nodes needed: " + str(self.nodesneeded()))

class Boardstate:

    def __init__(self, boardsize, player1, player2):
       self.boardsize = boardsize
       self.winningpaths = []
       self.winner = None
       self.nodes = []

    def generatepaths(self, boardsize):
        #horizontal
        leftrightdiagnodeIDs = []
        rightleftdiagnodeIDs = []
        for i in range(1, boardsize + 1):
            horizontalnodeIDs = []
            verticalnodeIDs = []

            for j in range(1, boardsize + 1):
                horizontalnodeIDs.append(str(i) + str(j))
                verticalnodeIDs.append(str(j) + str(i))

            leftrightdiagnodeIDs.append(str(i) + str(i))
            rightleftdiagnodeIDs.append((str(self.boardsize +1 - i) + str(i)))
            temp1 = Winningpath(horizontalnodeIDs)
            temp2 = Winningpath(verticalnodeIDs)
            
            self.winningpaths.append(temp1)
            self.winningpaths.append(temp2)

        temp3 = Winningpath(leftrightdiagnodeIDs)
        temp4 = Winningpath(rightleftdiagnodeIDs)
        self.winningpaths.append(temp3)
        self.winningpaths.append(temp4)

    def haswinner(self):
        for path in self.winningpaths:
            if path.winner != None: #winner found
                self.winner = path.winner 
                return True
        return False

    def validmove(self, move):
        if len(move) != 2 or type(int(move)) != int:
            return False
        if not (int(move[0]) > 0 and int(move[0]) <= self.boardsize):
            return False
        if not (int(move[1]) > 0 and int(move[1]) <= self.boardsize):
            return False

        for node in self.nodes:
            if node.ID == move:
                return False
        return True

    def searchtoprint(self, ID):
        for node in self.nodes:
            if node.ID == ID:
                return node.state

        return " "

    def printgame(self):
        type1 = "   #   #   "
        type2 = "###########"
        print("\n")
        print(type1)
        print(" " + self.searchtoprint("11") + " " + "#" + " " + self.searchtoprint("12")+ " " + "#" + " " + self.searchtoprint("13") + " ")
        print(type1)
        print(type2)
        print(type1)
        print(" " + self.searchtoprint("21") + " " + "#" + " " + self.searchtoprint("22")+ " " + "#" + " " + self.searchtoprint("23") + " ")
        print(type1)
        print(type2)
        print(type1)
        print(" " + self.searchtoprint("31") + " " + "#" + " " + self.searchtoprint("32")+ " " + "#" + " " + self.searchtoprint("33") + " ")
        print("\n")


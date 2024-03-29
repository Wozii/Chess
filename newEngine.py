from cv2 import insertChannel

'''
TO DO LIST: 
    - test en-passant
    - test castling 
    - probably play a game lol
'''

class GameEngine(): 
    def __init__ (self):        
        # initial state of board
        self.board = [
            ["bR1", "bN", "bB", "bQ", "bK1", "bB", "bN", "bR1"],
            ["bP2", "bP2", "bP2", "bP2", "bP2", "bP2", "bP2", "bP2"],
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP2", "wP2", "wP2", "wP2", "wP2", "wP2", "wP2", "wP2"],
            ["wR1", "wN", "wB", "wQ", "wK1", "wB", "wN", "wR1"]
        ]
        
        self.moveMethods = {'P': self.pawn, 'R': self.rook, 'N': self.knight, 'B': self.bishop, 'K': self.king, 'Q': self.queen}

        self.whiteTurn = True
        self.whiteKing = (7, 4)
        self.blackKing = (0, 4)
        self.pieceCaps = []
        self.inCheck = False
        self.checkPieces = []
        self.pins = []
        self.validMoves = []
        self.turns = 1
    
    def move(self, start, end):
        startR = start[0]
        startC = start[1]
        endR = end[0]
        endC = end[1]

        valid = True
        if len(self.validMoves) != 0:
            if end not in self.validMoves: 
                print("not valid ", end)
                valid = False

        piece = self.board[startR][startC]
        moves = self.moveMethods[piece[1]](startR, startC)
        
        # pawn en passant set up
        if piece[1] == 'P': 
            pDirec = 1 if self.whiteTurn else -1
                
        if end in moves and valid: 
            print (end, moves)
            self.board[startR][startC] = "--"
            dest = self.board[endR][endC] # store end sq for en-passant checks.            
            self.board[endR][endC] = piece
            
            # en passant case
            if piece[1] == 'P' and dest == '--':
                if self.board[endR + pDirec][endC][0] != piece[0] and self.board[endR + pDirec][endC][1] == 'P':
                    self.board[endR + pDirec][endC] = '--'
                    print('en-passant')

            if piece[1:] == "P2":
                self.board[endR][endC] = piece.replace("2", "1")
            elif piece[1:] == "P1":
                self.board[endR][endC] = piece.replace("1", "")
            elif piece[0:2] == "wK":
                self.whiteKing = end
                if piece[1:] == 'K1':
                    self.board[endR][endC] = piece.replace("1", "")
            elif piece[0:2] == "bK":
                self.blackKing = end
                if piece[1:] == 'K1':
                    self.board[endR][endC] = piece.replace("1", "")
            elif piece[1:] == "R1":
                self.board[endR][endC] = piece.replace("1", "")
            

            self.whiteTurn = not self.whiteTurn
            self.after_move()
    
    def after_move(self):
        self.inCheck, self.checkPieces, self.pins = self.getCheckPins()
        self.validMoves = self.getValidMoves()
        if len(self.validMoves) == 0: 
            print("checkmate, white turn: ", self.whiteTurn)

    def getCheckPins(self):
        direc = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))
        pins = []
        inCheck = False
        checkPieces = []
        if self.whiteTurn:
            r, c = self.whiteKing [0], self.whiteKing [1]
            ally = "w"
        else: 
            r, c = self.blackKing [0], self.blackKing [1]
            ally = "b"

        for i in range (len(direc)):
            row, col = r, c
            possiblePins = ()
            for j in range (1, 8):
                row = row + (direc[i][0]) * j
                col = col + (direc[i][1]) * j
                if 0 <= row <= 7 and 0 <= col <= 7:
                    piece = self.board [row][col]
                    piece_type = piece [1] 
                    if piece [0] == ally and piece[1] != 'K':
                        if possiblePins == (): 
                            possiblePins = (row, col, direc [i][0], direc [i][1])
                        else: 
                            break
                    else: 
                        if (0 <= i <= 3 and piece_type == "R") or (4 <= i <= 7 and piece_type == "B") or\
                            (i == 1 and 6 <= j <= 7 and piece[0] != ally and piece[1] == "P") or (i == 1 and 4 <= j <= 5 and piece[0] != ally and piece [1] == "P") or\
                            (j == 1 and piece_type == "K") or piece_type == "Q" :
                            # print ("hmm")
                            if possiblePins == ():
                                inCheck = True
                                checkPieces.append((row, col, direc [i][0], direc [i][1]))
                            else:
                                pins.append(possiblePins)
                                break
                else: 
                    break
        print ("in check method")
        print (inCheck, "\n", checkPieces, "\n", pins)
        return inCheck, checkPieces, pins

    def getValidMoves(self):
        moves = []
        validMoves = []

        if self.whiteTurn:
            r, c = self.whiteKing[0], self.whiteKing[1]
        else: 
            r, c = self.blackKing[0], self.blackKing[1]

        if self.inCheck:
            print("passed check check")
            if len(self.checkPieces) >= 1: 
                print("one check piece")
                moves = self.getPossibleMoves()
                check = self.checkPieces[0]
                checkR = check[0]
                checkC = check[1]
                checkP = self.board[checkR][checkC][1]

                #if knight must capture knight
                if checkP == "N":
                    print("check piece knight")
                    moves = [(checkR, checkC)]
                else:
                    print("check piece other")
                    d1, d2 = check[2], check[3] 
                    
                    # append everything in check direction
                    for i in range (1, 8):
                        validMoves.append((r + d1*i, c + d2*i))
                        if r + d1*i == checkR and c + d2*i == checkC: 
                            break
                    
                # afterwards, remove moves not in valid moves
                for i in range (len(moves) - 1, -1, -1):
                    if moves[i] not in validMoves:
                        moves.remove(moves[i]) 
            
            #have to check that the king's possible moves are valid
            moves.extend(self.king(r, c))
        else: 
            moves = self.getPossibleMoves()
        print("got valid moves")
        print(moves)
        #check for knight moves here
        return moves

    def getPossibleMoves(self):
        moves = []
        if self.whiteTurn: 
            typ = 'w'
        else: 
            typ = 'b'

        for r in range(0, 8):
            for c in range(0, 8):
                if self.board[r][c][0] == typ: 
                    moves.extend(self.moveMethods[self.board[r][c][1]](r, c))
        
        return moves


#############################################################################################################
    def king(self, r, c):
        moves = []
        direcs = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    
        for i in range(len(direcs)):
            direc = direcs[i]

            if 0 <= r + direc[0] <= 7 and 0 <= c + direc[1] <= 7: 
                if self.checkMove(r + direc[0], c + direc[1])!= False:
                    moves.append((r + direc[0], c + direc[1]))
        
        if self.inCheck:
            for i in range(len(moves)):
                # move the king to make sure it's not in check afterwards
                if self.whiteTurn: 
                    self.whiteKing = moves[i]
                else: 
                    self.blackKing = moves[i]

                check, checkP, pins = self.getCheckPins()    
                if check: 
                    moves.remove(moves[i])
            
            # restore king's og position
            if self.whiteTurn: 
                self.whiteKing = (r, c)
            else: 
                self.blackKing = (r, c)
        else:
            # castling 
            if self.board[r][c].find('1') != -1: 
                if self.board[r][c + 3].find('R1') != -1: 
                    # king side castle
                    if self.checkMove(r, c + 1) and self.checkMove(r, c + 2) and self.checkMove(r, c + 3):
                        temp = 0
                        if self.whiteTurn: 
                            for i in range(1, 3):
                                self.whiteKing = (r, c + i)
                                check, checkP, pins = self.getCheckPins()
                                if check: 
                                    break 
                                else: 
                                    temp += 1
                        else: 
                            for i in range(1, 3):
                                self.blackKing = (r, c + i)
                                check, checkP, pins = self.getCheckPins()
                                if check: 
                                    break 
                                else: 
                                    temp += 1
                        
                        if temp == 2: 
                            moves.append(r, c + 2)
                if self.board[r][c - 4].find('R1') != -1:
                    # queen side castle
                    if self.checkMove(r, c - 1) and self.checkMove(r, c - 2) and self.checkMove(r, c - 3) and self.checkMove(r, c - 4):
                        temp = 0
                        if self.whiteTurn: 
                            for i in range(1, 3):
                                self.whiteKing = (r, c - i)
                                check, checkP, pins = self.getCheckPins()
                                if check: 
                                    break 
                                else: 
                                    temp += 1
                        else: 
                            for i in range(1, 3):
                                self.blackKing = (r, c - i)
                                check, checkP, pins = self.getCheckPins()
                                if check: 
                                    break 
                                else: 
                                    temp += 1
                        
                        if temp == 2: 
                            moves.append(r, c - 2)

        return moves    
    
    def pawn(self, r, c):
        direc = 1
        moves = []
        ally = self.board[r][c][0]
        pinned = False
        
        # add case where if pawn eats enemy and blocks check
        for i in range(len(self.pins)):
            pin = self.pins[i]
            if r == pin[0] and c == pin[1]:
                pinned = True
                pinDirec = (pin[2], pin[3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteTurn:
            direc = -1
        
        if 0 <= r + direc <= 7:
            # forward 
            if self.checkMove(r + direc, c) and (not pinned or (direc, 0) == pinDirec):
                moves.append((r + direc, c))
            # take diag right and en-passant
            if c + 1 <= 7 and (not pinned or (direc, 1) == pinDirec):
                if self.checkMove(r + direc, c + 1) == None: 
                    moves.append((r + direc, c + 1))
                elif self.board[r][c + 1][0] != ally and self.board[r][c + 1][1:] == "P1" and self.checkMove(r + direc, c + 1): 
                    moves.append((r + direc, c + 1))
            # take diag left and en-passant
            if c - 1 >= 0 and (not pinned or (direc, -1) == pinDirec): 
                if self.checkMove(r + direc, c - 1) == None: 
                    moves.append((r + direc, c - 1))
                elif self.board[r][c - 1][0] != ally and self.board[r][c - 1][1:] == "P1" and self.checkMove(r + direc, c - 1): 
                    moves.append((r + direc, c - 1))    

        if self.board[r][c].find("2")!= -1 and 0 <= r + direc*2 <= 7 and (not pinned or (direc, 0) == pinDirec):
            #forward twice
            if self.checkMove(r + direc, c) and self.checkMove(r + direc*2, c):
                moves.append((r + direc*2, c))

        return moves

    def rook(self, r, c):
        moves = []
        direcs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        pinned = False
        for i in range(len(self.pins)):
            pin = self.pins[i]
            if r == pin[0] and c == pin[1]:
                pinned = True
                pinDirec = (pin[2], pin[3])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break
        
        for i in range(len(direcs)):
            for j in range(1, 8):
                direc = direcs[i]
                if 0 <= r + j*direc[0] <= 7 and 0 <= c + j*direc[1] <= 7 and (not pinned or direc == pinDirec): 
                    if self.checkMove(r + j*direc[0], c + j*direc[1]):
                        moves.append((r + j*direc[0], c + j*direc[1]))
                    elif self.checkMove(r + j*direc[0], c + j*direc[1]) == None: 
                        moves.append((r + j*direc[0], c + j*direc[1]))
                        break
                    else: 
                        break
                else: 
                    break

        return moves

    def knight(self, r, c):
        moves = []
        direcs = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

        pinned = False
        for i in range(len(self.pins)):
            pin = self.pins[i]
            if r == pin[0] and c == pin[1]:
                return moves
        
        for i in range(len(direcs)):
            direc = direcs[i]
            
            if 0 <= r + direc[0] <= 7 and 0 <= c + direc[1] <= 7:
                if self.checkMove(r + direc[0], c + direc[1]) != False: 
                    moves.append((r + direc[0], c + direc[1]))
        
        return moves

    def bishop(self, r, c):
        moves = []
        direcs = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        pinned = False
        for i in range(len(self.pins)):
            pin = self.pins[i]
            if r == pin[0] and c == pin[1]:
                pinned = True
                pinDirec = (pin[2], pin[3])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break
        
        for i in range(len(direcs)):
            direc = direcs[i]
            for j in range(1, 8):
                if 0 <= r + j*direc[0] <= 7 and 0 <= c + j*direc[1] <= 7 and (not pinned or direc == pinDirec): 
                    if self.checkMove(r + j*direc[0], c + j*direc[1]): 
                        moves.append((r + j*direc[0], c + j*direc[1]))
                    elif self.checkMove(r + j*direc[0], c + j*direc[1]) == None: 
                        moves.append((r + j*direc[0], c + j*direc[1]))
                        break
                    else: 
                        break
                else: 
                    break

        return moves

    def queen(self, r, c):
        moves = []
        moves.append(self.rook(r, c))
        moves.append(self.bishop(r, c))
        return moves

    def checkMove(self, r, c):
        if self.whiteTurn: 
            piece = 'w'
        else: 
            piece = 'b'

        if self.board[r][c] == "--":
            return True
        elif self.board[r][c][0] == piece: 
            return False
        else: 
            return None
             

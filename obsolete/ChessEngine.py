class GameState():
    def __init__ (self):        
        #what the board starts off as (will change later on)
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP2", "bP2", "bP2", "bP2", "bP2", "bP2", "bP2", "bP2"],
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP2", "wP2", "wP2", "wP2", "wP2", "wP2", "wP2", "wP2"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        
        self.whiteTurn = True
        self.whiteKing = (7, 4)
        self.blackKing = (0, 4)
        self.inCheck = False
        self.checkPieces = []
        self.pins = []

        self.validMoves = [0]
        
    def movePiece (self):
        valid = True
        sq = (self.endRow, self.endCol)
        if self.validMoves[0] != 0 and len(self.validMoves) != 0: 
            if sq not in self.validMoves:
                print("not valid? :", sq)
                valid = False
        
        if self.possibleMoves != None and sq in self.possibleMoves and valid:
            print (sq, self.possibleMoves)
            self.board [self.startRow][self.startCol] = "--"
            if self.pieceMoved [1:] == "P2":
                self.board [self.endRow][self.endCol] = self.pieceMoved.replace ("2", "1")
            else:
                self.board [self.endRow][self.endCol] = self.pieceMoved
            #will need to add something here to detect avant-garde
            
            if self.pieceMoved == "wK":
                self.whiteKing = (self.endRow, self.endCol)
            elif self.pieceMoved == "bK":
                self.blackKing = (self.endRow, self.endCol)
            self.whiteTurn = not self.whiteTurn

            self.inCheck, self.checkPieces, self.pins = self.getCheckAndPin()
            self.validMoves = self.getValidMoves(self.board)
            print(self.whiteTurn)
            print("valid moves: ", self.validMoves)
        
        #what piece did you capture
        # if self.board[move.endRow][move.endCol] != "--":
        #     pieceCap = self.board[move.endRow][move.endCol]
        
    def move (self, start, end):
        #start and end position of piece you moved
        print("trying move")
        self.startRow = start [0]
        self.startCol = start [1]
        self.endRow = end [0]
        self.endCol = end [1]
        self.pieceMoved = self.board [self.startRow][self.startCol]
                
        self.pieceMoveMethods = {'B': self.bishopMoves, 'K': self.kingMoves, 'N': self.knightMoves, 'P': self.pawnMoves, 
                                'Q': self.queenMoves, 'R': self.rookMoves}  

        self.possibleMoves = self.pieceMoveMethods[self.pieceMoved[1]](self.board)
        print(self.possibleMoves)        
        

    def getCheckAndPin (self):
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
                    if piece [0] == ally:
                        if possiblePins == (): 
                            possiblePins = (row, col, direc [i][0], direc [i][1])
                        else: 
                            break
                    else: 
                        if (0 <= i <= 3 and piece_type == "R") or (4 <= i <= 7 and piece_type == "B") or\
                            (i == 1 and 6 <= j <= 7 and piece[0:1] == "bP") or (i == 1 and 4 <= j <= 5 and piece [0:1] == "wP") or\
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

    def getValidMoves(self, board):
        moves = []
        validMoves = []

        if self.whiteTurn:
            r, c = self.whiteKing[0], self.whiteKing[1]
        else: 
            r, c = self.blackKing[0], self.blackKing[1]

        if self.inCheck:
            if len(self.checkPieces) == 1: 
                moves = self.getAllPossibleMoves(board)
                check = self.checkPieces[0]
                checkR = check[0]
                checkC = check[1]
                checkP = board[checkR][checkC][1]

                if checkP == "N":
                    moves = [(checkR, checkC)]
                else:
                    d1, d2 = check[2], check[3] 
                    for i in range (1, 8):
                        validMoves.append((r + d1*i, c + d2*i))
                        if r + d1*i == checkR and c + d2*i == checkC: 
                            break
                    
                    for i in range (len(moves), -1, -1):
                        if moves[i] not in validMoves:
                            moves.remove(moves[i]) 
            
            moves.append(self.kingMoves(board))
        else: 
            moves = self.getAllPossibleMoves(board)
        print("got valid moves")
        return moves        

    def getAllPossibleMoves(self, board):
        possibleMoves = []
        if self.whiteTurn:
            turn = 'w'
        else: 
            turn = 'b'
        print ("turn : ", turn)
        for r in range(0, 8):
            for c in range(0, 8):
                # print(r, c, board[r][c][0])
                if board[r][c][0] == turn: 
                    self.startRow = r
                    self.startCol = c
                    print(r, c, board[r][c][1])
                    print (self.startRow, self.startCol)
                    print(self.pieceMoveMethods[board[r][c][1]](board))
                    possibleMoves.extend(self.pieceMoveMethods[board[r][c][1]](board))
        
        print("possible moves: ", possibleMoves)
        return possibleMoves

    #most of the piece methods will find all possible squares that it could move to and put in array
    #add a check to see if this piece i spinned
    #possiblePins = (row, col, direc [i][0], direc [i][1])
    def pawnMoves (self, board):
        print("pawn move starting: ", self.startRow, self.startCol)
        direc = 1
        row = 1
        possibleMoves = []
        pinned = False
        
        for i in range(len(self.pins)):
            pin = self.pins[i]
            if self.startRow == pin[0] and self.startCol == pin[1]:
                pinned = True
                pinDirec = (pin[2], pin[3])
                self.pins.remove(self.pins[i])
                break
                
        if self.pieceMoved[0] == "w":
            direc = -1
            row = 6                    
        
        if 0 <= self.startRow + (direc)*(1) <= 7:
            #forward one
            if board [self.startRow + (direc)*(1)][self.startCol] == "--" and (not pinned or (direc, 0) == pinDirec):
                possibleMoves.append((self.startRow + (direc)*(1), self.startCol))

            #diagonal left
            if self.startCol - 1 >= 0 and (not pinned or (direc, -1) == pinDirec):
                if board [self.startRow + (direc)*(1)][self.startCol - 1][0] != self.pieceMoved[0] and \
                    board [self.startRow + (direc)*(1)][self.startCol - 1] != "--":
                    possibleMoves.append((self.startRow + (direc)*(1), self.startCol - 1))
            #diagonal right
            if self.startCol + 1 <= 7 and (not pinned or (direc, 1) == pinDirec):
                if board [self.startRow + (direc)*(1)][self.startCol + 1][0] != self.pieceMoved[0] and \
                    board [self.startRow + (direc)*(1)][self.startCol + 1] != "--":
                    possibleMoves.append((self.startRow + (direc)*(1), self.startCol + 1))
        
        #forward twice
        if board [self.startRow][self.startCol].find ("2") != -1 and (not pinned or (direc, 0) == pinDirec):
            # print (board [self.startRow][self.startCol][2])            
            if self.startRow == row: 
                if board [self.startRow + (direc)*(2)][self.startCol] == "--" and board [self.startRow + direc][self.startCol] == "--":
                    possibleMoves.append((self.startRow + (direc)*(2), self.startCol)) 
                                   
        return possibleMoves
    
    #rookie move 
    def rookMoves (self, board):
        possibleMoves = []
        print("rook move starting: ", self.startRow, self.startCol)
        temp_row = self.startRow
        temp_col = self.startCol
        hor_break , vert_break = True, True
        
        pinned = False
        for i in range(len(self.pins)):
            pin = self.pins[i]
            if self.startRow == pin[0] and self.startCol == pin[1]:
                pinned = True
                pinDirec = (pin[2], pin[3])
                if board[pin[0], pin[1]][1] != "Q":
                    self.pins.remove(self.pins[i])
                break

        while temp_row < 7 or temp_col < 7: 
            if temp_row < 7 and hor_break and (not pinned or (1, 0) == pinDirec):
                if self.checkMove (board, temp_row + 1, self.startCol): 
                    possibleMoves.append ((temp_row + 1, self.startCol))
                elif self.checkMove (board, temp_row + 1, self.startCol) == None:
                    possibleMoves.append ((temp_row + 1, self.startCol))
                    hor_break = False
                else: 
                    hor_break = False
            temp_row += 1            
            if temp_col < 7 and vert_break and (not pinned or (0, 1) == pinDirec):
                if self.checkMove (board, self.startRow, temp_col + 1): 
                    possibleMoves.append ((self.startRow, temp_col + 1))
                elif self.checkMove (board, self.startRow, temp_col + 1) == None:
                    possibleMoves.append ((self.startRow, temp_col + 1))
                    vert_break = False
                else: 
                    vert_break = False
            temp_col += 1            
            if not hor_break and not vert_break: 
                break
        
        temp_row = self.startRow
        temp_col = self.startCol
        hor_break , vert_break = True, True
        while temp_row > 0 or temp_col > 0: 
            if temp_row > 0 and hor_break and (not pinned or (-1, 0) == pinDirec):
                if self.checkMove (board, temp_row - 1, self.startCol): 
                    possibleMoves.append ((temp_row - 1, self.startCol))
                elif self.checkMove (board, temp_row - 1, self.startCol) == None:
                    possibleMoves.append ((temp_row - 1, self.startCol))
                    hor_break = False
                else: 
                    hor_break = False
            temp_row -= 1
            if temp_col > 0 and vert_break and (not pinned or (0, -1) == pinDirec): 
                if self.checkMove (board, self.startRow, temp_col - 1): 
                    possibleMoves.append ((self.startRow, temp_col - 1))
                elif self.checkMove (board, self.startRow, temp_col - 1) == None:
                    possibleMoves.append ((self.startRow, temp_col - 1))
                    vert_break = False
                else: 
                    vert_break = False
            temp_col -= 1            
            if not hor_break and not vert_break: 
                break

        return possibleMoves
    
    def knightMoves (self, board):
        print("knight: ", self.startRow, self.startCol)
        possibleMoves = []
        direc = 1 
        
        pinned = False
        for i in range(len(self.pins)):
            pin = self.pins[i]
            if self.startRow == pin[0] and self.startCol == pin[1]:
                pinned = True
                pinDirec = (pin[2], pin[3])
                self.pins.remove(self.pins[i])
                break

        for i in range (2):
            #1 row, 2 cols move
            if self.startRow + direc >= 0 and self.startRow + direc <= 7:
                if self.startCol + 2 <= 7:
                    if self.checkMove (board, self.startRow + direc, self.startCol + 2): 
                        possibleMoves.append ((self.startRow + direc, self.startCol + 2))
                    
                    # if self.checkMove (board, self.startRow + direc, self.startCol + 2):
                    #     if (self.checkMove (board, self.startRow, self.startCol + 1) and self.checkMove (board, self.startRow, self.startCol + 2)) or \
                    #     (self.checkMove (board, self.startRow + direc, self.startCol) and self.checkMove (board, self.startRow + direc, self.startCol + 1)):
                    #         possibleMoves.append ((self.startRow + direc, self.startCol + 2))
                    
                if self.startCol - 2 >= 0:
                    if self.checkMove (board, self.startRow + direc, self.startCol - 2):
                        possibleMoves.append ((self.startRow + direc, self.startCol - 2))
                        
                    # if self.checkMove (board, self.startRow + direc, self.startCol - 2):
                    #     if (self.checkMove (board, self.startRow, self.startCol - 1) and self.checkMove (board, self.startRow, self.startCol - 2)) or \
                    #     (self.checkMove (board, self.startRow + direc, self.startCol) and self.checkMove (board, self.startRow + direc, self.startCol - 1)):
                    #         possibleMoves.append ((self.startRow + direc, self.startCol - 2))
                        
            #2 rows, 1 col move
            if self.startRow + (direc)*2 >= 0 and self.startRow + (direc)*2 <= 7: 
                if self.startCol + 1 <= 7: 
                    if self.checkMove (board, self.startRow + (direc)*2, self.startCol + 1):
                        possibleMoves.append ((self.startRow + (direc)*2, self.startCol + 1))
                    # if self.checkMove (board, self.startRow + (direc)*2, self.startCol + 1):
                    #     if (self.checkMove (board, self.startRow + direc, self.startCol) and self.checkMove (board, self.startRow + (direc)*2, self.startCol)) or \
                    #     (self.checkMove (board, self.startRow, self.startCol + 1) and self.checkMove (board, self.startRow + direc, self.startCol + 1)):
                    #         possibleMoves.append ((self.startRow + (direc)*2, self.startCol + 1))
                
                if self.startCol - 1 >= 0: 
                    if self.checkMove (board, self.startRow + (direc)*2, self.startCol - 1):
                        possibleMoves.append ((self.startRow + (direc)*2, self.startCol - 1))
                        # if (self.checkMove (board, self.startRow + direc, self.startCol) and self.checkMove (board, self.startRow + (direc)*2, self.startCol)) or \
                        # (self.checkMove (board, self.startRow, self.startCol - 1) and self.checkMove (board, self.startRow + direc, self.startCol - 1)):
                        #     possibleMoves.append ((self.startRow + (direc)*2, self.startCol - 1))
            
            direc = -1
           
        return possibleMoves
    
    #no longer a rookie move
    def bishopMoves (self, board):
        print("bishop :", self.startRow, self.startCol)
        possibleMoves = []        
        temp_row = self.startRow
        temp_col = self.startCol
        count = 1
        down_right, down_left, up_right, up_left = True, True, True, True

        pinned = False
        for i in range(len(self.pins)):
            pin = self.pins[i]
            if self.startRow == pin[0] and self.startCol == pin[1]:
                pinned = True
                pinDirec = (pin[2], pin[3])
                self.pins.remove(self.pins[i])
                break
            
        while (temp_row + count <= 7 or temp_row - count >= 0) and (temp_col + count <= 7 or temp_col - count >= 0):
            #down right
            if temp_row + count <= 7 and temp_col + count <= 7 and down_right and (not pinned or (1, 1) == pinDirec): 
                if self.checkMove (board, temp_row + count, temp_col + count):
                    possibleMoves.append ((temp_row + count, temp_col + count))
                elif self.checkMove (board, temp_row + count, temp_col + count) == None:
                    possibleMoves.append ((temp_row + count, temp_col + count))
                    down_right = False
                else: 
                    down_right = False
            #down left
            if temp_row + count <= 7 and temp_col - count >= 0 and down_left and (not pinned or (1, -1) == pinDirec):
                if self.checkMove (board, temp_row + count, temp_col - count):
                    possibleMoves.append ((temp_row + count, temp_col - count))
                elif self.checkMove (board, temp_row + count, temp_col - count) == None:
                    possibleMoves.append ((temp_row + count, temp_col - count))
                    down_left = False
                else: 
                    down_left = False   
            #up right
            if temp_row - count >= 0 and temp_col + count <= 7 and up_right and (not pinned or (-1, 1) == pinDirec): 
                if self.checkMove (board, temp_row - count, temp_col + count):
                    possibleMoves.append ((temp_row - count, temp_col + count))
                elif self.checkMove (board, temp_row - count, temp_col + count) == None:
                    possibleMoves.append ((temp_row - count, temp_col + count))
                    up_right = False
                else: 
                    up_right = False
            #up left
            if temp_row - count >= 0 and temp_col - count >= 0 and up_left and (not pinned or (-1, -1) == pinDirec): 
                if self.checkMove (board, temp_row - count, temp_col - count):
                    possibleMoves.append ((temp_row - count, temp_col - count))
                elif self.checkMove (board, temp_row - count, temp_col - count) == None:
                    possibleMoves.append ((temp_row - count, temp_col - count))
                    up_left = False
                else: 
                    up_left = False

            if not down_right and not down_left and not up_right and not up_left:                 
                break
            count += 1

        return possibleMoves
    
    #same thing as pawn (as gay as pawn) but not bc will have to detect check here
    def kingMoves (self, board):
        print("king :", self.startRow, self.startCol)
        possibleMoves = []

        #horizontal move
        if self.startCol + 1 <= 7: 
            if board[self.startRow][self.startCol + 1][0] != self.pieceMoved[0]:
                possibleMoves.append((self.startRow, self.startCol + 1))
            
        if self.startCol - 1 >= 0: 
            if board[self.startRow][self.startCol - 1][0] != self.pieceMoved[0]:
                possibleMoves.append((self.startRow, self.startCol - 1))
        
        #diagonal and vertical move
        if self.startRow + 1 <= 7: 
            if self.startCol + 1 <= 7: 
                if board [self.startRow + 1][self.startCol + 1][0] != self.pieceMoved[0]:
                    possibleMoves.append ((self.startRow + 1, self.startCol + 1))
            
            if self.startCol - 1 >= 0: 
                if board [self.startRow + 1][self.startCol - 1][0] != self.pieceMoved[0]:
                    possibleMoves.append ((self.startRow + 1, self.startCol - 1))
            
            if board [self.startRow + 1][self.startCol][0] != self.pieceMoved[0]:
                possibleMoves.append ((self.startRow + 1, self.startCol))
            
        if self.startRow - 1 >= 0: 
            if self.startCol + 1 <= 7: 
                if board [self.startRow - 1][self.startCol + 1][0] != self.pieceMoved[0]:
                    possibleMoves.append ((self.startRow - 1, self.startCol + 1))
            
            if self.startCol - 1 >= 0: 
                if board [self.startRow - 1][self.startCol - 1][0] != self.pieceMoved[0]:
                    possibleMoves.append ((self.startRow - 1, self.startCol - 1))
            
            if board [self.startRow - 1][self.startCol][0] != self.pieceMoved[0]:
                possibleMoves.append ((self.startRow - 1, self.startCol))
        
        return possibleMoves
    
    #gotta check for bishop and rook moves basically 
    def queenMoves (self, board):
        possibleMoves = []
        
        possibleMoves.extend (self.rookMoves (board))  
        possibleMoves.extend (self.bishopMoves(board))      
        return possibleMoves 
    

    def checkMove (self, board, row, col):
        if board [row][col] == "--": #indicate if no piece blocking
            return True
        elif board [row][col][0] == self.pieceMoved[0]: #indicate if ally piece blocking
            return False
        else: 
            return None #indicate if enemy piece blocking
         
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
        
    def movePiece (self, move):
        sq = (move.endRow, move.endCol)
        
        if move.possibleMoves != None and sq in move.possibleMoves:
            print (sq, move.possibleMoves)
            self.board [move.startRow][move.startCol] = "--"
            if move.pieceMoved [1:] == "P2":
                self.board [move.endRow][move.endCol] = move.pieceMoved.replace ("2", "1")
            else:
                self.board [move.endRow][move.endCol] = move.pieceMoved
            #will need to add something here to detect avant-garde
            
            if move.pieceMoved == "wK":
                self.whiteKing = (move.endRow, move.endCol)
            elif move.pieceMoved == "bK":
                self.blackKing = (move.endRow, move.endCol)
            self.whiteTurn = not self.whiteTurn
        
        #what piece did you capture
        # if self.board[move.endRow][move.endCol] != "--":
        #     pieceCap = self.board[move.endRow][move.endCol]

    def getCheckAndPin (self):
        direc = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))
        if self.whiteTurn:
            r, c = self.whiteKing [0], self.whiteKing [1]
        else: 
            r, c = self.blackKing [0], self.blackKing [1]

        for i in range (len (direc)):
            row, col = r, c
            for j in range (1, 8):
                if row + (direc[i][0]) * j <= 7 and row + (direc[i][0]) * j >= 0 and col + (direc[i][1])*j <= 7 and col + (direc[i][1])*j >= 0:
                    pass
                else: 
                    break
            

        pass
    
    
#fuck need to change the format.. get rid of class Move() and just make it apart of gamestate    
        
class Move ():
    def __init__ (self, start, end, board):
        #dictionary that references letter that is present on the board to a function that determines all possible moves for that piece
        self.pieceMoveMethods = {'B': self.bishopMoves, 'K': self.kingMoves, 'N': self.knightMoves, 'P': self.pawnMoves, 
                                 'Q': self.queenMoves, 'R': self.rookMoves}
        
        #start and end position of piece you moved
        self.startRow = start [0]
        self.startCol = start [1]
        self.endRow = end [0]
        self.endCol = end [1]
        #what piece did you move
        self.pieceMoved = board [self.startRow][self.startCol]
                
        self.possibleMoves = self.getPossibleMoves(board)
          
    
    def getPossibleMoves(self, board):
        possibleMoves = []
        possibleMoves = self.pieceMoveMethods [self.pieceMoved[1]](board)

        #check if in check, checkmate

        return possibleMoves  

    

    #most of the piece methods will find all possible squares that it could move to and put in array
    def pawnMoves (self, board):
        direc = 1
        row = 1
        possibleMoves = []
                
        if self.pieceMoved[0] == "w":
            direc = -1
            row = 6                    
        
        if self.startRow + (direc)*(1) >= 0 and self.startRow + (direc)*(1) <= 7:
            #foward one
            if board [self.startRow + (direc)*(1)][self.startCol] == "--":
                possibleMoves.append((self.startRow + (direc)*(1), self.startCol))
            
            #diagonal left
            if self.startCol - 1 >= 0:
                if board [self.startRow + (direc)*(1)][self.startCol - 1][0] != self.pieceMoved[0] and \
                    board [self.startRow + (direc)*(1)][self.startCol - 1] != "--":
                    possibleMoves.append((self.startRow + (direc)*(1), self.startCol - 1))
            #diagonal right
            if self.startCol + 1 <= 7:
                if board [self.startRow + (direc)*(1)][self.startCol + 1][0] != self.pieceMoved[0] and \
                    board [self.startRow + (direc)*(1)][self.startCol + 1] != "--":
                    possibleMoves.append((self.startRow + (direc)*(1), self.startCol + 1))
        #foward twice
        if board [self.startRow][self.startCol].find ("2") != -1:
            # print (board [self.startRow][self.startCol][2])            
            if self.startRow == row: 
                if self.startRow + (direc)*(2) >= 0 and self.startRow + (direc)*(2) <= 7:
                    if board [self.startRow + (direc)*(2)][self.startCol] == "--" and board [self.startRow + direc][self.startCol] == "--":
                        possibleMoves.append((self.startRow + (direc)*(2), self.startCol)) 
                                   
        return possibleMoves
    
    #rookie move 
    def rookMoves (self, board):
        print ("rook move")
        possibleMoves = []

        temp_row = self.startRow
        temp_col = self.startCol
        hor_break , vert_break = True, True
        while temp_row < 7 or temp_col < 7: 
            if temp_row < 7 and hor_break:
                if self.checkMove (board, temp_row + 1, self.startCol): 
                    possibleMoves.append ((temp_row + 1, self.startCol))
                elif self.checkMove (board, temp_row + 1, self.startCol) == None:
                    possibleMoves.append ((temp_row + 1, self.startCol))
                    hor_break = False
                else: 
                    hor_break = False
            temp_row += 1            
            if temp_col < 7 and vert_break:
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
            if temp_row > 0 and hor_break:
                if self.checkMove (board, temp_row - 1, self.startCol): 
                    possibleMoves.append ((temp_row - 1, self.startCol))
                elif self.checkMove (board, temp_row - 1, self.startCol) == None:
                    possibleMoves.append ((temp_row - 1, self.startCol))
                    hor_break = False
                else: 
                    hor_break = False
            temp_row -= 1
            if temp_col > 0 and vert_break: 
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
    
    #gay... not finished; check the 3x3 square area around the knight and then based off that return moves
    def knightMoves (self, board):
        
        possibleMoves = []
        direc = 1 

        for i in range (2):
            #1 row, 2 cols move
            if self.startRow + direc >= 0 and self.startRow + direc <= 7:
                if self.startCol + 2 <= 7:
                    if self.checkMove (board, self.startRow + direc, self.startCol + 2) != False: 
                        possibleMoves.append ((self.startRow + direc, self.startCol + 2))
                    
                    # if self.checkMove (board, self.startRow + direc, self.startCol + 2):
                    #     if (self.checkMove (board, self.startRow, self.startCol + 1) and self.checkMove (board, self.startRow, self.startCol + 2)) or \
                    #     (self.checkMove (board, self.startRow + direc, self.startCol) and self.checkMove (board, self.startRow + direc, self.startCol + 1)):
                    #         possibleMoves.append ((self.startRow + direc, self.startCol + 2))
                    
                if self.startCol - 2 >= 0:
                    if self.checkMove (board, self.startRow + direc, self.startCol - 2) != False:
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
           
        print ("knight move")
        return possibleMoves
    
    #no longer a rookie move
    def bishopMoves (self, board):
        print ("bishop move")

        possibleMoves = []        
        temp_row = self.startRow
        temp_col = self.startCol
        count = 1
        down_right, down_left, up_right, up_left = True, True, True, True
        while (temp_row + count <= 7 or temp_row - count >= 0) and (temp_col + count <= 7 or temp_col - count >= 0):
            #down right
            if temp_row + count <= 7 and temp_col + count <= 7 and down_right: 
                if self.checkMove (board, temp_row + count, temp_col + count):
                    possibleMoves.append ((temp_row + count, temp_col + count))
                elif self.checkMove (board, temp_row + count, temp_col + count) == None:
                    possibleMoves.append ((temp_row + count, temp_col + count))
                    down_right = False
                else: 
                    down_right = False
            #down left
            if temp_row + count <= 7 and temp_col - count >= 0 and down_left:
                if self.checkMove (board, temp_row + count, temp_col - count):
                    possibleMoves.append ((temp_row + count, temp_col - count))
                elif self.checkMove (board, temp_row + count, temp_col - count) == None:
                    possibleMoves.append ((temp_row + count, temp_col - count))
                    down_left = False
                else: 
                    down_left = False   
            #up right
            if temp_row - count >= 0 and temp_col + count <= 7 and up_right: 
                if self.checkMove (board, temp_row - count, temp_col + count):
                    possibleMoves.append ((temp_row - count, temp_col + count))
                elif self.checkMove (board, temp_row - count, temp_col + count) == None:
                    possibleMoves.append ((temp_row - count, temp_col + count))
                    up_right = False
                else: 
                    up_right = False
            #up left
            if temp_row - count >= 0 and temp_col - count >= 0 and up_left: 
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
        
        print ("king move")
        return possibleMoves
    
    #gotta check for bishop and rook moves basically 
    def queenMoves (self, board):
        possibleMoves = []
        print ("queen move")
        
        possibleMoves.extend (self.bishopMoves(board))
        possibleMoves.extend (self.rookMoves (board))        
        return possibleMoves 
    

    def checkMove (self, board, row, col):
        if board [row][col] == "--": #indicate if no piece blocking
            return True
        elif board [row][col][0] == self.pieceMoved[0]: #indicate if ally piece blocking
            return False
        else: 
            return None #indicate if enemy piece blocking
         
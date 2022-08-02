import pygame as pg
import newEngine

#icon and title name
pg.display.set_caption ("Chess for LOSERS")
icon = pg.image.load ('icon.png')
pg.display.set_icon (icon)

#constants
DIMENSION = 8
SQ_SIZE = 800//DIMENSION
IMAGES = {}

#load in all the images (ONLY ONE)
def loadImages ():
    pieces = ['bB', 'bK', 'bN', 'bP', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wP', 'wQ', 'wR']
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale (pg.image.load ("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE - 10))


#drawing current state of game
def drawGame(screen, gs):
    drawBoard (screen)
    drawPieces (screen, gs.board)

#drawing the chessboard
def drawBoard (screen):
    colors = [pg.Color ("white"), pg.Color ("Grey")]
    for r in range(DIMENSION):
        for c in range (DIMENSION):
            color = colors [(r+c) % 2]
            pg.draw.rect (screen, color, pg.Rect (c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

#drawing all the pieces on the board    
def drawPieces (screen, board):
    for r in range (DIMENSION):
        for c in range (DIMENSION):
            piece = board[r][c][0:2]
            if piece != "--":
                screen.blit (IMAGES[piece], pg.Rect (c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

#main method that actually runs the thing
def main (): 
    pg.init()
    screen = pg.display.set_mode ([1000, 800])  
    running = True
    screen.fill((224,238,238))
    gs = newEngine.GameEngine()
    loadImages()
    sq_selected = ()
    playerClicks = []
    
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                
            #what happens when user clicks    
            elif event.type == pg.MOUSEBUTTONDOWN:
                position = pg.mouse.get_pos()
                #print (position//SQ_SIZE)
                pos_x = position [1]//SQ_SIZE
                pos_y = position [0]//SQ_SIZE
                if sq_selected != (pos_x, pos_y):
                    sq_selected = (pos_x, pos_y)
                    playerClicks.append (sq_selected)
                else: #resets everything if user clicked on the same square twice
                    sq_selected = ()
                    playerClicks = []
                
                #once user has clicked twice, it enters into the engine to make the piece move
                if len(playerClicks) == 2:
                    if (gs.board [playerClicks [0][0]][playerClicks [0][1]][0] == "w" and gs.whiteTurn == True) or \
                        (gs.board [playerClicks [0][0]][playerClicks [0][1]][0] == "b" and gs.whiteTurn == False):
                        #move = ChessEngine.Move(playerClicks [0], playerClicks[1], gs.board)
                        gs.move (playerClicks[0], playerClicks [1])
                        playerClicks = []
                        sq_selected = ()
                    else:
                        sq_selected = ()
                        playerClicks = []
            
                
        drawGame(screen, gs)
        pg.display.flip()

main()
            

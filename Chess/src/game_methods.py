"""
This module will store all event handling procedures
"""

import pygame as p

class Game:
    """ 
    we want a global dictionary of loaded images of our chess pieces. 
    This way we can access any image whenever we need it.
    It was already initialized in our settings class.
    """
    def load_images(self, chess_piece, engine_settings): #method to load images
        for piece in chess_piece.pieces: 
            #images are scaled down to an appropriate size after being loaded
            engine_settings.IMAGES[piece] = p.transform.scale(
                p.image.load("Chess/images/" + piece + ".png"), 
                (engine_settings.SQSIZE, engine_settings.SQSIZE))
            
    def displayChessBoard(self, screen, engine_settings): #displays the chess board
        global color
        """
        The chess board can be considered as an 8x8 matrix. The fist square Board[0][0] always has the color white (top left corner).
        If you add the row entry with the column entry of any white square and subsequently divide by two, the resulting number
        will have an even parity. The opposite is true for the black squares. 
        """
        for row in range(engine_settings.ROWS):
            for col in range(engine_settings.COLS):
                if (row + col) % 2 == 0: #if number is even
                    color = p.Color("light gray")
                    """
                    This function is used to draw a rectangle. It takes the surface, color, and pygame Rect object as 
                    an input parameter and draws a rectangle on the surface. The last argument is a tuple with 4 components:
                    (x, y, width, height), where (x,y) are the coordinates to the upper left hand corner of the rectangle. In a
                    matrix, the columns are x-coordinates and the rows are y-coordinates. 
                    """
                    p.draw.rect(
                        screen, color, p.Rect(
                            col*engine_settings.SQSIZE, row*engine_settings.SQSIZE,
                            engine_settings.SQSIZE, engine_settings.SQSIZE
                        )) #square 0 is 0 squares away from upper left corner of the screen, square 1 is one square size away etc. 
                else:
                    color = p.Color("dark green")
                    p.draw.rect(
                        screen, color, p.Rect(
                            col*engine_settings.SQSIZE, row*engine_settings.SQSIZE,
                            engine_settings.SQSIZE, engine_settings.SQSIZE
                        )) #square 0 is 0 squares away from upper left corner of the screen, square 1 is one square size away etc. 
        
    def displayChessPieces(self, screen, board, engine_settings): #displays the chess pieces on the board
        for row in range(engine_settings.ROWS):
            for col in range(engine_settings.COLS):
                if board[row][col] != "  ": #if chess square isn't empty
                    screen.blit( #display chess piece at its rightful place/position
                        engine_settings.IMAGES[board[row][col]], 
                        p.Rect(
                            col*engine_settings.SQSIZE, row*engine_settings.SQSIZE, 
                            engine_settings.SQSIZE, engine_settings.SQSIZE
                        ))
    
    def highlightSquares(self, screen, engine, validMoves, sqSelected, engine_settings, chess_piece):
        if sqSelected != (): #see if selected square is a piece
            (row, col) = sqSelected
            if engine.whiteTurn: #see if sqselected is a piece that can be moved
                #nested if statement. Spares us from having to do the same for black
                if engine.board[row][col][0] == ("w" if engine.whiteTurn else "b"): 
                    #highlight selected square
                    #a Surface in pygame is something that you can put images onto
                    #take x,y coordinates in its constructor
                    surface = p.Surface((engine_settings.SQSIZE, engine_settings.SQSIZE))
                    #set transparency value
                    surface.set_alpha(100) # 0 = transparent, 255 = opague
                    surface.fill(p.Color("green"))
                    screen.blit(surface, (col*engine_settings.SQSIZE, row*engine_settings.SQSIZE))
                    #highlight moves from that square
                    surface.fill(p.Color("yellow"))
                    for move in validMoves:
                        if move.initial_row == row and move.initial_col == col:
                            screen.blit(surface, (move.final_col*engine_settings.SQSIZE, move.final_row*engine_settings.SQSIZE))
       
        if engine.whiteTurn and engine.inCheck(chess_piece, engine): #highlight white king square if it is in check
            (row, col) = (engine.whiteKingPosition[0], engine.whiteKingPosition[1])
            surface = p.Surface((engine_settings.SQSIZE, engine_settings.SQSIZE))
            surface.set_alpha(100) 
            surface.fill(p.Color("red"))
            screen.blit(surface, (col*engine_settings.SQSIZE, row*engine_settings.SQSIZE))

        if not engine.whiteTurn and engine.inCheck(chess_piece, engine): #highlight king square if it is in check
            (row, col) = (engine.blackKingPosition[0], engine.blackKingPosition[1])
            surface = p.Surface((engine_settings.SQSIZE, engine_settings.SQSIZE))
            surface.set_alpha(100) 
            surface.fill(p.Color("red"))
            screen.blit(surface, (col*engine_settings.SQSIZE, row*engine_settings.SQSIZE))

    def drawText(self, screen, text, engine_settings):
        font = p.font.SysFont("Helvetica", 32, True, False)
        textObject = font.render(text, 0, p.Color("Gray"))

        #take half the width of the font and subtract that from moving half of the width of the screen
        #then center it
        textLocation = p.Rect(
            0, 0, engine_settings.WIDTH, engine_settings.HEIGHT).move(engine_settings.WIDTH/2 - textObject.get_width()/2,
            engine_settings.HEIGHT/2 - textObject.get_height()/2)
        screen.blit(textObject, textLocation)
        textObject = font.render(text, 0, p.Color("Black"))
        screen.blit(textObject, textLocation.move(2, 2))

    def updateGame(self, screen, engine, engine_settings, validMoves, sqSelected, chess_piece): #displays current game graphics
        self.displayChessBoard(screen, engine_settings)
        self.highlightSquares(screen, engine, validMoves, sqSelected, engine_settings, chess_piece)
        self.displayChessPieces(screen, engine.board, engine_settings)
        
    




        

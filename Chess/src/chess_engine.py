"""
This file will store information about the current state of the game.
"""

"""
A chess engine is a program that can analyze chess positions and make the best possible moves. 
It can be seen as an intelligent chess board.
"""

import pygame as p

from settings import Settings
from chess_pieces import CastleRights

class ChessEngine(): 
    def __init__(self): 
        self.board = [ #board represented as 2d list
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
            ]
        
        #has a piece moved?
        self.whiteTurn = True #white usually has the first turn
        self.moveLog = [] #to keep track of the moves made
       
       #keep track of king positions
        self.whiteKingPosition = (7, 4)
        self.blackKingPosition = (0, 4)

        self.checkMate = False #king is unable to evade check
        self.stalemate = False #king is not in check but has no valid moves

        self.enPassantPossible = () #coordinate for the square where an en passant capture is possible

        self.currentCastlingRight = CastleRights(True, True, True, True)
        #copy rights from what is modified in the updateCastleRights function and store in log
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, 
                                             self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]
        

    #works for all moves with the exception of special rules
    def makeMove(self, move): #this method will take in a move object so that we can access the methods in the Move() class 
        self.board[move.initial_row][move.initial_col] = "  " #when a move is made, the initial square becomes empty
        #the final square is occupied by the piece that was on the initial square
        self.board[move.final_row][move.final_col] = move.pieceMoved 
        self.moveLog.append(move) #log the moves so we kan keep track of them
        
        #update king's position if moved
        if move.pieceMoved == "wK": #to consider checks, we want to keep track of the king's position
            self.whiteKingPosition = (move.final_row, move.final_col)
        elif move.pieceMoved == "bK":
            self.blackKingPosition = (move.final_row, move.final_col)
        
        #pawn promotion
        if move.isPawnPromotion:
            promotedPiece = input("Promote to Q, R, B or N: ") #we can make the ui later
            self.board[move.final_row][move.final_col] = move.pieceMoved[0] + promotedPiece
            
        #en passant
        #if en passant move, must update the board to capture pawn
        if move.isEnPassant:
            self.board[move.initial_row][move.final_col] = "  " #capturing the pawn. same row, next col
        
        #update enPassantPossible variable
        #if pawn moves twice, next move can capture en passant
        if move.pieceMoved[1] == "P" and abs(move.initial_row - move.final_row) == 2: 
            self.enPassantPossible = ((move.initial_row + move.final_row) // 2, move.final_col) 
            #(1 square behind pawn, same initial col)
            #// = integer division
        else: 
            self.enPassantPossible = () #reset 

        #castle move
        if move.isCastle:
            if move.final_col - move.initial_col == 2: #if kingside castle move/click
                #move rook into new square
                self.board[move.final_row][move.final_col-1] = self.board[move.final_row][move.final_col+1]
               #remove rook from earlier square
                self.board[move.final_row][move.final_col+1] = "  " 
            else: #otherwise it's a queenside castle
                self.board[move.final_row][move.final_col+1] = self.board[move.final_row][move.final_col-2]
                self.board[move.final_row][move.final_col-2] = "  " 

        #update castling rights - whenever a rook or a king moves
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, 
                                                 self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))
        
        self.whiteTurn = not self.whiteTurn #switch turns

    def undo_move(self):
        if len(self.moveLog) != 0: #check if there is a move to undo
            move = self.moveLog.pop() #remove last move
            self.board[move.initial_row][move.initial_col] = move.pieceMoved #place moved piece at earlier position
            self.board[move.final_row][move.final_col] = move.pieceCaptured #place captured piece at earlier position
            #update king's position if needed
            if move.pieceMoved == "wK": #to consider checks, we want to keep track of the king's position
                self.whiteKingPosition = (move.initial_row, move.initial_col)
            elif move.pieceMoved == "bK":
                self.blackKingPosition = (move.initial_row, move.initial_col)
            #undo en passant move
            if move.isEnPassant:
                #place captured piece at earlier position by leaving landing square blank
                self.board[move.final_row][move.final_col] = "  "  
                #place captured piece at earlier position, same initial row, next col
                self.board[move.initial_row][move.final_col] = move.pieceCaptured
                self.enPassantPossible = (move.final_row, move.final_col) #allow en passant to happen on the next move
                #this way we are able to redo the en passant move
                ##update enPassantPossible variable when undoing a 2 square pawn advance 
                if move.pieceMoved[1] == "P" and abs(move.initial_row - move.final_row) == 2: #only on two square pawn advances
                    self.enPassantPossible = ()
            #undo castling rights
            self.castleRightsLog.pop() #get rid of the new castle rights from the move we are undoing
            self.currentCastlingRight = self.castleRightsLog[-1] #set current castle rights to the last one in the list
            #undo castle move
            if move.isCastle:
                if move.final_col - move.initial_col == 2: #if kingside castle 
                        #move rook into old square
                    self.board[move.final_row][move.final_col+1] = self.board[move.final_row][move.final_col-1]
                    #remove rook from earlier square
                    self.board[move.final_row][move.final_col-1] = "  "
                else: #queenside
                    self.board[move.final_row][move.final_col-2] = self.board[move.final_row][move.final_col+1]
                    self.board[move.final_row][move.final_col+1] = "  "

 
            self.whiteTurn = not self.whiteTurn #swich turns

        """
        conditions that may prevent one from castling:
            1) There are pieces between your king and your
            rook.
            2) You are in check.
            3) Your king would castle through or into a check.
            4) Your king has made any other move before.
            5) The rook you intend to castle with has already
            moved.
        """
        #update castle right given a move 
    def updateCastleRights(self, move): #4) + 5)
        if move.pieceMoved == "wK": #if king moves, no castling
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == "bK":
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == "wR": #white rooks
            if move.initial_row == 7: #if rooks starting move
                if move.initial_col == 0: #left rook
                    self.currentCastlingRight.wqs = False #no castling
                elif move.initial_col == 7: #right rook
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == "bR": #white rooks
            if move.initial_row == 0: #if rooks starting move
                if move.initial_col == 0: #left rook
                    self.currentCastlingRight.bqs = False
                elif move.initial_col == 7: #right rook
                    self.currentCastlingRight.bks = False
            
    def getValidMoves(self, chess_piece, engine): #all possible moves (considering checks)
        #when not considering checks
        #return self.getAllPossibleMoves()
        tempEnPassantPossible = self.enPassantPossible
        #copy current castle rights
        tempCastleRights = (CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, 
                                                 self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))
        #1.) generate all possible moves
        moves = self.getAllPossibleMoves(chess_piece, engine)

        """
        instead of calling getCastleMoves from getKingMoves, we call it from getValidMoves
        """
        if self.whiteTurn:
            chess_piece.getCastleMoves(self.whiteKingPosition[0], self.whiteKingPosition[1], moves, engine, chess_piece)
        else:
            chess_piece.getCastleMoves(self.blackKingPosition[0], self.blackKingPosition[1], moves, engine, chess_piece)


        #2.) for each move, make the move
        #when removing from a list, go backwards through that list to avoid bugs (like not removing all occurences of an element)
        for i in range(len(moves)-1, -1, -1): 
            self.makeMove(moves[i]) #this switches turns so we have to switch back
            #3.) generate all opponent's moves
            #4.) for each of the opponent's moves, see if they attack your king
            self.whiteTurn = not self.whiteTurn #switch back to player
            if self.inCheck(chess_piece, engine): #see if our king is in check
                #5.) if they do, invalid move
                moves.remove(moves[i]) #remove move from list of valid moves
            self.whiteTurn = not self.whiteTurn #switch back to player
            self.undo_move() #undo move from chess board
        if len(moves) == 0: #either checkmate or stalemate
            if self.inCheck(chess_piece, engine):
                self.checkMate = True
            else:
                self.stalemate = True
        else:
            self.checkMate = False
            self.stalemate = False

            """
            If we make a pawn move, and then undo that move, the value of enPassantPossible is going to change, 
            as we make those moves, even though they don't show up on the board. That is why we store the value 
            of this square in a temporary variable, and then reset it after this function is called. 
            We want to save the value when generating our moves
            """
        
        self.enPassantPossible = tempEnPassantPossible 
        #since we're constantly doing and undoing moves, changing the value of the original variable as with en passant
        self.currentCastlingRight = tempCastleRights 
        return moves #for now we won't worry about checks
    
    def inCheck(self, chess_piece, engine): #see if player is in check 
        if self.whiteTurn:
            return self.squareAttacked(self.whiteKingPosition[0], self.whiteKingPosition[1], chess_piece, engine)
        else:
            return self.squareAttacked(self.blackKingPosition[0], self.blackKingPosition[1], chess_piece, engine)

    def squareAttacked(self, row, col, chess_piece, engine): #see if enemy can attack your square (row, col)
        self.whiteTurn = not self.whiteTurn # switch to opponent's pov
        oppMoves = self.getAllPossibleMoves(chess_piece, engine)
        self.whiteTurn = not self.whiteTurn #switch back to player's pov
        for move in oppMoves:
            if move.final_row == row and move.final_col == col: #square is under attack
                return True
        return False #square is not under attack

    def getAllPossibleMoves(self, chess_piece, engine): #all possible moves (not considering checks)
        moves = [] #we start with an empty list of moves
        for row in range(len(self.board)): #number of rows
            for col in range(len(self.board[row])): #number of cols in a given row
                turn = self.board[row][col][0] #first character of a given square on a board which denotes the color. 
                if (turn == "w" and self.whiteTurn) or (turn == "b" and not self.whiteTurn):
                    piece = self.board[row][col][1]
                    chess_piece.moveFunctions[piece](row, col, moves, engine) #calls the appropriate move function based on piece type         
        return moves
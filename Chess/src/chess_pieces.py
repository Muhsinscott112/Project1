"""
This class will store information about the chess pieces, and all their valid moves
"""

import pygame as p

class Piece:
    def __init__(self): #the different chess pieces
        self.pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", 
                       "wR", "wN", "wB", "wQ", "wK", "wP"]
        #maps every letter to the given function that should be called, when the piece is of that type
        self.moveFunctions = { #prevents us from having to write 6 if statements in the getAllPossibleMoves() method
            "P": self.getPawnMoves, 
            "R": self.getRookMoves, 
            "N": self.getKnightMoves, 
            "B": self.getBishopMoves, 
            "Q": self.getQueenMoves, 
            "K": self.getKingMoves
            }
        
        #self.currentCastlingRight = CastleRights(True, True, True, True)
        
    def getPawnMoves(self, row, col, moves, engine): #get all pawn moves for pawn at position (row, col) and add these to the list
        if engine.whiteTurn: #white pawn moves
            if engine.board[row-1][col] == "  ": #if pawn can move 1 square forward, add move
                moves.append(Move((row, col), (row-1, col), engine.board))
                if row == 6 and engine.board[row-2][col] == "  ": #if pawn can move 2 squares forward, add move
                    moves.append(Move((row, col), (row-2, col), engine.board))
            if col-1 >= 0: #captures to the left
                if engine.board[row-1][col-1][0] == "b": #enemy piece to capture
                    moves.append(Move((row, col), (row-1, col-1), engine.board))
                elif (row-1, col-1) == engine.enPassantPossible: #if last enemy move was an en passant move
                    #we need to tell our engine that it is okay to capture an empty square
                    moves.append(Move((row, col), (row-1, col-1), engine.board, isEnPassant = True))
            if col+1 <= 7: #captures to the right
                if engine.board[row-1][col+1][0] == "b": #enemy piece to capture
                    moves.append(Move((row, col), (row-1, col+1), engine.board))
                elif (row-1, col+1) == engine.enPassantPossible: #if last enemy move was an en passant move
                    moves.append(Move((row, col), (row-1, col+1), engine.board, isEnPassant = True))
        
        else: #black pawn moves
            if engine.board[row+1][col] == "  ": #if pawn can move 1 square forward, add move
                moves.append(Move((row, col), (row+1, col), engine.board))
                if row == 1 and engine.board[row+2][col] == "  ": #if pawn can move 2 squares forward, add move
                    moves.append(Move((row, col), (row+2, col), engine.board))
            if col-1 >= 0: #captures to the left
                if engine.board[row+1][col-1][0] == "w": #enemy piece to capture
                    moves.append(Move((row, col), (row+1, col-1), engine.board))
                elif (row+1, col-1) == engine.enPassantPossible: #if last enemy move was an en passant move
                    moves.append(Move((row, col), (row+1, col-1), engine.board, isEnPassant = True))
            if col+1 <= 7: #captures to the right
                if engine.board[row+1][col+1][0] == "w": #enemy piece to capture
                    moves.append(Move((row, col), (row+1, col+1), engine.board))
                elif (row+1, col+1) == engine.enPassantPossible: #if last enemy move was an en passant move
                    moves.append(Move((row, col), (row+1, col+1), engine.board, isEnPassant = True))
            
    #add pawn promotion later

    def getRookMoves(self, row, col, moves, engine): #get all rook moves for rook at position (row, col) and add these to the list
        rookDirections = ((-1, 0), (0, -1), (1, 0), (0, 1)) #up, left, down, right
        if engine.whiteTurn: #determine the color of the enemy
            enemyColor = "b"
        else:
             enemyColor = "w"
        for d in rookDirections:
            for i in range(1, 8): #rook max range
                final_row = row + d[0] * i #starting row + its direction (up or down) * i
                final_col = col + d[1] * i  #starting col + its direction (left or right) * i
                if 0 <= final_row < 8 and 0 <= final_col < 8: # if position is on the board
                    finalPiece = engine.board[final_row][final_col] #variable that stores final position
                    if finalPiece == "  ": #if an empty space is available
                        moves.append(Move((row, col), (final_row, final_col), engine.board))
                    elif finalPiece[0] == enemyColor: #if an enemy piece can be captured
                        moves.append(Move((row, col), (final_row, final_col), engine.board))
                        break
                    else: #friendly piece, cannot take
                        break
                else: #not on the board
                    break

    def getKnightMoves(self, row, col, moves, engine): #get all knight moves for knight at position (row, col) and add these to the list       
            knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)) #possible knight moves
            if engine.whiteTurn: #determine the color of ally
                allyColor = "w"
            else:
                allyColor = "b"
            for move in knightMoves:
                final_row = row + move[0] 
                final_col = col + move[1]
                if 0 <= final_row < 8 and 0 <= final_col < 8: # if position is on the board
                    finalPiece = engine.board[final_row][final_col] #variable that stores final position
                    if finalPiece[0] != allyColor:
                        moves.append(Move((row, col), (final_row, final_col), engine.board))

    #only difference between bishop and rook is the direction
    def getBishopMoves(self, row, col, moves, engine): #get all rook moves for rook at position (row, col) and add these to the list
        bishopDirections = ((-1, -1), (-1, 1), (1, -1), (1, 1)) #diagonals
        if engine.whiteTurn: #determine the color of the enemy
            enemyColor = "b"
        else:
            enemyColor = "w"
        for d in bishopDirections:
            for i in range(1, 8): #rook max range
                final_row = row + d[0] * i #starting row + its direction (up or down) * i
                final_col = col + d[1] * i  #starting col + its direction (left or right) * i
                if 0 <= final_row < 8 and 0 <= final_col < 8: # if position is on the board
                    finalPiece = engine.board[final_row][final_col] #variable that stores final position
                    if finalPiece == "  ": #if an empty space is available
                        moves.append(Move((row, col), (final_row, final_col), engine.board))
                    elif finalPiece[0] == enemyColor: #if an enemy piece can be captured
                        moves.append(Move((row, col), (final_row, final_col), engine.board))
                        break
                    else: #friendly piece, cannot take
                        break
                else: #not on the board
                    break

    def getQueenMoves(self, row, col, moves, engine): #get all queen moves for queen at position (row, col) and add these to the list
        #a queen has the combined moves of a rook and a bishop
        self.getRookMoves(row, col, moves, engine)
        self.getBishopMoves(row, col, moves, engine)

    #pretty similar to knight
    def getKingMoves(self, row, col, moves, engine): #get all king moves for king at position (row, col) and add these to the list
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)) #possible king moves
        if engine.whiteTurn: #determine the color of ally
            allyColor = "w"
        else:
            allyColor = "b"
        for i in range(8):
            final_row = row + kingMoves[i][0]
            final_col = col + kingMoves[i][1] 
            if 0 <= final_row < 8 and 0 <= final_col < 8: # if position is on the board
                finalPiece = engine.board[final_row][final_col] #variable that stores final position
                if finalPiece[0] != allyColor:
                        moves.append(Move((row, col), (final_row, final_col), engine.board))

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
    
    def getCastleMoves(self, row, col, moves, engine, chess_piece):
        #1)
        if (engine.whiteTurn and engine.currentCastlingRight.wks) or (not engine.whiteTurn and engine.currentCastlingRight.bks):
            self.getKingSideCastleMoves(row, col, moves, engine, chess_piece)
        
        if (engine.whiteTurn and engine.currentCastlingRight.wqs) or (not engine.whiteTurn and engine.currentCastlingRight.bqs):
            self.getQueenSideCastleMoves(row, col, moves, engine, chess_piece)
        #2)
        if engine.squareAttacked(row, col, chess_piece, engine): 
            return #we can't castle if we're in check
        
    def getKingSideCastleMoves(self, row, col, moves, engine, chess_piece):
        if (engine.board[row][col+1] == "  ") and (engine.board[row][col+2] == "  "): #3) check to the right
            #if empty squares aren't attacked
            if not engine.squareAttacked(row, col+1, chess_piece, engine) and not engine.squareAttacked(row, col+2, chess_piece, engine): 
                moves.append(Move((row, col), (row, col+2), engine.board, isCastle=True)) #append move

    def getQueenSideCastleMoves(self, row, col, moves, engine, chess_piece):
        if engine.board[row][col-1] == "  " and engine.board[row][col-2] == "  " and engine.board[row][col-3] == "  ": #3) check to the left
            #if the two empty squares to the left aren't attacked
            if not engine.squareAttacked(row, col-1, chess_piece, engine) and not engine.squareAttacked(row, col-2, chess_piece, engine):
                moves.append(Move((row, col), (row, col-2), engine.board, isCastle=True)) #append move

class CastleRights:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs =bqs

class Move:
    #maps keys to values
    #key : value
    #these dictionaries are  what we will use to get chess notation
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()} #reverses dictionary (value : key)
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, initial_square, final_square, board, isEnPassant = False, isCastle = False):
        self.initial_row = initial_square[0]
        self.initial_col = initial_square[1]
        self.final_row = final_square[0]
        self.final_col = final_square[1]
        self.pieceMoved = board[self.initial_row][self.initial_col] #initial_square(row, col)
        self.pieceCaptured = board[self.final_row][self.final_col]  #final_square(row, col)
        
        #unique moveID between 0 and 7777. For example: 0002 would mean a move from [0, 0] to [0, 2]
        self.moveID = self.initial_row * 1000 + self.initial_col * 100 + self.final_row * 10 + self.final_col 

        #pawn promotion
        self.isPawnPromotion = False
        if (self.pieceMoved == "wP" and self.final_row == 0) or (self.pieceMoved == "bP" and self.final_row == 7):
            self.isPawnPromotion = True
        
        #en passant
        #we need to pass an optional parameter isEnPassant for en passant moves
        self.isEnPassant = isEnPassant
        
        if self.isEnPassant: #if next move is en passant move
            if self.pieceMoved == "bP": #if black pawn has en passant
                self.pieceCaptured = "wP" #white pawn is stored as the captured piece
            else: #else, black's pawn is stored as the captured piece
                self.pieceCaptured = "bP"
        
        #castle move
        self.isCastle = isCastle

    #overriding the built-in equals method
    def __eq__(self, other): #compares an object to another object which is saved in the parameter "other" 
        """Make sure other object is an instance of the Move class, since if we were to compare a move to a number, 
        and then say something like Move().initial_row, it won't work!""" 
        if isinstance(other, Move): 
            return self.moveID == other.moveID #check if moveID's are equal
        return False

    def getChessNotation(self, engine): #gets chess notation
        piece = engine.board[self.initial_row][self.initial_col][1]
        if piece == "P":
            return self.getFileRank(self.final_row, self.final_col)
        else:
            return piece + self.getFileRank(self.final_row, self.final_col)
    
    def getFileRank(self, row, col): #convert from (row, col) notation to (file, rank) notation 
        return self.colsToFiles[col] + self.rowsToRanks[row]
    
    
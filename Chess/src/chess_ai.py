import random

import pygame as p

class ChessAI:
    def __init__(self):
        #in order to implement the algorithms, we need to assign a value to each piece.
        #we define a dictionary of pieces, mapped to their value on the chess board
        self.pieceValue = { 
                "P": 1, 
                "R": 5, 
                "N": 3, 
                "B": 3, 
                "Q": 9, 
                "K": 1000 #cannot be captured
                }
        self.CHECKMATE = 1000  #if positive, white wins, if negative, black wins
        self.STALEMATE = 0 #always better than a losing position

    def findRandomMove(self, validMoves): #used if algorithm can't come up with a move (endgames)
        return validMoves[random.randint(0, len(validMoves)-1)] #random move from list of valid ones

    #MinMax
    #1) after we make a move, look at opponent's max score
    #2) find the minimum score
    #find the best move, only considering material
    def findGreedyMove(self, chess_piece, engine, validMoves): #greedy algorithm
        turnMultiplier = 1 if engine.whiteTurn else -1 #so that algortihm can look at both colors
       
        opponentMinMaxScore = self.CHECKMATE #store highest possible score for black
        #we want to find the minimum of the opponent's best moves, so we have to think two moves into the future
        bestPlayerMove = None
        random.shuffle(validMoves)
        for playerMove in validMoves: #greedy algorithm begin #for each of our moves
            engine.makeMove(playerMove) #make our move
            opponentsMoves = engine.getValidMoves(chess_piece, engine) #get opponent's moves
            #opponent's best move
            opponentMaxScore = -self.CHECKMATE #since we are calculating two moves deep, positive and negative values change
            #go through all of opponent's moves and find their best possible move/score
            for opponentsMove in opponentsMoves:
                engine.makeMove(opponentsMove)
                if engine.checkMate:
                    score = -self.CHECKMATE * (-turnMultiplier) #current score of the board
                elif engine.stalemate:
                    score = self.STALEMATE
                score = self.scoreMaterial(engine.board) * (-turnMultiplier)
                if score > opponentMaxScore: #check if score is larger than opponent's max score so far
                    opponentMaxScore = score #if so, it becomes new max
                #greedy algorithm end
                engine.undo_move() #so that we can make our actual move
            #MinMax algorithm
            #for each move the player makes, what's the opponent's best response
            if opponentMaxScore < opponentMinMaxScore: #if opponent max score is less than their previous one
                opponentMinMaxScore = opponentMaxScore #then that becomes player's best move
                bestPlayerMove = playerMove
            engine.undo_move()
        return bestPlayerMove

    def scoreMaterial(self, board): #keep track of scores
        score = 0
         #look at each space and see if there is a piece there
         #if that piece is a white or black piece, we'll score based on its value in the dictionary
        for row in board:
            for square in row:
                if square[0] == "w":
                    score += self.pieceValue[square[1]]
                elif square[0] == "b":
                    score -= self.pieceValue[square[1]]
        return score

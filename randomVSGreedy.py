
from agents import Player
from dealer import Dealer
from random import randint
from bcolors import bcolors
from agents import GreedyAgent, ApproximateQLearningAgent, RandomAgent
from gameState import GameState
from saveWeights import saveWeights
from datetime import datetime

import sys

def runGame(p1, p2):
    p1.resetForNewGame()
    p2.resetForNewGame()
    d1 = Dealer(5)
    p1.cards = d1.dealCards()[0]
    p2.cards = d1.dealCards()[0]
    gameState = GameState(p1, p2)
    aqlearnScore = 0
    gameLoop = True
    while gameLoop:
        p1.pickCard()
        p2.pickCard()

        roundWinner = gameState.judgeRound(p1, p2)

        #? generating successor
        if roundWinner == p1:
            p1.accumulatedCards[p1.playedCard[1]] += 1
        if roundWinner == p2:
            p2.accumulatedCards[p2.playedCard[1]] += 1

        if gameState.judgeGameOver(p1, p2) == p1:
            return p1.name
            
        elif gameState.judgeGameOver(p1, p2) == p2:
            return p2.name

        p1.cards.append(d1.generateRandomCard())
        p2.cards.append(d1.generateRandomCard())


if __name__ == "__main__":
    now = datetime.now()
    dateString = now.strftime("%d-%m-%Y %HH %MM %SS.txt")

    sys.setrecursionlimit(10000000)
    # p1 = ApproximateQLearningAgent("aqlearn")
    p2 = GreedyAgent("Greedy")
    p1 = RandomAgent("random")
    games = 10000

    wins = 0
    for i in range(0, games):
        if runGame(p1, p2) == "Greedy":
            wins += 1
    print(p2.name + " won", str(wins), "out of", games, "games")
        

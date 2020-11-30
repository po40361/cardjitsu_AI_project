
from agents import Player
from dealer import Dealer
from random import randint
from bcolors import bcolors
from agents import GreedyAgent, ApproximateQLearningAgent, RandomAgent
from gameState import GameState
from saveWeights import saveWeights
from datetime import datetime

import sys

def runGame(p1, p2, mute):
    p1.resetForNewGame()
    p2.resetForNewGame()
    d1 = Dealer(5)
    p1.cards = d1.dealCards()[0]
    p2.cards = d1.dealCards()[0]
    gameState = GameState(p1, p2)
    aqlearnScore = 0
    gameLoop = True
    while gameLoop:

        # print(bcolors.OKBLUE+"opponent cards:")
        # for i, x in enumerate(p2.cards):
        #     print("     " + str(i + 1) + ". " + str(x))
        # print(bcolors.ENDC)

        #! aqlearn agent steps
            #1. update
            #2. get action
            #3. generateSuccessor

        # print("Your cards:")
        # # print(p1.cards)
        # for i, x in enumerate(p1.cards):
        #     print("     " + str(i + 1) + ". " + str(x))
        # print("Enter the numerical value of the card you'd like to pick.")

        # choice = int(input(">>> ")) - 1

        # if choice >= len(p1.cards):
        #     print(bcolors.WARNING + "Invalid index! Try again..." + bcolors.ENDC)
        #     continue

        p1.update(gameState, aqlearnScore)

        action = p1.doAction(gameState)

        p1.pickCard(action)
        p2.pickCard()

        #call agent.update()
        #


        roundWinner = gameState.judgeRound(p1, p2)

        #? generating successor
        if roundWinner == p1:
            # if not mute:
            #     print(bcolors.OKGREEN + "APQ won that round!" + bcolors.ENDC)
            p1.accumulatedCards[p1.playedCard[1]] += 1
        if roundWinner == p2:
            # if not mute:
            #     print(bcolors.FAIL + "APQ lost that round." + bcolors.ENDC)
            p2.accumulatedCards[p2.playedCard[1]] += 1

        #? get transitional rewards
        p1TransitionalReward = gameState.getRewards(p1, p2)
        aqlearnScore += p1TransitionalReward
        # print(bcolors.OKGREEN + "TransitionalRewards:", str(p1TransitionalReward) + bcolors.ENDC )
        # print(bcolors.OKGREEN + "Total Score:", str(aqlearnScore) + bcolors.ENDC )

        # print("           Score           ")
        # print("***************************")
        # print(p1.name + ": ")
        # print("Fire: " + str(p1.accumulatedCards["Fire"]))
        # print("Water: " + str(p1.accumulatedCards["Water"]))
        # print("Ice: " + str(p1.accumulatedCards["Ice"]))

        # print(p2.name + ": ")
        # print("Fire: " + str(p2.accumulatedCards["Fire"]))
        # print("Water: " + str(p2.accumulatedCards["Water"]))
        # print("Ice: " + str(p2.accumulatedCards["Ice"]))
        # print("")



        if gameState.judgeGameOver(p1, p2) == p1:
            p1.update(gameState, aqlearnScore)
            if not mute:
                print(bcolors.OKBLUE + "Game Over!", p1.name + " wins!" + bcolors.ENDC)
                p1.printEpisodeInfo()
            return (aqlearnScore, "aql")
            
        elif gameState.judgeGameOver(p1, p2) == p2:

            p1.update(gameState, aqlearnScore)
            if not mute:
                print(bcolors.FAIL + "Game Over!", p2.name + " wins!" + bcolors.ENDC)
                p1.printEpisodeInfo()
            return (aqlearnScore, "greedy")
            

        

        p1.cards.append(d1.generateRandomCard())
        p2.cards.append(d1.generateRandomCard())


if __name__ == "__main__":
    now = datetime.now()
    dateString = now.strftime("%d-%m-%Y %HH %MM %SS.txt")

    sys.setrecursionlimit(10000000)
    p1 = ApproximateQLearningAgent("aqlearn")
    # p2 = GreedyAgent("Greedy")
    p2 = RandomAgent("random")
    
    numTrainingEpisodes = 1000
    totalAQLearnScore = 0

    p1.args["epsilon"] = 0
    p1.args["alpha"] = 0

    originalEpsilon = p1.args["epsilon"]
    originalAlpha = p1.args["alpha"]

    for i in range(1, numTrainingEpisodes + 1):
        p1.args['epsilon'] = originalEpsilon * (i / numTrainingEpisodes)
        p1.args['alpha'] = originalAlpha * (i / numTrainingEpisodes)
        score = runGame(p1, p2, True)[0]
        totalAQLearnScore += score
        if i % (numTrainingEpisodes // 10) == 0:
            print(str(i), "training episodes completed.")
            print("Average Score:", str(totalAQLearnScore / i))
    
    wins = 0
    p1.args['epsilon'] = 0
    p1.args["alpha"] = 0
    games = 1000

    #save the weights in a file
    saveWeights(dateString, p1.weights, numTrainingEpisodes)

    for i in range(0, games):
        if runGame(p1, p2, True)[1] == "aql":
            wins += 1
    print("AQL won", str(wins), "out of", games, "games")
        

    
    # while gameLoop:

    #     # print(bcolors.OKBLUE+"opponent cards:")
    #     # for i, x in enumerate(p2.cards):
    #     #     print("     " + str(i + 1) + ". " + str(x))
    #     # print(bcolors.ENDC)

    #     #! aqlearn agent steps
    #         #1. update
    #         #2. get action
    #         #3. generateSuccessor

    #     # print("Your cards:")
    #     # # print(p1.cards)
    #     # for i, x in enumerate(p1.cards):
    #     #     print("     " + str(i + 1) + ". " + str(x))
    #     # print("Enter the numerical value of the card you'd like to pick.")

    #     # choice = int(input(">>> ")) - 1

    #     # if choice >= len(p1.cards):
    #     #     print(bcolors.WARNING + "Invalid index! Try again..." + bcolors.ENDC)
    #     #     continue

    #     p1.update(gameState, aqlearnScore)

    #     action = p1.doAction(gameState)

    #     p1.pickCard(action)
    #     p2.pickCard()

    #     #call agent.update()
    #     #


    #     roundWinner = gameState.judgeRound(p1, p2)

    #     #? generating successor
    #     if roundWinner == p1:
    #         print(bcolors.OKGREEN + "APQ won that round!" + bcolors.ENDC)
    #         p1.accumulatedCards[p1.playedCard[1]] += 1
    #     if roundWinner == p2:
    #         print(bcolors.FAIL + "APQ lost that round." + bcolors.ENDC)
    #         p2.accumulatedCards[p2.playedCard[1]] += 1

    #     #? get transitional rewards
    #     p1TransitionalReward = gameState.getRewards(p1, p2)
    #     aqlearnScore += p1TransitionalReward
    #     print(bcolors.OKGREEN + "TransitionalRewards:", str(p1TransitionalReward) + bcolors.ENDC )
    #     print(bcolors.OKGREEN + "Total Score:", str(aqlearnScore) + bcolors.ENDC )

    #     print("           Score           ")
    #     print("***************************")
    #     print(p1.name + ": ")
    #     print("Fire: " + str(p1.accumulatedCards["Fire"]))
    #     print("Water: " + str(p1.accumulatedCards["Water"]))
    #     print("Ice: " + str(p1.accumulatedCards["Ice"]))

    #     print(p2.name + ": ")
    #     print("Fire: " + str(p2.accumulatedCards["Fire"]))
    #     print("Water: " + str(p2.accumulatedCards["Water"]))
    #     print("Ice: " + str(p2.accumulatedCards["Ice"]))
    #     print("")



    #     if gameState.judgeGameOver(p1, p2) == p1:
    #         print(bcolors.OKBLUE + "Game Over!", p1.name + " wins!" + bcolors.ENDC)
    #         p1.update(gameState, aqlearnScore)
    #         p1.printEpisodeInfo()
    #         break
    #     elif gameState.judgeGameOver(p1, p2) == p2:
    #         print(bcolors.OKBLUE + "Game Over!", p2.name + " wins!" + bcolors.ENDC)
    #         p1.update(gameState, aqlearnScore)
    #         p1.printEpisodeInfo()
    #         break

        

    #     p1.cards.append(d1.generateRandomCard())
    #     p2.cards.append(d1.generateRandomCard())



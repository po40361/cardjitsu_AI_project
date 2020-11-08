
from agents import Player
from dealer import Dealer
from random import randint
from bcolors import bcolors
from agents import GreedyAgent
from gameState import GameState

    
if __name__ == "__main__":
    gameLoop = True
    p1 = Player("powei")
    d1 = Dealer(5)
    p1.cards = d1.dealCards()[0]
    p2 = GreedyAgent("Greedy")
    p2.cards = d1.dealCards()[0]
    gameState = GameState(p1, p2)

    while gameLoop:

        print(bcolors.OKBLUE+"opponent cards:")
        for i, x in enumerate(p2.cards):
            print("     " + str(i + 1) + ". " + str(x))
        print(bcolors.ENDC)


        print("Your cards:")
        # print(p1.cards)
        for i, x in enumerate(p1.cards):
            print("     " + str(i + 1) + ". " + str(x))
        print("Enter the numerical value of the card you'd like to pick.")

        choice = int(input(">>> ")) - 1

        if choice >= len(p1.cards):
            print(bcolors.WARNING + "Invalid index! Try again..." + bcolors.ENDC)
            continue

        p1.pickCard(choice)
        p2.pickCard()
        roundWinner = gameState.judgeRound(p1, p2)

        if roundWinner == p1:
            print(bcolors.OKGREEN + "You won that round!" + bcolors.ENDC)
            # p1.accumulatedCards[p1.playedCard[1]] += 1
        if roundWinner == p2:
            print(bcolors.FAIL + "You lost that round." + bcolors.ENDC)
            p2.accumulatedCards[p2.playedCard[1]] += 1

        print("           Score           ")
        print("***************************")
        print(p1.name + ": ")
        print("Fire: " + str(p1.accumulatedCards["Fire"]))
        print("Water: " + str(p1.accumulatedCards["Water"]))
        print("Ice: " + str(p1.accumulatedCards["Ice"]))

        print(p2.name + ": ")
        print("Fire: " + str(p2.accumulatedCards["Fire"]))
        print("Water: " + str(p2.accumulatedCards["Water"]))
        print("Ice: " + str(p2.accumulatedCards["Ice"]))
        print("")

        if gameState.judgeGameOver(p1, p2) == p1:
            print(bcolors.OKBLUE + "Game Over!", p1.name + " wins!" + bcolors.ENDC)
            break
        elif gameState.judgeGameOver(p1, p2) == p2:
            print(bcolors.OKBLUE + "Game Over!", p2.name + " wins!" + bcolors.ENDC)
            break

        p1.cards.append(d1.generateRandomCard())
        p2.cards.append(d1.generateRandomCard())



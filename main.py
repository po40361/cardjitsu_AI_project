
from player import Player
from dealer import Dealer
from random import randint
from bcolors import bcolors


def judgeRound(p1, p2):
    #returns winner of a round
    p1Card = p1.playedCard
    p2Card = p2.playedCard
    print(p1.name + " chose: " + str(p1.playedCard))
    print(p2.name + "chose: " + str(p2.playedCard))

    if p1Card[1] == p2Card[1]:
        return max(p1, p2, key=lambda x: x.playedCard[1])
    else:
        if p1Card[1] == "Fire" and p2Card[1] == "Water":
            return p2
        elif p1Card[1] == "Fire" and p2Card[1] == "Ice":
            return p1
        elif p1Card[1] == "Water" and p2Card[1] == "Fire":
            return p1
        elif p1Card[1] == "Water" and p2Card[1] == "Ice":
            return p2
        elif p1Card[1] == "Ice" and p2Card[1] == "Fire":
            return p2
        elif p1Card[1] == "Ice" and p2Card[1] == "Water":
            return p1

def judgeStreak(cards):
    #A streak is when you have 3 of the same cards acccumulated. A win condition
    if cards["Fire"] == 3 or cards["Ice"] == 3 or cards["Water"] == 3:
        return True
    else:
        return False

def judgeThreeOfAKind(cards):
    if cards["Fire"] >= 1 and cards["Ice"] >= 1 and cards["Water"] >= 1:
        return True
    else:
        return False

def judgeGameOver(p1, p2):
    if judgeStreak(p1.accumulatedCards) or judgeThreeOfAKind(p1.accumulatedCards):
        return p1
    elif judgeStreak(p2.accumulatedCards) or judgeThreeOfAKind(p2.accumulatedCards):
        return p2
    else:
        return None
    
if __name__ == "__main__":
    gameLoop = True
    p1 = Player("powei")
    d1 = Dealer(5)
    p1.cards = d1.dealCards()[0]
    p2 = Player("A.I.")
    p2.cards = d1.dealCards()[0]

    while gameLoop:
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
        p2.pickCard(randint(0, 4))
        roundWinner = judgeRound(p1, p2)

        if roundWinner == p1:
            print(bcolors.OKGREEN + "You won that round!" + bcolors.ENDC)
            p1.accumulatedCards[p1.playedCard[1]] += 1
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

        if judgeGameOver(p1, p2) == p1:
            print(bcolors.OKBLUE + "Game Over!", p1.name + " wins!" + bcolors.ENDC)
            break
        elif judgeGameOver(p1, p2) == p2:
            print(bcolors.OKBLUE + "Game Over!", p2.name + " wins!" + bcolors.ENDC)
            break

        p1.cards.append(d1.generateRandomCard())
        p2.cards.append(d1.generateRandomCard())




from player import Player
from dealer import Dealer
from random import randint
from bcolors import bcolors


def judgeOutcome(p1, p2):
    #returns winner
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
    roundWinner = judgeOutcome(p1, p2)
    if roundWinner == p1:
        print(bcolors.OKGREEN + "You won that round!" + bcolors.ENDC)
    if roundWinner == p2:
        print(bcolors.FAIL + "You lost that round." + bcolors.ENDC)
    p1.cards.append(d1.generateRandomCard())
    p2.cards.append(d1.generateRandomCard())



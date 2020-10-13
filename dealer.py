from random import randint

class Dealer:
    def __init__(self, startingCardNumber ):
        self.startingCardNumber = startingCardNumber
        self.cardElements = ["Water", "Fire", "Ice"]

    def generateRandomCard(self):
        cardValue = randint(1, 10)
        cardElement = self.cardElements[randint(0, 2)]
        return (cardValue, cardElement)

    def dealCards(self):
        p1Cards = []
        p2Cards = []
        for _ in range(0, self.startingCardNumber):
            p1Cards.append(self.generateRandomCard())
            p2Cards.append(self.generateRandomCard())
        return [p1Cards, p2Cards]
    

            



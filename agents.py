from random import randint

class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.accumulatedCards = {"Fire": 0, "Water": 0, "Ice": 0}
        self.playedCard = None
    
    def pickCard(self, index):
        # Takes in the index of the card to be picked in self.cards
        self.playedCard = self.cards[index]
        self.cards.pop(index)
        return
    
# from main import judgeStreak, judgeThreeOfAKind
class GreedyAgent(Player):

    def pickCard(self):
        currentCards = {"Fire": [], "Water": [], "Ice": []}
        for c in self.cards:
            currentCards[c[1]].append(c)
        # print("self.accumulatedCards", self.accumulatedCards)
        # print(" ")
        # print("currentCards", currentCards)
        pickedElement = self.checkForThreeOfAKind(currentCards)
        if pickedElement == "":
            if self.accumulatedCards["Fire"] + len(currentCards["Fire"]) >= 3:
                pickedElement = "Fire"
            elif self.accumulatedCards["Water"] + len(currentCards["Water"]) >= 3:
                pickedElement = "Water"
            elif self.accumulatedCards["Ice"] + len(currentCards["Ice"]) >= 3:
                pickedElement = "Ice"
        # else:
        #     # check for three of a kind
        #     elements = ["Fire", "Ice", "Water"]
        #     i = 0
        #     while len(elements) > 1 and i < len(elements):
        #         if self.accumulatedCards[elements[i]] > 0:
        #             elements.pop(i)
        #         else:
        #             i += 1
        #     if len(elements) == 0:
        #         pickedElement = elements[0]
        
        if pickedElement:
            card = max(currentCards[pickedElement], key=lambda x: x[0])
        else:
            card = max(self.cards, key=lambda x: x[0])
        
        self.playedCard = card
        self.cards.remove(card)
        return

    def checkForThreeOfAKind(self, currentCards):
        pickedElement = ""
        elements = ["Fire", "Ice", "Water"]
        i = 0
        while len(elements) > 1 and i < len(elements):
            if self.accumulatedCards[elements[i]] > 0:
                elements.pop(i)
            else:
                i += 1
        print("elements", elements)
        if len(elements) == 1:
            print("currentCards", currentCards)
            if len(currentCards[elements[0]]) > 0:
                pickedElement = elements[0]
        print("elements", elements)
        print("pickedElement after check()", pickedElement)
        return pickedElement

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
    

        
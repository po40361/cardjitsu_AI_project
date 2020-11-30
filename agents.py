import random
import copy
from collections import Counter
from featureExtractor import FeatureExtractor
from bcolors import bcolors

class Player:
    def __init__(self, name):
        self.name = name
        self.cards = [] #(cardValue, cardElement)
        self.accumulatedCards = {"Fire": 0, "Water": 0, "Ice": 0}
        self.playedCard = None
    
    def pickCard(self, index):
        # Takes in the index of the card to be picked in self.cards
        self.playedCard = self.cards[index]
        self.cards.pop(index)
        return

    def resetForNewGame(self):
        self.cards = []
        self.accumulatedCards = {"Fire": 0, "Water": 0, "Ice": 0}
        self.playedCard = None
    
# from main import judgeStreak, judgeThreeOfAKind
class GreedyAgent(Player):

    def pickCard(self):
        currentCards = {"Fire": [], "Water": [], "Ice": []}
        for c in self.cards:
            currentCards[c[1]].append(c)

        pickedElement = self.checkForThreeOfAKind(currentCards)
        if pickedElement == "":
            if self.accumulatedCards["Fire"] + len(currentCards["Fire"]) >= 3:
                pickedElement = "Fire"
            elif self.accumulatedCards["Water"] + len(currentCards["Water"]) >= 3:
                pickedElement = "Water"
            elif self.accumulatedCards["Ice"] + len(currentCards["Ice"]) >= 3:
                pickedElement = "Ice"
        
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
        # print("elements", elements)
        if len(elements) == 1:
            # print("currentCards", currentCards)
            if len(currentCards[elements[0]]) > 0:
                pickedElement = elements[0]
        # print("elements", elements)
        # print("pickedElement after check()", pickedElement)
        return pickedElement

class RandomAgent(Player):
    def pickCard(self):
        card = random.choice(self.cards)
        self.playedCard = card
        self.cards.remove(card)

class ApproximateQLearningAgent(Player):
    def __init__(self, name, epsilon=0.05, gamma=0.8, alpha=0.2, numTraining=0):
        self.name = name
        self.cards = [] #(cardValue, cardElement)
        self.accumulatedCards = {"Fire": 0, "Water": 0, "Ice": 0}
        self.playedCard = None

        self.args = {}
        self.args['epsilon'] = epsilon
        self.args['gamma'] = gamma
        self.args['alpha'] = alpha
        self.args['numTraining'] = numTraining
        self.weights = Counter()

        # self.weights["enemy-distance-to-closest-win"] = 1.3999995454998298e-06 
        # self.weights["agent-distance-to-closest-win"] = 1.299999463999758e-06

        self.weights["enemy-distance-to-closest-win"] = -4.120535635213156 
        self.weights["agent-distance-to-closest-win"] = 9.586679017815417 
        self.weights["agent-went-closer-to-win"] = -0.9656494587969497 
        self.weights["agent-can-block-enemy-advancement"] = 15.147299275663869 


        self.featExtractor = FeatureExtractor()
        self.lastState = None
        self.lastAction = None
        self.lastScore = 0
    
    def resetForNewGame(self):
        self.cards = []
        self.accumulatedCards = {"Fire": 0, "Water": 0, "Ice": 0}
        self.playedCard = None
        self.lastState = None
        self.lastAction = None
        self.lastScore = 0


    def pickCard(self, card):
        # Takes in the index of the card to be picked in self.cards
        if card not in self.cards:
            print(card)
            print(self.cards)
            raise ValueError('Picked card not in current cards!')

        self.playedCard = card
        self.cards.remove(card)
        return

    def getLegalActions(self, gameState):
        if self.name == gameState.p1.name:
            return gameState.p1.cards
        else:
            return gameState.p2.cards
        return self.cards

        
    def getQValue(self, gameState, action):
        """
          Should return Q(gameState,action) = w * featureVector
          where * is the dotProduct operator
        """
        result = 0
        features = self.featExtractor.getFeatures(gameState, action, self.name)
        for feature in features:
          result += features[feature] * self.weights[feature]
        return result

    def flipCoin(self, prob):
        r = random.random()
        return r < prob

    def computeActionFromQValues(self, gameState):
        actions = self.getLegalActions(gameState)
        max_action = None
        max_q_val = float("inf")
        if not actions:
            return None
        for a in actions:
            q_val = self.getQValue(gameState, a)
            if q_val < max_q_val:
                max_q_val = q_val
                max_action = a
        if max_action is None:
            return random.choice(actions)
        else:
            return max_action  

    def doAction(self, gameState):
        legalActions = self.getLegalActions(gameState)
        action = None
        "*** YOUR CODE HERE ***"
        # if not legalActions:
        #     action = None
        # else:
        coinflip = self.flipCoin(self.args["epsilon"])
        if coinflip:
            action = random.choice(legalActions)
        elif not coinflip:
            action = self.computeActionFromQValues(gameState)
        
        # print("setting lastState")
        self.lastState = copy.deepcopy(gameState) 
        # print("self.lastState",self.lastState)
        self.lastAction = copy.deepcopy(action)

        return action

    def update(self, gameState, score):
        """
           Should update your weights based on transition
        """
        # deleted action, nextState, reward from params
        # print("self.lastState",self.lastState)
        if self.lastState is not None:
            state, action, nextState, deltaReward = self.lastState, self.lastAction, gameState, score - self.lastScore

            actions = self.getLegalActions(nextState)
            max_qval_action = (float("-inf"), None)
            if not actions:
                max_qval_action = 0
            elif actions:
                for a in actions:
                    #! going through all the actions to get max action
                    q_val = self.getQValue(nextState, a)
                    max_qval_action = max(max_qval_action, (q_val, a), key=lambda x: x[0])
            difference = deltaReward + self.args['gamma'] * max_qval_action[0] - self.getQValue(state, action)
            
            features = self.featExtractor.getFeatures(state, action, self.name)
            for feature in features:
            # print(feature, "weights:", self.weights[feature])
                self.weights[feature] = self.weights[feature] + self.args['alpha'] * difference * features[feature]
        
        self.lastScore = score

    def printEpisodeInfo(self):
        print(bcolors.OKBLUE + "AQL score:", str(self.lastScore))
        print(bcolors.OKBLUE + "AQL accumulated cards:", str(self.accumulatedCards))
        # print(bcolors.OKBLUE + "AQL weights:")

        # for key, value in self.weights.items():
        #     print("     ",key, value)

        print( bcolors.ENDC)


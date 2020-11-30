from collections import Counter
import copy
class FeatureExtractor:

    def getEnemyDistanceToWin(self, enemyAccumulatedCards):
        #enemy distance will be assuming worst case (enemy has all cards necessary)
        minDistance = float('inf')
        #checking distance to streak wins
        for element in enemyAccumulatedCards:
            distance =  3 - enemyAccumulatedCards[element] 
            minDistance = min(distance, minDistance)
        
        threeKind = 0
        for element in enemyAccumulatedCards:
            if enemyAccumulatedCards[element] > 0:
                threeKind += 1
        
        minDistance = min(3 - threeKind, minDistance)
        return minDistance


    def canBlockEnemyWin(self, action, enemyAccumulatedCards):
        enemyPossibleElements = set()
        if enemyAccumulatedCards["Fire"] == 2:
            enemyPossibleElements.add("Fire")
        if enemyAccumulatedCards["Ice"] == 2:
            enemyPossibleElements.add("Ice")
        if enemyAccumulatedCards["Water"] == 2:
            enemyPossibleElements.add("Water")
        
        if enemyAccumulatedCards["Fire"] >= 1 and enemyAccumulatedCards["Ice"] >= 1:
            enemyPossibleElements.add("Water")

        if enemyAccumulatedCards["Water"] >= 1 and enemyAccumulatedCards["Ice"] >= 1:
            enemyPossibleElements.add("Fire")
        
        if enemyAccumulatedCards["Fire"] >= 1 and enemyAccumulatedCards["Water"] >= 1:
            enemyPossibleElements.add("Ice")
        
        if action[1] in enemyPossibleElements:
            return 1
        else:
            return 0



    def getAgentDistanceToWin(self, agentAccumulatedCards, agentCards):
        # agent distance will be assuming best case given current cards (assume 
        # next round we'll get the cards we need if we don't have them)
        # agentAccumulatedCards = copy.deepcopy(agent.accumulatedCards)
        minDistance = float('inf')
        #checking distance to streak wins
        for element in agentAccumulatedCards:
            distance =  3 - agentAccumulatedCards[element] 
            onHand = 0
            for card in agentCards:
                if card[1] == element:
                    onHand += 1
            if onHand == 0:
                distance += 1
            minDistance = min(distance, minDistance)
        
        #finding three of a kind distance
        threeKind = 0
        elements = ["Fire", "Ice", "Water"]
        for element in agentAccumulatedCards:
            if agentAccumulatedCards[element] > 0:
                threeKind += 1
                elements.remove(element)
        
        distance = 3 - threeKind
        for element in elements:
            for card in agentCards:
                if card[1] == element:
                    onHand += 1
            if onHand == 0:
                distance += 1

        minDistance = min(distance, minDistance)
        return minDistance
        
   


    def getFeatures(self, gameState, action, agentName):
        #make this correspond to an action, so u get an action and then pretend like you already did it.
        features = Counter()

        if gameState.p1.name == agentName:
            enemyAccumulatedCards = copy.deepcopy(gameState.p2.accumulatedCards)
            agentAccumulatedCards = copy.deepcopy(gameState.p1.accumulatedCards)
            agentCards = copy.deepcopy(gameState.p1.cards)
        else:
            enemyAccumulatedCards = copy.deepcopy(gameState.p1.accumulatedCards)
            agentAccumulatedCards = copy.deepcopy(gameState.p2.accumulatedCards)
            agentCards = copy.deepcopy(gameState.p2.cards)

        #action is the card to be played
        # features["agent-went-closer-to-win"] = self.agentAdvancedToWin(action, agentAccumulatedCards)
        prevAgentMinDistanceToWin = self.getAgentDistanceToWin(agentAccumulatedCards, agentCards)
        agentCards.remove(action)
        agentAccumulatedCards[action[1]] += 1

        features["enemy-distance-to-closest-win"] = self.getEnemyDistanceToWin(enemyAccumulatedCards)
        if features["enemy-distance-to-closest-win"] == 1:
            features["agent-can-block-enemy-advancement"] = self.canBlockEnemyWin(action, enemyAccumulatedCards)
        # else:
        #     features["agent-can-block-enemy-advancement"] = self.canBlockEnemyAdvancement(action, enemyAccumulatedCards)


        # this feature measures the agent's distance to closest win assuming that it wins this current round
        features["agent-distance-to-closest-win"] = self.getAgentDistanceToWin(agentAccumulatedCards, agentCards)
        
        if prevAgentMinDistanceToWin - features["agent-distance-to-closest-win"] > 0:
            features["agent-went-closer-to-win"] = 1

        # divisor = 10
        # divisor = float(divisor)
        # for key in features:
        #     features[key] /= divisor

        # 
        return features

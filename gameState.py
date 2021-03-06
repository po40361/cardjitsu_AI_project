from bcolors import bcolors
import copy

class GameState:
    def __init__(self, p1, p2):
        # self.players = {
        #     p1.name: p1,
        #     p2.name: p2
        # }
        self.p1 = p1
        self.p2 = p2
        

    def judgeRound(self, p1, p2):
        #returns winner of a round
        p1Card = p1.playedCard
        p2Card = p2.playedCard
        # print(self.p1.cards)
        # print(p1.name + " chose: " + str(p1.playedCard))
        # print(p2.name + "chose: " + str(p2.playedCard))

        if p1Card[1] == p2Card[1]:
            return max(p1, p2, key=lambda x: x.playedCard[0])
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

    def judgeStreak(self, cards):
        #A streak is when you have 3 of the same cards acccumulated. A win condition
        if cards["Fire"] == 3 or cards["Ice"] == 3 or cards["Water"] == 3:
            return True
        else:
            return False

    def judgeThreeOfAKind(self, cards):
        if cards["Fire"] >= 1 and cards["Ice"] >= 1 and cards["Water"] >= 1:
            return True
        else:
            return False

    def judgeGameOver(self, p1, p2):
        if self.judgeStreak(p1.accumulatedCards) or self.judgeThreeOfAKind(p1.accumulatedCards):
            return p1
        elif self.judgeStreak(p2.accumulatedCards) or self.judgeThreeOfAKind(p2.accumulatedCards):
            return p2
        else:
            return None
    
    def getRewards(self, agent, enemy):
        reward = 0
        roundWinner = self.judgeRound(agent, enemy)
        if roundWinner == agent:
            reward += 5
            if self.blockedEnemyVictory(agent, enemy):
                # print(bcolors.OKGREEN + "Enemy Victory Blocked!" + bcolors.ENDC)
                reward += 10
            if self.judgeGameOver(agent, enemy):
                reward += 20
        else:
            reward -= 5
            if self.judgeGameOver(agent, enemy):
                reward -= 20
        return reward
        
    def blockedEnemyVictory(self, agent, enemy):
        """ Checking if agent blocked enemy victory """
        enemyCards = copy.deepcopy(enemy.accumulatedCards)
        enemyCards[enemy.playedCard[1]] += 1
        if self.judgeStreak(enemyCards) or self.judgeThreeOfAKind(enemyCards):
            return True
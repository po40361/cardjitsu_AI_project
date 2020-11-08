# from main import judgeThreeOfAKind, judgeStreak
import unittest

from agents import GreedyAgent
# from gameState import judgeThreeOfAKind, judgeStreak

# class TestJudgeMethods(unittest.TestCase):

#     def test_judge_threeofakind(self):
#         self.assertFalse(judgeThreeOfAKind({"Fire": 0, "Water": 0, "Ice": 0}))
#         self.assertTrue(judgeThreeOfAKind({"Fire": 1, "Water": 1, "Ice": 1}))
#         self.assertTrue(judgeThreeOfAKind({"Fire": 2, "Water": 2, "Ice": 2}))
#         self.assertFalse(judgeThreeOfAKind({"Fire":0, "Water": 2, "Ice": 2}))

#     def test_judge_streak(self):
#         self.assertFalse(judgeStreak({"Fire": 0, "Water": 0, "Ice": 0}))
#         self.assertFalse(judgeStreak({"Fire": 1, "Water": 1, "Ice": 1}))
#         self.assertTrue(judgeStreak({"Fire": 3, "Water": 0, "Ice": 0}))
#         self.assertTrue(judgeStreak({"Fire": 0, "Water": 3, "Ice": 0}))
#         self.assertTrue(judgeStreak({"Fire": 0, "Water": 0, "Ice": 3}))

class TestGreedyAgent(unittest.TestCase):
        
    def pick_highest_num_test(self):
        greedyAgent = GreedyAgent("greedy")
        greedyAgent.cards = [(2, "Fire"), (3, "Ice"), (4, "Water")]
        greedyAgent.pickCard()
        self.assertEqual(greedyAgent.playedCard, (4, "Water"))
    
    def pick_low_num_for_streak(self):
        greedyAgent = GreedyAgent("greedy")
        greedyAgent.cards = [(2, "Fire"), (3, "Ice"), (4, "Water")]
        greedyAgent.pickCard()
        greedyAgent.accumulatedCards["Water"] += 1
        greedyAgent.cards.append((1, "Water"))
        greedyAgent.cards.append((0, "Water"))
        greedyAgent.pickCard()
        self.assertEqual(greedyAgent.playedCard, (1, "Water"))
        greedyAgent.accumulatedCards["Water"] += 1
        greedyAgent.pickCard()
        self.assertEqual(greedyAgent.playedCard, (0, "Water"))
    
    def pick_random(self):
        greedyAgent = GreedyAgent("greedy")
        greedyAgent.cards = [(3, "Fire"), (3, "Ice"), (3, "Water")]
        



suite = unittest.TestLoader().loadTestsFromTestCase(TestGreedyAgent)
unittest.TextTestRunner(verbosity=2).run(suite)
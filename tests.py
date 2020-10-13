from main import judgeThreeOfAKind, judgeStreak
import unittest

class TestJudgeMethods(unittest.TestCase):

    def test_judge_threeofakind(self):
        self.assertFalse(judgeThreeOfAKind({"Fire": 0, "Water": 0, "Ice": 0}))
        self.assertTrue(judgeThreeOfAKind({"Fire": 1, "Water": 1, "Ice": 1}))
        self.assertTrue(judgeThreeOfAKind({"Fire": 2, "Water": 2, "Ice": 2}))
        self.assertFalse(judgeThreeOfAKind({"Fire":0, "Water": 2, "Ice": 2}))

    def test_judge_streak(self):
        self.assertFalse(judgeStreak({"Fire": 0, "Water": 0, "Ice": 0}))
        self.assertFalse(judgeStreak({"Fire": 1, "Water": 1, "Ice": 1}))
        self.assertTrue(judgeStreak({"Fire": 3, "Water": 0, "Ice": 0}))
        self.assertTrue(judgeStreak({"Fire": 0, "Water": 3, "Ice": 0}))
        self.assertTrue(judgeStreak({"Fire": 0, "Water": 0, "Ice": 3}))

suite = unittest.TestLoader().loadTestsFromTestCase(TestJudgeMethods)
unittest.TextTestRunner(verbosity=2).run(suite)
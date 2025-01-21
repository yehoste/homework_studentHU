import unittest
from tree import Record, Diagnoser, build_tree, optimal_tree

class TestDiagnoser(unittest.TestCase):
    def setUp(self):
        self.record1 = Record("influenza", ["cough", "fever"])
        self.record2 = Record("cold", ["cough"])
        self.record3 = Record("healthy", [])
        self.records = [self.record1, self.record2, self.record3]

    def test_build_tree(self):
        tree = build_tree(self.records, ["fever"])
        self.assertIsInstance(tree, Diagnoser)
        self.assertEqual(tree.diagnose(["fever"]), "influenza")
        self.assertEqual(tree.diagnose([]), "cold")

    def test_optimal_tree(self):
        tree = optimal_tree(self.records, ["cough", "fever"], 1)
        self.assertIsInstance(tree, Diagnoser)
        self.assertIn(tree.diagnose(["cough"]), ["influenza", "cold"])
        self.assertEqual(tree.diagnose([]), "healthy")

    def test_minimize(self):
        tree = build_tree(self.records, ["cough", "fever"])
        tree.minimize()
        self.assertEqual(tree.diagnose(["cough"]), "cold")
        self.assertEqual(tree.diagnose(["fever"]), "influenza")
        self.assertEqual(tree.diagnose([]), "healthy")

if __name__ == "__main__":
    unittest.main()

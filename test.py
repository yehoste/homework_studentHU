import unittest
from tree import Record, Node, Diagnoser, build_tree, optimal_tree, parse_data

class TestDiagnoser(unittest.TestCase):
    def setUp(self):
        self.records = [
            Record("Flu", ["fever", "cough"]),
            Record("Cold", ["cough"]),
            Record("Covid", ["fever", "cough", "fatigue"]),
            Record("Allergy", ["sneezing"])
        ]
        
        self.symptoms = ["fever", "cough", "fatigue", "sneezing"]
        self.diagnoser = build_tree(self.records, self.symptoms)

    def test_diagnose(self):
        self.assertEqual(self.diagnoser.diagnose(["fever", "cough"]), "Flu")
        self.assertEqual(self.diagnoser.diagnose(["cough"]), "Cold")
        self.assertEqual(self.diagnoser.diagnose(["fever", "cough", "fatigue"]), "Covid")
        self.assertEqual(self.diagnoser.diagnose(["sneezing"]), "Allergy")
        self.assertIsNone(self.diagnoser.diagnose(["headache"]))

    def test_calculate_success_rate(self):
        success_rate = self.diagnoser.calculate_success_rate(self.records)
        self.assertTrue(0 <= success_rate <= 1)

    def test_all_illnesses(self):
        illnesses = self.diagnoser.all_illnesses()
        expected = ["Flu", "Cold", "Covid", "Allergy"]
        self.assertCountEqual(illnesses, expected)

    def test_paths_to_illness(self):
        paths = self.diagnoser.paths_to_illness("Flu")
        self.assertTrue(any(isinstance(path, list) for path in paths))

    def test_minimize(self):
        self.diagnoser.minimize()
        self.assertIsNotNone(self.diagnoser.root)

    def test_build_tree_exceptions(self):
        with self.assertRaises(TypeError):
            build_tree(["invalid"], self.symptoms)
        with self.assertRaises(TypeError):
            build_tree(self.records, [42])

    def test_optimal_tree(self):
        optimal = optimal_tree(self.records, self.symptoms, 2)
        self.assertIsInstance(optimal, Diagnoser)

    # def test_parse_data(self):
    #     # Assuming "test_data.txt" contains valid formatted data
    #     records = parse_data("test_data.txt")
    #     self.assertTrue(all(isinstance(record, Record) for record in records))

if __name__ == "__main__":
    unittest.main()

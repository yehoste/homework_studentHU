import itertools
from collections import Counter

class Record:
    def __init__(self, illness, symptoms):
        self.illness = illness
        self.symptoms = symptoms

class Node:
    def __init__(self, data, yes_child=None, no_child=None):
        self.data = data
        self.yes_child = yes_child
        self.no_child = no_child


def parse_data(filepath):
    records = []
    with open(filepath, "r") as file:
        for line in file:
            parts = line.strip().split()
            if parts:
                illness, symptoms = parts[0], parts[1:]
                records.append(Record(illness, symptoms))
    return records

class Diagnoser:
    def __init__(self, root):
        self.root = root

    def diagnose(self, symptoms):
        node = self.root
        while node.yes_child and node.no_child:
            if node.data in symptoms:
                node = node.yes_child
            else:
                node = node.no_child
        return node.data
    
    def calculate_success_rate(self, records):
        if not records:
            raise ValueError("Records list is empty")
        successes = sum(1 for record in records if self.diagnose(record.symptoms) == record.illness)
        return successes / len(records)

    def all_illnesses(self):
        illness_count = {}

        def traverse(node):
            if node.positive_child is None and node.negative_child is None:
                if node.data:
                    illness_count[node.data] = illness_count.get(node.data, 0) + 1
            else:
                traverse(node.positive_child)
                traverse(node.negative_child)

        traverse(self.root)
        return sorted(illness_count, key=lambda illness: -illness_count[illness])

    def paths_to_illness(self, illness):
        paths = []

        def traverse(node, path):
            if node.positive_child is None and node.negative_child is None:
                if node.data == illness:
                    paths.append(path)
            else:
                traverse(node.positive_child, path + [True])
                traverse(node.negative_child, path + [False])

        traverse(self.root, [])
        return paths

    def minimize(self, remove_empty=False):
        def helper(node):
            if not node or (not node.yes_child and not node.no_child):
                return node
            node.yes_child = helper(node.yes_child)
            node.no_child = helper(node.no_child)
            if node.yes_child and node.no_child and node.yes_child.data == node.no_child.data:
                return node.yes_child
            if remove_empty and (not node.yes_child or not node.no_child):
                return node.yes_child if node.yes_child else node.no_child
            return node
        self.root = helper(self.root)



def build_tree(records, symptoms):
    if not all(isinstance(record, Record) for record in records):
        raise TypeError("All elements in records must be of type Record.")
    if not all(isinstance(symptom, str) for symptom in symptoms):
        raise TypeError("All elements in symptoms must be strings.")

    def build_recursive(records_subset, remaining_symptoms):
        if not remaining_symptoms:  # If no symptoms left, return the most common illness
            illnesses = [record.illness for record in records_subset]
            most_common = Counter(illnesses).most_common(1)
            return Node(most_common[0][0] if most_common else None)

        symptom = remaining_symptoms[0]
        yes_records = [record for record in records_subset if symptom in record.symptoms]
        no_records = [record for record in records_subset if symptom not in record.symptoms]

        yes_branch = build_recursive(yes_records, remaining_symptoms[1:])
        no_branch = build_recursive(no_records, remaining_symptoms[1:])

        return Node(symptom, yes_branch, no_branch)

    return Diagnoser(build_recursive(records, symptoms))


def optimal_tree(records, symptoms, depth):
    if not (0 <= depth <= len(symptoms)):
        raise ValueError("Depth must be between 0 and len(symptoms).")
    if len(set(symptoms)) != len(symptoms):
        raise ValueError("Symptoms list must not contain duplicates.")
    if not all(isinstance(record, Record) for record in records):
        raise TypeError("All elements in records must be of type Record.")
    if not all(isinstance(symptom, str) for symptom in symptoms):
        raise TypeError("All elements in symptoms must be strings.")

    best_diagnoser = None
    best_accuracy = 0

    for subset in itertools.combinations(symptoms, depth):
        diagnoser = build_tree(records, list(subset))
        accuracy = diagnoser.calculate_success_rate(records)  # Assumes this function exists

        if accuracy > best_accuracy:
            best_diagnoser = diagnoser
            best_accuracy = accuracy

    return best_diagnoser

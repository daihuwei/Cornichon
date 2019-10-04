import unittest


class AddOneOtherHelper(unittest.TestCase):
    """Test class helper"""
    def __init__(self):
        """Initialiser"""
        print("  Feature: Accumulator")
        print("    Scenario: Add one other")

    def GivenAnInitial(self, value):
        """Gherkin DSL step"""
        print("      Given an initial " + str(value))

    def WhenYouAddA(self, second):
        """Gherkin DSL step"""
        print("      When you add a " + str(second))

    def ThenTheResultIs(self, sum):
        """Gherkin DSL step"""
        print("      Then the result is " + str(sum))


class AddTwoOthersHelper(unittest.TestCase):
    """Test class helper"""
    def __init__(self):
        """Initialiser"""
        print("  Feature: Accumulator")
        print("    Scenario: Add two others")

    def GivenAnInitial(self, value):
        """Gherkin DSL step"""
        print("      Given an initial " + str(value))

    def WhenYouAddA(self, second):
        """Gherkin DSL step"""
        print("      When you add a " + str(second))

    def ThenTheResultIs(self, sum):
        """Gherkin DSL step"""
        print("      Then the result is " + str(sum))
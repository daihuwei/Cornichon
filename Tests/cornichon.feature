Feature: Cornichon

Background:
  Given a feature file called <name>

Scenario Outline: cppunittest
  When the generator is cppunittest
  Then the generated test is the same as the saved
  Examples:
    | name |
    | example |

Scenario Outline: cpphelpers
  When the generator is cpphelpers
  Then the generated test is the same as the saved
  Examples:
    | name |
    | example |

Scenario Outline: googletest
  When the generator is googletest
  Then the generated test is the same as the saved
  Examples:
    | name |
    | example |
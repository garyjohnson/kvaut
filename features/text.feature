Feature: Automate label
  As a developer testing my app
  I want to assert that text is visible
  So I can build tests

  Scenario: I see text
    Given I am running "_2_label.py"
    Then I see "Hello world"

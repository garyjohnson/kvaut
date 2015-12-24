Feature: Custom Automator
  As a developer testing my app
  I want to build custom automators
  So I can automate my custom widgets

  Scenario: Custom criteria is ignored by built-in automators
    Given I am running "_1_widget.py"
    Then I see "my_widget" with custom criteria

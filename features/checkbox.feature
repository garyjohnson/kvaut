Feature: Automate checkbox
  As a developer testing my app
  I want to assert that checkboxes are visible and checkable
  So I can build tests

  Scenario: I see checkbox
    Given I am running "_5_checkbox.py"
    Then I see "my_checkbox"

  Scenario: I can inspect checkbox state
    Given I am running "_5_checkbox.py"
    Then I see "my_checkbox" is not active

  Scenario: I can check checkbox
    Given I am running "_5_checkbox.py"
    When I tap "my_checkbox"
    Then I see "my_checkbox" is active

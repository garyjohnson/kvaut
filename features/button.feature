Feature: Automate button
  As a developer testing my app
  I want to assert that buttons are visible and clickable
  So I can build tests

  Scenario: I see button
    Given I am running "_3_button.py"
    Then I see "Hello world"

  Scenario: I see button by id
    Given I am running "_3_button.py"
    Then I see "goodbye_world"

  Scenario: I can tap button
    Given I am running "_3_button.py"
    When I tap "Hello world"
    Then I see "Howdy"

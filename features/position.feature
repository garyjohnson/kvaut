Feature: Position
  As a developer testing my app
  I want to verify position of elements relative to each other
  So I know my widgets are laid out correctly

  Scenario: Widgets above others
    Given I am running "_7_position.py"
    Then "top" is above "bottom"


Feature: Find widgets by id
  As a developer testing my app
  I want to assert that widgets are visible
  So I can build tests

  @wip
  Scenario: I see widget
    Given I am running "1_widget.py"
    Then I see "my_widget"

  Scenario: I do not see widget
    Given I am running "1_widget.py"
    Then I do not see "nonexistant_widget"

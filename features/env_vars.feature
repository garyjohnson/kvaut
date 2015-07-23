Feature: Launch automation server
  As a developer testing my app
  I want to only run kvaut when testing
  So I keep performance running good

  Scenario: I launch app without env vars
    Given I am running "1_widget.py" without enabling server
    Then I get an error waiting for automation server

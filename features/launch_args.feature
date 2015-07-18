Feature: Launch automation server
  As a developer testing my app
  I want to only run kvaut when testing
  So I keep performance running good

  Scenario: I launch app with args
    Given I am running "4_launch_args.py" with arg "--automation_server"
    Then I see "my_widget"

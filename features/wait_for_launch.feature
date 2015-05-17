Feature: Wait for launch
  As a developer testing my app
  I want to wait for automation server to launch
  So I can run assertions against it

  @wip
  Scenario: I see widget
    When I launch "0_no_server.py"
    Then I get an error waiting for automation server

Feature: Custom Automator
  As a developer testing my app
  I want to build custom automators
  So I can automate my custom widgets

  Scenario: Custom criteria causes built-in automators to fail match
    Given I am running "_1_widget.py"
    Then I do not see "my_widget" with attributes
      | name  | value |
      | test  | test  |

  Scenario: Find by custom attributes
    Given I am running "_6_custom_widget.py"
    Then I see "my_custom_widget" with attributes
      | name    | value   |
      | status  | ok      |

  Scenario: Fail to find by custom attributes
    Given I am running "_6_custom_widget.py"
    Then I do not see "my_custom_widget" with attributes
      | name    | value   |
      | status  | not ok  |

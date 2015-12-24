Feature: Custom Automator
  As a developer testing my app
  I want to build custom automators
  So I can automate my custom widgets

  Scenario: Custom criteria is ignored by built-in automators
    Given I am running "_1_widget.py"
    Then I see "my_custom_widget" with attributes
      | name  | value |
      | test  | test  |

  @wip
  Scenario: Find by custom attributes
    Given I am running "_6_custom_widget.py"
    Then I see "my_custom_widget" with attributes
      | name       | value   |
      | is_active  | True    |

  @wip
  Scenario: Fail to find by custom attributes
    Given I am running "_6_custom_widget.py"
    Then I do not see "my_custom_widget" with attributes
      | name       | value    |
      | is_active  | False    |

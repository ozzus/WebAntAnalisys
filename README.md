### Пример ответа:

Gherkin

```
Feature: User Login
  Scenario: User Login - 1
    Given I open the URL '/login'
    When I enter 'test@example.com' into the element '#email'
    And I click the element '.submit-btn'
    Then The element '.welcome' should contain text 'Welcome!'```

Feature: Web Tables User Management

  Background:
    Given User navigate to "http://www.way2automation.com/angularjs-protractor/webtables/"


  Scenario: Validate User List Table page
    Then User should see the user list table with headers:
      | First Name | Last Name | User Name | Customer | Role | E-mail | Cell Phone | Locked |

  Scenario: Add a user from CSV and verify in list
   Given User clicks "Add User" button
   When User load user data from CSV file "users.csv" row 0
   And User add the latest user
   Then User should see the latest user in the user list
# Banking Portal Web Application in Python

# List of Libraries (currently)
flask, flask_sqlalchemy, flask_session, passlib

# Documentation
Currently, users can log in and log out of their banking accounts and register a new account if needed. 

Register account accomodates for empty email strings and empty password strings as well as checking if the email is already in use. 

Login page acknowledges if emails dont exist in system as well as incorrect passwords input.

Passwords are stored securely through encryption by using external library passlib.

Flask sessions is used as well to provide support for a server side session to the banking app. The session accounts for clients logging in and out of the server with the data being stored on the server.

There exists user roles which are either Client or Employee. Clients can manage their finances and submit help requests from employees as well as view their submitted help requests. Employees have all the same functions as clients except they can view a list of all help requests and resolve any of them through the request number.

# Collaborators
Andrew Cowin, David Lee, Alexander Wolff, Jake Moretz, Addison Nugent

# Functional and non-functional requirements:

[x] The user shall be able to login with a correct username and password

[x] The users login information shall be handles securely

[x] The banking portal shall have different levels of user access (such as standard bank client, bank employee, or premium client)

[x] A database shall store all of the accounts of the bank alongside their permissions, and general bank information (such as balances, transactions, settings, etc.)

[x] Upon login, the user shall have access to their bank accounts (checking, savings)

[] The user shall have access to their recent transaction history

[] The user shall be able to deposit checks, pay bills, or make transfers to other users of the bank (alongside other banking functionalities)

[x] The banking portal shall be stable and support multiple users to login at the same time

[x] The client information shall be secure and private

[x] Clients can request for help from Employees and can view their help requests under a tab

[x] Employees can see help requests and close them

During the development, we will add to this list of features that our web application shall have.
We will split up the work group members different functionalities that they should implement.

# Division of Labor
**David Lee**:

    Secure Login,
    Secure Register Page,
    Multi User Access via Flask Sessions,
    Dashboards,
    Role Based Access,
    Submit Help Request,
    View Help Request,
    Manage Users Help Request (ie. closing or deleting requests)
  

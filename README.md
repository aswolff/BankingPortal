# Banking Portal Web Application in Python

# List of Libraries (currently)
flask, flask_sqlalchemy, flask_session, passlib

# Documentation
Currently, users can log in and log out of their banking accounts and register a new account if needed. 

Register account accomodates for empty email strings and empty password strings as well as checking if the email is already in use. 

Log in page succesffully informs user if password is incorrect however the log in page doesnt currently inform the user if the email is in the system already.

# Collaborators
Andrew Cowin, David Lee, Alexander Wolff, Jake Moretz, Addison Nugent

# Functional and non-functional requirements:

[x] The user shall be able to login with a correct username and password

[x] The users login information shall be handles securely

[] The banking portal shall have different levels of user access (such as standard bank client, bank employee, or premium client)

[] A database shall store all of the accounts of the bank alongside their permissions, and general bank information (such as balances, transactions, settings, etc.)

[x] Upon login, the user shall have access to their bank accounts (checking, savings)

[] The user shall have access to their recent transaction history

[] The user shall be able to deposit checks, pay bills, or make transfers to other users of the bank (alongside other banking functionalities)

[] The banking portal shall be stable and support multiple users to login at the same time

[] Upon request of the client, the bank employee account shall have permission to delete their account

[x] The client information shall be secure and private


During the development, we will add to this list of features that our web application shall have.
We will split up the work group members different functionalities that they should implement.

# Banking Portal Web Application in Python
The original proposal was that we implemented a secure banking portal web application in Python. This would be accomplished using Flask and a database which we opted for MySQL. We also wanted to add roles in employees and regular clients and they were essentially both the same except employees can access all help requests and close help requests.


# How to Run / Setup

Included is a dbsetup.txt which is an executable script for creating the 'Bank' database as well as all tables associated with the database. This is vital for being able to use the web app for the first time! Also included is a requirements.txt which is used with Docker to build the container image which can be installed via pip. The requirements.txt is a text file that includes all libraries used for the web app.

**Inside the app.py make sure to adjust the app.config to match your system**

    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'YOUR_PASSWORD_HERE'
    app.config['MYSQL_DB'] = 'Bank'

# Role Based Access

**Begin by doing a simple script execution to make a client an employee:**

    UPDATE Client
    SET Employee = 1
    WHERE Email = 'INSERT_THEIR_EMAIL_HERE';
From there the user can log in to their newly employed role as an employee to the bank! 
This is indicated by the new welcome screen/dashboard. 
Now the user can open the newly represented "View Help Requests" link from which they can see all the requests ever made. 
On a request that user can manually copy the 'Help Number' and click 'Close' which would redirect them to a fill out form. 
That form will document the resolution of the problem and sign the email from the backend to the resolution. 
Whenever a client views their help requests they can then see the resolution and which employee it was closed by.


# Current Bugs
The table for viewing requests has a problem in that the text area for problems spans past the table cell.

Not a bug but transferring funds is only available for checking and not savings accounts

# Project Members
Andrew Cowin, David Lee, Alexander Wolff, Jake Moretz, Addison Nugent

# Actual Collaborators
David Lee, Alexander Wolff, Jake Moretz

# Functional and non-functional requirements:

[x] The user shall be able to login with a correct username and password

[x] The users login information shall be handles securely

[x] The banking portal shall have different levels of user access (such as standard bank client, bank employee, or premium client)

[x] A database shall store all of the accounts of the bank alongside their permissions, and general bank information (such as balances, transactions, settings, etc.)

[x] Upon login, the user shall have access to their bank accounts (checking, savings)

[x] The user shall have access to their recent transaction history

[x] The user shall be able to deposit checks, pay bills, or make transfers to other users of the bank (alongside other banking functionalities)

[x] The banking portal shall be stable and support multiple users to login at the same time

[x] The client information shall be secure and private

[x] Clients can request for help from Employees and can view their help requests under a tab

[x] Employees can see help requests and close them

During the development, we will add to this list of features that our web application shall have.
We will split up the work group members different functionalities that they should implement.

# Division of Labor
**David Lee**:

    README.md
    Secure Login,
    Secure Register Page,
    Setup MySQL database to work with Flask,
    Dashboards,
    Role Based Access (ie. employee dashboards and client dashboards),
    Submit Help Request,
    View Help Request,
    Manage Users Help Requests,
    Delete Users Own Requests,
    Close Requests (accessible only by employees),
    Created style sheet for Front End,
    Front End Programming:
        Index,
        Login,
        Register,
        Dashboard,
        Help Requests,
        Checking/Savings
 
 **Jake Moretz**:
    
    Helped edit and added a few databases,
    Checking dashboard,
    Savings dashboard,
    Deposit money into savings and checking,
    Withdraw money from savings and checking,
    Display recent transactions for savings and checking
    
 **Alexander Wolff**:
    
    Transfering funds between users in database,
    Created multiple html pages,
    Setup MySQL database,
    Setup Docker
    Project Writeup (Functional and non-functional requirements)


# CITATION / RESOURCES USED
**IMAGES:**

    https://www.seekpng.com/ipng/u2q8i1y3i1i1o0r5_login/

    https://www.seekpng.com/ipng/u2q8w7r5u2o0o0i1_circled-user-icon-user-profile-icon-png/

    https://www.seekpng.com/ipng/u2q8q8r5i1w7r5e6_home-icon-free-ios-home-icon/

    https://www.seekpng.com/ipng/u2q8y3y3e6q8i1i1_home-improvement-comments-home-improvement-icon/
**TUTORIALS/RESOURCES**
    
    https://www.freecodecamp.org/news/html-button-link-code-examples-how-to-make-html-hyperlinks-using-the-href-attribute-on-tags/

    https://codeshack.io/login-system-python-flask-mysql/

    https://dev.to/dcodeyt/creating-beautiful-html-tables-with-css-428l


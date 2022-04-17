import sqlite3

# If no existing database is found then one is created
conn = sqlite3.connect('Bank.db')
print("Opened database successfully")

# SQLite doesn't impose length restrictions i.e. VARCHAR(255) is ignored and has resulting affinity TEXT
conn.execute('CREATE TABLE Client (Email TEXT, Password TEXT, Employee INTEGER)')
conn.execute('CREATE TABLE Issue (Email TEXT, Problem TEXT, Date TEXT)')
print("Tables created successfully")
conn.close()

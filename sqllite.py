import sqlite3

connection = sqlite3.connect('system.db')

cursor = connection.cursor()

#cursor.execute("""CREATE TABLE users (
        #username text,
        #password text,
        #balance real,
        #rec_transfer text,
        #sent_transfer text,
        #request text
        #)""")

#connection.commit()


# Upon Login - check if entered credentials match database credentials
def userExists(username, password):
    with connection:
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password, ))
        return cursor.fetchone()
    
# Upon Registration - Check if username is already registered
# When Sending money - verifying that username of recipient exists
def usernameExists(username):
    with connection:
        cursor.execute("SELECT * FROM users WHERE username = ?", (username, ))
        return cursor.fetchone()
    
# Register user function
def registerUser(username, password, balance, rec_transfer, sent_transfer, request):
    with connection:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (username, password, balance, rec_transfer, sent_transfer, 
                                                                       request))

        numRows = cursor.rowcount

        if(numRows > 0):
            return True
        
        else:
            return False

# Get user's balance
def getUserBalance(username):
    with connection:
        cursor.execute("SELECT balance FROM users WHERE username = ?", (username, ))
        balance = cursor.fetchone()
        
        return balance[0]

# Apply balance changes for both sender and recipient and store payment information.
def handleMoneyTransfer(senderUser, recipientUser, amount, sent_transfer_log, rec_transfer_log):
    with connection:
        sender_balance = getUserBalance(senderUser) - amount
        receiver_balance = getUserBalance(recipientUser) + amount
        
        # Sender Information Updated
        cursor.execute("UPDATE users SET balance = ?, sent_transfer = ? WHERE username = ?", (sender_balance, sent_transfer_log, senderUser))

        # Recipient Information Updated
        cursor.execute("SELECT rec_transfer FROM users WHERE username = ?", (recipientUser, ))
        prev_rec_transfers = cursor.fetchone()

        rec_transfer_log = str(prev_rec_transfers[0]) + rec_transfer_log

        rec_transfer_log = rec_transfer_log.replace("None","")

        cursor.execute("UPDATE users SET balance = ?, rec_transfer = ? WHERE username = ?", (receiver_balance, rec_transfer_log, recipientUser))

        numRows = cursor.rowcount
        if(numRows > 0):
            return True
            
        else:
            return False

# Get received transfer information
def fetchReceivedTransfer(username):
    with connection:
        cursor.execute("SELECT rec_transfer FROM users WHERE username = ?", (username, ))
        received_log = cursor.fetchone()

        if(received_log == None):
            return None
        else:
            return received_log[0]


def updatePassword(username, new_pass):
    with connection:
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_pass, username))

        numRows = cursor.rowcount
        if(numRows > 0):
            return True
        
        else:
            return False

#  query for checking all entries in the database
#cursor.execute("SELECT * FROM users")
#x = cursor.fetchall()
#for i in x: 
    #print(i)

connection.close()
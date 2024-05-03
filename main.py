from sqllite import userExists, usernameExists, registerUser, getUserBalance, handleMoneyTransfer, fetchReceivedTransfer, updatePassword

# Verifying login credentials to see if user exists or not 
def verifyLogin(username, password):
    exists = userExists(username, password)

    if(exists != None):
        return True
    else:
        return False
    
# Checking to see if entered username is already registered
def verifyUsername(username):
    exists = usernameExists(username)

    if(exists != None):
        return True
    else:
        return False
    
# Register the user
def register(username, password, balance, rec, sent, req):
    r = registerUser(username, password, balance, rec, sent, req)
    return r

# Get user's balance
def balance(username):
    b = getUserBalance(username)
    return b

# Quit Menu
def quit(valid):
    if(valid == True):
        valid = False
        print("Quitting...thank you for using the app!")
    return valid

# Sets an amount to be sent, ensures that there is a max limit of $200 sent on each transfer
def calculate_amount_sent(recipient):
    reached_send_limit = False
    
    amount_sent = input("Please indicate the amount of money that you would like to send to " + recipient + ": \n")

    while(reached_send_limit == False):
        if(amount_sent.isdigit() and float(amount_sent) <= 200):
            reached_send_limit = True
            return float(amount_sent)

        else:
            amount_sent = input("Send limit reached. Please enter an amount that is $200 or below.\n")

# Gives user option to send a message when sending a payment transfer
def sender_message(recipient):
    message = input("Please enter a message: \n")
    return message
   
# Send money transfer
def sendMoneyTransfer(sender, recipient, amount_sent, message):
    sent_transfer_log = "Sent $"+str(amount_sent)+" to "+ recipient+"\n"
    received_transfer_log = "Received $"+str(amount_sent) + " from "+sender+" with message: "+message+"\n"

    transfer_complete = handleMoneyTransfer(sender, recipient, amount_sent, sent_transfer_log, received_transfer_log)
    return transfer_complete

# As a recipient, view received payment details
def viewReceivedTransfers(username):
    rec = fetchReceivedTransfer(username)
    return rec

# Resetting password with new password
def passwordReset(username, new_password):
    resetSuccess = updatePassword(username, new_password)
    return resetSuccess

# MAIN PROCESS
loginCounter = 0
registerCounter = 0
backToStart = 0

while(backToStart < 1):
    backToStart = 1
    print("Hello, welcome to the P2P Money Transfer App! Are you registered with us?\n")

    registered = input("Y/N\n")

    if(registered.upper() == "Y"):
        # LOGIN 
        while(loginCounter < 5):
            print("Please enter your login credentials\n")

            user = input("Username: ")
            password = input("Password: ")

            validUser = verifyLogin(user, password)     

            if(validUser == False):
                print("Incorrect credentials. Please try again.\n")
                loginCounter = loginCounter + 1
            else:
                print("Login Successful!\n")
                break

    else:
        # REGISTER
        while(registerCounter < 1):
            print("Create an account\n")

            user_reg = input("Username: ")
            password_reg = input("Password: ")
            password_verify_reg = input("Verify Password: ")

            if(password_reg != password_verify_reg):
                print("Verified password does not match password. Please try again.\n")

            else:
                # Call verifyUsername() function to check if there is someone with that username existing
                validUsername = verifyUsername(user_reg)

                if(validUsername == True):
                    print("Username is taken. Please enter a different username.\n")

                else:
                    registrationSuccessful = register(user_reg, password_reg, 500.00, None, None, None)

                    if(registrationSuccessful == True):
                        print("Registration successful.\n")  
                        registerCounter = 1
                        backToStart = 0


if(loginCounter == 5):
    print("Too many login attempts. Please try again later.")     

# MENU
while(validUser == True):
    print(str(user)+", what action would you like to perform?\n")

    print(" 1. View balance\n 2. Send payment transfer\n 3. View received transfers\n 4. Reset password\n 5. QUIT\n")

    choice = input()
    if(not choice.isdigit() or int(choice) < 1 or int(choice) > 6):
        print("Please enter a valid option.\n")
   
    elif(int(choice) == 1):
        currentBalance = balance(user)
        print(str(user) + "'s BALANCE: $" + str(currentBalance)+"\n")

        print("Would you like to continue using the app?\n")
        stayInApp = input("Y/N\n")

        if(stayInApp.upper() == "N"):
            validUser = quit(validUser)

    elif(int(choice) == 2):
        recipientFound = False
        while(recipientFound == False):
            recipient = input("\nPlease enter the username of the recipient that you would like to transfer money to: \n")
            valid_recipient = verifyUsername(recipient)
            if(recipient == user or valid_recipient == False):
                print("User does not exist. Please try again. \n")
            else:
                recipientFound = True
                amount_sent = calculate_amount_sent(recipient)

                old_balance = balance(user)
                balance_after_transfer = old_balance - amount_sent

                if(balance_after_transfer < 0):
                    print("You do not have enough funds to complete this transfer.\n")

                else:
                    message = sender_message(recipient)

                    print("\n Transfer details:\n You are sending $" + str(amount_sent) + " to " + recipient + 
                    "\n Balance before transaction: $" + str(old_balance) + "\n" + " Balance after transaction: $" + str(balance_after_transfer)+"\n")

                    if(message is not None):
                        print("Message: " + message+"\n")

                    # Type CONFIRM to confirm sending money, or else it will ask you to quit or continue using app.
                    sendConfirm = input("Please type 'CONFIRM' to send the transfer.\n")

                    if(sendConfirm.upper() == "CONFIRM"):
                        transactionComplete = sendMoneyTransfer(user, recipient, amount_sent, message)
                        if(transactionComplete == True):
                            print("Payment transaction completed. Redirecting to the main menu.")

                    else:
                        print("Transaction cancelled. Would you like to continue using the app?\n")
                        stayInApp = input("Y/N\n")

                        if(stayInApp.upper() == "N"):
                            validUser = quit(validUser)


    # View received transfers
    elif(int(choice) == 3):
        rec = viewReceivedTransfers(user)

        if(rec is not None):
            print(str(rec) + "\n")

        else:
            print("No received transfers.\n")

        print("Would you like to continue using the app?\n")
        stayInApp = input("Y/N\n")

        if(stayInApp.upper() == "N"):
            validUser = quit(validUser)

    elif(int(choice) == 4):
        reset_password = False
        while(reset_password == False):
            old_pass = input("Please enter your old password: \n")

            new_pass = input("Please enter your new password: \n")

            verify_pass = input("Verify new password: \n")

            if(old_pass != password or new_pass == old_pass or verify_pass != new_pass):
                print("Information is incorrect. Please re-enter.\n")

            else:
                reset_password = passwordReset(user, new_pass)
                if(reset_password == True):
                    print("Password successfully changed! Log in again with new credentials.")
                    validUser = quit(validUser)


    elif(int(choice) == 5):
        validUser = quit(validUser)
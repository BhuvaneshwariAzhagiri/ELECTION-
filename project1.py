import mysql.connector
import smtplib
from datetime import datetime

# Connection code to database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="election"
)
mycursor = mydb.cursor()

# Database setup
def database_setup():
    # Candidates table
    try:
        mycursor.execute("CREATE TABLE IF NOT EXISTS candidates (candidate VARCHAR(50) PRIMARY KEY, votes INT DEFAULT 0)")
        
        # Voters table
        mycursor.execute("CREATE TABLE IF NOT EXISTS voters (name VARCHAR(70), email VARCHAR(70))")
        
        # People list table
        mycursor.execute("CREATE TABLE IF NOT EXISTS people_list (name VARCHAR(70), email VARCHAR(70) PRIMARY KEY )")
        
        # Email id names for people list table
        email_id = ["aishravi03@gmail.com", "thamaraignanavel1976@gmail.com", "vaish4571@gmail.com", "vivedha24688@gmail.com"]
        names = ["aishwarya", "thamarai", "vaish", "vivedha"]
        #ages=[21,45,23,25]
        for email, name in zip(email_id, names):
            mycursor.execute("INSERT INTO people_list (name, email) VALUES (%s, %s)", (name, email))
        
        # Candidates for candidates table
        candidates = ["thurai", "velu", "raja"]
        for candidate in candidates:
            mycursor.execute("INSERT INTO candidates (candidate) VALUES (%s)", (candidate,))
        
        mydb.commit()
    except mysql.connector.Error as err:
        print(f"Error:{err}")

# Email sending
def email_sending(email_id, name):
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("bhuvaneshwarial48@gmail.com", "szcn udcy dwle haiw")
        subject = "Thank you for voting"
        body = f"Hi {name},\nThank you for voting. You have successfully cast your vote."
        now = datetime.now()
        now_dt = now.strftime("%Y-%m-%d %H:%M:%S %p")
        message = f"Subject: {subject}\n\n{body}\n\nTime of voting: {now_dt}"
        s.sendmail("bhuvaneshwarial48@gmail.com", email_id, message)
        s.quit()
        print("Mail sent successfully...")
    except Exception as e:
        print(f"Mail not sent: {e}")

# Function to check if an email exists in people_list
def check_email(email):
    mycursor.execute("SELECT * FROM people_list WHERE email = %s", (email,))
    result = mycursor.fetchone()
    return result is not None

# Election process
def election():
    database_setup()
    print("TAMILNADU ELECTION")
    candidate_names = ["thurai", "velu", "raja"]

    while True:
        try:
            email = input("Enter your email id (or 'q' to quit): ")
            if email.lower() == 'q':
                break

            if check_email(email):  # Call the function to check email in people_list
                name = input("Enter your name: ")
               
                print("Candidate Names:\n1. Thurai\n2. Velu\n3. Raja")
                vote = int(input("Press 1, 2, or 3 to cast your vote: "))
                
                if vote in [1, 2, 3]:
                    candidate = candidate_names[vote - 1]
                    mycursor.execute("INSERT INTO voters (email, name) VALUES (%s, %s)", (email, name))
                    mycursor.execute("UPDATE candidates SET votes = votes + 1 WHERE candidate = %s", (candidate,))
                    mydb.commit()
                    print(f"You voted for {candidate}")
                    email_sending(email, name)
                else:
                    print("Invalid vote, please try again.")
            else:
                print("You are not in the list of eligible voters.")
        except Exception as e:
            print(f"An error occurred: {e}")

election()
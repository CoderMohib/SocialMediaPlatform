import pyodbc
import time
import os
import msvcrt
def connect_db():
    conn = pyodbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'
                      r'SERVER=DESKTOP-GJV1NCC\SQLEXPRESS;'
                      r'DATABASE=SocialMediaPlatform;'
                      r'Trusted_Connection=yes')

    return conn

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def center_text(text, width):
    return text.center(width)

def get_password():
    while(True):
        print("Enter Password:", end=" ", flush=True)
        password = ""
        while True:
            char = msvcrt.getch()  
            if char == b'\r':  
                break
            else:
                password += char.decode('utf-8')
                print('*', end='', flush=True) 
        print()
        if len(password) >= 8:
            return password
        else:
            print("Length is Too Small!")

def display_social_media_platform_page():
    terminal_width = os.get_terminal_size().columns

    print(center_text("_" * terminal_width, terminal_width))
    print(center_text("_" * terminal_width, terminal_width))
    print("\n")
    print(center_text("🌐 Welcome to SocialMedia 🌐", terminal_width))
    print(center_text("_" * terminal_width, terminal_width))
    print(center_text("_" * terminal_width, terminal_width))
    print("\n")
    time.sleep(2)
    clear_screen()
def showTimeline(conn, userID):
    cursor = conn.cursor()
    while True:
        cursor.execute("SELECT * FROM getUserPost(?) ORDER BY CreatedAt DESC", (userID,))
        rows = cursor.fetchall()
        clear_screen()
        if rows:
            for row in rows:
                cursor.execute("select dbo.retriveName(?)", (userID,))
                userName = cursor.fetchone()
                print(f"Name: {userName[0]}")
                print(f"Created At: {row[2]}")
                print(f"Post Content: {row[1]}")  
                cursor.execute("select dbo.getLikes(?)", (row[0],))
                like = cursor.fetchone()
                print(f"Likes: {like[0]}", end=" ")
                cursor.execute("select dbo.getComments(?)", (row[0],))
                comment = cursor.fetchone()
                print(f"Commets: {comment[0]}")
                print()
        else:
            print("No Posts!")
            time.sleep(2)
            break

        check = input("Would you like to exit? (Y/N): ").strip().lower()
        if check == "y":
            break
        elif check == "n":
            continue
        else:
            print("Invalid input, please enter 'Y' or 'N'.")
            time.sleep(1)

def CreatePost(conn,userID):
    while(True):
        cursor=conn.cursor()
        content=input("Enter Content of the post: ")
        check = input("Would You like to post it?(Y/N): ")
        if check.lower() == "n":
            break
        else:
            cursor.execute("Exec inputPosts ?,?", (userID,content))
            print("Post Created SuccessFully!")
            time.sleep(2)
            conn.commit()
            break


def updateSettings(conn,userID):
    terminal_width = os.get_terminal_size().columns
    cursor=conn.cursor()
    while (True):
        clear_screen()
        print(center_text("~" * terminal_width, terminal_width))
        print("1. Update UserName")
        print("2. Update Password")
        print("3. Update Your Name")
        print("4. Deactivate Your Account")
        print("5. Delete Your Account")
        print("6. Exit")
        print(center_text("~" * terminal_width, terminal_width))
        Userinput=input()
        if Userinput in ['1','2','3','4','5','6']:
            clear_screen()
            if Userinput == '1':
                x = input("You New User Name: ")
                cursor.execute("Exec updateUserName ?,?", (userID,x))
                conn.commit()
            elif Userinput == '2':
                x = get_password()
                cursor.execute("Exec updatePassWord ?,?", (userID,x))
                conn.commit()
            elif Userinput == '3':
                while(True):
                    clear_screen()
                    fName = input("Enter Your First Name: ").strip()
                    LName = input("Enter Your Last Name: ").strip()
                    check = input("Would You like To continue(Y/N): ").strip()
                    if check.lower() == "n":
                        break
                    elif check.lower() == "y":
                        cursor.execute("Exec updateName ?,?,?", (userID,fName,LName))
                        conn.commit()
                        break
                    else:
                        print("Invalid Input!")
                        time.sleep(2)

            elif Userinput == '4':
                while(True):
                    clear_screen()
                    x = input("You Want to Deactivate Your Account?(Y/N): ")
                    if x.upper() == "Y":
                        cursor.execute("Exec updateAccountStatus ?,?", (userID,'Deactivated'))
                        conn.commit()
                        return 'Y'
                    elif check.lower() == "n":
                        break
                    else:
                        print("Invalid Input!")
                        time.sleep(2)
            elif Userinput == '5':
                while(True):
                    clear_screen()
                    check = input("Would You like To Delete Your Account(Y/N): ").strip()
                    if check.lower() == "n":
                        break
                    elif check.lower() == "y":
                        cursor.execute("Exec DelComments ?", (userID,))
                        cursor.execute("Exec DelLikes ?", (userID,))
                        cursor.execute("Exec DelPost ?", (userID,))
                        cursor.execute("Exec DelUser ?", (userID,))
                        print("Your Account Has been Deleted SuccessFully!")
                        time.sleep(2)
                        conn.commit()
                        return 'Y'
                    else:
                        print("Invalid Input!")
                        time.sleep(2)
                break
            elif Userinput == '6':
                break
        else:
            clear_screen()
            print(center_text("Invalid Input!" , terminal_width))
            time.sleep(1.5) 

def UserOptions(conn,userID):
    terminal_width = os.get_terminal_size().columns
    while (True):
        clear_screen()
        print(center_text("~" * terminal_width, terminal_width))
        print("1. Show Feed")
        print("2. Timeline")
        print("3. Add Friends")
        print("4. Create Post")
        print("5. Join Group")
        print("6. Show Groups")
        print("7. Update Account Setting")
        print("8. Logout")
        print(center_text("~" * terminal_width, terminal_width))
        Userinput=input()
        if Userinput in ['1','2','3','4','5','6','7']:
            clear_screen()
            if Userinput == '1':
                pass
            elif Userinput == '2':
                showTimeline(conn,userID)
            elif Userinput == '3':
                pass
            elif Userinput == '4':
                CreatePost(conn,userID)
            elif Userinput == '5':
                pass
            elif Userinput == '6':
                pass
            elif Userinput == '7':  
                if updateSettings(conn,userID) == "Y":
                    break
            elif Userinput == '8':  
                break
        else:
            clear_screen()
            print(center_text("Invalid Input!" , terminal_width))
            time.sleep(1.5)   

# login Info 
def login(conn):
    cursor=conn.cursor()
    while(True):
        clear_screen()
        email = input("Enter Email Name: ")
        PassWord = get_password()
        cursor.execute("SELECT * FROM retriveUSERID(?,?)",(email,PassWord))
        result = cursor.fetchone()
        if result:
            if result[1]== 'Deactivated':
                print("Your Account is Deactivated!")
                check = input("Wants To Activate Your Account(Y/N):")
                if check.upper() == "Y":
                    cursor.execute("Exec updateAccountStatus ?,?", (result[0],'Active'))
                    conn.commit()
                    print("Activated Your Account SuccessFully!")
                    time.sleep(1.7)
                    UserOptions(conn,result[0])
                break
            elif result[1]== 'Suspended':
                print("Your Account is Suspened For Some Reasons!")
                time.sleep(1.7)
                break
            else:
                UserOptions(conn,result[0])
                break
        else:
            print("Invalid Email OR Password!")
            time.sleep(1.7)
            x=input("Want To Continue?(Y/N): ")
            if x.upper() == "N":
                break
        
#SignUp info
def SignUp(conn):
    cursor = conn.cursor()
    while(True):
        clear_screen()
        userName = input("Enter User Name: ")
        email = input("Enter Email Name: ")
        PassWord = get_password()
        if userName==PassWord:
            print("UserName and Password Cannot be same!")
            time.sleep(1.7)
            continue
        FirstName= input("Enter First Name: ")
        LastName= input("Enter Last Name: ")
        dateOfBirth = input("Enter Date Of Birth(YYYY-MM-DD):")
        cursor.execute("SELECT * FROM retriveDataEmailAndUserName(?,?)",(userName,email))
        result = cursor.fetchone()
        if result:
            if result[1] == email and result[0] == userName:
                print("Username and Email is already taken!")
            elif result[0] == userName:
                print("Username is already taken!")
            elif result[1] == email:
                print("Email is already taken!")
            time.sleep(1.7)
            clear_screen()
            x=input("Want To Continue?(Y/N): ")
            if x.upper() == "N":
                break
        else:
            cursor.execute("Exec InsertUser ?, ?, ?,?,?,?", (userName, email, PassWord,dateOfBirth,FirstName,LastName))
            conn.commit()
            break


if __name__ == "__main__":
    conn = connect_db()
    display_social_media_platform_page()
    terminal_width = os.get_terminal_size().columns
    while (True):
        clear_screen()
        print(center_text("~" * terminal_width, terminal_width))
        print("1. Login")
        print("2. Sign Up")
        print("3. Exit")
        print(center_text("~" * terminal_width, terminal_width))
        Userinput=input()
        if Userinput in ['1','2','3']:
            clear_screen()
            if Userinput == '1':
                login(conn)
            elif Userinput == '2':
                SignUp(conn)
            else:
                terminal_width = os.get_terminal_size().columns
                print(center_text("_" * terminal_width, terminal_width))
                print(center_text("_" * terminal_width, terminal_width))
                print("\n")
                print(center_text("🌐 Thanks For Coming! 🌐", terminal_width))
                print(center_text("_" * terminal_width, terminal_width))
                print(center_text("_" * terminal_width, terminal_width))
                break
        else:
            clear_screen()
            print(center_text("Invalid Input!" , terminal_width))
            time.sleep(1.5)     


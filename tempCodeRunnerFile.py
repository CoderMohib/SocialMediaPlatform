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
        posts = cursor.fetchall()
        clear_screen()
        if posts:
            for i, post in enumerate(posts, 1):
                cursor.execute("SELECT dbo.retriveName(?)", (userID,))
                userName = cursor.fetchone()
                print(f"Post #{i}")
                print(f"Name: {userName[0]}")
                print(f"Created At: {post[2]}")
                print(f"Post Content: {post[1]}")  
                
                cursor.execute("SELECT dbo.getLikes(?)", (post[0],))
                like_count = cursor.fetchone()
                print(f"Likes: {like_count[0]}", end=" ")

                cursor.execute("SELECT dbo.getComments(?)", (post[0],))
                comment_count = cursor.fetchone()
                print(f"Comments: {comment_count[0]}")
                print()

            while True:
                print("\nOptions:")
                print("1. See who liked a post")
                print("2. See comments on a post")
                print("3. Add a comment to a post")
                print("4. Like a post")
                print("5. Go back to timeline")
                choice = input("Enter your choice: ")

                if choice == '1':
                    post_no = int(input("Enter post number to see likes: "))
                    post_id = posts[post_no - 1][0]  # Get PostID from selected post
                    cursor.execute("SELECT * FROM getPostLikes(?)", (post_id,))
                    likes = cursor.fetchall()
                    print(f"Likes for Post #{post_no}:")
                    for like in likes:
                        print(f"- {like[0]}")
                    input("Press Enter to continue...")

                elif choice == '2':
                    post_no = int(input("Enter post number to see comments: "))
                    post_id = posts[post_no - 1][0]  # Get PostID from selected post
                    cursor.execute("EXEC getPostComments ?", (post_id,))
                    comments = cursor.fetchall()
                    print(f"Comments for Post #{post_no}:")
                    for comment in comments:
                        print(f"- {comment[0]}: {comment[1]}")
                    input("Press Enter to continue...")

                elif choice == '3':
                    post_no = int(input("Enter post number to comment on: "))
                    post_id = posts[post_no - 1][0]  # Get PostID from selected post
                    comment = input("Enter your comment: ")
                    cursor.execute("EXEC insertComment ?, ?, ?", (post_id, userID, comment))
                    conn.commit()
                    print("Comment added successfully!")
                    break

                elif choice == '4':
                    post_no = int(input("Enter post number to like: "))
                    post_id = posts[post_no - 1][0]  # Get PostID from selected post
                    cursor.execute("SELECT * FROM checkUserLikedPost(?, ?)", (post_id, userID))
                    is_liked = cursor.fetchone()
                    if is_liked:
                        print("You have already liked this post!")
                    else:
                        cursor.execute("EXEC addLike ?, ?", (post_id, userID))
                        conn.commit()
                        print("Post liked successfully!")
                    break

                elif choice == '5':
                    break
                else:
                    print("Invalid input, please try again.")
        else:
            print("No Posts!")
            time.sleep(2)
            break

        check = input("Would you like to exit? (Y/N): ").strip().lower()
        if check == "y":
            break

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

def manageFriends(conn, userID):
    cursor = conn.cursor()
    while True:
        clear_screen()
        print("1. Send Friend Request")
        print("2. View Pending Friend Requests")
        print("3. View Sent Friend Requests")
        print("4. View Friends List")
        print("5. Remove a Friend")
        print("6. Exit")
        choice = input("Enter your choice: ")

        # Send Friend Request
        if choice == '1':
            while True:
                clear_screen()
                friend_user_id = int(input("Enter the User ID of the person you want to add as a friend: "))
                if friend_user_id == userID: 
                        print("Invalid Input!")
                        time.sleep(1.5)
                else:
                    cursor.execute("Select * from getFriendship(? , ?)",userID, friend_user_id)
                    x = cursor.fetchone()
                    if x:
                        if x[2] == "Pending":
                            if x[0] == userID:  # Current user is the sender
                                print("Friend request is already in Pending!")
                            else:  # Current user is the receiver
                                print("Friend request already sent to you. Please accept or reject.")
                        elif x[2] == "Accepted":
                            print("You are already friends!")
                    else:
                        cursor.execute("EXEC sendFriendRequest ?, ?", (userID, friend_user_id))
                        conn.commit()
                        print("Friend Request send successfull!")
                    time.sleep(1.5)
                    break

        # View Pending Friend Requests
        elif choice == '2':
            cursor.execute("Select * from getPendingFriendRequests(?)", (userID,))
            requests = cursor.fetchall()
            if requests:
                print("Pending Friend Requests:")
                for req in requests:
                    print(f"ID: {req[0]} | UserName: {req[1]} | Name: {req[2]} {req[3]}")
                friend_id = int(input("Enter the Friend ID to accept/reject the request: "))
                action = input("Accept (A) or Reject (R): ").strip().upper()
                if action == 'A':
                    cursor.execute("EXEC updateFriendRequestStatus ?, ?", (friend_id, 'Accepted'))
                    print("Friend request accepted!")
                elif action == 'R':
                    cursor.execute("EXEC updateFriendRequestStatus ?, ?", (friend_id, 'Rejected'))
                    print("Friend request rejected!")
                conn.commit()
                time.sleep(1.5)
            else:
                print("No pending friend requests.")
                time.sleep(1.5)

        # View Sent Friend Requests
        elif choice == '3':
            cursor.execute("EXEC getSentRequests ?", (userID,))
            requests = cursor.fetchall()
            if requests:
                print("Sent Friend Requests:")
                for req in requests:
                    print(f"ID: {req[0]} | UserName: {req[1]} | Name: {req[2]} {req[3]} | Status: {req[4]}")
            else:
                print("No sent friend requests.")
            input("Press Enter to continue...")

        # View Friends List
        elif choice == '4':
            cursor.execute("EXEC getFriendsList ?", (userID,))
            friends = cursor.fetchall()
            if friends:
                print(f"Your Friends: {len(friends)} ")
                for friend in friends:
                    print(f"UserName: {friend[1]} | Name: {friend[2]} {friend[3]}")
            else:
                print("No friends yet.")
            input("Press Enter to continue...")

        # Remove a Friend
        elif choice == '5':
            cursor.execute("EXEC getFriendsList ?", (userID,))
            friends = cursor.fetchall()
            if friends:
                print("Your Friends:")
                for i in range(len(friends)):
                    print(f"{i+1}. UserName: {friends[i][1]} | Name: {friends[i][2]} {friends[i][3]}")
                choice = int(input("Enter the number of the friend to remove: "))
                if 1 <= choice <= len(friends):
                    friend_user_id = friends[choice - 1][0]
                    cursor.execute("EXEC removeFriend ?, ?", (userID, friend_user_id))
                    conn.commit()
                    print("Friend removed successfully!")
                else:
                    print("Invalid choice.")
            else:
                print("No friends to remove.")
            time.sleep(1.5)

        # Exit
        elif choice == '6':
            break

        # Invalid Choice
        else:
            print("Invalid input. Please try again.")
            time.sleep(1.5)
def manageGroupsForALL(conn,userID,groupsJoin,CheckInp):
    cursor = conn.cursor()
    while (True):
        clear_screen()
        if groupsJoin[CheckInp-1][2] == userID:
            print("HI")
        else:
            break

def manageGroups(conn,userID):
    cursor = conn.cursor()
    while (True):
        clear_screen()
        print("1. Create Group")
        print("2. Join Group")
        print("3. View Your Groups")
        print("4. Exit")
        Userinput=input()
        if Userinput in ['1','2','3','4']:
            if Userinput == '1':
                name = input("Enter Group Name: ").strip()
                description = input("Enter Group Description(Optional): ")
                cursor.execute("Exec newGroup ?,?,?",(userID,name,description))
                conn.commit()
                print("Group Created SuccessFully!")
                time.sleep(1.8)
            elif Userinput == '2':
                cursor.execute("Select * from getALLGroup()")
                groups = cursor.fetchall()
                for i in range(len(groups)):
                    print(f"GR NO. {i+1} GROUP NAME: {groups[i][1]}")
                    print(f"Description: {groups[i][2]}")
                    print()
                inputNUM = int(input("Enter Group Number to Join: "))
                if 1 <= inputNUM <= len(groups):
                    groupID = groups[inputNUM-1][0]
                    cursor.execute("Select * from getGroupMembers(?,?)",(groupID,userID))
                    if cursor.fetchone():
                        print("You Already Member of this Group!")
                    else:
                        cursor.execute("Exec insertGroupMember ?,?",(groupID,userID))
                        conn.commit()
                        print("Successfully join in the Group!")
                else:
                    print("Invalid Input!")
                time.sleep(1.8)
            elif Userinput == '3':
                cursor.execute("Select * from specificGroupsOfUser(?)",(userID,))
                groupsJoin = cursor.fetchall()
                if groupsJoin:
                    for i in range (len(groupsJoin)):
                        print(f"Total Groups: {len(groupsJoin)}")
                        print(f"Group Number: {i+1} Group Name: {groupsJoin[i][0]}")
                        
                    CheckInp = int(input("Enter Group Number to view: "))
                    if 1 <= CheckInp <= len(groupsJoin):
                        manageGroupsForALL(conn,userID,groupsJoin,CheckInp)
                    else:
                        print("Invalid Input!")
                else:
                    print("No Groups Join Yet!")
                time.sleep(1.7)
            elif Userinput == '4':
                break
        else:
            print("Invalid Input!")
            time.sleep(1.7)
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
        print("3. Create Post")
        print("4. Manage Friends")
        print("5. Manage Groups")
        print("6. Update Account Setting")
        print("7. Logout")
        print(center_text("~" * terminal_width, terminal_width))
        Userinput=input()
        if Userinput in ['1','2','3','4','5','6','7']:
            clear_screen()
            if Userinput == '1':
                pass
            elif Userinput == '2':
                showTimeline(conn,userID)
            elif Userinput == '3':
                CreatePost(conn,userID)
            elif Userinput == '4':
                manageFriends(conn, userID)
            elif Userinput == '5':
                manageGroups(conn,userID)
            elif Userinput == '6':  
                if updateSettings(conn,userID) == "Y":
                    break
            elif Userinput == '7':  
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


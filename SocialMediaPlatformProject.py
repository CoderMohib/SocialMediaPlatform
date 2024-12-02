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
        return password

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
# For database connection

def loadChat(conn,userID,friendID,friendName):
    cursor= conn.cursor()
    cursor.execute("Exec getChat ?,?",(userID,friendID))
    messages = cursor.fetchall()
    if messages:
        clear_screen()
        print(f'Name: {friendName}')
        for i in messages:
            if i[1] == userID:        
                print(f"               {i[3]} - You")
            else:
                print(f"Friend- {i[3]}")
    else:
        print("No message Yet!")
def Chat(conn,userID):
    cursor = conn.cursor()
    while(True):
        clear_screen()
        cursor.execute("EXEC getFriendsList ?", (userID,))
        friends = cursor.fetchall()
        if friends:
            print(f"Your Friends: {friends[0][4]} ")
            for i in range(len(friends)):
                    print(f"{i+1}. UserName: {friends[i][1]} | Name: {friends[i][2]} {friends[i][3]}")
            x = int(input("Enter Number to chat: "))
            if 1 <= x <= len(friends):
                try:
                    cursor.execute("Exec updateMessageRead ?,?",(userID,friends[x-1][0]))
                except pyodbc.Error as ex:
                    sqlstate = ex.args[0]  
                    message = ex.args[1]   
                    print(f"SQL State: {sqlstate}, Error Message: {message}")
                    time.sleep(1.6)
                    break
                else:
                    conn.commit()
                while(True):
                    loadChat(conn,userID,friends[x-1][0],friends[i][2]+' '+ friends[i][3])
                    newmsg= input("Enter New Message: ")
                    cursor.execute("Exec newMsg ?,?,?",(userID,friends[x-1][0],newmsg))
                    conn.commit()
                    xs = input("Want to exit(Y/N):")
                    if xs.lower()=="y":
                        break
                break
            else:
                print("Invalid Input!")
                input("Press Enter to Continue.....")
                
        else:
            print("No friends yet.")
            input("Press Enter to continue...")
            break

def showTimeline(conn, userID):
    cursor = conn.cursor() 
    check = 0
    choice = ''
    cursor.execute("Select * from retriveDataSUsers(?)",(userID,))
    userDetail = cursor.fetchone()
    while True:
        clear_screen()
        cursor.execute("SELECT * FROM getUserPost(?) ORDER BY CreatedAt DESC", (userID,))
        posts = cursor.fetchall()
        if posts:
            for i in range(len(posts)):
                clear_screen()
                print(f"UserName: {userDetail[1]}")
                print(f"Profile Name: {userDetail[6]} {userDetail[7]}")
                print(f"Date of Birth: {userDetail[8]}")
                print(f"Total Post: {userDetail[10]}")
                print(f"Total Friends: {userDetail[11]}")
                print()
                print(f"Post #{i+1}")
                print(f"Name: {posts[i][1]}")
                print(f"Created At: {posts[i][3]}")
                print(f"post Content: {posts[i][2]}")  
                print(f"Likes: {posts[i][4]}", end=" ")
                print(f"Comments: {posts[i][5]}")
                print()

                if check == i:
                    print("\nOptions:")
                    print("1. See who liked a post")
                    print("2. See comments on a post")
                    print("3. Add a comment to post")
                    print("4. Like a post")
                    print("5. Continue")
                    print("6. Go back")
                    choice = input("Enter your choice: ")

                    if choice == '1':
                        cursor.execute("SELECT * FROM getPostLikes(?)", (posts[i][0],))
                        likes = cursor.fetchall()
                        if likes:
                            print(f"Likes for Post #{posts[i][0]}:")
                            for like in likes:
                                print(f"- {like[0]}") 
                        else:
                            print('No One Liked!')
                        input("Press Enter to Continue...")
                        break
                    elif choice == '2':
                        cursor.execute("EXEC getPostComments ?", (posts[i][0],))
                        comments = cursor.fetchall()
                        if comments:
                            print(f"Comments for Post #{posts[i][0]}:")
                            for comment in comments:
                                print(f"- {comment[0]}: {comment[1]}")
                        else:
                            print("No Comments Yet")
                        input("Press Enter to continue...")
                        break
                    elif choice == '3':
                        comment = input("Enter your comment: ")
                        try:
                            cursor.execute("EXEC insertComment ?, ?, ?", (posts[i][0], userID, comment))
                        except pyodbc.Error as ex:
                            sqlstate = ex.args[0]  
                            message = ex.args[1]   
                            print(f"SQL State: {sqlstate}, Error Message: {message}")
                            time.sleep(1.6)
                        else:
                            conn.commit()
                            print("Comment added successfully!")
                            break
                    elif choice == '4':
                        cursor.execute("SELECT * FROM checkUserLikedPost(?, ?)", (posts[i][0], userID))
                        is_liked = cursor.fetchone()
                        if is_liked:
                            print("You have already liked this post!")
                            time.sleep(1.6)
                            break
                        else:
                            try:
                                cursor.execute("EXEC addLike ?, ?", (posts[i][0], userID))
                            except pyodbc.Error as ex:
                                sqlstate = ex.args[0]  
                                message = ex.args[1]   
                                print(f"SQL State: {sqlstate}, Error Message: {message}")
                                time.sleep(1.6)
                                break
                            else:
                                conn.commit()
                                print("Post liked successfully!")
                                break
                    elif choice == '5':
                        check+=1
                    elif choice == '6':
                        break
                    else:
                        print("Invalid input, please try again.")
            else:
                break
               
        else:
            print("No Posts!")
            time.sleep(2)
            break

        if choice == '6':
            break

def CreatePost(conn,userID):
    while(True):
        cursor=conn.cursor()
        content=input("Enter Content of the post: ")
        check = input("Would You like to post it?(Y/N): ")
        if check.lower() == "n":
            break
        elif check.lower() == "y":
            try:
                cursor.execute("Exec inputPosts ?,?", (userID,content))
            except pyodbc.Error as ex:
                sqlstate = ex.args[0]  
                message = ex.args[1]   
                print(f"SQL State: {sqlstate}, Error Message: {message}")
                time.sleep(1.6)
                break
            else:
                print("Post Created SuccessFully!")
                time.sleep(2)
                conn.commit()
                break
        else:
            print("Invalid input. Please try again.")
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
                    try:
                        cursor.execute("Select * from getFriendship(? , ?)",userID, friend_user_id)
                        x = cursor.fetchone()
                    except Exception as e:
                        print(f"Error: {e}")
                    else:

                        if x:
                            if x[2] == "Pending":
                                if x[0] == userID:  # Current user is the sender
                                    print("Friend request is already in Pending!")
                                else:  # Current user is the receiver
                                    print("Friend request already sent to you. Please accept or reject.")
                            elif x[2] == "Accepted":
                                print("You are already friends!")
                        else:
                            try:
                                cursor.execute("EXEC sendFriendRequest ?, ?", (userID, friend_user_id))
                                conn.commit()
                                print("Friend Request send successfull!")
                            except Exception as e:
                                print(f"Error: {e}")
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
                try:
                    friend_id = int(input("Enter the Friend ID to accept/reject the request: "))
                except Exception as e:
                    print(f'Error: {e}')
                else:
                    action = input("Accept (A) or Reject (R): ").strip().upper()
                    if action == 'A':
                        try:
                            cursor.execute("EXEC updateFriendRequestStatus ?, ?", (friend_id, 'Accepted'))
                            print("Friend request accepted!")
                            conn.commit()
                        except pyodbc.Error as ex:
                            sqlstate = ex.args[0]  
                            message = ex.args[1]   
                            print(f"SQL State: {sqlstate}, Error Message: {message}")
                    elif action == 'R':
                        try:
                            cursor.execute("EXEC updateFriendRequestStatus ?, ?", (friend_id, 'Rejected'))
                            print("Friend request rejected!")
                            conn.commit()
                        except pyodbc.Error as ex:
                            sqlstate = ex.args[0]  
                            message = ex.args[1]   
                            print(f"SQL State: {sqlstate}, Error Message: {message}")
                    
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
                try:
                    choice = int(input("Enter the number of the friend to remove: "))
                except Exception as e:
                    print(f'Error: {e}')
                else:
                    if 1 <= choice <= len(friends):
                        friend_user_id = friends[choice - 1][0]
                        try:
                            cursor.execute("EXEC removeFriend ?, ?", (userID, friend_user_id))
                        except pyodbc.Error as ex:
                            sqlstate = ex.args[0]  
                            message = ex.args[1]   
                            print(f"SQL State: {sqlstate}, Error Message: {message}")
                        else:
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
def manageGroupsForMember(conn,userID,groupsJoin,CheckInp):
    cursor = conn.cursor()
    while (True):
        clear_screen()
        print("1. Post in Group")
        print("2. Show Groups Post")
        print("3. Show Group Members")
        print("4. Leave Group")
        print("5. Exit")
        userinput = input("Enter Option: ")
        if userinput in ['1','2','3','4','5']:
            if userinput == '1':
                while(True):
                    cursor=conn.cursor()
                    content=input("Enter Content of the post: ")
                    check = input("Would You like to post it?(Y/N): ")
                    if check.lower() == "n":
                        break
                    elif check.lower() == "y":
                        try:
                            cursor.execute("Exec inputGroupPosts ?,?,?", (userID,content,groupsJoin[CheckInp-1][0]))
                        except pyodbc.Error as e:
                            print(f'Error: {e}')
                            time.sleep(2)
                            break
                        else:
                            print("Post Created SuccessFully!")
                            time.sleep(2)
                            conn.commit()
                            break
                    else:
                        print("Invalid Input!")
                        time.sleep(1.5)
                        break
            elif userinput == "2":
                check = 0
                while(True):
                    takeInput = ''
                    clear_screen()
                    cursor.execute("Exec getGroupPosts ?", (groupsJoin[CheckInp-1][0],))
                    posts = cursor.fetchall()
                    if len(posts) != 0:
                        print(f"Group Name: {posts[0][1]}")
                        for i in range(len(posts)):
                            clear_screen()
                            print(f"Post# {i+1} ")
                            print(f"User: {posts[i][3]}")
                            print(f"Content: {posts[i][2]}")
                            print(f"Likes: {posts[i][4]}  Commets: {posts[i][5]}")
                            print()
                            if check == i:
                                print("1. Like This Post ")
                                print("2. Comment on this Post")
                                print("3. See Comments")
                                print("4. Continue..")
                                print("5. Go Back")
                                takeInput = input()
                                if takeInput == '4':
                                    check+=1
                                elif takeInput == '1':
                                    x = input('Would You Want to like this post?(Y/N): ')
                                    if x.lower() == "y":
                                        cursor.execute("Select * from getUserLike(?,?,?)",(userID,posts[i][0],groupsJoin[CheckInp-1][0]))
                                        res = cursor.fetchone()
                                        if res:
                                           pass
                                        else:
                                            try:
                                                cursor.execute("Exec setGroupPostlikes ?,?,?",(userID,posts[i][0],groupsJoin[CheckInp-1][0]))
                                                conn.commit()
                                            except pyodbc.Error as e:
                                                print(f'Error: {e}')
                                                time.sleep(1.5)
                                                
                                        break
                                    else:
                                        break
                                elif takeInput == '2':
                                    x = input("Enter a comment: ").strip()
                                    if x:
                                        try:
                                            cursor.execute("Exec setGroupPostComments ?,?,?,?",(userID,posts[i][0],groupsJoin[CheckInp-1][0],x))
                                            conn.commit()
                                        except pyodbc.Error as e:
                                                print(f'Error: {e}')
                                                time.sleep(1.5)
                                        break
                                elif takeInput == '3':
                                    if posts[i][5] != 0:
                                        cursor.execute("Exec getCommentGroupPost ?,?",(posts[i][0],groupsJoin[CheckInp-1][0]))
                                        comments = cursor.fetchall()
                                        for i in range(len(comments)):
                                            print(f"{i+1}. UserName: {comments[i][0]}")
                                            print(f"Comment: {comments[i][1]}      Time: {comments[i][2]}")
                                            print()
                                    else:
                                        print("No Comment to show!")
                                    input("Enter to continue....")
                                    break
                                elif takeInput == '5':
                                    break
                                else:
                                    print("Invalid Input!")
                                    time.sleep(1.6)
                                    break
                        else:
                            break
                        if  takeInput ==  '5':
                            break     
                    else:
                        print("No Posts in group!")
                        input("Press Enter to Continue....")
                        break
            elif userinput == "3":
                cursor.execute("Select * from getMembers(?)",(groupsJoin[CheckInp-1][0]))
                members = cursor.fetchall()
                cursor.execute("Select dbo.getTotalMembers(?)",(groupsJoin[CheckInp-1][0]))
                tmembers=cursor.fetchone()
                print(f"Total Members: {tmembers[0]}" )
                if tmembers[0] != 0:
                    for i in range(len(members)):
                        print(f"{i+1}. userName: {members[i][1]}  Name: {members[i][2]}")
                else:
                    print("No members Yet!")
                input("Press Enter to continue...")

            elif userinput == '4':
                x = input("You want to exit the group!(Y/N): ")
                if x.lower() == "y":
                    try:
                        cursor.execute("Exec exitGroup ?,?",(userID,groupsJoin[CheckInp-1][0]))
                    except pyodbc.Error as e:
                        print(f'Error: {e}')
                        time.sleep(1.5)
                        return
                    else:
                        conn.commit()
                        print("Group left!")
                        time.sleep(1.5)
                        return
            elif userinput == '5':
                break
        else:
            print("Inavlid Input!")
            time.sleep(1.7)
            
def manageGroupsForAdmin(conn,userID,groupsJoin,CheckInp):
    cursor = conn.cursor()
    while (True):
        clear_screen()
        print("1. Post in Group")
        print("2. Show Groups Post")
        print("3. Show Group Members")
        print("4. Leave Group")
        print("5. Delete this group")
        print("6. Exit")
        userinput = input("Enter Option: ")
        if userinput in ['1','2','3','4','5','6']:
            if userinput == '1':
                while(True):
                    cursor=conn.cursor()
                    content=input("Enter Content of the post: ")
                    check = input("Would You like to post it?(Y/N): ")
                    if check.lower() == "n":
                        break
                    elif check.lower() == "y":
                        try:
                            cursor.execute("Exec inputGroupPosts ?,?,?", (userID,content,groupsJoin[CheckInp-1][0]))
                        except pyodbc.Error as e:
                            print(f'Error: {e}')
                            time.sleep(2)
                            break
                        else:
                            print("Post Created SuccessFully!")
                            time.sleep(2)
                            conn.commit()
                            break
                    else:
                        print("Invalid Input!")
                        time.sleep(1.5)
                        break
            elif userinput == "2":
                check = 0
                while(True):
                    takeInput = ''
                    clear_screen()
                    cursor.execute("Exec getGroupPosts ?", (groupsJoin[CheckInp-1][0],))
                    posts = cursor.fetchall()
                    if posts:
                        print(f"Group Name: {posts[0][1]}")
                        for i in range(len(posts)):
                            clear_screen()
                            print(f"Post# {i+1} ")
                            print(f"User: {posts[i][3]}")
                            print(f"Content: {posts[i][2]}")
                            print(f"Likes: {posts[i][4]}  Commets: {posts[i][5]}")
                            print()
                            if check == i:
                                print("1. Like This Post ")
                                print("2. Comment on this Post")
                                print("3. See Comments")
                                print("4. Continue..")
                                print("5. Delete This Post")
                                print("6. Go Back")
                                takeInput = input()
                                if takeInput == '4':
                                    check+=1
                                elif takeInput == '1':
                                    x = input('Would You Want to like this post?(Y/N): ')
                                    if x.lower() == "y":
                                        cursor.execute("Select * from getUserLike(?,?,?)",(userID,posts[i][0],groupsJoin[CheckInp-1][0]))
                                        res = cursor.fetchone()
                                        if res:
                                           pass
                                        else:
                                            try:
                                                cursor.execute("Exec setGroupPostlikes ?,?,?",(userID,posts[i][0],groupsJoin[CheckInp-1][0]))
                                                conn.commit()
                                            except pyodbc.Error as e:
                                                print(f'Error: {e}')
                                                time.sleep(1.5)
                                                
                                        break
                                    else:
                                        break
                                elif takeInput == '2':
                                    x = input("Enter a comment: ").strip()
                                    if x:
                                        try:
                                            cursor.execute("Exec setGroupPostComments ?,?,?,?",(userID,posts[i][0],groupsJoin[CheckInp-1][0],x))
                                            conn.commit()
                                        except pyodbc.Error as e:
                                                print(f'Error: {e}')
                                                time.sleep(1.5)
                                        break
                                elif takeInput == '3':
                                    if posts[i][5] != 0:
                                        cursor.execute("Exec getCommentGroupPost ?,?",(posts[i][0],groupsJoin[CheckInp-1][0]))
                                        comments = cursor.fetchall()
                                        for i in range(len(comments)):
                                            print(f"{i+1}. UserName: {comments[i][0]}")
                                            print(f"Comment: {comments[i][1]}      Time: {comments[i][2]}")
                                            print()
                                    else:
                                        print("No Comment to show!")
                                    input("Enter to continue....")
                                    break
                                elif takeInput == '5':
                                    try:
                                        cursor.execute("Exec deleteGroupPost ?,?",(posts[i][0],groupsJoin[CheckInp-1][0]))
                                    except pyodbc.Error as e:
                                        print(f'Error: {e}')
                                        time.sleep(1.7)
                                        break
                                    else:
                                        conn.commit()
                                        print("Successfully deleted")
                                        time.sleep(1.7)
                                        break
                                elif takeInput == '6':
                                    break
                                else:
                                    print("Invalid Input!")
                                    time.sleep(1.6)
                                    break
                        else:
                            break
                        if  takeInput ==  '6':
                            break     
                    else:
                        print("No Posts in group!")
                        input("Press Enter to Continue....")
                        break
            elif userinput == "3":
                temp=0
                while(True):
                    cursor.execute("Select * from getMembers(?)",(groupsJoin[CheckInp-1][0]))
                    members = cursor.fetchall()
                    cursor.execute("Select dbo.getTotalMembers(?)",(groupsJoin[CheckInp-1][0]))
                    tmembers=cursor.fetchone()
                    print(f"Total Members: {tmembers[0]}" )
                    if tmembers[0] != 0:
                        takeUser = ''
                        for i in range(len(members)):
                            clear_screen()
                            print(f"{i+1}. userName: {members[i][1]}  Name: {members[i][2]}  Role: {members[i][3]}")
                            if members[i][3] != "Admin":
                                print("1. Remove This Member")
                            print("2. Continue")
                            print("3. Go Back")
                            takeUser = input()
                            if takeUser in ['1','2','3']:
                                if takeUser == '3':
                                    break
                                elif takeUser == '2':
                                    temp+=1
                                elif takeUser == '1':
                                    cursor.execute("Select * from getMemGroupPosts(?,?)",(members[i][0],groupsJoin[CheckInp-1][0]))
                                    posid = cursor.fetchall()
                                    for i in range(len(posid)):
                                        try:
                                            cursor.execute("Exec deleteGroupPost ?,?",(posid[i][0],groupsJoin[CheckInp-1][0]))
                                        except pyodbc.Error as e:
                                            print(f'Error: {e}')
                                            time.sleep(1.7)
                                            break
                                        else:
                                            conn.commit()
                                    else:
                                        try:
                                            cursor.execute("Exec deleteMember ?,?", (members[i][0],groupsJoin[CheckInp-1][0]))
                                        except pyodbc.Error as e:
                                            print(f'Error: {e}')
                                            time.sleep(1.7)
                                            break
                                        else:
                                            conn.commit()
                                            break
                            else:
                                print("Invalid Input!")
                                time.sleep(1.6)
                                break
                        else:
                            break
                        if takeUser == '3':
                            break
                    else:
                        print("No members Yet!")
                        input("Press Enter to continue...")
                        break

            elif userinput == '4':
                x = input("You want to exit the group!(Y/N): ")
                if x.lower() == "y":
                    try:
                        cursor.execute("Exec exitGroup ?,?",(userID,groupsJoin[CheckInp-1][0]))
                    except pyodbc.Error as e:
                        print(f'Error: {e}')
                    else:
                        conn.commit()
                        print("Group left!")
                    time.sleep(1.5)
                    return
            elif userinput == '5':
                x = input("Do you want this group deleted permanently?(Y/N): ")
                if x.lower() == "y":
                    try:
                        cursor.execute("Exec deleteGroup ?",(groupsJoin[CheckInp-1][0],))
                        print("Deleted Successfully!")
                        conn.commit()
                        input("Press Enter to Continue....")
                        return
                    except pyodbc.Error as e:
                        print(f'Error: {e}')
                        time.sleep(1.7)
                        return
            elif userinput == '6':
                break
        else:
            print("Inavlid Input!")
            time.sleep(1.7)

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
                try:
                    cursor.execute("Exec newGroup ?,?,?",(userID,name,description))
                    conn.commit()
                    print("Group Created SuccessFully!")
                except pyodbc.Error as e:
                    print(f'Error: {e}')
                time.sleep(1.8)
            elif Userinput == '2':
                cursor.execute("Select * from getALLGroup()")
                groups = cursor.fetchall()
                for i in range(len(groups)):
                    print(f"GR NO. {i+1} GROUP NAME: {groups[i][1]}")
                    print(f"Description: {groups[i][2]}")
                    print()
                try: 
                    inputNUM = int(input("Enter Group Number to Join: "))
                    if 1 <= inputNUM <= len(groups):
                        groupID = groups[inputNUM-1][0]
                        cursor.execute("Select * from getGroupMembers(?,?)",(groupID,userID))
                        if cursor.fetchone():
                            print("You Already Member of this Group!")
                        else:
                            try:
                                cursor.execute("Exec insertGroupMember ?,?",(groupID,userID))
                                conn.commit()
                                print("Successfully join in the Group!")
                            except pyodbc.Error as e:
                                print(f'Error: {e}')
                    else:
                        print("Invalid Input!")
                except Exception as e:
                    print(f"Error occurred: {e}")
                time.sleep(1.8)
            elif Userinput == '3':
                cursor.execute("Select * from specificGroupsOfUser(?)",(userID,))
                groupsJoin = cursor.fetchall()
                if groupsJoin:
                    print(f"Total Groups: {len(groupsJoin)}")
                    for i in range (len(groupsJoin)):
                        print(f"Group Number: {i+1} Group Name: {groupsJoin[i][1]}")
                    try: 
                        CheckInp = int(input("Enter Group Number to view: "))
                        if 1 <= CheckInp <= len(groupsJoin):
                            if not(groupsJoin[CheckInp-1][3] == 'Admin'):
                                manageGroupsForMember(conn,userID,groupsJoin,CheckInp)
                            else:
                                manageGroupsForAdmin(conn,userID,groupsJoin,CheckInp)
                        else:
                            print("Invalid Input!")
                    except Exception as e:
                        print(f'Error: {e}')
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
                try:
                    cursor.execute("Exec updateUserName ?,?", (userID,x))
                    
                except:
                    print('UserName is already Taken!')
                else:
                    conn.commit()
                time.sleep(2)
            elif Userinput == '2':
                x = get_password()
                try:
                    cursor.execute("Exec updatePassWord ?,?", (userID,x))
                    print("PassWord Updated Sucessfully")
                    conn.commit()
                except pyodbc.Error as e:
                    print(f"Error: {e}")
                time.sleep(1.7)
                
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
                        try:
                            cursor.execute("Exec updateAccountStatus ?,?", (userID,'Deactivated'))
                            conn.commit()
                            return 'Y'
                        except pyodbc.Error as e:
                            print(f'Error: {e}')
                            time.sleep(2)
                            break
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
                        try:
                            cursor.execute("Exec DelUser ?", (userID,))
                            print("Your Account Has been Deleted SuccessFully!")
                            time.sleep(2)
                            conn.commit()
                            return 'Y'
                        except pyodbc.Error as e:
                            print(f"Error: {e}")
                            time.sleep(2)
                            break
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
        print("1. Chat with Friends")
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
                Chat(conn,userID)
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
                    try:
                        cursor.execute("Exec updateAccountStatus ?,?", (result[0],'Active'))
                    except pyodbc.Error as ex:
                        sqlstate = ex.args[0]  
                        message = ex.args[1]   
                        print(f"SQL State: {sqlstate}, Error Message: {message}")
                    else:
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
        FirstName= input("Enter First Name: ")
        LastName= input("Enter Last Name: ")
        dateOfBirth = input("Enter Date Of Birth(YYYY-MM-DD):")
        try:
            cursor.execute("Exec InsertUser ?, ?, ?,?,?,?", (userName, email, PassWord,dateOfBirth,FirstName,LastName))
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]  
            message = ex.args[1]   
            print(f"SQL State: {sqlstate}, Error Message: {message}")
            x = input("Do You Want to Continue...(Y/N):").strip()
            if x.lower() == "n":
                break
            elif x.lower() == "y":
                pass
            else:
                print("Invalid Input")
                break
        else:
            print("Account Created SuccessFully! Now Login...")
            conn.commit()
            input("Press Enter to Continue....")
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


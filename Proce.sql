use SocialMediaPlatform;
GO
CREATE OR ALTER PROCEDURE InsertUser
    @Username VARCHAR(50),
    @Email VARCHAR(100),
    @PasswordF VARCHAR(255),
    @Birthdate DATE,
    @FirstName VARCHAR(50),
    @LastName VARCHAR(50)
AS
INSERT INTO Users
    (Username, Email, PasswordF, DateOfBirth ,FirstName ,LastName)
VALUES
    (@Username, @Email, @PasswordF, @Birthdate , @FirstName, @LastName);

GO
CREATE OR ALTER PROCEDURE updateAccountStatus
    @UserID INT,
    @AccountStatus VARCHAR(20)
AS
UPDATE Users
SET AccountStatus = @AccountStatus, UpdatedAt = GETDATE()
WHERE UserID= @UserID;

GO
CREATE OR ALTER PROCEDURE updateUserName
    @UserID INT,
    @Username VARCHAR(50)
AS
UPDATE Users
SET Username  = @Username,UpdatedAt = GETDATE()
WHERE UserID= @UserID
GO
CREATE OR ALTER PROCEDURE updatePassWord
    @UserID INT,
    @PasswordF VARCHAR(255)
AS
UPDATE Users
SET PasswordF=@PasswordF, UpdatedAt = GETDATE()
WHERE UserID= @UserID

GO
CREATE OR ALTER PROCEDURE updateName
    @UserID INT,
    @Fname VARCHAR(50),
    @Lname VARCHAR(50)
AS
UPDATE Users
SET FirstName=@Fname, LastName = @Lname, UpdatedAt = GETDATE()
WHERE UserID= @UserID
GO
CREATE OR ALTER PROCEDURE DelUser
    @UserID INT
AS
DELETE FROM Users WHERE UserID = @UserID;
GO

CREATE OR ALTER PROCEDURE inputPosts
    @UserID INT,
    @Content Text
AS
INSERT INTO Posts
    (UserID,Content)
VALUES
    (@UserID, @Content);
GO
CREATE OR ALTER PROCEDURE DelPost
    @UserID INT
AS
DELETE FROM Posts WHERE UserID = @UserID;



GO
CREATE OR ALTER PROCEDURE DelLikes
    @UserID INT
AS
DELETE FROM Likes WHERE UserID = @UserID;


GO
CREATE OR ALTER PROCEDURE DelComments
    @UserID INT
AS
DELETE FROM Comments WHERE UserID = @UserID;

GO

CREATE OR ALTER PROCEDURE getPostComments
    @PostID INT
AS
BEGIN
    SELECT Users.Username, Comments.Content
    FROM Comments
        JOIN Users ON Comments.UserID = Users.UserID
    WHERE Comments.PostID = @PostID
    ORDER BY Comments.CreatedAt DESC;
END;

GO
CREATE OR ALTER PROCEDURE addLike
    @PostID INT,
    @UserID INT
AS
BEGIN
    INSERT INTO Likes
        (PostID, UserID, LikedAt)
    VALUES
        (@PostID, @UserID, GETDATE());
END;

GO
CREATE OR ALTER PROCEDURE insertComment
    @PostID INT,
    @UserID INT,
    @CommentContent NVARCHAR(MAX)
AS
BEGIN
    INSERT INTO Comments
        (PostID, UserID, Content, CreatedAt)
    VALUES
        (@PostID, @UserID, @CommentContent, GETDATE());
END;

GO
CREATE OR ALTER PROCEDURE sendFriendRequest
    @UserID INT,
    @FriendUserID INT
AS
BEGIN
    INSERT INTO Friends
        (SenderID, ReceiverID, Status , FriendshipDate)
    VALUES
        (@UserID, @FriendUserID, 'Pending', GETDATE());
END;

GO

CREATE OR ALTER PROCEDURE updateFriendRequestStatus
    @SenderID INT,
    @Status VARCHAR(20)
AS
BEGIN
    UPDATE Friends
    SET Status = @Status, FriendshipDate =  GETDATE()
    WHERE SenderID = @SenderID AND Status = 'Pending';
END;

GO

CREATE OR ALTER PROCEDURE getSentRequests
    @UserID INT
AS
BEGIN
    SELECT 
        ReceiverID AS FriendID,
        U.Username,
        U.FirstName,
        U.LastName,
        F.Status
    FROM Friends F
    INNER JOIN Users U ON F.ReceiverID = U.UserID
    WHERE F.SenderID = @UserID and Status = 'Pending'
END;
GO
CREATE OR ALTER PROCEDURE getFriendsList
    @UserID INT
AS
BEGIN
    SELECT 
        CASE 
            WHEN F.SenderID = @UserID THEN F.ReceiverID
            ELSE F.SenderID
        END AS FriendID,
        U.Username,
        U.FirstName,
        U.LastName
    FROM Friends F
    INNER JOIN Users U ON 
        (F.SenderID = @UserID AND U.UserID = F.ReceiverID) OR 
        (F.ReceiverID = @UserID AND U.UserID = F.SenderID)
    WHERE F.Status = 'Accepted';
END;

GO
CREATE OR ALTER PROCEDURE removeFriend
    @UserID INT,
    @FriendID INT
AS
BEGIN
    DELETE FROM Friends
    WHERE (SenderID = @UserID AND ReceiverID = @FriendID) OR 
          (SenderID = @FriendID AND ReceiverID = @UserID);
END;
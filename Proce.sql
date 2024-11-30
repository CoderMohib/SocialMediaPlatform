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
        U.LastName,
        U.NoOfFriends
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
GO
CREATE OR ALTER PROCEDURE newGroup
    @UserID INT,
    @GroupName VARCHAR(100),
    @Description Text
AS
INSERT INTO Groups
    (GroupName, Description, CreatedBy)
VALUES
    ( @GroupName, @Description, @UserID );
DECLARE @GroupID INT;
SELECT @GroupID = GroupID
from Groups
WHERE CreatedBy = @UserID;
INSERT INTO GroupMembers
    (GroupID,UserID,Role)
VALUES
    ( @GroupID, @UserID, 'Admin' );
    
GO
CREATE OR ALTER PROCEDURE insertGroupMember
    @GroupID Int,
    @UserID Int
AS
BEGIN
    INSERT INTO GroupMembers
        (GroupID,UserID,Role)
    VALUES
        ( @GroupID, @UserID, 'Member')
END



GO
CREATE OR ALTER PROCEDURE inputGroupPosts
    @UserID INT,
    @Content NVARCHAR(MAX),
    @GroupID INT
AS
INSERT INTO GroupPosts
    (UserID,Content,GroupID)
VALUES
    (@UserID, @Content, @GroupID);

GO
CREATE OR ALTER PROCEDURE getGroupPosts
    @GroupID INT
AS
BEGIN
    SELECT gp.GroupPostID, (Select GroupName
        from Groups
        where GroupID = @GroupID) AS GroupName, gp.Content ,
        (Select FirstName + ' ' + LastName
        from Users
        where UserID = gp.UserID) AS UserName,
        TotalLikes,
        TotalComments
    from GroupPosts gp
    WHERE GroupID = @GroupID
    ORDER BY PostDate DESC
END
GO
CREATE OR ALTER PROCEDURE setGroupPostlikes
    @UserID INT,
    @PostID INT,
    @GroupID INT
AS
BEGIN
    INSERT INTO GroupLikes
        (GroupID,UserID,GroupPostID)
    VALUES(@GroupID, @UserID, @PostID)
END
GO
CREATE OR ALTER PROCEDURE setGroupPostComments
    @UserID INT,
    @PostID INT,
    @GroupID INT,
    @Content TEXT
AS
BEGIN
    INSERT INTO GroupComments
        (GroupID,UserID,GroupPostID,Content)
    VALUES(@GroupID, @UserID, @PostID, @Content)
END

GO

CREATE OR ALTER PROCEDURE getCommentGroupPost
    @PostID INT,
    @GroupID INT
AS
BEGIN
    SELECT (Select (FirstName + ' '+ LastName)
        from Users
        where Users.UserID = GroupComments.UserID) AS FullName,
        Content, CreatedAt
    From GroupComments
    Where GroupPostID = @PostID AND GroupID = @GroupID
    ORDER BY CreatedAt DESC
END

GO


CREATE OR ALTER PROCEDURE deleteMember
    @UserID INT,
    @GroupID INT
AS
BEGIN
    DELETE FROM GroupMembers WHERE UserID=@UserID AND @GroupID=GroupID
END
GO



-----------------------
--Get chat
CREATE OR ALTER PROCEDURE getChat @SenderID INT , @ReceiverID INT 
AS
BEGIN
SELECT MessageID, SenderID, ReceiverID, Content, SentAt, IsRead
FROM Messages
WHERE (SenderID = @SenderID AND ReceiverID = @ReceiverID)
   OR (SenderID = @ReceiverID AND ReceiverID = @SenderID)
ORDER BY SentAt ASC
END

GO
CREATE OR ALTER PROCEDURE updateMessageRead @UserID INT, @ChatPartnerID INT
AS
BEGIN
UPDATE Messages
SET IsRead = 1
WHERE ReceiverID = @UserID AND SenderID = @ChatPartnerID AND IsRead = 0;
END;

GO

CREATE OR ALTER PROCEDURE newMsg @UserID INT, @ChatPartnerID INT, @Content NVARCHAR(MAX)
AS 
BEGIN
INSERT INTO Messages (SenderID, ReceiverID, Content)
VALUES (@UserID, @ChatPartnerID, @Content)
END
GO
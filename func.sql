use SocialMediaPlatform;
GO
CREATE OR ALTER FUNCTION retriveDataFromUsers()
RETURNS TABLE
AS
RETURN
    SELECT *
from Users;

GO
CREATE OR ALTER FUNCTION retriveDataSUsers(@UserID INT)
RETURNS TABLE
AS
RETURN
    SELECT *
from Users
WHERE UserID=@UserID;
GO

CREATE OR ALTER FUNCTION retriveName(@UserID INT)
RETURNS VARCHAR(100)
AS
BEGIN
    RETURN
    (SELECT FirstName + ' ' + LastName
    from Users
    WHERE UserID=@UserID)
END;


GO
CREATE OR ALTER FUNCTION retriveDataUserName (@Username VARCHAR(50))
RETURNS TABLE
AS
RETURN
    SELECT Username
FROM Users
WHERE Username = @Username;


GO
CREATE OR ALTER FUNCTION retriveDataEmail(@Email VARCHAR(100))
RETURNS TABLE
AS
RETURN
    SELECT Email
from Users
WHERE Email = @Email;


GO
CREATE OR ALTER FUNCTION retriveDataEmailAndUserName(@Username VARCHAR(50),@Email VARCHAR(100))
RETURNS TABLE
AS
RETURN
    SELECT Username, Email
from Users
WHERE Email = @Email OR Username = @Username;

GO

CREATE OR ALTER FUNCTION retriveUSERID (@Email VARCHAR(100),@PasswordF VARCHAR(255) )
RETURNS TABLE
AS
RETURN
    SELECT UserID, AccountStatus
from Users
WHERE Email = @Email AND PasswordF = @PasswordF;

GO
CREATE OR ALTER FUNCTION GetPostsByUserID (@UserID INT)
RETURNS TABLE
AS
RETURN
    SELECT Content, CreatedAt
FROM Posts
WHERE UserID = @UserID;


GO

CREATE OR ALTER FUNCTION getUserPost(@UserID INT)
RETURNS TABLE
AS
RETURN( SELECT PostID, Content, CreatedAt
from Posts
WHERE UserID = @UserID );


GO

CREATE OR ALTER FUNCTION getComments(@PostID INT)
RETURNS INT
AS
BEGIN
    RETURN(SELECT COUNT(UserID)
    from Comments
    WHERE PostID = @PostID AND UserID IS NOT NULL)
END

GO
CREATE OR ALTER FUNCTION getLikes(@PostID INT)
RETURNS INT
AS
BEGIN
    RETURN(SELECT COUNT(UserID)
    from Likes
    WHERE PostID = @PostID AND UserID IS NOT NULL)
END

GO
CREATE OR ALTER FUNCTION getPostLikes
(@PostID INT)
RETURNS TABLE
AS
RETURN(
    SELECT Users.Username
FROM Likes
    JOIN Users ON Likes.UserID = Users.UserID
WHERE Likes.PostID = @PostID);

GO

CREATE OR ALTER FUNCTION checkUserLikedPost (@PostID INT, @UserID INT)
RETURNS TABLE
AS
    RETURN (
        SELECT *
FROM Likes
WHERE PostID = @PostID AND UserID = @UserID
    )

GO

CREATE OR ALTER FUNCTION getFriendship(@UserID INT , @FriendUserID Int)
RETURNS TABLE
AS
    RETURN (
        SELECT SenderID,
    ReceiverID,
    Status
FROM Friends
WHERE (SenderID = @UserID AND ReceiverID = @FriendUserID) OR (SenderID = @FriendUserID AND ReceiverID = @UserID)
    )

GO
CREATE OR ALTER FUNCTION getPendingFriendRequests(@UserID INT)
RETURNS TABLE
AS
RETURN (
 SELECT
    SenderID AS FriendID,
    U.Username,
    U.FirstName,
    U.LastName
FROM Friends F
    INNER JOIN Users U ON F.SenderID = U.UserID
WHERE F.ReceiverID = @UserID AND F.Status = 'Pending'
)
GO
CREATE OR ALTER FUNCTION getALLGroup()
RETURNS TABLE
AS
RETURN(SELECT *
from Groups)
GO

CREATE OR ALTER FUNCTION getGroupMembers(@GroupID INT,@UserID INT)
RETURNS TABLE
AS
RETURN(SELECT *
from GroupMembers
WHERE GroupID = @GroupID and UserID = @UserID)
GO

CREATE OR ALTER FUNCTION specificGroupsOfUser
(@UserID INT)
RETURNS TABLE
AS
RETURN(
    SELECT G.GroupID, G.GroupName , (SELECT UserID from Users WHERE UserID = G.CreatedBy) AS [ADMIN ID]
from Groups G INNER join GroupMembers GM on GM.GroupID = G.GroupID AND GM.UserID = @UserID
     )
GO
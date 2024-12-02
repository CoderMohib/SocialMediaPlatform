use SocialMediaPlatform;

--ok
GO
CREATE OR ALTER FUNCTION retriveDataSUsers(@UserID INT)
RETURNS TABLE
AS
RETURN
    SELECT *
from Users
WHERE UserID=@UserID;


GO
--ok
CREATE OR ALTER FUNCTION retriveUSERID (@Email VARCHAR(100),@PasswordF VARCHAR(255) )
RETURNS TABLE
AS
RETURN
    SELECT UserID, AccountStatus
from Users
WHERE Email = @Email AND PasswordF = @PasswordF;

GO
--extra
CREATE OR ALTER FUNCTION GetPostsByUserID (@UserID INT)
RETURNS TABLE
AS
RETURN
    SELECT Content, CreatedAt
FROM Posts
WHERE UserID = @UserID;

GO
--ok
CREATE OR ALTER FUNCTION getUserPost(@UserID INT)
RETURNS TABLE
AS
RETURN( SELECT p.PostID, (u.FirstName + ' ' + u.LastName) AS FullName, p.Content, p.CreatedAt , p.NoOfLikes, p.NoOfComments
from Posts p INNER JOIN Users u on u.UserID = p.UserID
WHERE p.UserID = @UserID );


GO
--extra
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
--ok
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
--ok
CREATE OR ALTER FUNCTION checkUserLikedPost (@PostID INT, @UserID INT)
RETURNS TABLE
AS
    RETURN (
        SELECT *
FROM Likes
WHERE PostID = @PostID AND UserID = @UserID
    )

GO
--ok
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
--ok
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

-----groups ke func ok
CREATE OR ALTER FUNCTION getALLGroup()
RETURNS TABLE
AS
RETURN(SELECT *
from Groups)
GO
-- Ke agar user kisi alread group mai ho aur wo us mai dobara join karna ki kosish kra --ok
CREATE OR ALTER FUNCTION getGroupMembers(@GroupID INT,@UserID INT)
RETURNS TABLE
AS
RETURN(SELECT *
from GroupMembers
WHERE GroupID = @GroupID and UserID = @UserID)
GO
--ok
CREATE OR ALTER FUNCTION specificGroupsOfUser
(@UserID INT)
RETURNS TABLE
AS
RETURN(
    SELECT G.GroupID, G.GroupName , (SELECT UserID
    from Users
    WHERE UserID = G.CreatedBy) AS [ADMIN ID], Role
from Groups G INNER join GroupMembers GM on GM.GroupID = G.GroupID AND GM.UserID = @UserID
     )
GO
--ok
CREATE OR ALTER FUNCTION getMembers(@GroupID INT)
RETURNS TABLE
AS 
RETURN(
    SELECT u.UserID, u.UserName , (u.FirstName + ' ' + u.LastName) AS FullName, GM.Role
FROM Users u
    INNER JOIN GroupMembers GM on GM.UserID = u.UserID
where GM.GroupID = @GroupID
)
GO
--ok
CREATE OR ALTER FUNCTION getTotalMembers(@GroupID INT)
RETURNS INT
AS 
BEGIN
    DECLARE @TMEM INT
    SELECT @TMEM = NoOfGroupMembers
    from Groups
    WHERE GroupID = @GroupID
    RETURN @TMEM
END

GO
--ok
CREATE OR ALTER FUNCTION getUserLike(@UserID INT,
    @PostID INT,
    @GroupID INT)
RETURNS TABLE
AS 
RETURN(
    SELECT UserID
From GroupLikes
Where GroupPostID = @PostID AND UserID = @UserID AND GroupID = @GroupID
)

GO
--ok
---sari groups ki pos ko le rha hai kisi specific member of he group ki
CREATE OR ALTER FUNCTION getMemGroupPosts(@UserID INT,
@GroupID INT)
RETURNS TABLE
AS 
RETURN(
    SELECT GroupPostID
from GroupPosts
where UserID= @UserID AND GroupID = @GroupID
)
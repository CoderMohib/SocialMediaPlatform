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
RETURN( SELECT PostID,Content,CreatedAt from Posts WHERE UserID = @UserID );


GO

CREATE OR ALTER FUNCTION getComments(@PostID INT)
RETURNS INT
AS
BEGIN
RETURN(SELECT COUNT(UserID) from Comments WHERE PostID = @PostID AND UserID IS NOT NULL)
END


GO
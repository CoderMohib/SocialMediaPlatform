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
CREATE OR ALTER PROCEDURE updateAccountStatus
    @UserID INT,
    @AccountStatus VARCHAR(20)
AS
UPDATE Users
SET AccountStatus = @AccountStatus, UpdatedAt = GETDATE()
WHERE UserID= @UserID

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
-----------------------------------------------------
CREATE OR ALTER PROCEDURE inputPosts
@UserID INT,
@Content Text
AS
    INSERT INTO Posts(UserID,Content) VALUES (@UserID,@Content);
GO
CREATE OR ALTER PROCEDURE DelPost
    @UserID INT
AS
DELETE FROM Posts WHERE UserID = @UserID;
GO

CREATE OR ALTER FUNCTION getUserPost(@UserID INT)
RETURNS TABLE
AS
RETURN( SELECT PostID,Content,CreatedAt from Posts WHERE UserID = @UserID );

GO
CREATE OR ALTER PROCEDURE DelLikes
    @UserID INT
AS
DELETE FROM Likes WHERE UserID = @UserID;
GO
CREATE OR ALTER FUNCTION getLikes(@PostID INT)
RETURNS INT
AS
BEGIN
RETURN(SELECT COUNT(UserID) from Likes WHERE PostID = @PostID AND UserID IS NOT NULL)
END

GO

CREATE OR ALTER FUNCTION getComments(@PostID INT)
RETURNS INT
AS
BEGIN
RETURN(SELECT COUNT(UserID) from Comments WHERE PostID = @PostID AND UserID IS NOT NULL)
END

GO
CREATE OR ALTER PROCEDURE DelComments
    @UserID INT
AS
DELETE FROM Comments WHERE UserID = @UserID;
GO
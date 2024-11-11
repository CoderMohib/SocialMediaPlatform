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




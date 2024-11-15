CREATE DATABASE SocialMediaPlatform;

USE SocialMediaPlatform;
CREATE TABLE Users
(
    UserID INT PRIMARY KEY IDENTITY(1,1),
    Username VARCHAR(50) NOT NULL UNIQUE,
    Email VARCHAR(100) NOT NULL UNIQUE,
    PasswordF VARCHAR(255) NOT NULL CHECK (LEN(PasswordF) >= 8),
    CreatedAt DATETIME NOT NULL DEFAULT GETDATE(),
    UpdatedAt DATETIME NOT NULL DEFAULT GETDATE(),
    FirstName VARCHAR(50) NULL,
    LastName VARCHAR(50) NULL,
    DateOfBirth DATE NULL CHECK (DATEADD(YEAR, 13, DateOfBirth) <= GETDATE()),
    AccountStatus VARCHAR(20) NOT NULL DEFAULT 'Active',
    Age AS DATEDIFF(YEAR, DateOfBirth, GETDATE()) 
        - CASE WHEN (MONTH(DateOfBirth) > MONTH(GETDATE()))
        OR (MONTH(DateOfBirth) = MONTH(GETDATE()) AND DAY(DateOfBirth) > DAY(GETDATE()))
               THEN 1 ELSE 0 END,
    CHECK (AccountStatus IN ('Active', 'Suspended', 'Deactivated')),
    CHECK (Username <> PasswordF)
);

CREATE INDEX idx_Users_UserID
ON Users (UserID)

-- hi kesi ho
CREATE INDEX idx_Users_Username
ON Users (Username)

CREATE INDEX idx_Users_Email
ON Users (Email)

CREATE INDEX idx_Users_UserName_Email
ON Users (Username,Email)


CREATE TABLE Posts
(
    PostID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT NOT NULL,
    Content TEXT NULL,
    CreatedAt DATETIME NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

CREATE INDEX idx_Post_PostID
On Posts (PostID)

CREATE INDEX idx_Post_UserID
On Posts (UserID)

CREATE INDEX idx_Post_UserPostID
On Posts (UserID,PostID)


CREATE TABLE Likes (
    LikeID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT NULL,  -- Allow NULLs
    PostID INT NOT NULL,
    LikedAt DATETIME NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ,
    FOREIGN KEY (PostID) REFERENCES Posts(PostID)  
);


CREATE INDEX idx_Likes_PostID
On Likes (PostID)

CREATE INDEX idx_Likes_UserID
On Likes (UserID)

CREATE INDEX idx_Likes_LikesID
On Likes (LikeID)

CREATE INDEX idx_Likes_UserPostID
On Likes (UserID,PostID)

CREATE INDEX idx_Likes_UserLikesID
On Likes (UserID,LikeID)


CREATE TABLE Comments (
    CommentID INT PRIMARY KEY IDENTITY(1,1),
    PostID INT NULL,
    UserID INT NULL,
    Content TEXT NOT NULL,
    CreatedAt DATETIME NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (PostID) REFERENCES Posts(PostID) ,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) 
);

CREATE INDEX idx_Comments_PostID
On Comments (PostID)

CREATE INDEX idx_Comments_UserID
On Comments (UserID)

CREATE INDEX idx_Comments_CommentsID
On Comments (CommentID)

CREATE INDEX idx_Comments_UserPostID
On Comments (UserID,PostID)

CREATE INDEX idx_Comments_UserCommentsID
On Comments (UserID,CommentID)













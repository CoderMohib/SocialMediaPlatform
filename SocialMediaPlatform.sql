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
    NoOfPost INT DEFAULT 0,
    NoOfFriends INT DEFAULT 0,
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
    Content TEXT NULL, --NVARCHAR(MAX)
    CreatedAt DATETIME NOT NULL DEFAULT GETDATE(),
    NoOfLikes INT DEFAULT 0,
    NoOfComments INT DEFAULT 0,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

CREATE INDEX idx_Post_PostID
On Posts (PostID)

CREATE INDEX idx_Post_UserID
On Posts (UserID)

CREATE INDEX idx_Post_UserPostID
On Posts (UserID,PostID)


CREATE TABLE Likes
(
    LikeID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT NOT NULL,
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


CREATE TABLE Comments
(
    CommentID INT PRIMARY KEY IDENTITY(1,1),
    PostID INT NOT NULL,
    UserID INT NOT NULL,
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

CREATE TABLE Friends (
    SenderID INT NOT NULL,
    ReceiverID INT NOT NULL,
    Status VARCHAR(20) NOT NULL DEFAULT 'Pending' CHECK (Status IN ('Pending', 'Accepted', 'Rejected')),
    FriendshipDate DATETIME NOT NULL DEFAULT GETDATE(),
    PRIMARY KEY (SenderID , ReceiverID),
    FOREIGN KEY (SenderID) REFERENCES Users(UserID),
    FOREIGN KEY (ReceiverID) REFERENCES Users(UserID)
)

CREATE INDEX idx_FRIENDS_SenderID
On Friends (SenderID)

CREATE INDEX idx_FRIENDS_ReceiverID
On Friends (ReceiverID)

CREATE INDEX idx_FRIENDS_SR
On Friends (SenderID,ReceiverID)

CREATE TABLE Groups (
    GroupID INT PRIMARY KEY IDENTITY(1,1),
    GroupName VARCHAR(100) NOT NULL,
    Description TEXT NULL,
    CreatedAt DATETIME NOT NULL DEFAULT GETDATE(),
    CreatedBy INT NOT NULL,
    NoOfGroupPost INT DEFAULT 0,
    NoOfGroupMembers INT DEFAULT 0,
    FOREIGN KEY (CreatedBy) REFERENCES Users(UserID)
);
CREATE TABLE GroupMembers (
    GroupID INT NOT NULL,
    UserID INT NOT NULL,
    Role VARCHAR(20) NOT NULL DEFAULT 'Member' CHECK (Role IN ('Member','Admin')),
    JoinedAt DATETIME NOT NULL DEFAULT GETDATE(),
    TotalGroupPost INT DEFAULT 0,
    PRIMARY KEY (GroupID, UserID),
    FOREIGN KEY (GroupID) REFERENCES Groups(GroupID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE GroupPosts (
    GroupPostID INT IDENTITY(1,1) PRIMARY KEY ,
    GroupID INT NOT NULL,
    UserID INT NOT NULL,
    Content NVARCHAR(MAX) NULL,
    TotalLikes INT DEFAULT 0,
    TotalComments INT DEFAULT 0,
    PostDate DATETIME NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (GroupID) REFERENCES Groups(GroupID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE GroupLikes (
    GroupLikeID INT IDENTITY(1,1) PRIMARY KEY ,
    GroupID INT NOT NULL,
    UserID INT NOT NULL,
    GroupPostID INT NOT NULL,
    PostDate DATETIME NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (GroupID) REFERENCES Groups(GroupID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (GroupPostID) REFERENCES GroupPosts(GroupPostID)
);

CREATE TABLE GroupComments
(
    GroupCommentID INT PRIMARY KEY IDENTITY(1,1),
    GroupPostID INT NULL,
    GroupID INT NOT NULL,
    UserID INT NOT NULL,
    Content TEXT NOT NULL,
    CreatedAt DATETIME NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (GroupPostID) REFERENCES GroupPosts(GroupPostID) ,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (GroupID) REFERENCES Groups(GroupID)
);



CREATE INDEX idx_Groups_CreatedBy
ON Groups (CreatedBy);

CREATE INDEX idx_Groups_GroupName
ON Groups (GroupName);

CREATE INDEX idx_GroupMembers_GroupID
ON GroupMembers (GroupID);

CREATE INDEX idx_GroupMembers_UserID
ON GroupMembers (UserID);

CREATE INDEX idx_GroupMembers_GroupID_UserID
ON GroupMembers (GroupID, UserID);

CREATE INDEX idx_GroupPosts_GroupID
ON GroupPosts (GroupID);


CREATE INDEX idx_GroupPosts_UserID
ON GroupPosts (UserID);


CREATE INDEX idx_GroupPosts_GroupID_PostDate
ON GroupPosts (GroupID, PostDate);

CREATE INDEX idx_GroupLikes_GroupID
ON GroupLikes (GroupID);

CREATE INDEX idx_GroupLikes_GroupPostID
ON GroupLikes (GroupPostID);

CREATE INDEX idx_GroupLikes_UserID_GroupPostID
ON GroupLikes (UserID, GroupPostID);

CREATE INDEX idx_GroupComments_GroupID
ON GroupComments (GroupID);

CREATE INDEX idx_GroupComments_GroupPostID
ON GroupComments (GroupPostID);


CREATE INDEX idx_GroupComments_UserID
ON GroupComments (UserID);

CREATE INDEX idx_GroupComments_GroupPostID_CreatedAt
ON GroupComments (GroupPostID, CreatedAt);

CREATE TABLE Messages (
    MessageID INT PRIMARY KEY IDENTITY(1,1), 
    SenderID INT NOT NULL, 
    ReceiverID INT NOT NULL, 
    Content NVARCHAR(MAX) NOT NULL, 
    SentAt DATETIME NOT NULL DEFAULT GETDATE(), 
    IsRead BIT DEFAULT 0,
    FOREIGN KEY (SenderID) REFERENCES Users(UserID),
    FOREIGN KEY (ReceiverID) REFERENCES Users(UserID) 
);


CREATE INDEX idx_Messages_SenderID
ON Messages (SenderID);

CREATE INDEX idx_Messages_ReceiverID
ON Messages (ReceiverID);

CREATE INDEX idx_Messages_SentAt
ON Messages (SentAt);

-- Composite index for sender-receiver pair
CREATE INDEX idx_Messages_SenderReceiver
ON Messages (SenderID, ReceiverID);







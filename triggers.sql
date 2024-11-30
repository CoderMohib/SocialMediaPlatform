USE SocialMediaPlatform;

GO

CREATE  TRIGGER NoOfUserPosts
ON Posts
AFTER INSERT
AS
BEGIN
    UPDATE Users
    SET NoOfPost = NoOfPost + 1
    WHERE UserID IN (SELECT UserID FROM Inserted);
END;
GO

CREATE  TRIGGER NoOfUsersPosts
ON Posts
AFTER DELETE
AS
BEGIN
    UPDATE Users
    SET NoOfPost = NoOfPost - 1
    WHERE UserID IN (SELECT UserID FROM deleted);
END;

GO

CREATE  TRIGGER Inc_likes
ON Likes
AFTER INSERT
AS
BEGIN 
    UPDATE Posts 
    SET NoOfLikes = NoOfLikes + 1 
    WHERE PostID IN (SELECT PostID From Inserted);
END;
GO

CREATE  TRIGGER Inc_Comments
ON Comments
AFTER INSERT
AS
BEGIN 
    UPDATE Posts 
    SET NoOfComments = NoOfComments + 1 
    WHERE PostID IN (SELECT PostID From Inserted);
END;

GO
CREATE  TRIGGER Dec_likes
ON Likes
AFTER DELETE
AS
BEGIN 
    UPDATE Posts 
    SET NoOfLikes = NoOfLikes - 1 
    WHERE PostID IN (SELECT PostID From deleted);
END;
GO

CREATE  TRIGGER Dec_Comments
ON Comments
AFTER DELETE
AS
BEGIN 
    UPDATE Posts 
    SET NoOfComments = NoOfComments - 1 
    WHERE PostID IN (SELECT PostID From deleted);
END;


GO

CREATE  TRIGGER trg_UpdateFriendRequestStatus
ON Friends
AFTER UPDATE
AS
BEGIN
    -- SET NOCOUNT ON;
    -- if true/1  false/0 if exis 1
    IF EXISTS (SELECT 1 FROM Inserted WHERE Status = 'Accepted' AND Status != (SELECT Status FROM Deleted))
    BEGIN
        UPDATE Users
        SET NoOfFriends = NoOfFriends + 1
        WHERE UserID IN (SELECT SenderID FROM Inserted WHERE Status = 'Accepted');

        UPDATE Users
        SET NoOfFriends = NoOfFriends + 1
        WHERE UserID IN (SELECT ReceiverID FROM Inserted WHERE Status = 'Accepted');
    END
END;

GO

CREATE TRIGGER trg_RemoveFriend
ON Friends
AFTER DELETE
AS
BEGIN
    UPDATE Users
    SET NoOfFriends = NoOfFriends - 1
    WHERE UserID IN (SELECT SenderID FROM Deleted);

    UPDATE Users
    SET NoOfFriends = NoOfFriends - 1
    WHERE UserID IN (SELECT ReceiverID FROM Deleted);
END;

GO
CREATE TRIGGER INC_GROUP_POST
ON GroupPosts
AFTER INSERT
AS
BEGIN
    UPDATE Groups
    SET NoOfGroupPost = NoOfGroupPost + 1
    WHERE GroupID IN (SELECT GroupID FROM INSERTED);
END;
GO
CREATE TRIGGER DEC_GROUP_POST
ON GroupPosts
AFTER DELETE
AS
BEGIN
    UPDATE Groups
    SET NoOfGroupPost = NoOfGroupPost - 1
    WHERE GroupID IN (SELECT GroupID FROM DELETED);
END;

GO
CREATE TRIGGER INC_GROUP_MEM
ON GroupMembers
AFTER INSERT
AS
BEGIN
    UPDATE Groups
    SET NoOfGroupMembers = NoOfGroupMembers + 1
    WHERE GroupID IN (SELECT GroupID FROM INSERTED);
END;
GO
CREATE TRIGGER DEC_GROUP_MEM
ON GroupMembers
AFTER DELETE
AS
BEGIN
    UPDATE Groups
    SET NoOfGroupMembers = NoOfGroupMembers - 1
    WHERE GroupID IN (SELECT GroupID FROM DELETED);
END;
GO

CREATE TRIGGER INC_GROUPPOST_LIKE
ON GroupLikes
AFTER INSERT
AS
BEGIN 
    UPDATE GroupPosts
    SET TotalLikes = TotalLikes + 1
    WHERE GroupPostID IN (SELECT GroupPostID FROM INSERTED)
END;
GO
CREATE TRIGGER DEC_GROUPPOST_LIKE
ON GroupLikes
AFTER DELETE
AS
BEGIN 
    UPDATE GroupPosts
    SET TotalLikes = TotalLikes - 1
    WHERE GroupPostID IN (SELECT GroupPostID FROM DELETED)
END;
GO

CREATE TRIGGER INC_GROUPPOST_COMM
ON GroupComments
AFTER INSERT
AS
BEGIN 
    UPDATE GroupPosts
    SET TotalComments = TotalComments + 1
    WHERE GroupPostID IN (SELECT GroupPostID FROM INSERTED)
END;
GO
CREATE TRIGGER DEC_GROUPPOST_COMM
ON GroupComments
AFTER DELETE
AS
BEGIN 
    UPDATE GroupPosts
    SET TotalComments = TotalComments - 1
    WHERE GroupPostID IN (SELECT GroupPostID FROM DELETED)
END;

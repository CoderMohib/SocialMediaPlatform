USE SocialMediaPlatform;
---------------------------------------
GO
CREATE OR ALTER PROCEDURE deleteGroup
    @GroupID INT
AS
BEGIN
    BEGIN TRANSACTION
    BEGIN TRY 
        DELETE GroupLikes WHERE GroupID = @GroupID;
        DELETE GroupComments WHERE GroupID = @GroupID;
        DELETE GroupPosts WHERE GroupID = @GroupID;
        DELETE GroupMembers WHERE GroupID = @GroupID
        DELETE FROM Groups WHERE @GroupID=GroupID;
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO
--------------------------------------------------
CREATE OR ALTER PROCEDURE deleteGroupPost
    @PostID INT,
    @GroupID INT
AS
BEGIN
    BEGIN TRANSACTION;

    BEGIN TRY
        DELETE FROM GroupLikes WHERE GroupPostID = @PostID AND GroupID = @GroupID;
        DELETE FROM GroupComments WHERE GroupPostID = @PostID AND GroupID = @GroupID;
        DELETE FROM GroupPosts WHERE GroupPostID = @PostID AND GroupID = @GroupID;
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;

        THROW;
    END CATCH
END;

-----------------------------------------------------------
GO
CREATE OR ALTER PROCEDURE exitGroup
    @UserID INT,
    @GroupID INT
AS
BEGIN
    BEGIN TRANSACTION
    BEGIN TRY
        -- Check if the user is the creator of the group
        IF EXISTS (
            SELECT 1
    FROM Groups
    WHERE CreatedBy = @UserID AND GroupID = @GroupID
        )
        BEGIN
        -- Check for other members in the group
        DECLARE @NewAdminID INT;
        SELECT TOP 1
            @NewAdminID = UserID
        FROM GroupMembers
        WHERE GroupID = @GroupID AND UserID != @UserID
        ORDER BY JoinedAt ASC;

        -- If there are other members, assign a new admin
        IF @NewAdminID IS NOT NULL
            BEGIN
            UPDATE GroupMembers
                SET Role = 'Admin'
                WHERE UserID = @NewAdminID AND GroupID = @GroupID;
            UPDATE Groups SET CreatedBy = @NewAdminID WHERE GroupID = @GroupID;
        END
            ELSE
            BEGIN
            -- No other members, delete the group
            DELETE FROM Groups WHERE GroupID = @GroupID;
            PRINT 'Group deleted as no members remain.';
        END
    END
        ELSE
        BEGIN
        -- Remove the user from the group
        DELETE FROM GroupMembers
        WHERE GroupID = @GroupID AND UserID = @UserID;
    END
        COMMIT TRANSACTION;
        PRINT 'User successfully exited the group.';
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        PRINT 'Error occurred: ' + ERROR_MESSAGE();
        THROW;
    END CATCH
END;

GO
---------------------------------------------
CREATE OR ALTER PROCEDURE DelUser
    @UserID INT
AS
BEGIN
    BEGIN TRANSACTION;
    BEGIN TRY
        -- Delete likes and comments by the user
        DELETE FROM Likes WHERE UserID = @UserID;
        DELETE FROM Comments WHERE UserID = @UserID;
        
        -- Delete likes and comments associated with the user's posts
        DELETE FROM Likes WHERE PostID IN (SELECT PostID FROM Posts WHERE UserID = @UserID);
        DELETE FROM Comments WHERE PostID IN (SELECT PostID FROM Posts WHERE UserID = @UserID);
        
        -- Delete the user's posts
        DELETE FROM Posts WHERE UserID = @UserID;

        -- Delete group-related records for the user
        DELETE FROM GroupComments WHERE UserID = @UserID;
        DELETE FROM GroupLikes WHERE UserID = @UserID;
        DELETE FROM GroupLikes
        WHERE GroupPostID IN (SELECT GroupPostID FROM GroupPosts WHERE UserID = @UserID);
        DELETE FROM GroupComments
        WHERE GroupPostID IN (SELECT GroupPostID FROM GroupPosts WHERE UserID = @UserID);
        DELETE FROM GroupPosts WHERE UserID = @UserID;
        DELETE FROM GroupMembers WHERE UserID = @UserID;

        -- Handle group ownership and deletion
        DECLARE @GroupID INT;

        DECLARE group_cursor CURSOR FOR
        SELECT GroupID FROM Groups WHERE CreatedBy = @UserID;
        OPEN group_cursor;

        FETCH NEXT FROM group_cursor INTO @GroupID;
        WHILE @@FETCH_STATUS = 0
        BEGIN
            EXEC exitGroup @UserID, @GroupID;
            FETCH NEXT FROM group_cursor INTO @GroupID;
        END

        CLOSE group_cursor;
        DEALLOCATE group_cursor;
        DELETE From Messages Where SenderID = @UserID OR ReceiverID = @UserID;
        DELETE FROM Friends WHERE SenderID = @UserID OR ReceiverID = @UserID;
        DELETE FROM Users WHERE UserID = @UserID;

        COMMIT TRANSACTION;
        PRINT 'User and all associated records deleted successfully.';
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        PRINT 'Error occurred: ' + ERROR_MESSAGE();
        THROW;
    END CATCH
END;
GO

GO



        
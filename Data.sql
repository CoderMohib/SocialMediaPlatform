USE SocialMediaPlatform;     
-- Select rows from a Table or View 'TableOrViewName' in schema 'SchemaName'
GO
DELETE FROM Messages WHERE Content = 'python -u "d:\4 seme\DBLAB\Project\tempCodeRunnerFile.py"'
SELECT * from Messages
-- Insert Users
INSERT INTO Users (Username, Email, PasswordF, FirstName, LastName, DateOfBirth)
VALUES 
('john_doe', 'john.doe@example.com', 'password123', 'John', 'Doe', '1990-05-15'),
('jane_doe', 'jane.doe@example.com', 'securepass1', 'Jane', 'Doe', '1985-07-20'),
('alice_wonder', 'alice.wonder@example.com', 'mypassword8', 'Alice', 'Wonder', '1998-01-10'),
('bob_builder', 'bob.builder@example.com', 'buildstrong1', 'Bob', 'Builder', '1980-12-05');

-- Insert Posts
INSERT INTO Posts (UserID, Content)
VALUES 
(1, 'Hello World! This is my first post!'),
(2, 'Excited to be here! Looking forward to connecting with everyone.'),
(3, 'Just sharing some thoughts about life and the universe.'),
(1, 'Here’s another update from me! Loving this platform.'),
(4, 'Building dreams one post at a time.');

-- Insert Likes
INSERT INTO Likes (UserID, PostID)
VALUES 
(2, 1),
(3, 1),
(1, 2),
(4, 2),
(2, 3),
(3, 4);
UPDATE GroupMembers SET Role = 'Admin' WHERE UserID = 1
-- Insert Comments
INSERT INTO Comments (PostID, UserID, Content)
VALUES 
(1, 2, 'Great post, John! Looking forward to more updates.'),
(1, 3, 'Interesting thoughts, John! Keep it up.'),
(2, 1, 'Thanks, Jane! Welcome aboard.'),
(4, 3, 'Nice update, John! I agree!'),
(5, 1, 'Love this mindset, Bob. Keep building!');

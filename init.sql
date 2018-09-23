DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Forums;
DROP TABLE IF EXISTS Threads;
DROP TABLE IF EXISTS Posts;

CREATE TABLE Users
(
  `UserId` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
  `Username` TEXT NOT NULL UNIQUE,
  `Password` TEXT NOT NULL
);

CREATE TABLE Forums
(
  `ForumId` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
  `CreatorId` INTEGER NOT NULL,
  `ForumsName` TEXT NOT NULL UNIQUE,
  FOREIGN KEY(`CreatorId`) REFERENCES `Users`(`UserId`) ON DELETE CASCADE
);

CREATE TABLE Threads
(
  `ThreadId` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
  `ForumId` INTEGER NOT NULL,
  `ThreadsTitle` TEXT NOT NULL,
  FOREIGN KEY(`ForumId`) REFERENCES `Forums`(`ForumId`) ON DELETE CASCADE
);

CREATE TABLE Posts
(
  `PostId` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
  `ThreadBelongsTo` INTEGER NOT NULL,
  `AuthorId` INTEGER NOT NULL,
  `PostsTimestamp` TEXT NOT NULL,
  `Message` TEXT NOT NULL,
  FOREIGN KEY(`ThreadBelongsTo`) REFERENCES `Thread`(`ThreadId`) ON DELETE CASCADE,
  FOREIGN KEY(`AuthorId`) REFERENCES `Users`(`UserId`) ON DELETE CASCADE
);

CREATE INDEX `PostsChronological`
ON `Posts`
(
  `PostsTimestamp` ASC
);

CREATE INDEX `UserId`
ON `Users`
(
  `UserId` ASC
);

INSERT INTO Users
  (`Username`, `Password`)
VALUES
    ('cameron', 'test'),
    ('brian', 'test'),
    ('elmer', 'test');

INSERT INTO Forums
  (`CreatorId`, `ForumsName`)
VALUES
  (1, 'Forum Test1'),
  (2, 'Forum Test2'),
  (3, 'Forum Test3');

INSERT INTO Threads
  (`ForumId`, `ThreadsTitle`)
VALUES
  (1, 'Thread Test 1'),
  (2, 'Thread Test 2'),
  (3, 'Thread Test 3');

INSERT INTO Posts
  (`AuthorId`, `ThreadBelongsTo`, `PostsTimestamp`, `Message`)
VALUES
  (1, 1, 'Tue, 02 Sep 2018 15:42:28 GMT', 'Post Test 1'),
  (2, 1, 'Wed, 03 Sep 2018 15:43:28 GMT', 'Post Test 2'),
  (3, 2, 'Tue, 04 Sep 2018 15:42:28 GMT', 'Post Test 3'),
  (2, 2, 'Wed, 05 Sep 2018 15:43:28 GMT', 'Post Test 4');

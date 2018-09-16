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
  `AuthorId` INTEGER NOT NULL,
  `PostsTimestamp` TEXT NOT NULL,
  `Message` TEXT NOT NULL,
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
    ('sorryiforogtyourname', 'test');

INSERT INTO Forums
  (`CreatorId`, `ForumsName`)
VALUES
  (1, 'Test1'),
  (2, 'Test2'),
  (3, 'Test3');

INSERT INTO Threads
  (`ForumId`, `ThreadsTitle`)
VALUES
  (1, 'Forum Test 1'),
  (2, 'Forum Test 2'),
  (3, 'Forum Test 3');

INSERT INTO Posts
  (`AuthorId`, `PostsTimestamp`, `Message`)
VALUES
  (1, 'Tue, 05 Sep 2018 15:42:28 GMT', 'Thread Test 1'),
  (2, 'Wed, 04 Sep 2018 15:42:28 GMT', 'Thread Test 2'),
  (3, 'Tue, 03 Sep 2018 15:42:28 GMT', 'Thread Test 3');

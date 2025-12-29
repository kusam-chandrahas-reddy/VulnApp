CREATE TABLE IF NOT EXISTS users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
	password TEXT NOT NULL,
	fullname TEXT NOT NULL
);

INSERT OR IGNORE INTO users (username, email, password, fullname) VALUES ('sectester', 'sectester@example.com','mypasswordisempty','Security Tester');
INSERT OR IGNORE INTO users (username, email, password, fullname) VALUES ('root', 'root@example.com','mypasswordistoor','ROOT User');

CREATE TABLE IF NOT EXISTS Posts (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    author TEXT NOT NULL,
    post_heading TEXT NOT NULL,
	post_data TEXT NOT NULL,
	dt TEXT NOT NULL
);

INSERT OR IGNORE INTO Posts ('author','post_heading','post_data','dt') VALUES ('tester', 'My First Post', 'This is a basic post with just a simple details in it','2025-08-12 10:10:10');
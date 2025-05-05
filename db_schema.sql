CREATE TABLE IF NOT EXISTS users (
	id INTEGER AUTOINCREMENT,
    username TEXT PRIMARY KEY NOT NULL,
    email TEXT NOT NULL,
	password TEXT NOT NULL,
	fullname TEXT NOT NULL
);

INSERT INTO users (username, email, password, fullname) VALUES ('sectester', 'sectester@example.com','mypasswordisempty','Security Tester');
INSERT INTO users (username, email, password, fullname) VALUES ('root', 'root@example.com','mypasswordistoor','ROOT User');
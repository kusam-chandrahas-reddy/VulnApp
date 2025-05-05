CREATE TABLE IF NOT EXISTS users (
	id INTEGER AUTO_INCREMENT,
    username TEXT PRIMARY KEY,
    email TEXT NOT NULL,
	password TEXT NOT NULL,
	fullname TEXT NOT NULL
);

INSERT OR IGNORE INTO users (username, email, password, fullname) VALUES ('sectester', 'sectester@example.com','mypasswordisempty','Security Tester');
INSERT OR IGNORE INTO users (username, email, password, fullname) VALUES ('root', 'root@example.com','mypasswordistoor','ROOT User');
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE user (
	id INTEGER NOT NULL, 
	name VARCHAR(80) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	phone VARCHAR(15) NOT NULL, 
	password VARCHAR(80) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (email), 
	UNIQUE (phone)
);
INSERT INTO user VALUES(1,'pooja','aktech701@gmail.com','1234567891','scrypt:32768:8:1$nDmvQMk1tEi44CMA$36a77e7df440e0537cdb199eaae6cd10e4e5bcf1a34a97470603ca178a7ebfb0adce3141d289060538077acac0625edd414791578f436181d61819ddb7465999');
CREATE TABLE admin (
	id INTEGER NOT NULL, 
	username VARCHAR(80) NOT NULL, 
	password VARCHAR(80) NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO admin VALUES(1,'admin','scrypt:32768:8:1$lfn96eNbmhtjuL3d$3c3cfe89f40a0262c0141258d04a3d04e4a873c7e4a4f6b277bcb12e34698f9d9335bc78bbbb3e2ee75353a10bd26e80243b643c332cef4fa02d4f26dafc91e8');
INSERT INTO admin VALUES(2,'admin','scrypt:32768:8:1$KII0sS5JBNF33OqD$80c1f52139bc0eb2d30e4695bc97bacf1a18e7f04403e0e1a0e6ca4232f0be9e449f82cae8e7f92df7c64ddfa2632799f3c9ca45d981dcf8c899a2818cec63fd');
CREATE TABLE parking_lot (
	id INTEGER NOT NULL, 
	prime_location_name VARCHAR(80) NOT NULL, 
	price FLOAT NOT NULL, 
	address VARCHAR(120) NOT NULL, 
	pin_code VARCHAR(10) NOT NULL, 
	maximum_number_of_spots INTEGER NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO parking_lot VALUES(1,'gandi chowk',40.0,'gandhi chowk','145001',12);
INSERT INTO parking_lot VALUES(2,'saili_road',50.0,'saili road, pathankot','145001',18);
INSERT INTO parking_lot VALUES(3,'dhangu road',60.0,'dhangu road ,pathankot','145001',24);
CREATE TABLE parking_spot (
	id INTEGER NOT NULL, 
	lot_id INTEGER NOT NULL, 
	status VARCHAR(20) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(lot_id) REFERENCES parking_lot (id)
);
INSERT INTO parking_spot VALUES(1,1,'available');
INSERT INTO parking_spot VALUES(2,1,'available');
INSERT INTO parking_spot VALUES(3,1,'available');
INSERT INTO parking_spot VALUES(4,1,'available');
INSERT INTO parking_spot VALUES(5,1,'available');
INSERT INTO parking_spot VALUES(6,1,'available');
INSERT INTO parking_spot VALUES(7,1,'available');
INSERT INTO parking_spot VALUES(8,1,'available');
INSERT INTO parking_spot VALUES(9,1,'available');
INSERT INTO parking_spot VALUES(10,1,'available');
INSERT INTO parking_spot VALUES(11,1,'available');
INSERT INTO parking_spot VALUES(12,1,'available');
INSERT INTO parking_spot VALUES(13,2,'available');
INSERT INTO parking_spot VALUES(14,2,'available');
INSERT INTO parking_spot VALUES(15,2,'available');
INSERT INTO parking_spot VALUES(16,2,'available');
INSERT INTO parking_spot VALUES(17,2,'available');
INSERT INTO parking_spot VALUES(18,2,'available');
INSERT INTO parking_spot VALUES(19,2,'available');
INSERT INTO parking_spot VALUES(20,2,'available');
INSERT INTO parking_spot VALUES(21,2,'available');
INSERT INTO parking_spot VALUES(22,2,'available');
INSERT INTO parking_spot VALUES(23,2,'available');
INSERT INTO parking_spot VALUES(24,2,'available');
INSERT INTO parking_spot VALUES(25,2,'available');
INSERT INTO parking_spot VALUES(26,2,'available');
INSERT INTO parking_spot VALUES(27,2,'available');
INSERT INTO parking_spot VALUES(28,2,'available');
INSERT INTO parking_spot VALUES(29,2,'available');
INSERT INTO parking_spot VALUES(30,2,'available');
INSERT INTO parking_spot VALUES(31,3,'available');
INSERT INTO parking_spot VALUES(32,3,'available');
INSERT INTO parking_spot VALUES(33,3,'available');
INSERT INTO parking_spot VALUES(34,3,'available');
INSERT INTO parking_spot VALUES(35,3,'available');
INSERT INTO parking_spot VALUES(36,3,'available');
INSERT INTO parking_spot VALUES(37,3,'available');
INSERT INTO parking_spot VALUES(38,3,'available');
INSERT INTO parking_spot VALUES(39,3,'available');
INSERT INTO parking_spot VALUES(40,3,'available');
INSERT INTO parking_spot VALUES(41,3,'available');
INSERT INTO parking_spot VALUES(42,3,'available');
INSERT INTO parking_spot VALUES(43,3,'available');
INSERT INTO parking_spot VALUES(44,3,'available');
INSERT INTO parking_spot VALUES(45,3,'available');
INSERT INTO parking_spot VALUES(46,3,'available');
INSERT INTO parking_spot VALUES(47,3,'available');
INSERT INTO parking_spot VALUES(48,3,'available');
INSERT INTO parking_spot VALUES(49,3,'available');
INSERT INTO parking_spot VALUES(50,3,'available');
INSERT INTO parking_spot VALUES(51,3,'available');
INSERT INTO parking_spot VALUES(52,3,'available');
INSERT INTO parking_spot VALUES(53,3,'available');
INSERT INTO parking_spot VALUES(54,3,'available');
CREATE TABLE reservation_parking_spot (
	id INTEGER NOT NULL, 
	spot_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	parking_timestamp DATETIME, 
	leaving_timestamp DATETIME, 
	parking_cost_per_unit_time FLOAT NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(spot_id) REFERENCES parking_spot (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
COMMIT;

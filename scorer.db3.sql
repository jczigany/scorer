BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "players" (
	"player_id"	INTEGER,
	"player_name"	TEXT,
	PRIMARY KEY("player_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "network" (
	"server_ip"	TEXT,
	"server_port"	INTEGER,
	"station_id"	INTEGER
);
CREATE TABLE IF NOT EXISTS "matches" (
	"match_id"	INTEGER,
	"leg_id"	INTEGER,
	"set_id"	INTEGER,
	"winner_id"	INTEGER,
	"timestamp"	TEXT
);
CREATE TABLE IF NOT EXISTS "dobas" (
	"player_id"	INTEGER,
	"round_number"	INTEGER,
	"points"	INTEGER,
	"leg_id"	INTEGER,
	"set_id"	INTEGER,
	"match_id"	INTEGER,
	"timestamp"	TEXT
);
CREATE TABLE IF NOT EXISTS "match_settings" (
	"match_id"	INTEGER,
	"player1_id"	INTEGER,
	"player2_id"	INTEGER,
	"variant"	TEXT,
	"sets"	INTEGER,
	"legsperset"	INTEGER,
	"timestamp"	INTEGER,
	PRIMARY KEY("match_id" AUTOINCREMENT)
);
INSERT INTO "players" VALUES (1,'Laci');
INSERT INTO "players" VALUES (2,'Fecó');
INSERT INTO "players" VALUES (3,'Jani');
INSERT INTO "players" VALUES (4,'Reni');
INSERT INTO "players" VALUES (5,'Czigány Jani');
INSERT INTO "dobas" VALUES (5,1,50,1,1,274266,'2021-03-22T12:29:37.841');
INSERT INTO "dobas" VALUES (1,1,100,1,1,274266,'2021-03-22T12:29:41.071');
INSERT INTO "match_settings" VALUES (274266,5,1,'501',3,1,NULL);
COMMIT;

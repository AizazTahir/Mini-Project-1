drop table if exists perform;
drop table if exists artists;
drop table if exists plinclude;
drop table if exists playlists;
drop table if exists listen;
drop table if exists sessions;
drop table if exists songs;
drop table if exists users;

PRAGMA foreign_keys = ON;

create table users (
  uid		char(4),
  name		text,
  pwd		text,
  primary key (uid)
);
create table songs (
  sid		int,
  title		text,
  duration	int,
  primary key (sid)
);
create table sessions (
  uid		char(4),
  sno		int,
  start 	date,
  end 		date,
  primary key (uid,sno),
  foreign key (uid) references users
	on delete cascade
);
create table listen (
  uid		char(4),
  sno		int,
  sid		int,
  cnt		real,
  primary key (uid,sno,sid),
  foreign key (uid,sno) references sessions,
  foreign key (sid) references songs
);
create table playlists (
  pid		int,
  title		text,
  uid		char(4),
  primary key (pid),
  foreign key (uid) references users
);
create table plinclude (
  pid		int,
  sid		int,
  sorder	int,
  primary key (pid,sid),
  foreign key (pid) references playlists,
  foreign key (sid) references songs
);
create table artists (
  aid		char(4),
  name		text,
  nationality	text,
  pwd		text,
  primary key (aid)
);
create table perform (
  aid		char(4),
  sid		int,
  primary key (aid,sid),
  foreign key (aid) references artists,
  foreign key (sid) references songs
);

--- DATA ---

--- Users ---
insert into users values ('u1', 'Maheen Lynn');
--- Spelled with mixed cases ---
insert into users values ('u2', 'leena markham');
insert into users values ('u3', 'BranDen escobar');
insert into users values ('u4', 'DigBy TieRney');
--- Spelled with mixed cases ---
insert into users values ('u5', 'Harriet Beck');
insert into users values ('u6', 'Aron Gu');
insert into users values ('u7', 'Jeevan Dillard');
insert into users values ('u8', 'Laaibah Cano');
insert into users values ('u9', 'Ameila Pike');
insert into users values ('u10','Davood Rafiei');

--- Artists ---
insert into artists values ('a1', 'Lady Gaga', 'uniTed States');
--- Spelled with mixed cases ---
insert into artists values ('a2', 'ONeRepublic', 'uNited States');
insert into artists values ('a3', 'ImaGine dragons', 'United States');
insert into artists values ('a4', 'pSY', 'SouTh KoRea');
--- Spelled with mixed cases ---
insert into artists values ('a5', 'P!nk', 'American');
insert into artists values ('a6', 'Nate Reuss', 'American');
insert into artists values ('a7', 'Kelly Clarkson', 'United States');
insert into artists values ('a8', 'Janelle Monáe', 'United States');
insert into artists values ('a9', 'Maroon 5', 'United States');
insert into artists values ('a10', 'Drake', 'Canada');

--- Perform ---
insert into perform values ('a1', 2);
insert into perform values ('a1', 19);
insert into perform values ('a2', 4);
insert into perform values ('a3', 3);
insert into perform values ('a4', 22);
insert into perform values ('a5', 6);
insert into perform values ('a6', 6);
insert into perform values ('a7', 7);
insert into perform values ('a8', 8);
insert into perform values ('a9', 9);
insert into perform values ('a10', 5);

--- Songs ---
insert into songs values (2, 'Applause', 212);
insert into songs values (19, 'applause master', 238);
insert into songs values (4, 'Counting Stars', 259);
insert into songs values (3, 'Demons kill', 177);
insert into songs values (22, 'Gentleman applause', 194);
insert into songs values (6, 'Just Give Me a Reason', 242);
insert into songs values (7, 'Stronger(What Doesn`t Kill You)', 222);
insert into songs values (8, 'We Are Young', 233);
insert into songs values (9, 'Moves Like Jagger', 201);
insert into songs values (5, 'Wavin flag', 220);

--- Sessions ---
insert into sessions values ('u10', 1, '2022-09-27', '2022-09-28');
insert into sessions values ('u2', 1, '2022-09-25', '2022-09-27');
insert into sessions values ('u3', 2, '2022-09-24', '2022-09-25');
insert into sessions values ('u4', 3, '2022-09-24', '2022-09-25');
insert into sessions values ('u1', 4, '2022-09-23', '2022-09-27');
insert into sessions values ('u5', 5, '2022-09-22', '2022-09-24');
insert into sessions values ('u6', 5, '2022-09-22', '2022-09-23');
insert into sessions values ('u7', 6, '2022-09-16', '2022-09-18');
insert into sessions values ('u8', 6, '2022-09-12', '2022-09-21');
insert into sessions values ('u9', 7, '2022-09-13', '2022-09-16');
insert into sessions values ('u2', 8, '2022-09-12', '2022-09-14');
insert into sessions values ('u4', 9, '2022-09-08', '2022-09-15');
insert into sessions values ('u5', 9, '2022-09-06', '2022-09-09');
insert into sessions values ('u8', 10, '2022-09-02', '2022-09-04');

--- Listen ---
insert into listen values ('u10', 1, 2, 1.2);
insert into listen values ('u10', 1, 19, 2.0);
insert into listen values ('u9', 1, 19, 33);
insert into listen values ('u7', 1, 4, 14);
insert into listen values ('u2', 1, 6, 22);

insert into listen values ('u3', 2, 42, 9.7);
insert into listen values ('u3', 2, 30, 11.8);

insert into listen values ('u1', 4, 2, 3);
insert into listen values ('u1', 4, 12, 5);
insert into listen values ('u1', 4, 16, 4);

insert into listen values ('u5', 4, 2, 3);
insert into listen values ('u5', 4, 12, 5);
insert into listen values ('u5', 4, 16, 4);
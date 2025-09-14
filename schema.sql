-- Cricbuzz Analytics Database Schema (Expanded with Sample Data)

DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS player_stats;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS venues;
DROP TABLE IF EXISTS series;

-- ----------------
-- Players Table
-- ----------------
CREATE TABLE players (
    player_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name     TEXT NOT NULL,
    playing_role  TEXT,
    batting_style TEXT,
    bowling_style TEXT,
    country       TEXT NOT NULL
);

-- ----------------
-- Player Stats Table
-- ----------------
CREATE TABLE player_stats (
    stat_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id     INTEGER,
    format        TEXT CHECK(format IN ('Test','ODI','T20')),
    total_runs    INTEGER DEFAULT 0,
    batting_avg   REAL DEFAULT 0,
    centuries     INTEGER DEFAULT 0,
    highest_score INTEGER DEFAULT 0,
    wickets       INTEGER DEFAULT 0,
    bowling_avg   REAL DEFAULT 0,
    five_wkts     INTEGER DEFAULT 0,
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

-- ----------------
-- Venues Table
-- ----------------
CREATE TABLE venues (
    venue_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    venue_name TEXT NOT NULL,
    city       TEXT,
    country    TEXT,
    capacity   INTEGER
);

-- ----------------
-- Series Table
-- ----------------
CREATE TABLE series (
    series_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    series_name  TEXT NOT NULL,
    host_country TEXT,
    match_type   TEXT CHECK(match_type IN ('Test','ODI','T20')),
    start_date   DATE,
    end_date     DATE,
    total_matches INTEGER
);

-- ----------------
-- Matches Table
-- ----------------
CREATE TABLE matches (
    match_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    series_id   INTEGER,
    team1       TEXT NOT NULL,
    team2       TEXT NOT NULL,
    venue_id    INTEGER,
    match_date  DATE,
    match_desc  TEXT,
    result      TEXT,
    FOREIGN KEY (series_id) REFERENCES series(series_id),
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id)
);

-- ----------------
-- Insert Venues
-- ----------------
INSERT INTO venues (venue_name, city, country, capacity) VALUES
('Wankhede Stadium', 'Mumbai', 'India', 33000),
('Eden Gardens', 'Kolkata', 'India', 68000),
('Melbourne Cricket Ground', 'Melbourne', 'Australia', 100024),
('Lord''s Cricket Ground', 'London', 'England', 30000),
('SCG', 'Sydney', 'Australia', 48000);

-- ----------------
-- Insert Series
-- ----------------
INSERT INTO series (series_name, host_country, match_type, start_date, end_date, total_matches) VALUES
('India vs Australia 2024', 'India', 'Test', '2024-02-01', '2024-03-10', 4),
('World Cup 2023', 'India', 'ODI', '2023-10-05', '2023-11-19', 48),
('Ashes 2023', 'England', 'Test', '2023-06-15', '2023-07-31', 5);

-- ----------------
-- Insert Matches
-- ----------------
INSERT INTO matches (series_id, team1, team2, venue_id, match_date, match_desc, result) VALUES
(1, 'India', 'Australia', 1, '2024-02-05', '1st Test', 'India Win'),
(1, 'India', 'Australia', 2, '2024-02-15', '2nd Test', 'Australia Win'),
(2, 'India', 'Pakistan', 2, '2023-10-15', 'Group Stage', 'India Win'),
(2, 'Australia', 'England', 3, '2023-10-20', 'Group Stage', 'England Win'),
(2, 'South Africa', 'New Zealand', 5, '2023-10-25', 'Group Stage', 'South Africa Win'),
(3, 'England', 'Australia', 4, '2023-06-15', '1st Test', 'Draw'),
(3, 'England', 'Australia', 5, '2023-06-25', '2nd Test', 'England Win'),
(3, 'England', 'Australia', 4, '2023-07-05', '3rd Test', 'Australia Win');

-- ----------------
-- Insert Players
-- ----------------
INSERT INTO players (full_name, playing_role, batting_style, bowling_style, country) VALUES
('Virat Kohli', 'Batsman', 'Right-hand bat', 'Right-arm medium', 'India'),
('Rohit Sharma', 'Batsman', 'Right-hand bat', NULL, 'India'),
('Shubman Gill', 'Batsman', 'Right-hand bat', NULL, 'India'),
('KL Rahul', 'Wicketkeeper', 'Right-hand bat', NULL, 'India'),
('Hardik Pandya', 'Allrounder', 'Right-hand bat', 'Right-arm medium-fast', 'India'),
('Ravindra Jadeja', 'Allrounder', 'Left-hand bat', 'Left-arm orthodox', 'India'),
('Jasprit Bumrah', 'Bowler', 'Right-hand bat', 'Right-arm fast', 'India'),
('MS Dhoni', 'Wicketkeeper', 'Right-hand bat', NULL, 'India'),
('Mitchell Starc', 'Bowler', 'Left-hand bat', 'Left-arm fast', 'Australia'),
('Pat Cummins', 'Bowler', 'Right-hand bat', 'Right-arm fast', 'Australia'),
('Steve Smith', 'Batsman', 'Right-hand bat', 'Right-arm legbreak', 'Australia'),
('David Warner', 'Batsman', 'Left-hand bat', NULL, 'Australia'),
('Travis Head', 'Batsman', 'Left-hand bat', 'Right-arm offbreak', 'Australia'),
('Ben Stokes', 'Allrounder', 'Left-hand bat', 'Right-arm fast-medium', 'England'),
('Joe Root', 'Batsman', 'Right-hand bat', 'Right-arm offbreak', 'England'),
('Jonny Bairstow', 'Wicketkeeper', 'Right-hand bat', NULL, 'England'),
('James Anderson', 'Bowler', 'Left-hand bat', 'Right-arm fast-medium', 'England'),
('Kane Williamson', 'Batsman', 'Right-hand bat', 'Right-arm offbreak', 'New Zealand'),
('Trent Boult', 'Bowler', 'Right-hand bat', 'Left-arm fast-medium', 'New Zealand'),
('Babar Azam', 'Batsman', 'Right-hand bat', 'Right-arm offbreak', 'Pakistan');

-- ----------------
-- Insert Player Stats
-- ----------------
INSERT INTO player_stats (player_id, format, total_runs, batting_avg, centuries, highest_score, wickets, bowling_avg, five_wkts) VALUES
(1, 'ODI', 13000, 58.0, 46, 183, 4, 35.2, 0),
(2, 'ODI', 10500, 49.8, 30, 264, 8, 40.0, 0),
(3, 'ODI', 2000, 45.0, 5, 121, 0, 0, 0),
(4, 'ODI', 4000, 42.0, 10, 112, 0, 0, 0),
(5, 'ODI', 3500, 35.5, 3, 92, 70, 28.5, 2),
(6, 'ODI', 2500, 33.0, 2, 85, 180, 30.0, 5),
(7, 'ODI', 300, 12.0, 0, 28, 120, 21.5, 6),
(8, 'ODI', 10773, 50.6, 10, 183, 1, 40.0, 0),
(9, 'ODI', 500, 15.2, 0, 52, 210, 22.5, 8),
(10, 'ODI', 800, 18.5, 0, 56, 180, 25.0, 6),
(11, 'ODI', 5000, 52.0, 15, 164, 20, 35.0, 1),
(12, 'ODI', 6000, 44.0, 18, 166, 5, 45.0, 0),
(13, 'ODI', 3500, 39.0, 7, 140, 10, 38.0, 0),
(14, 'ODI', 4500, 41.0, 8, 135, 80, 32.0, 3),
(15, 'ODI', 6000, 50.0, 16, 190, 25, 36.5, 0),
(16, 'ODI', 3500, 39.0, 7, 120, 0, 0, 0),
(17, 'ODI', 150, 10.5, 0, 25, 650, 27.0, 31),
(18, 'ODI', 6500, 47.0, 14, 145, 20, 40.0, 0),
(19, 'ODI', 400, 12.0, 0, 35, 220, 23.0, 9),
(20, 'ODI', 5500, 48.0, 13, 158, 10, 42.0, 0);

-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create a table where the tournament's players will be registered. This table will also maintain counts fo the plater's wins and total matches

CREATE TABLE players (
    id serial PRIMARY KEY,
    name text,
    wins integer DEFAULT 0,
    matches integer DEFAULT 0,
    bye_assigned boolean DEFAULT FALSE
);

-- Create a table where the tournament's matches will be recorded. This table will log the winner and loser of each match

CREATE TABLE matches (
    id serial PRIMARY KEY,
    winner_id integer,
    loser_id integer
);
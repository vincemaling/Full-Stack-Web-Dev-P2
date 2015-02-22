#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    # A simple query to delete all matches from the matches table
    c.execute("DELETE FROM matches")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    # A simple query to delete all players from the players table
    c.execute("DELETE FROM players")
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    # A simple query to aggregate the sum of players in the players table
    c.execute("SELECT count(*) FROM players")
    first_row = c.fetchone()
    player_count = first_row[0]
    DB.close()
    return player_count

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    # A simple query to insert a new player into the players table; aside from the name, all value are auto-populated by the table
    c.execute("INSERT INTO players (name) VALUES (%s)", (name,))
    DB.commit()
    DB.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    standings = []
    DB = connect()
    c = DB.cursor()
    # Below, we sort our players by number of wins, then create a list of tuples (see documentation above) 
    c.execute("SELECT * FROM players ORDER BY wins DESC")
    for row in c.fetchall():
        standings.append((row[0], str(row[1]), row[2], row[3]))
    DB.close()
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    # The queries below (1) record the match in the matches table and (2) update the wins and matches fields in the players table for the winner and loser. Note that the matches table is not strictly required, but I've included it in case the application were ever expanded to be able to provide a detailed history of matches played.
    c.execute("INSERT INTO matches (winner_id, loser_id) VALUES (%s, %s)", (winner, loser,))
    c.execute("UPDATE players SET wins = wins + 1, matches = matches + 1 WHERE id = %s", (winner,));
    c.execute("UPDATE players SET matches = matches + 1 WHERE id = %s", (loser,))
    DB.commit()
    DB.close() 

def assignBye():
    """In the case of an odd number of players, this function finds the highest-ranked player who has not yet received a BYE, and returns the id of that player
    """
    DB = connect()
    c = DB.cursor()
    # Here we determine the top-ranked player who has not been previously assigned a bye
    c.execute("SELECT id FROM players WHERE bye_assigned = FALSE ORDER BY wins DESC LIMIT 1")
    first_row = c.fetchone()
    # If EVERY player has already been assigned a bye, then we simply assign the bye to the top-ranked player
    if len(first_row) > 0:
        player_id = first_row[0]    
    else:
        player_id = 0
    # Since a bye represents a free win, we increment the players wins and matches field by 1
    c.execute("UPDATE players SET bye_assigned = TRUE, wins = wins + 1, matches = matches +1 WHERE id = %s", (player_id,))
    DB.commit()
    DB.close()
    return player_id
    
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairings = []
    currentstandings = [standing for standing in playerStandings()]
    # Below, we check to determine if there are an off number of players in currentstandings. If so, we call the assignBye function and remove that player from the list of players to be paired
    if len(currentstandings) % 2 != 0:
        revised_standings = []
        player_to_get_bye = assignBye()
        for player in currentstandings:
            if player[0] != player_to_get_bye:
                revised_standings.append(player)
        currentstandings = revised_standings
    # We loop through the current standings and match adjacent players for the next round of matches. NOTE: In the xrange loop below, we are using len(currentstandings) rather than countPlayers() because if an off number of players exist, we are removing one from the standings but not from the database
    for i in xrange(0, len(currentstandings), 2):
        pairings.append((currentstandings[i][0], currentstandings[i][1], currentstandings[i+1][0], currentstandings[i+1][1]))
    return pairings
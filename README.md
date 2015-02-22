Tournaments Project
==================
#####Udacity FS Web Developer Nanodegree - Project 2#####
---

Contents
--------

1. [How to Run / Test](#chapter-1)  
2. [Extra Credit: Odd Players & Byes](#chapter-2)    

How to Run / Test <a id="chapter-1"></a>
-----------------
Follow these steps to run the Tournaments project:    

1. Download and unzip the "Tournaments" folder
2. Create a Postgre SQL database on your server called "tournament"
3. Import the *tournament.sql* file to create two tables: *players* and *matches*
4. Run the *tournament_test.py* Python file to test the available functions

Here's a screenshot of what to expect: 

![Tournaments Test](https://github.com/vincemaling/Full-Stack-Web-Dev-P2/blob/master/screenshot_tournaments.png) 

Extra Credit: Odd Players and Byes <a id="chapter-2"></a>
-----------------
In addition to the required functionality, I modified *tournament.py* to accomodate an odd number of players in the tournament. The application now determines whether an odd number of players exist and, if so, assigns one of them a bye.  

<dl><dt>(1) assignBye()</dt>
<dd>In the case of an odd number of players, this function finds the highest-ranked player who has not yet received a BYE, and returns the id of that player. It also increments the player's wins and matches by one, as a BYE represents a free win.<dd>  

<dt>(2) swissPairings()</dt>
<dd>The existing swissPairings() function was also modified to accomodate BYEs. When odd players exist, it calls the assignBye() function to determine the player that will receive the BYE, then omits that player when creating pairings for the next round's matches.</dd>  

